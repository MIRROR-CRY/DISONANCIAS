#!/usr/bin/env python3
"""
Generate backing track for "Rescue Us" featuring distinct song sections:
- Gen Alpha Melody (F-B-E-A pattern) as the recurring hook motif
- Harmonic accompaniment (Dm-G-C-F progression)
- Spontaneous appearances of Dame Luz melody
- Section-based arrangement (Intro/Verse/Pre-Chorus/Chorus/Bridge/Outro)
  so the track has dynamic contrast instead of one flat loop.
"""

import numpy as np
from scipy.io import wavfile
import os

# Audio parameters
SAMPLE_RATE = 44100
BPM = 100
CHORD_DURATION = 2.0  # seconds per chord; one full Dm-G-C-F loop = 8s

# Section lengths (all multiples of 8s so the chord loop phase stays aligned)
SECTIONS = [
    ('intro',        8),
    ('verse',        16),
    ('pre_chorus',   8),
    ('chorus',       16),
    ('verse',        16),
    ('chorus',       16),
    ('bridge',       16),
    ('chorus_final', 24),
]

# Musical notes (frequencies in Hz)
NOTES = {
    'C': 261.63,   'C#': 277.18,  'D': 293.66,   'D#': 311.13,  'E': 329.63,
    'F': 349.23,   'F#': 369.99,  'G': 392.00,   'G#': 415.30,  'A': 440.00,
    'A#': 466.16,  'B': 493.88,
    # Octave down
    'C2': 130.81,  'D2': 146.83,  'E2': 164.81,  'F2': 174.61,  'G2': 196.00,
    'A2': 220.00,  'B2': 246.94,
    # Octave up
    'C4': 523.25,  'D4': 587.33,  'E4': 659.25,  'F4': 698.46,  'G4': 783.99,
    'A4': 880.00,  'B4': 987.77,
}

def generate_sine_wave(frequency, duration, amplitude=0.3):
    """Generate sine wave at given frequency."""
    samples = np.arange(int(SAMPLE_RATE * duration))
    waveform = amplitude * np.sin(2 * np.pi * frequency * samples / SAMPLE_RATE)
    return waveform

def generate_triangle_wave(frequency, duration, amplitude=0.3):
    """Generate triangle wave for softer synth sound."""
    samples = np.arange(int(SAMPLE_RATE * duration))
    period = SAMPLE_RATE / frequency
    waveform = amplitude * (2 * np.abs(2 * (samples / period - np.floor(samples / period + 0.5))) - 1)
    return waveform

def generate_chord(frequencies, duration, amplitude=0.2):
    """Generate chord from multiple frequencies."""
    waveform = np.zeros(int(SAMPLE_RATE * duration))
    for freq in frequencies:
        waveform += generate_sine_wave(freq, duration, amplitude / len(frequencies))
    return waveform

def apply_adsr_envelope(waveform, attack, decay, sustain_level, release):
    """Apply ADSR envelope to waveform."""
    samples = len(waveform)
    envelope = np.ones(samples)

    attack_samples = int(attack * SAMPLE_RATE)
    decay_samples = int(decay * SAMPLE_RATE)
    release_samples = int(release * SAMPLE_RATE)
    sustain_samples = samples - attack_samples - decay_samples - release_samples

    if sustain_samples < 0:
        sustain_samples = 0

    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

    start = attack_samples
    end = start + decay_samples
    envelope[start:end] = np.linspace(1, sustain_level, decay_samples)

    start = end
    end = start + sustain_samples
    envelope[start:end] = sustain_level

    start = end
    end = start + release_samples
    if release_samples > 0:
        envelope[start:end] = np.linspace(sustain_level, 0, release_samples)

    return waveform * envelope

def mix_audio(*tracks, normalize=True):
    """Mix multiple audio tracks together."""
    max_length = max(len(t) for t in tracks)
    mixed = np.zeros(max_length)

    for track in tracks:
        padded = np.pad(track, (0, max_length - len(track)), mode='constant')
        mixed += padded

    if normalize:
        max_val = np.max(np.abs(mixed))
        if max_val > 0:
            mixed = mixed / max_val * 0.95

    return mixed.astype(np.float32)

# Dm, G, C, F progression (root position)
CHORDS_FREQS = [
    ([NOTES['D2'], NOTES['F2'], NOTES['A2']], 'Dm'),
    ([NOTES['G2'], NOTES['B2'], NOTES['D'], NOTES['G']], 'G'),
    ([NOTES['C2'], NOTES['E2'], NOTES['G2']], 'C'),
    ([NOTES['F2'], NOTES['A2'], NOTES['C']], 'F'),
]
BASS_ROOTS = [NOTES['D2'], NOTES['G2'], NOTES['C2'], NOTES['F2']]

GEN_ALPHA_NOTES = [
    ('F', NOTES['F']),  # 4th degree
    ('B', NOTES['B']),  # 7th degree
    ('E', NOTES['E']),  # 3rd degree
    ('A', NOTES['A']),  # 6th degree
]

DAME_LUZ_PHRASE = [
    ('A', 0.4), ('A', 0.3), ('G', 0.3), ('F', 0.4),
    ('A', 0.3), ('B', 0.3), ('C4', 0.5),
]

def gen_chords(duration, amplitude=0.15):
    """Chord progression Dm-G-C-F, looping to fill duration."""
    out = np.array([])
    t = 0
    while t < duration:
        for freqs, _name in CHORDS_FREQS:
            if t >= duration:
                break
            wave = generate_chord(freqs, CHORD_DURATION, amplitude=amplitude)
            wave = apply_adsr_envelope(wave, 0.2, 0.3, 0.7, 0.2)
            out = np.concatenate([out, wave])
            t += CHORD_DURATION
    return out[:int(SAMPLE_RATE * duration)]

