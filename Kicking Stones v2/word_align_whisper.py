#!/usr/bin/env python3
"""
Word-level alignment using OpenAI Whisper with word_timestamps=True.
Matches Whisper output against our known lyrics, producing per-word start/end.

Usage:
  python3 word_align_whisper.py \
      --audio final_master/KickingStonesv5.mp3 \
      --out lyrics_timing.json

The output extends the existing format with a "words" array per line:
  {"text": "Singers taunting on pulpit mic", "start":6.5, "end":10.0,
   "words": [{"text":"Singers","start":6.5,"end":7.1}, ...]}
"""
import argparse
import json
import re
import os

def normalize(w: str) -> str:
    return re.sub(r"[^a-z']", "", w.lower())

def syllable_count(word: str) -> int:
    """Rough syllable count for proportional time distribution fallback."""
    w = word.lower()
    w = re.sub(r"[^a-z]", "", w)
    count = len(re.findall(r"[aeiouy]+", w))
    return max(1, count)

def split_hyphenated(word: str):
    """'mega-reform' -> ['mega', 'reform']"""
    if "-" in word:
        return word.split("-")
    return [word]

def interpolate_words(line_words, line_start, line_end):
    """
    Fallback: distribute time proportionally by syllable count.
    Used when whisper doesn't cover a word.
    """
    syllables = [syllable_count(w) for w in line_words]
    total = sum(syllables)
    duration = line_end - line_start
    result = []
    cursor = line_start
    for w, s in zip(line_words, syllables):
        word_dur = duration * s / total
        result.append({"text": w, "start": round(cursor, 3), "end": round(cursor + word_dur, 3)})
        cursor += word_dur
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="base", help="Whisper model: tiny/base/small/medium")
    ap.add_argument("--lyrics", default=None)
    args = ap.parse_args()

    import whisper

    base_dir = os.path.dirname(os.path.abspath(__file__))
    lyrics_path = args.lyrics or os.path.join(base_dir, "lyrics")

    # Load existing line-level timing for line start/end anchors
    timing_path = args.out
    with open(timing_path) as f:
        sections = json.load(f)

    print(f"Loading Whisper model '{args.model}'...")
    model = whisper.load_model(args.model)

    print(f"Transcribing with word timestamps: {args.audio}")
    result = model.transcribe(
        args.audio,
        word_timestamps=True,
        language="en",
        condition_on_previous_text=False,
    )

    # Collect all whisper word timestamps
    whisper_words = []
    for seg in result["segments"]:
        for w in seg.get("words", []):
            whisper_words.append({
                "text": normalize(w["word"]),
                "start": w["start"],
                "end": w["end"],
            })

    print(f"Whisper found {len(whisper_words)} words")

    # Match whisper words to our lyrics line by line
    wptr = 0
    for section in sections:
        for line in section["lines"]:
            raw_words = line["text"].split()
            # Expand hyphenated words
            expanded = []
            for rw in raw_words:
                parts = split_hyphenated(rw)
                expanded.extend(parts)

            line_start = line["start"]
            line_end = line["end"]

            # Find whisper words that fall within this line's time window
            line_wwords = [
                ww for ww in whisper_words
                if ww["start"] >= line_start - 0.5 and ww["end"] <= line_end + 0.5
            ]

            if len(line_wwords) >= max(1, len(expanded) // 2):
                # Good coverage — match greedily by normalized text
                word_timings = []
                ww_ptr = 0
                for ew in expanded:
                    en = normalize(ew)
                    matched = None
                    # Search forward for a match within window
                    for j in range(ww_ptr, min(ww_ptr + 5, len(line_wwords))):
                        if line_wwords[j]["text"] == en or en in line_wwords[j]["text"] or line_wwords[j]["text"] in en:
                            matched = line_wwords[j]
                            ww_ptr = j + 1
                            break
                    if matched:
                        word_timings.append({"text": ew, "start": round(matched["start"], 3), "end": round(matched["end"], 3)})
                    else:
                        # Fallback: interpolate from last known position
                        last_t = word_timings[-1]["end"] if word_timings else line_start
                        remaining_words = len(expanded) - len(word_timings)
                        remaining_time = line_end - last_t
                        dur = remaining_time / max(remaining_words, 1)
                        word_timings.append({"text": ew, "start": round(last_t, 3), "end": round(last_t + dur, 3)})
                line["words"] = word_timings
            else:
                # Poor coverage — use syllable interpolation
                line["words"] = interpolate_words(expanded, line_start, line_end)

            print(f"  [{section['section']}] {line['text'][:40]!r} -> {len(line['words'])} words")

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    print(f"\nSaved word-level timing to {args.out}")


if __name__ == "__main__":
    main()
