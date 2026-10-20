#!/usr/bin/env python3
"""
Overlays a scratch vocal take onto a section's instrumental mix, to preview
how the vocal cadence sits against the beat -- NOT a final vocal, just a
reference take to check timing/flow before recording for real.

Usage: python3 "musica/Kicking Stones v2/preview_with_vocal.py" \
    --section verse1 --vocal "vocals/reference_takes/verse1_part1_take1.m4a" \
    --version v11
"""
import argparse
import os
import subprocess
import numpy as np
from scipy.io import wavfile

SR = 44100
PROJECT_DIR = "musica/Kicking Stones v2"


def load_wav_mono(path):
    sr, data = wavfile.read(path)
    if data.ndim > 1:
        data = data.mean(axis=1)
    data = data.astype(np.float32)
    if data.dtype != np.float32 or np.max(np.abs(data)) > 1.5:
        data = data / 32768.0
    if sr != SR:
        raise ValueError(f"expected {SR} Hz, got {sr}")
    return data


def convert_to_wav(src_path, dst_path):
    subprocess.run(
        ["ffmpeg", "-y", "-i", src_path, "-ar", str(SR), "-ac", "1", dst_path],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", required=True, help="section name under versions/<version>/sections/")
    ap.add_argument("--vocal", required=True, help="path to the vocal take (m4a/wav), relative to repo root")
    ap.add_argument("--version", required=True, help="e.g. v11")
    ap.add_argument("--offset", type=float, default=0.0, help="seconds into the section where the vocal starts")
    ap.add_argument("--vocal-gain", type=float, default=1.0)
    args = ap.parse_args()

    section_dir = os.path.join(PROJECT_DIR, "versions", args.version, "sections", args.section)
    instrumental_path = os.path.join(section_dir, "mix.wav")
    instrumental = load_wav_mono(instrumental_path)

    vocal_src = args.vocal
    if not vocal_src.lower().endswith(".wav"):
        tmp_wav = "/tmp/_vocal_preview_tmp.wav"
        convert_to_wav(vocal_src, tmp_wav)
        vocal_src = tmp_wav
    vocal = load_wav_mono(vocal_src)
    vocal = vocal * args.vocal_gain

    offset_samples = int(args.offset * SR)
    n = max(len(instrumental), offset_samples + len(vocal))
    combined = np.zeros(n)
    combined[:len(instrumental)] += instrumental
    combined[offset_samples:offset_samples + len(vocal)] += vocal

    peak = np.max(np.abs(combined))
    if peak > 0.98:
        combined = combined * (0.98 / peak)

    out_path = os.path.join(section_dir, f"preview_with_vocal_{os.path.splitext(os.path.basename(args.vocal))[0]}.wav")
    wavfile.write(out_path, SR, (combined * 32767).astype(np.int16))
    print(f"guardado: {out_path}")


if __name__ == "__main__":
    main()
