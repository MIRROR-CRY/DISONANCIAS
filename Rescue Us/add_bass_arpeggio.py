#!/usr/bin/env python3
"""
Adds a real (sampled, non-synthetic) acoustic bass arpeggio to the
backing track, rendered via fluidsynth + a General MIDI soundfont
(FluidR3_GM, real sampled instruments) instead of sine/triangle waves.

Follows the same Dm-G-C-F progression and section structure as
generate_backing_track.py, with density/velocity varying per section
so it breathes with the rest of the arrangement.
"""

import subprocess
import os
import numpy as np
from scipy.io import wavfile
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

from generate_backing_track import SECTIONS, CHORD_DURATION, SAMPLE_RATE

SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
ACOUSTIC_BASS_PROGRAM = 32  # GM program: Acoustic Bass (real sampled upright bass)
TICKS_PER_BEAT = 480
BPM = 100

# Chord tones in MIDI note numbers, low register (bass range)
CHORD_TONES_MIDI = {
    'Dm': [38, 41, 45],  # D2 F2 A2
    'G':  [43, 47, 50],  # G2 B2 D3
    'C':  [36, 40, 43],  # C2 E2 G2
    'F':  [41, 45, 48],  # F2 A2 C3
}
CHORD_ORDER = ['Dm', 'G', 'C', 'F']

# Per-section arpeggio behavior: (note_pattern_indices, note_duration_s, velocity)
# note_pattern_indices index into the chord's [root, third, fifth]
SECTION_ARPEGGIO = {
    'intro':        None,                                   # silent, let the pad breathe
    'verse':        ([0, 2], 1.0, 55),                       # sparse: root-fifth half notes, quiet
    'pre_chorus':   ([0, 1, 2, 1], 0.5, 70),                  # building: quarter-note arpeggio
    'chorus':       ([0, 1, 2, 1, 0, 1, 2, 1], 0.25, 90),     # full eighth-note arpeggio
    'bridge':       ([0], 2.0, 45),                           # breakdown: just a held root, very quiet
    'chorus_final': ([0, 1, 2, 1, 0, 1, 2, 1], 0.25, 100),    # biggest, most active
}

def seconds_to_ticks(seconds, tempo_bpm=BPM):
    beats = seconds * tempo_bpm / 60
    return int(beats * TICKS_PER_BEAT)

def build_midi():
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)

    tempo = mido.bpm2tempo(BPM)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    track.append(Message('program_change', program=ACOUSTIC_BASS_PROGRAM, channel=0, time=0))

    events = []  # (tick, type, note, velocity)
    global_time = 0.0

    for kind, duration in SECTIONS:
        behavior = SECTION_ARPEGGIO.get(kind)
        section_end = global_time + duration

        if behavior is not None:
            pattern, note_dur, velocity = behavior
            t = global_time
            chord_i = 0
            chord_elapsed = 0.0
            pattern_i = 0
            while t < section_end:
                chord_name = CHORD_ORDER[chord_i % 4]
                tones = CHORD_TONES_MIDI[chord_name]
                note = tones[pattern[pattern_i % len(pattern)]]

                note_start = t
                note_end = min(t + note_dur, section_end)
                events.append((seconds_to_ticks(note_start), 'on', note, velocity))
                events.append((seconds_to_ticks(note_end), 'off', note, 0))

                t += note_dur
                chord_elapsed += note_dur
                pattern_i += 1
                if chord_elapsed >= CHORD_DURATION:
                    chord_elapsed = 0.0
                    chord_i += 1

        global_time = section_end

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

def mix_bass_into_backing_track():
    base_dir = os.path.dirname(__file__)
    audio_dir = os.path.join(base_dir, 'audio')
    midi_path = os.path.join(audio_dir, 'bass_arpeggio.mid')
    bass_wav_path = os.path.join(audio_dir, 'bass_arpeggio_render.wav')
    backing_track_path = os.path.join(audio_dir, 'backing_track_base.wav')

    print("[1/4] Building bass arpeggio MIDI (real acoustic bass instrument)...")
    mid = build_midi()
    mid.save(midi_path)

    print("[2/4] Rendering with fluidsynth + FluidR3_GM soundfont (sampled, non-synthetic)...")
    render_midi_to_wav(midi_path, bass_wav_path)

    print("[3/4] Loading and mixing into backing track...")
    sr_backing, backing = wavfile.read(backing_track_path)
    sr_bass, bass = wavfile.read(bass_wav_path)
    assert sr_backing == sr_bass == SAMPLE_RATE

    # fluidsynth renders stereo; downmix to mono to match backing track
    if bass.ndim == 2:
        bass = bass.mean(axis=1)

    backing_f = backing.astype(np.float64) / 32767.0
    bass_f = bass.astype(np.float64) / 32767.0

    # Pad/trim bass to match backing track length exactly
    if len(bass_f) < len(backing_f):
        bass_f = np.pad(bass_f, (0, len(backing_f) - len(bass_f)))
    else:
        bass_f = bass_f[:len(backing_f)]

    bass_gain = 0.6  # real bass sits under the synth layers, not on top of them
    mixed = backing_f + bass_f * bass_gain

    max_val = np.max(np.abs(mixed))
    if max_val > 1.0:
        mixed = mixed / max_val * 0.97

    mixed_16bit = (mixed * 32767).astype(np.int16)

    print("[4/4] Saving updated backing_track_base.wav...")
    wavfile.write(backing_track_path, SAMPLE_RATE, mixed_16bit)

    print()
    print("✓ Real acoustic bass arpeggio (FluidR3_GM soundfont) mixed into backing_track_base.wav")
    print(f"  MIDI: {midi_path}")
    print(f"  Rendered bass: {bass_wav_path}")

if __name__ == '__main__':
    mix_bass_into_backing_track()