def gen_bass(duration, amplitude=0.2):
    """Bass line on chord roots."""
    out = np.array([])
    t = 0
    while t < duration:
        for freq in BASS_ROOTS:
            if t >= duration:
                break
            wave = generate_sine_wave(freq, CHORD_DURATION, amplitude=amplitude)
            wave = apply_adsr_envelope(wave, 0.1, 0.2, 0.7, 0.1)
            out = np.concatenate([out, wave])
            t += CHORD_DURATION
    return out[:int(SAMPLE_RATE * duration)]

def gen_melody(duration, amplitude=0.25, octave_double=False):
    """Gen Alpha Melody (F-B-E-A), the song's recurring hook motif."""
    out = np.array([])
    note_duration = 0.5
    t = 0
    while t < duration:
        for _name, freq in GEN_ALPHA_NOTES:
            if t >= duration:
                break
            wave = generate_triangle_wave(freq, note_duration, amplitude=amplitude)
            wave = apply_adsr_envelope(wave, 0.05, 0.1, 0.8, 0.05)
            if octave_double:
                wave = wave + generate_triangle_wave(freq * 2, note_duration, amplitude=amplitude * 0.5)
            out = np.concatenate([out, wave])
            t += note_duration
    return out[:int(SAMPLE_RATE * duration)]

def gen_dame_luz_hit(duration, amplitude=0.3):
    """One Dame Luz phrase placed near the start of this section's duration."""
    silence = np.zeros(int(SAMPLE_RATE * duration))
    phrase = np.array([])
    for note_name, note_dur in DAME_LUZ_PHRASE:
        wave = generate_triangle_wave(NOTES[note_name], note_dur, amplitude=amplitude)
        wave = apply_adsr_envelope(wave, 0.05, 0.1, 0.8, 0.05)
        phrase = np.concatenate([phrase, wave])
    start_sample = int(1.0 * SAMPLE_RATE)  # small offset from section start
    end_sample = start_sample + len(phrase)
    if end_sample <= len(silence):
        silence[start_sample:end_sample] += phrase
    return silence

def build_section(kind, duration):
    """
    Build one section's audio according to its role in the song structure:
    - intro:        soft pad only, sets the mood, nothing else
    - verse:        sparse - chords + bass, melody quiet/absent, no Dame Luz
    - pre_chorus:   melody enters at moderate volume, building into the chorus
    - chorus:       full arrangement - loud melody (the hook) + chords + bass + Dame Luz
    - bridge:       breaks the pattern - strips the beat, spotlights Dame Luz melody
    - chorus_final: same melody tone as the other choruses (louder chords/bass
                     only) - cuts straight into the ambulance siren outro
    """
    layers = []

    if kind == 'intro':
        layers.append(gen_chords(duration, amplitude=0.08))

    elif kind == 'verse':
        layers.append(gen_chords(duration, amplitude=0.12))
        layers.append(gen_bass(duration, amplitude=0.15))
        layers.append(gen_melody(duration, amplitude=0.08))  # barely present

    elif kind == 'pre_chorus':
        layers.append(gen_chords(duration, amplitude=0.14))
        layers.append(gen_bass(duration, amplitude=0.18))
        layers.append(gen_melody(duration, amplitude=0.18))  # building

    elif kind == 'chorus':
        layers.append(gen_chords(duration, amplitude=0.16))
        layers.append(gen_bass(duration, amplitude=0.22))
        layers.append(gen_melody(duration, amplitude=0.28))  # the hook, full volume
        layers.append(gen_dame_luz_hit(duration, amplitude=0.3))

    elif kind == 'bridge':
        # break the pattern: no bass, no constant melody loop - just chords + one Dame Luz spotlight
        layers.append(gen_chords(duration, amplitude=0.10))
        layers.append(gen_dame_luz_hit(duration, amplitude=0.35))

    elif kind == 'chorus_final':
        layers.append(gen_chords(duration, amplitude=0.18))
        layers.append(gen_bass(duration, amplitude=0.24))
        layers.append(gen_melody(duration, amplitude=0.28))  # same tone as other choruses
        layers.append(gen_dame_luz_hit(duration, amplitude=0.35))

    return mix_audio(*layers, normalize=False)

def main():
    total_duration = sum(d for _k, d in SECTIONS)

    print("🎵 Generating backing track for \"Rescue Us\"...")
    print(f"   Structure: {' -> '.join(k for k, _d in SECTIONS)}")
    print(f"   Total duration: {total_duration} seconds")
    print(f"   BPM: {BPM}")
    print()

    section_waves = []
    for i, (kind, duration) in enumerate(SECTIONS, 1):
        print(f"   [{i}/{len(SECTIONS)}] {kind} ({duration}s)...")
        section_waves.append(build_section(kind, duration))

    print("   Mixing full track...")
    backing_track = np.concatenate(section_waves)

    # Normalize once across the whole track so section dynamics stay relative
    max_val = np.max(np.abs(backing_track))
    if max_val > 0:
        backing_track = backing_track / max_val * 0.95

    backing_track_16bit = (backing_track * 32767).astype(np.int16)

    output_path = os.path.join(os.path.dirname(__file__), 'audio', 'backing_track_base.wav')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wavfile.write(output_path, SAMPLE_RATE, backing_track_16bit)

    print()
    print(f"✓ Backing track generated successfully!")
    print(f"✓ Saved to: {output_path}")
    print()
    print("📝 Section map:")
    t = 0
    for kind, duration in SECTIONS:
        print(f"   {t:>4.0f}s - {t + duration:>4.0f}s : {kind}")
        t += duration
    print()
    print("🎤 Ready for vocal recording!")

if __name__ == '__main__':
    main()
