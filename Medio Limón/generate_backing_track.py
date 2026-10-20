#!/usr/bin/env python3
"""
Backing track generator for "Medio Limón" - tropipop, v7.

Target sound, defined with the user rather than guessed at: Carlos Vives'
"Volvi a Nacer" (F major, 97 BPM, tropipop - vallenato crossed with modern
pop, produced by Vives and Andres Castro). Clean modern production, the
voice out front with little behind it, warm and celebratory rather than
euphoric.

This is the fifth attempt and the previous four missed for reasons worth
recording, since each one narrowed the target:

  v1/v2  traditional accordion vallenato, quantized MIDI, no mix
  v3     nueva cumbia chilena (Chico Trujillo) - right that it was Chilean
         cumbia, wrong branch
  v4     classic cumbia sonora (Sonora Palacios) - well executed, kept as a
         separate song idea in musica/ideas/, but not this song

The tempo argument that ran through all of them was never about BPM. v3 ran
at 102 with the kick on 1 and 3, so the felt pulse was 51 per minute and it
read as slow. The reference sits at an even slower 97 but feels lively
because its kick marks densely: every beat carries a hit, so the felt pulse
is ~97. That is what this version does.

Arrangement principle: the vocal leads, so the verses stay sparse and the
accordion answers between vocal phrases instead of playing throughout.
"""

import os
import subprocess
import random
import numpy as np
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
SAMPLE_RATE = 44100
TICKS_PER_BEAT = 480

# Vallenato as a whole is written in 2/4, but the paseo - the aire these
# references are in - is the exception and squares in four beats. An earlier
# version applied the 2/4 rule to it and everything ran at double speed.
#
# The quarter note is the pulse the user counted by hand on the reference:
# 22 pulses in 12.49 seconds.
BPM = 105.5
BEAT = 60 / BPM
BAR = BEAT * 4
SWING = 0.04                   # lighter than cumbia: pop feel, closer to straight

rng = random.Random(11)

PROGRAMS = {
    'acoustic':  25,  # steel acoustic guitar - carries the song
    'apagado':   28,  # muted electric: the percussive damped strum of the paseo
    'electric':  27,  # clean electric, light accents only
    'accordion': 21,  # the Vives signature, used as color between phrases
    'organ':     16,  # drawbar organ - the records use a Hammond B3, not a piano
    'cello':     42,  # the reference album has cello; warm sustained low color
    'bass':      33,
}

# GM drum map
KICK, SNARE, SIDESTICK, CLAP = 36, 38, 37, 39
GUACHARACA, SHAKER = 73, 70
CAJA_LO, CAJA_HI, CONGA_HI = 64, 63, 62

# --- Harmony, taken from the references rather than invented ---------------
# "Volvi a Nacer" is in F and its intro runs F - Bb - Dm - C, with a borrowed
# Bbm appearing later. "Cuando nos volvamos a encontrar" (written here
# transposed from C to F) opens F - C - Dm - Bb - Bbm, its verse turns on a
# secondary dominant into the relative minor, and its chorus runs ii-V chains
# into keys other than the tonic.
#
# Two devices are common to both and were missing from every earlier version:
# the borrowed minor iv (Bbm) and secondary dominants (A7 into Dm, C7 into Bb).
# A plain I-V-vi-IV loop has neither, which is why it did not sound like them.
CHORDS = {
    'F':   {'gtr': [65, 69, 72], 'keys': [53, 57, 60], 'bass': 41},
    'C':   {'gtr': [64, 67, 72], 'keys': [48, 52, 55], 'bass': 36},
    'C7':  {'gtr': [64, 67, 70], 'keys': [48, 52, 55, 58], 'bass': 36},
    'Dm':  {'gtr': [62, 65, 69], 'keys': [50, 53, 57], 'bass': 38},
    'Gm':  {'gtr': [62, 67, 70], 'keys': [43, 46, 50], 'bass': 43},
    'Bb':  {'gtr': [65, 70, 74], 'keys': [46, 50, 53], 'bass': 34},
    'Bbm': {'gtr': [65, 70, 73], 'keys': [46, 49, 53], 'bass': 34},   # borrowed iv
    'A7':  {'gtr': [64, 69, 73], 'keys': [45, 49, 52, 55], 'bass': 45},  # V of Dm
}

INTRO   = ['F', 'Bb', 'Dm', 'C']                              # Volvi a Nacer, literal
VERSE   = ['F', 'C', 'Dm', 'A7', 'Bb', 'F', 'Gm', 'C']        # secondary dominant on bar 4
PRE     = ['Gm', 'C', 'Gm', 'C7']                             # ii-V chain
CHORUS  = ['F', 'Dm', 'Bb', 'Bbm', 'F', 'C', 'Bb', 'C']       # borrowed minor iv cadence

