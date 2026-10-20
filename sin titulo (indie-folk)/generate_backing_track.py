#!/usr/bin/env python3
"""
Backing track generator for the untitled indie-folk track, v1.

Built from the research in INVESTIGACION_ESTILO.md rather than improvised,
which is the process lesson "Medio Limon" cost twelve versions to learn.

Reference: "Ho Hey" (The Lumineers) - 79 BPM, C major, open chord shapes,
opening progression C - F - C - Am. No modulation, per the decision on record:
the lift at the end is carried by accumulation, not by a key change.

The two structural ideas driving the whole arrangement:

1. SECTIONS ARE TOLD APART BY DENSITY, not only by chords. Verses run bare,
   choruses open, the bridge drops to the lowest point of the arc immediately
   before the highest. That is what makes the final chorus land.

2. THE STOMP-CLAP IS A CROWD, NOT A PART. The published mix of the reference
   has seven tracks of stomps, percussion and claps against one acoustic
   guitar. So each stomp and clap layer here is its own part with its own
   timing offset, its own velocity range and its own place in the stereo
   field, and layers are ADDED as the song grows. Copying one clap track
   louder would only be louder; the dispersion between layers is the effect.

Vocals are absent: the song has no lyrics or shout yet. Their growth is
currently stood in for by the clap and stomp layers.
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

BPM = 79                       # the reference's tempo
BEAT = 60 / BPM
BAR = BEAT * 4

rng = random.Random(5)

PROGRAMS = {
    'guitar':   25,   # steel acoustic - the core of the song
    'picking':  25,   # second acoustic, higher, arpeggios in the fuller parts
    'cello':    42,
    'bass':     32,   # acoustic bass
}

STOMP, CLAP, TAMB = 35, 39, 54

# Open-position chords in C major, voiced so they keep ringing strings.
CHORDS = {
    'C':  {'gtr': [48, 52, 55, 60, 64], 'hi': [64, 67, 72], 'bass': 36},
    'F':  {'gtr': [41, 45, 48, 53, 57], 'hi': [65, 69, 72], 'bass': 41},
    'Am': {'gtr': [45, 52, 57, 60, 64], 'hi': [64, 69, 72], 'bass': 45},
    'G':  {'gtr': [43, 47, 50, 55, 59], 'hi': [62, 67, 71], 'bass': 43},
    'Em': {'gtr': [40, 47, 52, 55, 59], 'hi': [64, 67, 71], 'bass': 40},
}

# (kind, bars, chord cycle)
SECTIONS = [
    ('intro',        4, ['C', 'F', 'C', 'Am']),
    ('verse',        8, ['C', 'F', 'C', 'Am']),
    ('pre_chorus',   4, ['F', 'F', 'G', 'G']),
    ('chorus',       8, ['Am', 'G', 'C', 'F']),
    ('verse',        8, ['C', 'F', 'C', 'Am']),
    ('pre_chorus',   4, ['F', 'F', 'G', 'G']),
    ('chorus',       8, ['Am', 'G', 'C', 'F']),
    ('bridge',       4, ['F', 'G', 'Am', 'G']),
    ('chorus_final', 8, ['Am', 'G', 'C', 'F']),
    ('outro',        4, ['C', 'F', 'C', 'Am']),
]

# The crescendo, written as a table. Each section says how many stomp layers
# and how many clap layers are playing, and which instruments are in.
DENSITY = {
    #                stomps claps cello bass picking guitar_vel
    'intro':        (0,     0,    False, False, False, 66),
    'verse':        (1,     0,    False, False, False, 76),
    'pre_chorus':   (1,     0,    False, False, False, 78),
    'chorus':       (2,     1,    True,  True,  False, 92),
    'bridge':       (0,     2,    True,  False, False, 68),   # lowest point
    'chorus_final': (3,     4,    True,  True,  True,  106),  # highest
    'outro':        (3,     4,    True,  True,  True,  100),
}

# Second time through, verses and choruses carry a little more than the first.
GROWTH = {'verse': (1, 1), 'pre_chorus': (0, 1), 'chorus': (0, 1)}

N_STOMPS, N_CLAPS = 3, 4

# Right-hand patterns, one per bar, cycled and occasionally swapped. Each entry
# is (position in beats, direction, how much of the chord the stroke catches,
# velocity scale). The variants differ in which strokes exist at all - one
# skips a downstroke and lets the chord ring, another doubles an upstroke,
# another plays sparse and open.
STRUM_PATTERNS = [
    [(0.0, 'D', 1.0, 1.00), (0.5, 'U', 0.6, 0.72), (1.0, 'D', 0.85, 0.86),
     (1.5, 'U', 0.55, 0.68), (2.0, 'D', 1.0, 0.96), (2.5, 'U', 0.6, 0.72),
     (3.0, 'D', 0.85, 0.86), (3.5, 'U', 0.55, 0.70)],

    [(0.0, 'D', 1.0, 1.00), (0.5, 'U', 0.6, 0.70), (1.5, 'U', 0.5, 0.64),
     (2.0, 'D', 1.0, 0.94), (2.5, 'U', 0.6, 0.72), (3.0, 'D', 0.8, 0.84),
     (3.5, 'U', 0.55, 0.68)],

    [(0.0, 'D', 1.0, 1.00), (0.75, 'U', 0.5, 0.66), (1.0, 'D', 0.8, 0.84),
     (1.5, 'U', 0.6, 0.72), (2.0, 'D', 1.0, 0.95), (2.5, 'U', 0.55, 0.70),
     (3.0, 'D', 0.85, 0.88), (3.25, 'U', 0.4, 0.60), (3.5, 'U', 0.55, 0.70)],

    [(0.0, 'D', 1.0, 1.00), (1.0, 'D', 0.7, 0.80), (1.5, 'U', 0.6, 0.70),
     (2.0, 'D', 1.0, 0.95), (3.0, 'D', 0.8, 0.85), (3.5, 'U', 0.6, 0.72)],
]

# Each crowd layer has its own feel and its own place in the stereo field, so
# the layers read as different people rather than as one part turned up.
LAYER_PAN = [0.0, -0.45, 0.42, -0.28, 0.33, -0.5, 0.48]

# Hands and feet get separate, much tighter feel offsets than the first
# version had. A crowd clapping on a record sits inside about 15ms; past
# roughly 30ms the ear stops hearing thickness and starts hearing somebody
# clapping late. The first pass spread the layers over 60ms of fixed offset
# and then added 27ms of random on top, which put the worst pair 123ms
# apart - an audible mistake, not a crowd.
STOMP_FEEL = [-0.005, +0.007, -0.009]
CLAP_FEEL = [+0.005, -0.007, +0.010, -0.003]


def humanize(t, vel, feel, spread=0.010, vel_spread=3.5):
    return (max(0.0, t + feel + rng.gauss(0, spread)),
            int(np.clip(vel + rng.gauss(0, vel_spread), 1, 127)))


def ticks(seconds):
    return max(0, int(round(seconds * BPM / 60 * TICKS_PER_BEAT)))


class Part:
    def __init__(self, name, program=None, is_drums=False, feel=0.0, spread=0.008,
                 vel_spread=3.5):
        self.name, self.program, self.is_drums = name, program, is_drums
        self.feel, self.spread, self.events = feel, spread, []
        self.vel_spread = vel_spread

    def note(self, t, note, dur, vel):
        t, vel = humanize(t, vel, self.feel, self.spread, self.vel_spread)
        self.events.append((ticks(t), 'on', note, vel))
        self.events.append((ticks(t + max(0.04, dur)), 'off', note, 0))

    def strum(self, t, notes, dur, vel, direction='D', reach=1.0):
        """One stroke of a real right hand.

        A player does not repeat a gesture exactly. Three things vary per
        stroke and none of them are timing jitter:

        - how many strings the stroke actually catches (reach)
        - how fast the hand sweeps across them - a hard stroke sweeps in
          about 8ms, a gentle one takes closer to 20
        - how long each note is left to ring

        Small random offsets on a fixed gesture only smear it. Varying the
        gesture is what stops sixty bars from sounding like one bar repeated.
        """
        order = notes if direction == 'D' else list(reversed(notes))
        n = max(3, min(len(order), int(round(len(order) * reach))))
        picked = order[:n]
        sweep = (0.021 - 0.011 * min(1.0, vel / 110)) * rng.uniform(0.88, 1.14)
        for i, note in enumerate(picked):
            self.note(t + i * sweep, note,
                      dur * rng.uniform(0.92, 1.08),
                      vel - i * rng.randint(1, 3))

    def clap(self, t, note, dur, vel):
        """One person clapping, which is not the same as one drum hit.

        Three things a crowd does that a programmed clap track does not:
        a few people are late or miss the beat entirely, the two hands of
        one person do not land together (a flam of 20-40ms), and nobody
        hits twice with the same force. Kept small on purpose: past this
        the crowd stops sounding like a crowd and starts sounding sloppy.
        """
        if rng.random() < 0.03:          # somebody missed this one
            return
        self.note(t, note, dur, vel)
        if rng.random() < 0.05:          # the other hand, a hair behind
            self.note(t + rng.uniform(0.012, 0.022), note, dur * 0.8,
                      vel - rng.randint(18, 28))

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
    parts = {n: Part(n, PROGRAMS[n], feel=f)
             for n, f in (('guitar', 0.004), ('picking', 0.010),
                          ('cello', 0.014), ('bass', -0.008))}
    for i in range(N_STOMPS):
        parts[f'stomp{i+1}'] = Part(f'stomp{i+1}', is_drums=True,
                                    feel=STOMP_FEEL[i], spread=0.007,
                                    vel_spread=6.0)
    for i in range(N_CLAPS):
        parts[f'clap{i+1}'] = Part(f'clap{i+1}', is_drums=True,
                                   feel=CLAP_FEEL[i], spread=0.008,
                                   vel_spread=8.0)

    seen = {}
    t = 0.0
    for kind, bars, cycle in SECTIONS:
        pass_no = seen.get(kind, 0)
        seen[kind] = pass_no + 1
        n_stomp, n_clap, cello_on, bass_on, picking_on, gtr_vel = DENSITY[kind]
        if pass_no and kind in GROWTH:
            n_stomp = min(N_STOMPS, n_stomp + GROWTH[kind][0])
            n_clap = min(N_CLAPS, n_clap + GROWTH[kind][1])

        for b in range(bars):
            bar_t = t + b * BAR
            ch = CHORDS[cycle[b % len(cycle)]]
            last_bar = (b == bars - 1)

            # Acoustic guitar. The pattern itself changes bar to bar: the bare
            # sections get the sparser variants, the full ones the busier, and
            # the choice is nudged at random so it never settles into a loop.
            if gtr_vel < 80:
                choices = (3, 1, 3, 0)
            elif gtr_vel < 95:
                choices = (0, 1, 3, 2)
            else:
                choices = (0, 2, 0, 1)
            idx = choices[b % 4]
            if rng.random() < 0.10:
                idx = rng.choice(choices)
            for pos, direction, reach, vscale in STRUM_PATTERNS[idx]:
                notes = ch['gtr'] if direction == 'D' else ch['gtr'][1:]
                parts['guitar'].strum(bar_t + pos * BEAT, notes,
                                      BEAT * (0.9 if direction == 'D' else 0.4),
                                      int(gtr_vel * vscale), direction, reach)

            if picking_on:
                # Also varied rather than repeated: which notes get picked and
                # where they fall changes bar to bar.
                figures = [
                    ((0.5, 0), (1.5, 1), (2.5, 2), (3.5, 1)),
                    ((0.5, 2), (1.0, 1), (2.5, 0), (3.5, 2)),
                    ((0.5, 1), (1.5, 2), (2.0, 0), (3.5, 1), (3.75, 2)),
                    ((0.5, 0), (2.5, 2), (3.5, 1)),
                ]
                figure = figures[b % len(figures)]
                for pos, idx in figure:
                    parts['picking'].note(bar_t + pos * BEAT, ch['hi'][idx],
                                          BEAT * rng.uniform(0.45, 0.58),
                                          rng.randint(60, 68))

            if cello_on:
                parts['cello'].note(bar_t, ch['bass'] + 12, BAR * 0.92, 66)

            if bass_on:
                parts['bass'].note(bar_t, ch['bass'], BEAT * 1.6, 92)
                parts['bass'].note(bar_t + 2 * BEAT, ch['bass'], BEAT * 1.4, 84)

            # The crowd. Stomps on 1 and 3, claps on 2 and 4, one part per
            # layer so each keeps its own timing, velocity and position.
            for i in range(n_stomp):
                p = parts[f'stomp{i+1}']
                drift = rng.gauss(0, 0.003)
                for beat in (0, 2):
                    p.note(bar_t + beat * BEAT + drift, STOMP, 0.18, 100 - i * 4)
            for i in range(n_clap):
                p = parts[f'clap{i+1}']
                # Each layer drifts a little from bar to bar instead of sitting
                # on one fixed offset for three minutes.
                drift = rng.gauss(0, 0.003)
                for beat in (1, 3):
                    p.clap(bar_t + beat * BEAT + drift, CLAP, 0.14, 96 - i * 5)
                # In the fullest sections the crowd starts filling the offbeats
                if kind in ('chorus_final', 'outro') and i >= 2:
                    p.clap(bar_t + 3.5 * BEAT + drift, CLAP, 0.12, 74)

            # A tambourine rides the top of the biggest sections
            if kind in ('chorus_final', 'outro'):
                for i in range(8):
                    parts['clap1'].note(bar_t + i * 0.5 * BEAT, TAMB, BEAT * 0.4, 58)

            if last_bar and kind in ('pre_chorus', 'bridge'):
                for i, pos in enumerate((3.0, 3.5)):
                    parts['stomp1'].note(bar_t + pos * BEAT, STOMP, 0.16, 96 + i * 6)

        t += bars * BAR
    return parts, t


MIX = {
    # name:      (highpass, presence_f, presence_g, pan, thresh, ratio, makeup, echo, volume)
    'guitar':    (90,  3000, 3.0, -0.12, 0.14, 2.6, 2.2, '0.9:0.2:45|80:0.2|0.12',   2.60),
    'picking':   (200, 3600, 3.0,  0.30, 0.15, 2.5, 1.9, '0.9:0.26:60|105:0.26|0.16', 6.00),
    'cello':     (70,   800, 1.5,  0.14, 0.15, 2.5, 1.9, '0.9:0.26:80|130:0.26|0.16', 2.00),
    'bass':      (35,   700, 1.0,  0.00, 0.11, 3.5, 2.2, None,                        0.90),
}
# Every crowd layer shares one room, which is what ties them together.
CROWD_ECHO = '0.9:0.24:38|66|104:0.26|0.18|0.12'


def crowd_mix(name, i):
    if name.startswith('stomp'):
        return (45, 2500, 2.0, LAYER_PAN[i] * 0.5, 0.15, 2.8, 2.6, CROWD_ECHO, 6.00)
    return (250, 4200, 3.5, LAYER_PAN[i], 0.15, 2.6, 2.4, CROWD_ECHO, 4.60)


def render_stem(midi_path, wav_path):
    subprocess.run(['fluidsynth', '-ni', SOUNDFONT, midi_path, '-F', wav_path,
                    '-r', str(SAMPLE_RATE)], check=True, capture_output=True)


def process_stem(src, dst, params):
    hp, pf, pg, pan, thr, ratio, makeup, echo, vol = params
    chain = [f'highpass=f={hp}',
             f'equalizer=f={pf}:width_type=q:width=1.2:g={pg}',
             f'acompressor=threshold={thr}:ratio={ratio}:attack=10:release=160:makeup={makeup}']
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
    # loudnorm and the limiter run BEFORE the fade on purpose: both are
    # level-dependent, and with the fade first they claw the decaying tail
    # back up, which is what made the ending read as accelerated rather than
    # even. curve=tri is a straight line in amplitude, so the drop per second
    # is constant from the first bar of the outro to silence.
    chain = (f'amix=inputs={len(stems)}:duration=longest:normalize=0,'
             'acompressor=threshold=0.28:ratio=2:attack=30:release=260:makeup=1.5,'
             'equalizer=f=300:width_type=q:width=1.1:g=-1.5,'
             'equalizer=f=3500:width_type=q:width=1.3:g=1.5,'
             'alimiter=limit=0.95,loudnorm=I=-14:TP=-1.0:LRA=11,'
             f'afade=t=out:curve=tri:st={total - fade}:d={fade},'
             f'atrim=end={total + 0.5},asetpts=N/SR/TB')
    subprocess.run(['ffmpeg', '-y'] + inputs + ['-filter_complex', chain,
                    '-ar', str(SAMPLE_RATE), out_path], check=True, capture_output=True)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    audio = os.path.join(base, 'audio')
    stems_dir = os.path.join(audio, 'stems')
    os.makedirs(stems_dir, exist_ok=True)

    print('Indie-folk backing track, v1')
    print(f'  {BPM} BPM, C major, {sum(b for _k, b, _c in SECTIONS)} bars, no modulation')
    print(f'  Crowd: {N_STOMPS} stomp layers + {N_CLAPS} clap layers, added as the song grows')
    print()

    parts, total = build_arrangement()

    print('Rendering stems...')
    processed = []
    crowd_i = 0
    for name, part in parts.items():
        mid = os.path.join(stems_dir, f'{name}.mid')
        raw = os.path.join(stems_dir, f'{name}_raw.wav')
        proc = os.path.join(stems_dir, f'{name}.wav')
        part.save(mid)
        render_stem(mid, raw)
        if name in MIX:
            params = MIX[name]
        else:
            params = crowd_mix(name, crowd_i)
            crowd_i += 1
        process_stem(raw, proc, params)
        os.remove(raw)
        processed.append(proc)
        print(f'  - {name}')

    out = os.path.join(audio, 'backing_track_base.wav')
    mix_and_master(processed, out, total, SECTIONS[-1][1] * BAR)
    print(f'\n  Output: {out}\n  Duration: {total:.1f}s')


if __name__ == '__main__':
    main()
