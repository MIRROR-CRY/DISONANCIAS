#!/usr/bin/env python3
"""
Equalizes perceived loudness across sections so no part of the song
sounds quieter than another (even though arrangement density still
varies - fewer instruments in the verse/bridge, more in the chorus -
the overall volume level stays consistent throughout).

Computes RMS per section, scales each section to match a common
target RMS, and crossfades at section boundaries to avoid clicks.
Must run LAST, after all layers (synth, bass, strings) are mixed in.
"""

import numpy as np
from scipy.io import wavfile
import os

from generate_backing_track import SECTIONS, SAMPLE_RATE

CROSSFADE_MS = 30

def rms(signal):
    return np.sqrt(np.mean(signal.astype(np.float64) ** 2))

def normalize_sections(audio, sections, sample_rate):
    audio = audio.astype(np.float64)
    boundaries = []
    t = 0
    for kind, duration in sections:
        start = int(t * sample_rate)
        end = int((t + duration) * sample_rate)
        boundaries.append((start, min(end, len(audio)), kind))
        t += duration

    section_rms = [rms(audio[s:e]) for s, e, _k in boundaries]
    nonzero = [r for r in section_rms if r > 1e-6]
    target_rms = np.median(nonzero) if nonzero else 1.0

    out = np.zeros_like(audio)
    for (start, end, kind), r in zip(boundaries, section_rms):
        gain = (target_rms / r) if r > 1e-6 else 1.0
        # Cap gain so near-silent sections (like a held root) don't get
        # blown up into noise - just brought within a reasonable range.
        gain = min(gain, 3.0)
        out[start:end] = audio[start:end] * gain
        print(f"   {kind:<13} rms={r:.4f} -> gain={gain:.2f}x")

    # Crossfade at each internal boundary to avoid clicks from the gain jump
    fade_samples = int(sample_rate * CROSSFADE_MS / 1000)
    for i in range(1, len(boundaries)):
        boundary = boundaries[i][0]
        lo = max(0, boundary - fade_samples // 2)
        hi = min(len(out), boundary + fade_samples // 2)
        if hi > lo:
            fade = np.linspace(0, 1, hi - lo)
            prev_gain = min((target_rms / section_rms[i - 1]) if section_rms[i - 1] > 1e-6 else 1.0, 3.0)
            curr_gain = min((target_rms / section_rms[i]) if section_rms[i] > 1e-6 else 1.0, 3.0)
            raw = audio[lo:hi]
            out[lo:hi] = raw * (prev_gain * (1 - fade) + curr_gain * fade)

    return out

def main():
    base_dir = os.path.dirname(__file__)
    backing_track_path = os.path.join(base_dir, 'audio', 'backing_track_base.wav')

    sr, audio = wavfile.read(backing_track_path)
    assert sr == SAMPLE_RATE

    print("Equalizing loudness per section:")
    audio_f = audio.astype(np.float64) / 32767.0
    normalized = normalize_sections(audio_f, SECTIONS, sr)

    max_val = np.max(np.abs(normalized))
    if max_val > 0:
        normalized = normalized / max_val * 0.95

    normalized_16bit = (normalized * 32767).astype(np.int16)
    wavfile.write(backing_track_path, sr, normalized_16bit)

    print()
    print("✓ Loudness equalized across all sections")
    print(f"✓ Saved to: {backing_track_path}")

if __name__ == '__main__':
    main()