SECTIONS = [
    ('intro',      4,  INTRO),
    ('verse',      8,  VERSE),
    ('pre_chorus', 4,  PRE),
    ('chorus',     8,  CHORUS),
    ('chorus',     8,  CHORUS),
    ('verse',      16, VERSE),
    ('pre_chorus', 4,  PRE),
    ('chorus',     8,  CHORUS),
    ('outro',      8,  CHORUS),
    ('outro',      8,  CHORUS),
]

FEEL = {
    'acoustic':  +0.004,
    'apagado':   +0.003,
    'electric':  +0.008,
    'accordion': +0.012,
    'organ':     +0.006,
    'cello':     +0.010,
    'bass':      -0.009,
    'drums':      0.0,
}

# The accordion figures are built from whatever chord is sounding rather than
# being a fixed melody, so they stay consonant over the borrowed Bbm and the
# A7 instead of clashing with them. Each entry is (beat, index into the chord
# tones, duration in beats).
ACCORDION_FIGURES = [
    [(0.0, 2, 1.0), (1.5, 1, 0.5), (2.0, 2, 1.0), (3.0, 0, 1.0)],
    [(0.0, 1, 1.0), (1.0, 2, 1.0), (2.5, 1, 0.5), (3.0, 0, 1.5)],
]

# Short answer in the gap at the end of a vocal phrase.
ACCORDION_ANSWER = [(2.5, 2, 0.5), (3.0, 1, 0.5), (3.5, 0, 1.0)]


def swing_offset(pos):
    return SWING * BEAT if abs((pos % 1.0) - 0.5) < 0.01 else 0.0


def humanize(t, vel, role):
    return max(0.0, t + FEEL[role] + rng.gauss(0, 0.006)), int(np.clip(vel + rng.gauss(0, 4), 1, 127))


def ticks(seconds):
    return max(0, int(round(seconds * BPM / 60 * TICKS_PER_BEAT)))


class Part:
    def __init__(self, name, program=None, is_drums=False):
        self.name, self.program, self.is_drums, self.events = name, program, is_drums, []

    def note(self, t, note, dur, vel):
        role = 'drums' if self.is_drums else self.name
        t, vel = humanize(t, vel, role)
        self.events.append((ticks(t), 'on', note, vel))
        self.events.append((ticks(t + max(0.04, dur)), 'off', note, 0))

    def chord(self, t, notes, dur, vel, spread=0.006):
        for i, n in enumerate(notes):
            self.note(t + i * spread, n, dur, vel - i * 2)

    def save(self, path):
        mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM), time=0))
        ch = 9 if self.is_drums else 0
        if self.program is not None:
            track.append(Message('program_change', program=self.program, channel=ch, time=0))
        self.events.sort(key=lambda e: e[0])
        last = 0
        for tick, kind, note, vel in self.events:
            track.append(Message('note_on' if kind == 'on' else 'note_off',
                                 note=note, velocity=vel, channel=ch, time=max(0, tick - last)))
            last = max(last, tick)
        mid.save(path)


