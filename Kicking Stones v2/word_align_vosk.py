#!/usr/bin/env python3
"""
Word-level forced alignment using Vosk (lightweight offline ASR).
Transcribes the audio with word timestamps, then matches against known lyrics.

Usage:
  cd "musica/Kicking Stones v2"
  python3 word_align_vosk.py
"""
import json, os, re, subprocess, wave, struct

AUDIO   = os.path.join(os.path.dirname(__file__), "final_master/KickingStonesVoiceOnly.mp3")
TIMING  = os.path.join(os.path.dirname(__file__), "lyrics_timing.json")
MODEL   = "/tmp/vosk-model-small-en-us-0.15"
WAV_TMP = "/tmp/ks_mono16k.wav"


def to_wav(src, dst):
    subprocess.run([
        "ffmpeg", "-y", "-i", src,
        "-ar", "16000", "-ac", "1", "-f", "wav", dst
    ], check=True, capture_output=True)


def run_vosk(wav_path, model_path):
    from vosk import Model, KaldiRecognizer, SetLogLevel
    SetLogLevel(-1)
    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    words = []
    with wave.open(wav_path) as wf:
        while True:
            data = wf.readframes(4000)
            if not data:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                words.extend(result.get("result", []))
    result = json.loads(rec.FinalResult())
    words.extend(result.get("result", []))
    return words  # [{word, start, end, conf}, ...]


def normalize(w):
    return re.sub(r"[^a-z']", "", w.lower())


def syllable_count(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    return max(1, len(re.findall(r"[aeiouy]+", w)))


def interpolate(tokens, t_start, t_end):
    sylls = [syllable_count(t) for t in tokens]
    total = sum(sylls)
    dur = t_end - t_start
    result, cursor = [], t_start
    for t, s in zip(tokens, sylls):
        d = dur * s / total
        result.append({"text": t, "start": round(cursor, 3), "end": round(cursor + d, 3)})
        cursor += d
    return result


def expand(text):
    tokens = []
    for w in text.split():
        if "-" in w:
            tokens.extend(w.split("-"))
        else:
            tokens.append(w)
    return tokens


def match_line(tokens, vosk_words, t_start, t_end, window=0.6):
    """
    Match tokens to vosk words in strict chronological order within line window.
    Falls back to syllable interpolation for unmatched tokens.
    """
    candidates = sorted([
        w for w in vosk_words
        if w["end"] >= t_start - window and w["start"] <= t_end + window
    ], key=lambda w: w["start"])

    result = [None] * len(tokens)
    used = set()
    cptr = 0  # strictly advance forward through candidates

    for i, tok in enumerate(tokens):
        norm_tok = normalize(tok)
        for j in range(cptr, len(candidates)):
            if j in used:
                continue
            norm_cw = normalize(candidates[j]["word"])
            if norm_cw == norm_tok or norm_tok in norm_cw or norm_cw in norm_tok:
                ws = max(candidates[j]["start"], t_start)
                we = min(candidates[j]["end"], t_end)
                if we > ws:
                    result[i] = {"text": tok, "start": round(ws, 3), "end": round(we, 3)}
                    used.add(j)
                    cptr = j + 1
                    break

    # Fill unmatched tokens with interpolation between neighbors
    i = 0
    while i < len(result):
        if result[i] is not None:
            i += 1
            continue
        # find run of unmatched
        j = i
        while j < len(result) and result[j] is None:
            j += 1
        seg_start = result[i-1]["end"] if i > 0 and result[i-1] else t_start
        seg_end = result[j]["start"] if j < len(result) and result[j] else t_end
        filled = interpolate([tokens[k] for k in range(i, j)], seg_start, seg_end)
        for k, entry in zip(range(i, j), filled):
            result[k] = entry
        i = j

    # Final pass: ensure strictly monotonic start times
    cursor = t_start
    for entry in result:
        if entry["start"] < cursor:
            entry["start"] = round(cursor, 3)
        if entry["end"] <= entry["start"]:
            entry["end"] = round(entry["start"] + 0.1, 3)
        cursor = entry["end"]

    return result


def main():
    print("Converting to 16kHz mono WAV...")
    to_wav(AUDIO, WAV_TMP)

    print("Running Vosk ASR with word timestamps...")
    vosk_words = run_vosk(WAV_TMP, MODEL)
    print(f"  {len(vosk_words)} words recognized")

    with open(TIMING) as f:
        sections = json.load(f)

    for section in sections:
        for line in section["lines"]:
            tokens = expand(line["text"])
            timings = match_line(tokens, vosk_words, line["start"], line["end"])
            line["words"] = timings
            print(f"[{section['section']}] {line['text'][:40]!r}")
            for wt in timings:
                print(f"  {wt['text']:20s} {wt['start']:.3f} -> {wt['end']:.3f}")

    with open(TIMING, "w") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    print(f"\nSaved: {TIMING}")


if __name__ == "__main__":
    main()
