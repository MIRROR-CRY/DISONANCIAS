#!/usr/bin/env python3
"""
Forced alignment of the known lyrics against the real vocal audio, via
classical MFCC + DTW (Dynamic Time Warping) -- the same core principle
behind lyrics-to-audio alignment research and tools like aeneas.

Why this instead of WhisperX/wav2vec2 (the actual industry-standard tool
for this today): this environment's network policy blocks every host that
serves pretrained model weights (download.pytorch.org, dl.fbaipublicfiles.com
for Demucs, huggingface.co) with a 403 -- confirmed via the proxy's own
status endpoint, not a guess. aeneas itself also fails to build here (its
C extension setup.py is incompatible with the numpy/setuptools versions in
this environment; a pre-existing packaging problem, not something to route
around with a flag). What IS available with no network model download:
espeak-ng (installed via apt, a plain system package) for synthesizing a
reference reading of the lyrics, and librosa (local, already installed)
for MFCC + DTW. This reimplements the same alignment idea aeneas uses --
without either of the two blockers above.

How it works:
  1. Synthesize each lyric word individually with espeak-ng, trim its
     silence, and concatenate all words (with a small fixed gap) into one
     synthetic reference track -- this gives exact word boundaries in
     SYNTHETIC time.
  2. Compute MFCCs for the synthetic track and the real vocal audio.
  3. Run DTW between them (librosa.sequence.dtw) to get a warping path
     from synthetic time to real time.
  4. Map each word's synthetic boundary through that path to get its
     estimated REAL start/end time.
  5. Regroup words back into lines/sections for captioning.

This is inherently less precise than a neural forced aligner (DTW on a
robotic TTS reference vs. a sung, reverb-heavy vocal is a rougher match
than phoneme-level acoustic modeling), especially through gang vocals,
melisma, or heavy effects -- but it uses the real audio's actual timing
signal, which is what the user asked for, instead of a fixed guess from
bar counts.

Usage:
  python3 "musica/Kicking Stones v2/align_lyrics.py" \
      --audio "musica/Kicking Stones v2/final_master/KickingStonesv5.mp3" \
      --out "musica/Kicking Stones v2/lyrics_timing.json"
"""
import argparse
import json
import os
import re
import subprocess
import sys

import librosa
import numpy as np

SR = 22050  # matches espeak-ng's native output rate, avoids resampling the synthetic track


def parse_lyrics_lines(path):
    blocks = []
    current_name = None
    current_lines = None
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        m = re.match(r"^\[(.+)\]$", line)
        if m:
            if current_name is not None:
                blocks.append((current_name, current_lines))
            current_name = m.group(1)
            current_lines = []
        elif line and current_name is not None:
            current_lines.append(line)
    if current_name is not None:
        blocks.append((current_name, current_lines))
    return blocks


