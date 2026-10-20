#!/usr/bin/env python3
"""
Builds the base lyric video for Kicking Stones: 16:9 frame, dark background,
the square (1:1) cover art centered near the top, English lyric captions
below it timed against the REAL vocal audio via DTW forced alignment
(align_lyrics.py), with the Spanish translation shown smaller underneath.

Usage:
  python3 "musica/Kicking Stones v2/build_videoclip.py" \
      --audio "musica/Kicking Stones v2/final_master/KickingStonesv5.mp3" \
      --timing "musica/Kicking Stones v2/lyrics_timing.json" \
      --cover "musica/Kicking Stones v2/portada.jpg" \
      --lyrics-es "musica/Kicking Stones v2/lyrics_es" \
      --out videoclip_v10_16x9.mp4
"""
import argparse
import json
import os
import re

from moviepy import (
    ImageClip, TextClip, CompositeVideoClip, ColorClip, AudioFileClip,
)

W, H = 1920, 1080  # 16:9
BG_COLOR = (0, 0, 0)  # pure black
COVER_SIZE = 560  # the 1:1 square cover art, native aspect, not stretched --
# shrunk to make room for two caption rows (English + Spanish) below it
COVER_TOP = 40
EN_CAPTION_TOP = COVER_TOP + COVER_SIZE + 20
EN_CAPTION_HEIGHT = 190
ES_CAPTION_TOP = EN_CAPTION_TOP + EN_CAPTION_HEIGHT + 10
ES_CAPTION_HEIGHT = 170
FPS = 24
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def max_caption_duration(text):
    """A single word (or short phrase) sometimes lands right before a long
    instrumental gap with nothing else to anchor against -- the alignment
    then has no real signal for how long it should hold and can stretch a
    caption across the whole gap. Cap by word count so a caption disappears
    once it's plausibly finished being sung, not when the next line begins."""
    words = len(text.split())
    return min(8.0, words * 1.3 + 1.0)


def parse_lyrics_lines_flat(path):
    """Flat list of lines (dropping [Section] tags), in file order -- used
    to pair the Spanish translation file 1:1 by position with the English
    lines already time-stamped in lyrics_timing.json. The two files use
    different section names (Verso vs Verse, Coro vs Chorus, ...) so pairing
    by name isn't reliable; pairing by position is, since both follow the
    same song structure."""
    lines = []
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if line and not (line.startswith("[") and line.endswith("]")):
            lines.append(line)
    return lines


def slow_zoom_cover(image_path, duration, zoom_to=1.05):
    """The cover art, native 1:1 square, centered near the top of the 16:9
    frame -- with a barely-there zoom so it isn't a dead frozen image."""
    base = ImageClip(image_path)
    scale = max(COVER_SIZE / base.w, COVER_SIZE / base.h) * zoom_to * 1.02
    base = base.resized(scale)

    def resize_over_time(t):
        frac = t / duration if duration > 0 else 0
        return 1.0 + (zoom_to - 1.0) * frac

    zoomed = base.resized(resize_over_time).with_position(("center", "center"))
    cropped = CompositeVideoClip([zoomed], size=(COVER_SIZE, COVER_SIZE)).with_duration(duration)
    return cropped.with_position(("center", COVER_TOP))


def caption_clip(text, duration, top, box_height, font_size, color):
    # No stroke: a stroke outline paints pixels beyond the glyph's own
    # bounding box on every edge. No bar behind the text either: captions
    # only ever sit in the solid-black area below the cover art (never over
    # the art itself), so a dark bar there is invisible by construction --
    # plain bold text against the pure-black background already has full
    # contrast.
    #
    # size=(width, None) (auto height) is what was ACTUALLY clipping
    # descenders (g, y, j, ...): moviepy/Pillow's own auto-computed caption
    # height under-measures them, cutting the bottom of the glyph regardless
    # of stroke. A fixed, generous box height with vertical_align="center"
    # gives every glyph room on both sides instead of being sized tight
    # around a measurement that doesn't account for descenders.
    txt = TextClip(font=FONT, text=text, font_size=font_size, color=color, method="caption",
                    size=(int(W * 0.8), box_height), text_align="center", vertical_align="center")
    return txt.with_duration(max(duration, 0.05)).with_position(("center", top))


def build(audio_path, timing_path, cover_path, lyrics_es_path, out_path):
    audio = AudioFileClip(audio_path)
    total_dur = audio.duration

    with open(timing_path, encoding="utf-8") as f:
        section_timing = json.load(f)

    es_lines = parse_lyrics_lines_flat(lyrics_es_path) if lyrics_es_path else None
    en_lines_flat = [line for section in section_timing for line in section["lines"]]
    if es_lines is not None and len(es_lines) != len(en_lines_flat):
        raise ValueError(f"lyrics_es has {len(es_lines)} lines but lyrics_timing.json has "
                          f"{len(en_lines_flat)} -- they must match 1:1 by position")

    bg = ColorClip((W, H), color=BG_COLOR).with_duration(total_dur)
    cover = slow_zoom_cover(cover_path, total_dur)

    overlay_clips = []
    for i, line in enumerate(en_lines_flat):
        raw_dur = line["end"] - line["start"]
        dur = max(0.3, min(raw_dur, max_caption_duration(line["text"])))
        cap = caption_clip(line["text"], dur, EN_CAPTION_TOP, EN_CAPTION_HEIGHT,
                            font_size=42, color="white").with_start(line["start"])
        overlay_clips.append(cap)
        if es_lines is not None:
            # A distinct color (not just dimmer white) makes clear this is a
            # translation to read, not a second vocal to sing along with.
            es_cap = caption_clip(es_lines[i], dur, ES_CAPTION_TOP, ES_CAPTION_HEIGHT,
                                   font_size=37, color="#FFD23F").with_start(line["start"])
            overlay_clips.append(es_cap)

    final = CompositeVideoClip([bg, cover, *overlay_clips], size=(W, H)).with_duration(total_dur)
    final = final.with_audio(audio)

    final.write_videofile(out_path, fps=FPS, codec="libx264", audio_codec="aac",
                           preset="medium", threads=4)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--timing", required=True)
    ap.add_argument("--cover", required=True)
    ap.add_argument("--lyrics-es", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    build(args.audio, args.timing, args.cover, args.lyrics_es, args.out)