def build_arrangement():
    parts = {n: Part(n, PROGRAMS[n]) for n in PROGRAMS}
    parts['drums'] = Part('drums', is_drums=True)

    t = 0.0
    phrase = 0
    for kind, bars, cycle in SECTIONS:
        full = kind in ('chorus', 'outro')
        sparse = kind == 'verse'
        for b in range(bars):
            bar_t = t + b * BAR
            ch = CHORDS[cycle[b % len(cycle)]]
            pb = b % len(cycle)

            d = parts['drums']
            # Kick marks every beat, accented on 1 and 3, so the felt pulse is
            # the 105 per minute the user counted on the reference. Leaving it
            # on 1 and 3 only would halve that to 52, which is what made the
            # earliest versions drag.
            for beat in range(4):
                d.note(bar_t + beat * BEAT, KICK, 0.14, 104 if beat % 2 == 0 else 80)
            # Backbeat on 2 and 4
            for beat in (1, 3):
                d.note(bar_t + beat * BEAT, CLAP if full else SIDESTICK,
                       0.10, 92 if full else 78)
            # Guacharaca in sixteenths: about seven strokes a second, which is
            # the real density of the instrument in this style. In eighths it
            # was half that and the groove had no forward motion.
            for i in range(16):
                pos = i * 0.25
                d.note(bar_t + pos * BEAT, GUACHARACA, BEAT * 0.2,
                       78 if i % 4 == 0 else (62 if i % 2 == 0 else 46))
            # Caja vallenata: bass tone on 1, slap on 2, syncopated double slap
            # before 3
            d.note(bar_t, CAJA_LO, 0.12, 90)
            d.note(bar_t + 1 * BEAT, CAJA_HI, 0.10, 84)
            for pos in (1.5, 1.75):
                d.note(bar_t + pos * BEAT, CAJA_HI, 0.08, 66)
            d.note(bar_t + 2 * BEAT, CAJA_LO, 0.12, 82)
            if full:
                d.note(bar_t + 3.5 * BEAT + swing_offset(3.5), CONGA_HI, 0.10, 74)
                for i in range(8):
                    d.note(bar_t + i * 0.5 * BEAT, SHAKER, BEAT * 0.25, 56)

            # Bass: rooted and simple, with an octave lift into the next bar
            # Vallenato bass: a main bass and a secondary bass, the upper octave
            # of the tonic for rhythmic character, and the syncopation that the
            # style is built on - the next chord's root anticipated on the "and"
            # of 4 and tied across the barline. That anticipation is what pulls
            # the music forward; flat roots on 1 and 3 do not.
            root = ch['bass']
            nxt = CHORDS[cycle[(b + 1) % len(cycle)]]['bass']
            anticipates = (b % 2 == 1)
            preceded = (b % 2 == 0 and b > 0)

            # Main bass, softer when the previous bar already anticipated it
            parts['bass'].note(bar_t, root, BEAT * (0.7 if preceded else 1.1),
                               84 if preceded else 102)
            # Upper octave of the tonic
            parts['bass'].note(bar_t + 1.5 * BEAT + swing_offset(1.5), root + 12,
                               BEAT * 0.4, 80)
            # Secondary bass on the fifth
            parts['bass'].note(bar_t + 2 * BEAT, root + 7, BEAT * 0.9, 94)
            if anticipates:
                parts['bass'].note(bar_t + 3.5 * BEAT + swing_offset(3.5), nxt,
                                   BEAT * 1.0, 96)

            # Paseo strum: thumb bass on the beat, an immediate upstroke after
            # it, and a damped percussive hit where the notation would show a
            # rest. That damped hit is what gives the style its drive - without
            # it the guitar is just sustained chords and the track drags at any
            # tempo.
            #
            #   1      &        2        &       3      &        4        &
            #   bass   upstroke apagado  upstroke bass  upstroke apagado  upstroke
            gtr = ch['gtr']
            low = gtr[0] - 12
            fifth = low + 7
            for beat, kind_hit in ((0, 'bass'), (1, 'mute'), (2, 'bass'), (3, 'mute')):
                bt = bar_t + beat * BEAT
                if kind_hit == 'bass':
                    parts['acoustic'].note(bt, low if beat == 0 else fifth,
                                           BEAT * 0.45, 98 if full else 90)
                else:
                    parts['apagado'].chord(bt, gtr, BEAT * 0.12,
                                           86 if full else 76, spread=0.003)
                up = bt + BEAT * 0.5 + swing_offset(0.5)
                parts['acoustic'].chord(up, gtr, BEAT * 0.28, 84 if full else 74)

            # Piano: quiet bed, only where the arrangement can carry it
            # Hammond-style organ pad, and cello doubling the root an octave up
            if not sparse:
                parts['organ'].chord(bar_t, ch['keys'], BAR * 0.9, 58)
            if full:
                parts['cello'].note(bar_t, ch['bass'] + 12, BAR * 0.92, 70)

            # Clean electric: single accents on the backbeat, chorus only
            if full:
                parts['electric'].chord(bar_t + 1 * BEAT, ch['gtr'], BEAT * 0.5, 70)
                parts['electric'].chord(bar_t + 3 * BEAT, ch['gtr'], BEAT * 0.5, 66)

            # Accordion: the hook in intro/chorus/outro, short answers between
            # vocal lines in the verses, silent everywhere else.
            # Accordion: figures over the chord in the fuller sections, a short
            # answer in the phrase gap during verses, a rising line into the
            # chorus. It never plays underneath the vocal line itself.
            tones = ch['gtr']
            if kind in ('intro', 'chorus', 'outro'):
                figure = ACCORDION_FIGURES[(b // 2) % len(ACCORDION_FIGURES)]
                for pos, idx, dur in figure:
                    parts['accordion'].note(bar_t + pos * BEAT + swing_offset(pos),
                                            tones[idx], dur * BEAT * 0.9, 88)
            elif sparse and pb % 4 == 3:
                for pos, idx, dur in ACCORDION_ANSWER:
                    parts['accordion'].note(bar_t + pos * BEAT + swing_offset(pos),
                                            tones[idx], dur * BEAT * 0.85, 80)
            elif kind == 'pre_chorus' and b >= 2:
                parts['accordion'].note(bar_t + 2 * BEAT, tones[1], BEAT * 1.6, 80 + b * 4)

        t += bars * BAR
    return parts, t


# Per-stem chain. Brighter and cleaner than the cumbia versions, with the
# acoustic guitar forward and everything leaving room in the midrange for a
# vocal to sit on top later.
# Levels set from measured stem loudness. The brief is acoustic guitar as the
# backbone with the vocal going on top later, so the guitar and drums lead, the
# bass supports instead of dominating, and the midrange stays uncluttered.
MIX = {
    # name:       (highpass, presence_f, presence_g, pan, thresh, ratio, makeup, echo, volume)
    'bass':       (35,   800,  1.5,  0.00, 0.11, 3.5, 2.2, None,                             0.45),
    'drums':      (55,  5000,  2.5,  0.00, 0.15, 2.8, 2.4, '0.9:0.14:28|48:0.14|0.09',       5.50),
    'acoustic':   (90,  3200,  3.5, -0.16, 0.14, 2.8, 2.2, '0.9:0.2:45|80:0.22|0.14',        3.40),
    'apagado':    (200, 3000,  4.0, -0.20, 0.13, 3.2, 2.0, '0.9:0.18:40|70:0.18|0.11',       6.50),
    'electric':   (170, 2800,  3.0,  0.26, 0.14, 3.0, 1.9, '0.9:0.26:60|105:0.26|0.17',      1.50),
    'accordion':  (180, 2400,  3.0,  0.17, 0.14, 3.0, 2.0, '0.9:0.24:65|110|160:0.26|0.18|0.12', 2.70),
    'organ':      (140, 1800,  1.5, -0.22, 0.16, 2.5, 1.8, '0.9:0.22:70|120:0.24|0.15',      5.60),
    'cello':      (80,   900,  1.5,  0.12, 0.15, 2.5, 1.9, '0.9:0.24:80|130:0.26|0.16',      2.40),
}


def render_stem(midi_path, wav_path):
    subprocess.run(['fluidsynth', '-ni', SOUNDFONT, midi_path, '-F', wav_path,
                    '-r', str(SAMPLE_RATE)], check=True, capture_output=True)


def process_stem(src, dst, name):
    hp, pf, pg, pan, thr, ratio, makeup, echo, vol = MIX[name]
    chain = [f'highpass=f={hp}',
             f'equalizer=f={pf}:width_type=q:width=1.2:g={pg}',
             f'acompressor=threshold={thr}:ratio={ratio}:attack=8:release=140:makeup={makeup}']
    if echo:
        chain.append(f'aecho={echo}')
    if abs(pan) > 0.01:
        chain.append(f'stereotools=balance_out={pan}')
    chain.append(f'volume={vol}')
    subprocess.run(['ffmpeg', '-y', '-i', src, '-af', ','.join(chain), dst],
                   check=True, capture_output=True)


def mix_and_master(stems, out_path, total, fade):
    inputs = []
    for s in stems:
        inputs += ['-i', s]
    chain = (f'amix=inputs={len(stems)}:duration=longest:normalize=0,'
             'acompressor=threshold=0.28:ratio=2:attack=30:release=260:makeup=1.5,'
             'equalizer=f=300:width_type=q:width=1.1:g=-1.5,'
             'equalizer=f=3500:width_type=q:width=1.3:g=1.5,'
             f'afade=t=out:st={total - fade}:d={fade},'
             'alimiter=limit=0.95,loudnorm=I=-14:TP=-1.0:LRA=11')
    subprocess.run(['ffmpeg', '-y'] + inputs + ['-filter_complex', chain,
                    '-ar', str(SAMPLE_RATE), out_path], check=True, capture_output=True)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    audio = os.path.join(base, 'audio')
    stems_dir = os.path.join(audio, 'stems')
    os.makedirs(stems_dir, exist_ok=True)

    total_bars = sum(b for _k, b, _c in SECTIONS)
    print('Generating "Medio Limón" backing track (v5, tropipop)')
    print(f'  {BPM} BPM, F major, {total_bars} bars')
    print('  Reference: Carlos Vives "Volvi a Nacer" - clean modern production, vocal forward')
    print()

    print('[1/4] Writing arrangement (acoustic guitar forward, accordion as color)...')
    parts, total = build_arrangement()

    print('[2/4] Rendering stems...')
    processed = []
    for name, part in parts.items():
        mid = os.path.join(stems_dir, f'{name}.mid')
        raw = os.path.join(stems_dir, f'{name}_raw.wav')
        proc = os.path.join(stems_dir, f'{name}.wav')
        part.save(mid)
        render_stem(mid, raw)
        print(f'      - {name}')
        process_stem(raw, proc, name)
        os.remove(raw)
        processed.append(proc)

    print('[3/4] Mixing...')
    out = os.path.join(audio, 'backing_track_base.wav')
    mix_and_master(processed, out, total, SECTIONS[-1][1] * BAR)

    print('[4/4] Done.')
    print(f'\n  Output: {out}\n  Duration: {total:.1f}s')


if __name__ == '__main__':
    main()
