#!/usr/bin/env python3
"""
Word-level timing using ffmpeg silencedetect within each known line window.

Strategy:
  1. For each line (start/end known), run ffmpeg silencedetect on that slice.
  2. Use detected silence boundaries as word separators.
  3. If not enough silences found, fall back to syllable-proportional distribution.
  4. Split hyphenated words (mega-reform -> mega + reform).

Usage:
  cd "musica/Kicking Stones v2"
  python3 word_align_ffmpeg.py
"""
import json, os, re, subprocess, sys

AUDIO = os.path.join(os.path.dirname(__file__), "final_master/KickingStonesv5.mp3")
TIMING = os.path.join(os.path.dirname(__file__), "lyrics_timing.json")
OUT = TIMING  # overwrite in place

# Silence detection on vocal-frequency band (200Hz-3kHz bandpass)
# Isolating vocal range from full mix makes gaps between words detectable
SILENCE_DB = -28
SILENCE_MIN_DUR = 0.04  # 40ms minimum


def split_word(w):
    """'mega-reform' -> ['mega', 'reform'], else [w]"""
    if "-" in w:
        return w.split("-")
    return [w]

def expand_words(text):
    """Split line text into display tokens, expanding hyphens."""
    tokens = []
    for w in text.split():
        tokens.extend(split_word(w))
    return tokens

def syllable_count(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w))
    return max(1, n)

def interpolate(words, start, end):
    sylls = [syllable_count(w) for w in words]
    total = sum(sylls)
    dur = end - start
    result, cursor = [], start
    for w, s in zip(words, sylls):
        d = dur * s / total
        result.append({"text": w, "start": round(cursor, 3), "end": round(cursor + d, 3)})
        cursor += d
    return result

def detect_silences(t_start, t_end):
    """Returns list of (silence_start, silence_end) in absolute time."""
    duration = t_end - t_start
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(t_start), "-t", str(duration),
        "-i", AUDIO,
        # bandpass to vocal range, then detect silence — instruments won't mask word gaps
        "-af", f"highpass=f=200,lowpass=f=3000,silencedetect=noise={SILENCE_DB}dB:d={SILENCE_MIN_DUR}",
        "-f", "null", "-"
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    output = r.stderr

    silences = []
    starts = re.findall(r"silence_start: ([\d.]+)", output)
    ends   = re.findall(r"silence_end: ([\d.]+)", output)
    for s, e in zip(starts, ends):
        s, e = float(s), float(e)
        if s >= t_start - 0.1 and e <= t_end + 0.1:
            silences.append((s, e))
    return silences

def assign_words(words, t_start, t_end, silences):
    """
    Map N words to time segments using silence boundaries.
    Silences mark gaps between words — we need N-1 boundaries for N words.
    """
    n = len(words)
    if n == 1:
        return [{"text": words[0], "start": round(t_start, 3), "end": round(t_end, 3)}]

    # Use silence midpoints as word boundaries
    boundaries = sorted([(s + e) / 2 for s, e in silences])

    # Filter to only boundaries within the line window
    boundaries = [b for b in boundaries if t_start < b < t_end]

    if len(boundaries) >= n - 1:
        # Enough boundaries — use first n-1 of them
        bounds = [t_start] + sorted(boundaries[:n-1]) + [t_end]
    elif len(boundaries) > 0:
        # Some boundaries — use what we have, fill the rest with interpolation
        # Place found boundaries at the "most likely" positions
        result = []
        # Assign known boundaries greedily to word gaps
        word_starts = [t_start]
        for b in boundaries:
            word_starts.append(b)
        while len(word_starts) < n:
            # Fill remaining with interpolation in the last segment
            last = word_starts[-1]
            remaining = n - len(word_starts) + 1
            remaining_words = words[len(word_starts)-1:]
            interp = interpolate(remaining_words, last, t_end)
            for item in interp[1:]:
                word_starts.append(item["start"])
            break
        word_starts = sorted(set(word_starts))[:n]
        ends = word_starts[1:] + [t_end]
        return [
            {"text": w, "start": round(s, 3), "end": round(e, 3)}
            for w, s, e in zip(words, word_starts, ends)
        ]
    else:
        # No usable boundaries — syllable interpolation
        return interpolate(words, t_start, t_end)

    result = []
    for i, w in enumerate(words):
        result.append({"text": w, "start": round(bounds[i], 3), "end": round(bounds[i+1], 3)})
    return result

def main():
    with open(TIMING) as f:
        sections = json.load(f)

    for section in sections:
        for line in section["lines"]:
            words = expand_words(line["text"])
            t_start = line["start"]
            t_end = line["end"]

            if len(words) <= 1:
                line["words"] = [{"text": w, "start": t_start, "end": t_end} for w in words]
                continue

            silences = detect_silences(t_start, t_end)
            word_timings = assign_words(words, t_start, t_end, silences)
            line["words"] = word_timings

            print(f"[{section['section']}] {line['text'][:40]!r}")
            for wt in word_timings:
                print(f"  {wt['text']:20s} {wt['start']:.2f} -> {wt['end']:.2f}")

    with open(OUT, "w") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    print(f"\nSaved: {OUT}")

if __name__ == "__main__":
    main()
