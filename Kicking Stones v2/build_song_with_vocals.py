#!/usr/bin/env python3
"""
Overlays vocal reference audio directly onto a version's continuous
mix.wav (from build_song.py's build_continuous_song), at the exact time
each Rap/Faster section starts.

Since the full mix is now one continuous render per instrument (no
per-section crossfade concatenation -- see build_continuous_song), section
start times are just cumulative bar durations at the song's single fixed
tempo: no crossfade-shrinkage math needed, unlike the old per-section-glue
approach this replaces.

Only the Rap/Faster sections currently have vocal reference material:
  - rapfaster1 ("Singers taunting..."): the user's own fully mastered
    Rap/Faster demo (vocals/mastered_reference/rap_faster_mastered.mp3).
  - rapfaster2 ("In the shadow..."): the short scratch take
    (vocals/reference_takes/verse1_part1_take1.m4a), placed at the top of
    the section as a flow reference (it's only ~3.8s, shorter than the
    8-bar section).

Usage: python3 "musica/Kicking Stones v2/build_song_with_vocals.py" --version v18
"""
import argparse
import os
import subprocess
import sys
import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(__file__))
from build_song import SR, PROJECT_DIR, SECTIONS, write_wav

VOCAL_GAIN_MASTERED = 1.4
VOCAL_GAIN_SCRATCH = 1.6


def load_wav_mono(path):
    sr, data = wavfile.read(path)
    if data.ndim > 1:
        data = data.mean(axis=1)
    data = data.astype(np.float32)
    if np.max(np.abs(data)) > 1.5:
        data = data / 32768.0
    if sr != SR:
        raise ValueError(f"expected {SR} Hz, got {sr} in {path}")
    return data


def convert_to_wav(src_path, dst_path):
    subprocess.run(
        ["ffmpeg", "-y", "-i", src_path, "-ar", str(SR), "-ac", "1", dst_path],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def load_any(path):
    if path.lower().endswith(".wav"):
        return load_wav_mono(path)
    tmp = f"/tmp/_vocal_conv_{os.path.basename(path)}.wav"
    convert_to_wav(path, tmp)
    return load_wav_mono(tmp)


def section_start_times():
    """Cumulative start time (sec) of each section in the continuous mix --
    just bars * seconds-per-bar at the song's single fixed tempo, since
    there's no crossfade shrinkage to account for anymore."""
    bpm = SECTIONS[0]["bpm"]
    assert all(s["bpm"] == bpm for s in SECTIONS), "expected one fixed tempo across the song"
    sec_per_bar = 4 * (60.0 / bpm)
    starts = {}
    cum_bars = 0
    for s in SECTIONS:
        starts[s["name"]] = cum_bars * sec_per_bar
        cum_bars += s["bars"]
    return starts


def overlay(mix, vocal, gain, offset_sec):
    vocal = vocal * gain
    offset = int(offset_sec * SR)
    out = mix.copy()
    end = min(len(out), offset + len(vocal))
    if end > offset:
        out[offset:end] += vocal[: end - offset]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True, help="e.g. v18")
    args = ap.parse_args()

    version_dir = os.path.join(PROJECT_DIR, "versions", args.version)
    mix_path = os.path.join(version_dir, "mix.wav")
    mix = load_wav_mono(mix_path)

    starts = section_start_times()

    mastered_path = os.path.join(PROJECT_DIR, "vocals/mastered_reference/rap_faster_mastered.mp3")
    scratch_path = os.path.join(PROJECT_DIR, "vocals/reference_takes/verse1_part1_take1.m4a")
    mastered_vocal = load_any(mastered_path)
    scratch_vocal = load_any(scratch_path)

    mix = overlay(mix, mastered_vocal, VOCAL_GAIN_MASTERED, starts["rapfaster1"])
    mix = overlay(mix, scratch_vocal, VOCAL_GAIN_SCRATCH, starts["rapfaster2"])

    peak = np.max(np.abs(mix))
    if peak > 0.98:
        mix = mix * (0.98 / peak)

    out_path = os.path.join(version_dir, "mix_with_vocals.wav")
    write_wav(mix, out_path)
    print(f"rapfaster1 vocal @ {starts['rapfaster1']:.2f}s, rapfaster2 vocal @ {starts['rapfaster2']:.2f}s")


if __name__ == "__main__":
    main()
