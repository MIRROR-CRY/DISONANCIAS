#!/usr/bin/env python3
"""
Adds a real (sampled, non-synthetic) low string instrument (cello) during
the bridge section, right where the Gen Alpha melody ("ni-ni-ni-ni") drops
out - so the bridge has something warm and real filling that space instead
of just chords + Dame Luz.

Same approach as add_bass_arpeggio.py: MIDI rendered through fluidsynth
with the FluidR3_GM soundfont (GM program 42, Cello - real sampled string
audio, not a sine/triangle oscillator).
"""

import subprocess
import os
import numpy as np
from scipy.io import wavfile
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

from generate_backing_track import SECTIONS, CHORD_DURATION, SAMPLE_RATE

SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
CELLO_PROGRAM = 42  # GM program: Cello (real sampled low strings)
TICKS_PER_BEAT = 480
BPM = 100

# Chord root notes in cello register (warm, low but not bass-register)
CHORD_ROOTS_MIDI = {
    'Dm': 50,  # D3
    'G':  55,  # G3
    'C':  48,  # C3
    'F':  53,  # F3
}
CHORD_ORDER = ['Dm', 'G', 'C', 'F']

def seconds_to_ticks(seconds, tempo_bpm=BPM):
    return int(seconds * tempo_bpm / 60 * TICKS_PER_BEAT)

def find_bridge_window():
    t = 0.0
    for kind, duration in SECTIONS:
        if kind == 'bridge':
            return t, t + duration
        t += duration
    raise ValueError("No 'bridge' section found in SECTIONS")

def build_midi():
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)

    tempo = mido.bpm2tempo(BPM)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    track.append(Message('program_change', program=CELLO_PROGRAM, channel=0, time=0))

    bridge_start, bridge_end = find_bridge_window()

    events = []
    t = bridge_start
    chord_i = 0
    velocity = 65  # warm, present but not overpowering
    while t < bridge_end:
        chord_name = CHORD_ORDER[chord_i % 4]
        note = CHORD_ROOTS_MIDI[chord_name]
        note_start = t
        note_end = min(t + CHORD_DURATION, bridge_end)
        events.append((seconds_to_ticks(note_start), 'on', note, velocity))
        events.append((seconds_to_ticks(note_end), 'off', note, 0))
        t += CHORD_DURATION
        chord_i += 1

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, kind, note, velocity in events:
        delta = tick - last_tick
        if kind == 'on':
            track.append(Message('note_on', note=note, velocity=velocity, channel=0, time=delta))
        else:
            track.append(Message('note_off', note=note, velocity=0, channel=0, time=delta))
        last_tick = tick

    return mid

def render_midi_to_wav(midi_path, wav_path):
    subprocess.run([
        'fluidsynth', '-ni', SOUNDFONT, midi_path,
        '-F', wav_path, '-r', str(SAMPLE_RATE)
    ], check=True, capture_output=True)

def mix_strings_into_backing_track():
    base_dir = os.path.dirname(__file__)
    audio_dir = os.path.join(base_dir, 'audio')
    midi_path = os.path.join(audio_dir, 'strings_bridge.mid')
    strings_wav_path = os.path.join(audio_dir, 'strings_bridge_render.wav')
    backing_track_path = os.path.join(audio_dir, 'backing_track_base.wav')

    print("[1/4] Building cello line MIDI for the bridge section...")
    mid = build_midi()
    mid.save(midi_path)

    print("[2/4] Rendering with fluidsynth + FluidR3_GM soundfont (real sampled cello)...")
    render_midi_to_wav(midi_path, strings_wav_path)

    print("[3/4] Loading and mixing into backing track...")
    sr_backing, backing = wavfile.read(backing_track_path)
    sr_strings, strings = wavfile.read(strings_wav_path)
    assert sr_backing == sr_strings == SAMPLE_RATE

    if strings.ndim == 2:
        strings = strings.mean(axis=1)

    backing_f = backing.astype(np.float64) / 32767.0
    strings_f = strings.astype(np.float64) / 32767.0

    if len(strings_f) < len(backing_f):
        strings_f = np.pad(strings_f, (0, len(backing_f) - len(strings_f)))
    else:
        strings_f = strings_f[:len(backing_f)]

    strings_gain = 0.7
    mixed = backing_f + strings_f * strings_gain

    max_val = np.max(np.abs(mixed))
    if max_val > 1.0:
        mixed = mixed / max_val * 0.97

    mixed_16bit = (mixed * 32767).astype(np.int16)

    print("[4/4] Saving updated backing_track_base.wav...")
    wavfile.write(backing_track_path, SAMPLE_RATE, mixed_16bit)

    print()
    print("✓ Real cello line (FluidR3_GM soundfont) mixed into the bridge section")
    print(f"  MIDI: {midi_path}")
    print(f"  Rendered strings: {strings_wav_path}")

if __name__ == '__main__':
    mix_strings_into_backing_track()
