#!/usr/bin/env python3
"""Transcribe a clean vocal take into notes.

Pitch tracking on a vocal is not the same problem as pitch tracking on a
synthesiser, and two things have to be handled or the result is garbage:

1. THE TAKE IS NOT AT CONCERT PITCH. These recordings sit about 30 cents
   below the master. Rounding raw frequencies to the nearest semitone
   without correcting for that pushes roughly a third of the notes to the
   wrong one. The offset is measured per file and subtracted first.

2. A SUNG NOTE IS NOT A CONSTANT FREQUENCY. It has an attack that slides
   into pitch, vibrato around it, and a release that falls away. Taking the
   mean of a note's frames drags it toward the glide; the median of its
   stable middle does not, so that is what is used.

What comes out is a transcription, not a ground truth. Every note carries
its confidence, and anything the tracker was unsure about is reported
rather than quietly rounded into the score.
"""

import numpy as np


def transcribe(path, bpm, sr=22050, fmin=70, fmax=700,
               min_note_sec=0.08, onset_delta=0.12, min_conf=0.0):
    import librosa

    y, _sr = librosa.load(path, sr=sr, mono=True)
    tuning = librosa.estimate_tuning(y=y, sr=sr)      # in fractions of a semitone

    f0, voiced, prob = librosa.pyin(
        y, fmin=fmin, fmax=fmax, sr=sr, frame_length=2048)
    times = librosa.times_like(f0, sr=sr)
    midi = librosa.hz_to_midi(f0) - tuning            # to concert pitch

    # Segment on onsets, not on pitch stability. A first attempt grouped
    # frames by how close they stayed to a running median, and on a delivery
    # this speech-like the median drifts with the voice, so a whole sung
    # line came out as one note. Where a singer starts a new syllable is an
    # onset, and that is the boundary that matters.
    onset_f = librosa.onset.onset_detect(
        y=y, sr=sr, backtrack=True, units="frames",
        hop_length=512, delta=onset_delta, wait=3)
    onset_t = librosa.frames_to_time(onset_f, sr=sr, hop_length=512)
    edges = [0.0] + [t for t in onset_t if t > 0] + [times[-1]]

    notes = []
    for a, b in zip(edges[:-1], edges[1:]):
        if b - a < min_note_sec:
            continue
        sel = [(times[i], midi[i], prob[i]) for i in range(len(midi))
               if a <= times[i] < b and voiced[i] and not np.isnan(midi[i])
               and prob[i] >= min_conf]
        # NOTE: filter on the voiced FLAG, not on voiced_prob. pyin's
        # voiced_prob on these takes has a median of 0.01 even where it
        # confidently reports an f0, so thresholding it at 0.55 threw away
        # 96% of the usable frames and the first run found almost no notes.
        if len(sel) < 3:
            continue
        notes.append(sel)

    beat = 60.0 / bpm
    out = []
    for grp in notes:
        t0, t1 = grp[0][0], grp[-1][0]
        if t1 - t0 < min_note_sec:
            continue
        # The middle of the note, where the pitch has settled.
        core = grp[len(grp) // 4: max(len(grp) // 4 + 1, 3 * len(grp) // 4)]
        pitch = float(np.median([c[1] for c in core]))
        conf = float(np.mean([c[2] for c in core]))
        cents = (pitch - round(pitch)) * 100
        out.append({
            "midi": int(round(pitch)),
            "start_sec": float(t0),
            "dur_sec": float(t1 - t0),
            "start_beat": t0 / beat,
            "dur_beats": (t1 - t0) / beat,
            "cents_off": cents,
            "confidence": conf,
        })
    return out, tuning


def summarise(notes, tuning, key_notes=None):
    import librosa
    print(f"  afinacion de la toma: {tuning * 100:+.0f} cents (corregida)")
    print(f"  notas detectadas: {len(notes)}")
    if not notes:
        return
    ms = [n["midi"] for n in notes]
    print(f"  rango: {librosa.midi_to_note(min(ms))} a {librosa.midi_to_note(max(ms))}")
    off = np.mean([abs(n["cents_off"]) for n in notes])
    print(f"  desviacion media del semitono: {off:.0f} cents")
    conf = np.mean([n["confidence"] for n in notes])
    print(f"  confianza media: {conf:.2f}")
    if key_notes:
        inside = sum(1 for m in ms if m % 12 in key_notes)
        print(f"  notas dentro de la tonalidad: {inside}/{len(ms)} = {100*inside/len(ms):.0f}%")