def synth_word(word, tmp_path, rate_wpm=150):
    subprocess.run(
        ["espeak-ng", "-v", "en", "-s", str(rate_wpm), "-w", tmp_path, word],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    audio, sr = librosa.load(tmp_path, sr=SR)
    trimmed, _ = librosa.effects.trim(audio, top_db=30)
    if len(trimmed) == 0:
        trimmed = audio
    return trimmed


def build_synthetic_track(flat_words, tmp_dir, gap_sec=0.08):
    gap = np.zeros(int(gap_sec * SR))
    pieces = []
    word_bounds = []  # (start_sec, end_sec) in synthetic-track time
    cursor = 0.0
    for i, w in enumerate(flat_words):
        tmp_path = os.path.join(tmp_dir, f"w{i}.wav")
        audio = synth_word(w, tmp_path)
        os.remove(tmp_path)
        start = cursor
        end = cursor + len(audio) / SR
        word_bounds.append((start, end))
        pieces.append(audio)
        pieces.append(gap)
        cursor = end + gap_sec
    track = np.concatenate(pieces) if pieces else np.zeros(0)
    return track, word_bounds


def dtw_map(synthetic, real, sr=SR):
    hop = 512
    mfcc_synth = librosa.feature.mfcc(y=synthetic, sr=sr, n_mfcc=20, hop_length=hop)
    mfcc_real = librosa.feature.mfcc(y=real, sr=sr, n_mfcc=20, hop_length=hop)
    # normalize each frame (cosine-like matching, robust to loudness/timbre differences
    # between a robotic TTS reference and a produced, effects-heavy vocal)
    mfcc_synth = mfcc_synth / (np.linalg.norm(mfcc_synth, axis=0, keepdims=True) + 1e-8)
    mfcc_real = mfcc_real / (np.linalg.norm(mfcc_real, axis=0, keepdims=True) + 1e-8)
    D, wp = librosa.sequence.dtw(X=mfcc_synth, Y=mfcc_real, metric="euclidean")
    wp = np.array(wp[::-1])  # librosa returns path end-to-start; flip to start-to-end
    synth_frames = wp[:, 0] * hop / sr
    real_frames = wp[:, 1] * hop / sr

    def to_real_time(t_synth):
        return float(np.interp(t_synth, synth_frames, real_frames))

    return to_real_time


def parse_anchor(spec):
    """'Section Name=12.5' -> ('Section Name', 12.5). Also accepts
    'line:exact line text=12.5' to anchor to a specific LINE's first word
    instead of a whole section's -- needed when the drift happens inside a
    section, not just at its boundary."""
    name, secs = spec.rsplit("=", 1)
    return name.strip(), float(secs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True, help="real vocal or full-mix audio to align against")
    ap.add_argument("--lyrics", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tmp-dir", default="/tmp/align_lyrics_words")
    ap.add_argument("--vocal-start", type=float, default=0.0,
                     help="seconds into --audio where singing actually starts. Standard DTW "
                          "always maps synthetic time 0 to real time 0, so without this, any "
                          "wordless intro gets silently swallowed.")
    ap.add_argument("--anchor", action="append", default=[],
                     help="'Section Name=seconds' where that section's FIRST word really starts "
                          "in --audio, e.g. --anchor 'Pre-Chorus=32.0'. Repeatable. A single "
                          "global DTW across the whole song drifts once it hits anything the "
                          "TTS reference doesn't match well (an ad-lib, a long instrumental gap, "
                          "layered/gang vocals) -- once it drifts, EVERYTHING after that point is "
                          "wrong, because standard DTW has no way to 'reset'. Anchors break the "
                          "song into independently-aligned segments so an error in one segment "
                          "can't propagate into the next.")
    args = ap.parse_args()

    lyrics_path = args.lyrics or os.path.join(os.path.dirname(__file__), "lyrics")
    blocks = parse_lyrics_lines(lyrics_path)

    flat_words = []
    word_owner = []
    section_first_word_idx = {}
    line_word_idx = {}  # line text -> [start_idx, start_idx, ...] (one per occurrence, in order)
    for si, (name, lines) in enumerate(blocks):
        for li, line in enumerate(lines):
            for wi, w in enumerate(line.split()):
                if name not in section_first_word_idx:
                    section_first_word_idx[name] = len(flat_words)
                if wi == 0:
                    line_word_idx.setdefault(line, []).append(len(flat_words))
                flat_words.append(w)
                word_owner.append((si, li))

    print(f"{len(flat_words)} words across {len(blocks)} sections")

    os.makedirs(args.tmp_dir, exist_ok=True)
    print("synthesizing reference speech with espeak-ng ...")
    synthetic_track, word_bounds_synth = build_synthetic_track(flat_words, args.tmp_dir)

    print("loading real audio ...")
    real_audio, _ = librosa.load(args.audio, sr=SR, mono=True)
    audio_dur = len(real_audio) / SR

    # anchors: (word_index, real_time), always starting at word 0 / vocal-start
    anchors = [(0, args.vocal_start)]
    def normalize_word(w):
        return re.sub(r"[^a-z']", "", w.lower())

    def parse_occurrence(text):
        """'some text#2' -> ('some text', 2). Bare text (no '#N') means
        occurrence 1 -- the first (and normally only) one."""
        m = re.match(r"^(.*)#(\d+)$", text)
        if m:
            return m.group(1).strip(), int(m.group(2))
        return text, 1

    for spec in args.anchor:
        name, secs = parse_anchor(spec)
        if name.startswith("word:"):
            target_text, occurrence = parse_occurrence(name[len("word:"):].strip())
            target = normalize_word(target_text)
            matches = [i for i, w in enumerate(flat_words) if normalize_word(w) == target]
            if not matches:
                raise ValueError(f"anchor word '{target_text}' not found in lyrics")
            if occurrence < 1 or occurrence > len(matches):
                raise ValueError(f"anchor word '{target_text}' has {len(matches)} occurrence(s), "
                                  f"asked for #{occurrence} -- use 'word:{target_text}#N=secs'")
            anchors.append((matches[occurrence - 1], secs))
        elif name.startswith("line:"):
            line_text, occurrence = parse_occurrence(name[len("line:"):].strip())
            if line_text not in line_word_idx:
                raise ValueError(f"anchor line '{line_text}' not found; known lines: {list(line_word_idx)}")
            starts = line_word_idx[line_text]
            if occurrence < 1 or occurrence > len(starts):
                raise ValueError(f"anchor line '{line_text}' has {len(starts)} occurrence(s), "
                                  f"asked for #{occurrence} -- use 'line:{line_text}#N=secs'")
            anchors.append((starts[occurrence - 1], secs))
        else:
            if name not in section_first_word_idx:
                raise ValueError(f"anchor section '{name}' not found; known sections: {list(section_first_word_idx)}")
            anchors.append((section_first_word_idx[name], secs))
    anchors.sort(key=lambda a: a[0])
    # de-dupe (e.g. if an anchor lands on word 0 again)
    seen = set()
    anchors = [a for a in anchors if not (a[0] in seen or seen.add(a[0]))]

    print(f"aligning in {len(anchors)} segment(s) using anchors: {anchors}")

    word_bounds_real = [None] * len(flat_words)
    for seg_i in range(len(anchors)):
        w_start, t_start = anchors[seg_i]
        w_end = anchors[seg_i + 1][0] if seg_i + 1 < len(anchors) else len(flat_words)
        t_end = anchors[seg_i + 1][1] if seg_i + 1 < len(anchors) else audio_dur

        synth_seg_start = word_bounds_synth[w_start][0]
        synth_seg_end = word_bounds_synth[w_end - 1][1]
        synth_slice = synthetic_track[int(synth_seg_start * SR):int(synth_seg_end * SR)]
        real_slice = real_audio[int(t_start * SR):int(t_end * SR)]

        print(f"  segment words[{w_start}:{w_end}]: {len(synth_slice)/SR:.1f}s synthetic vs "
              f"{len(real_slice)/SR:.1f}s real ({t_start:.1f}s-{t_end:.1f}s)")
        to_real_time = dtw_map(synth_slice, real_slice)

        for k in range(w_start, w_end):
            s, e = word_bounds_synth[k]
            local_s = s - synth_seg_start
            local_e = e - synth_seg_start
            word_bounds_real[k] = (t_start + to_real_time(local_s), t_start + to_real_time(local_e))

    section_timing = []
    for si, (name, lines) in enumerate(blocks):
        line_entries = []
        for li, line in enumerate(lines):
            idxs = [k for k, owner in enumerate(word_owner) if owner == (si, li)]
            if not idxs:
                continue
            s = min(word_bounds_real[k][0] for k in idxs)
            e = max(word_bounds_real[k][1] for k in idxs)
            line_entries.append({"text": line, "start": round(s, 3), "end": round(e, 3)})
        section_timing.append({"section": name, "lines": line_entries})

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(section_timing, f, indent=2, ensure_ascii=False)
    print(f"saved: {args.out}")


if __name__ == "__main__":
    main()
