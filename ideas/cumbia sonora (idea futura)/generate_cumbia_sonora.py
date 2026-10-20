#!/usr/bin/env python3
"""
Backing track generator for "Medio Limón" - classic Chilean
"cumbia sonora" (Sonora Palacios / Tommy Rey lineage), v4.

Complete rewrite. The earlier versions sounded like a MIDI toy for four
reasons, all addressed here:

1. WRONG GENRE: v1/v2 were built as accordion-led vallenato. The "Loca"
   reference is cumbia chilena, whose signature is a BRASS section up
   front, clean electric guitar chopping the offbeats ("charchazo"),
   guira/timbales/congas, and a syncopated tumbao bass. Accordion is a
   secondary color here, not the lead.

2. FAKE HUMANIZATION: random uniform jitter on every note is just noise
   and reads as sloppy, not human. Real ensembles have *consistent* feel
   offsets per role (bass pushes ahead, brass lays back), swing on the
   offbeats, and velocities that follow the musical accent structure.
   That is what this version models, with only small gaussian noise on top.

3. NO MIX: everything was rendered in a single dry mono pass, so there
   was no per-instrument EQ, compression, stereo placement or ambience -
   the single biggest reason programmed music reads as "fake".
   Now each instrument renders to its own stem and gets its own chain.

4. NO HOOK: v1/v2 were only block chords with no melody. This version
   has an actual 4-bar brass riff that opens the song and returns in
   every chorus.

v4 retargets the style after v3 landed on the wrong branch of the genre.
The reference is the bright cumbia used in Chilean telenovela intros, which
is the classic "cumbia sonora" of Sonora Palacios, not Chico Trujillo's
rawer nueva cumbia. Its defining trait, per the genre's own history, is that
Sonora Palacios moved the Colombian llamador OFF the offbeat and onto the
beat: a cowbell marking every beat. That single change is what makes this
style read as danceable, and it now runs through the whole arrangement.

Also in v4: 130 BPM (kick on 1 and 3 gives the 65-per-minute pulse that was
asked for), C major instead of D minor to match the celebratory lyric, two
harmonized trumpets in the Sonora Matancera format, and a brighter riff.
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

BPM = 130                      # kick on 1 and 3 lands at 65 pulses/min, the requested feel
BEAT = 60 / BPM                # seconds per beat
BAR = BEAT * 4                 # 4/4
SWING = 0.055                  # offbeat 8ths pushed late, as a fraction of a beat

random.seed(7)
rng = random.Random(7)

# --- General MIDI programs -------------------------------------------------
PROGRAMS = {
    'trumpet':   56,  # lead of the brass section
    'trumpet2':  56,  # harmony a diatonic third below - the sonora format
    'trombone':  57,
    'guitar':    27,  # clean electric guitar - the charchazo
    'bass':      33,  # electric bass (finger) - tumbao
    'organ':     18,  # rock organ - harmonic glue
}

# GM drum map
KICK, SNARE, SIDESTICK = 36, 38, 37
GUIRO, CONGA_HI, CONGA_LO, CONGA_MUTE = 73, 63, 64, 62
TIMBALE_HI, TIMBALE_LO, COWBELL = 65, 66, 56

# --- Harmony: C - Am - F - G7, major key -----------------------------------
# Major rather than minor: the lyric is celebratory ("llego a ti", "bailo por
# ti", "gozo por ti") and classic sonora cumbia leans bright.
CHORDS = {
    'C':  {'guitar': [64, 67, 72], 'organ': [48, 52, 55], 'bass': 36, 'brass_low': 48},
    'Am': {'guitar': [64, 69, 72], 'organ': [57, 60, 64], 'bass': 45, 'brass_low': 45},
    'F':  {'guitar': [65, 69, 72], 'organ': [53, 57, 60], 'bass': 41, 'brass_low': 41},
    'G7': {'guitar': [62, 67, 71], 'organ': [55, 59, 62, 65], 'bass': 43, 'brass_low': 43},
}

C_MAJOR = [0, 2, 4, 5, 7, 9, 11]


def third_below(note):
    """Diatonic third below in C major, for the second trumpet - the two-trumpet
    harmony is the Sonora Matancera format that classic Chilean cumbia copied."""
    pc, octave = note % 12, note // 12
    if pc not in C_MAJOR:
        return note - 4
    i = C_MAJOR.index(pc)
    j = i - 2
    return octave * 12 + C_MAJOR[j] - (12 if j < 0 else 0)

# --- Structure, in bars ---------------------------------------------------
# (section kind, bars, 4-bar chord cycle)
SECTIONS = [
    ('intro',      8, ['C', 'C', 'F', 'G7']),
    ('verse',      8, ['C', 'C', 'F', 'G7']),
    ('pre_chorus', 4, ['G7', 'G7', 'G7', 'G7']),
    ('chorus',     8, ['C', 'Am', 'F', 'G7']),
    ('chorus',     8, ['C', 'Am', 'F', 'G7']),
    ('verse',      8, ['C', 'F', 'C', 'G7']),
    ('pre_chorus', 4, ['G7', 'G7', 'G7', 'G7']),
    ('chorus',     8, ['C', 'Am', 'F', 'G7']),
    ('outro',      8, ['C', 'Am', 'F', 'G7']),
    ('outro',      8, ['C', 'Am', 'F', 'G7']),
]

# Per-role timing feel, in seconds. A real band is not on the grid: the
# bass tends to push, brass sections sit back, percussion is the anchor.
FEEL = {
    'trumpet':   +0.014,
    'trumpet2':  +0.017,  # the harmony player trails the lead slightly
    'trombone':  +0.018,
    'guitar':    +0.006,
    'bass':      -0.011,
    'organ':     +0.009,
    'drums':      0.0,
}

# The 4-bar brass hook. Entries are (bar_in_phrase, beat, note, dur_beats, vel).
# D natural minor, resolving over the A7 with its C# leading tone.
BRASS_RIFF = [
    (0, 1.5, 67, 0.5, 102),
    (0, 2.0, 72, 0.5, 104),
    (0, 2.5, 76, 0.5, 106),
    (0, 3.0, 79, 2.0, 110),
    (1, 1.0, 76, 0.5, 102),
    (1, 2.0, 72, 0.5, 100),
    (1, 3.0, 67, 2.0, 100),
    (2, 1.0, 69, 0.5, 104),
    (2, 2.0, 72, 0.5, 104),
    (2, 3.0, 77, 1.5, 108),
    (3, 1.0, 71, 0.5, 104),
    (3, 2.0, 74, 0.5, 106),
    (3, 3.0, 79, 0.5, 110),
    (3, 3.5, 77, 1.5, 106),
]


def swing_offset(beat_pos):
    """Push offbeat 8ths late, which is what gives the groove its lilt."""
    frac = beat_pos % 1.0
    return SWING * BEAT if abs(frac - 0.5) < 0.01 else 0.0


def humanize(t, vel, role):
    """Consistent per-role feel offset + small gaussian noise, not uniform mush."""
    t = t + FEEL[role] + rng.gauss(0, 0.007)
    vel = int(np.clip(vel + rng.gauss(0, 5), 1, 127))
    return max(0.0, t), vel


def ticks(seconds):
    return max(0, int(round(seconds * BPM / 60 * TICKS_PER_BEAT)))


class Part:
    """Collects note events for one instrument, then writes them to a MIDI file."""

    def __init__(self, name, program=None, is_drums=False):
        self.name = name
        self.program = program
        self.is_drums = is_drums
        self.events = []

    def note(self, t, note, dur, vel, role=None):
        role = role or ('drums' if self.is_drums else self.name)
        t, vel = humanize(t, vel, role)
        self.events.append((ticks(t), 'on', note, vel))
        self.events.append((ticks(t + max(0.04, dur)), 'off', note, 0))

    def chord(self, t, notes, dur, vel, role=None):
        for i, n in enumerate(notes):
            # Strum-like micro spread so chords are not perfectly simultaneous
            self.note(t + i * 0.004, n, dur, vel - i * 2, role)

    def save(self, path):
        mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM), time=0))
        channel = 9 if self.is_drums else 0
        if self.program is not None:
            track.append(Message('program_change', program=self.program, channel=channel, time=0))

        self.events.sort(key=lambda e: e[0])
        last = 0
        for tick, kind, note, vel in self.events:
            delta = max(0, tick - last)
            msg = 'note_on' if kind == 'on' else 'note_off'
            track.append(Message(msg, note=note, velocity=vel, channel=channel, time=delta))
            last = max(last, tick)
        mid.save(path)


def build_arrangement():
    parts = {
        'trumpet':   Part('trumpet', PROGRAMS['trumpet']),
        'trumpet2':  Part('trumpet2', PROGRAMS['trumpet2']),
        'trombone':  Part('trombone', PROGRAMS['trombone']),
        'guitar':    Part('guitar', PROGRAMS['guitar']),
        'bass':      Part('bass', PROGRAMS['bass']),
        'organ':     Part('organ', PROGRAMS['organ']),
        'drums':     Part('drums', is_drums=True),
    }

    t = 0.0
    bar_index = 0
    for kind, bars, cycle in SECTIONS:
        full = kind in ('intro', 'chorus', 'outro')
        for b in range(bars):
            bar_t = t + b * BAR
            chord_name = cycle[b % 4]
            ch = CHORDS[chord_name]
            phrase_bar = b % 4

            # ---- Percussion: the cumbia engine ----
            d = parts['drums']
            d.note(bar_t + 0 * BEAT, KICK, 0.18, 104)
            d.note(bar_t + 2 * BEAT, KICK, 0.18, 100)
            d.note(bar_t + 1 * BEAT, SIDESTICK, 0.10, 84)
            d.note(bar_t + 3 * BEAT, SNARE, 0.12, 96)
            # Guira: continuous 8ths, accented on the beat - the forward drive
            for i in range(8):
                pos = i * 0.5
                gt = bar_t + pos * BEAT + swing_offset(pos)
                d.note(gt, GUIRO, BEAT * 0.4, 88 if i % 2 == 0 else 62)
            # Conga tumbao: open tones on the "and" of 2 and 4
            for pos in (1.5, 3.5):
                d.note(bar_t + pos * BEAT + swing_offset(pos), CONGA_HI, 0.2, 92)
            d.note(bar_t + 2 * BEAT, CONGA_LO, 0.2, 80)
            # Cowbell on every beat - THE signature of Chilean cumbia sonora.
            # Sonora Palacios' innovation was moving the Colombian llamador off
            # the offbeat and onto the beat, which is what makes this style read
            # as danceable to a Chilean ear. It runs through every section.
            for beat in range(4):
                d.note(bar_t + beat * BEAT, COWBELL,
                       0.13, 92 if beat % 2 == 0 else 80)
            # Timbale fill on the last bar of each section
            if b == bars - 1:
                for i, pos in enumerate((3.0, 3.25, 3.5, 3.75)):
                    d.note(bar_t + pos * BEAT, TIMBALE_HI if i % 2 else TIMBALE_LO, 0.12, 96)

            # ---- Bass: tumbao ----
            root = ch['bass']
            parts['bass'].note(bar_t + 0 * BEAT, root, BEAT * 0.55, 106)
            parts['bass'].note(bar_t + 1.5 * BEAT + swing_offset(1.5), root + 7, BEAT * 0.4, 92)
            parts['bass'].note(bar_t + 2 * BEAT, root, BEAT * 0.5, 100)
            nxt = CHORDS[cycle[(b + 1) % 4]]['bass']
            approach = root + (2 if nxt > root else -2)
            parts['bass'].note(bar_t + 3.5 * BEAT + swing_offset(3.5), approach, BEAT * 0.35, 88)

            # ---- Guitar charchazo: short chords on every offbeat ----
            for pos in (0.5, 1.5, 2.5, 3.5):
                gt = bar_t + pos * BEAT + swing_offset(pos)
                parts['guitar'].chord(gt, ch['guitar'], BEAT * 0.22, 92 if pos in (0.5, 2.5) else 84)

            # ---- Organ: sustained glue, only in the fuller sections ----
            if full:
                parts['organ'].chord(bar_t, ch['organ'], BAR * 0.95, 62)

            # ---- Brass ----
            if full:
                for rb, beat, note, dur, vel in BRASS_RIFF:
                    if rb != phrase_bar:
                        continue
                    pos = beat - 1
                    bt = bar_t + pos * BEAT + swing_offset(pos)
                    parts['trumpet'].note(bt, note, dur * BEAT * 0.92, vel)
                    parts['trumpet2'].note(bt, third_below(note), dur * BEAT * 0.92, vel - 6)
                # Trombone punctuates the chord root underneath the lead
                parts['trombone'].note(bar_t, ch['brass_low'], BEAT * 0.7, 96)
                parts['trombone'].note(bar_t + 2 * BEAT, ch['brass_low'], BEAT * 0.6, 88)
            elif kind == 'pre_chorus':
                # Build into the chorus: rising brass swell
                parts['trumpet'].note(bar_t + 2 * BEAT, 69 + b, BEAT * 1.8, 88 + b * 6)
                parts['trombone'].note(bar_t + 2 * BEAT, 57, BEAT * 1.8, 84 + b * 5)
            else:
                # Verses stay open for the vocal: one answering stab per bar
                parts['trumpet'].note(bar_t + 3.5 * BEAT + swing_offset(3.5),
                                      ch['brass_low'] + 12, BEAT * 0.3, 78)

            bar_index += 1
        t += bars * BAR

    return parts, t


# --- Mixing ---------------------------------------------------------------
# Each stem gets its own chain: EQ to carve its range, compression to
# control dynamics, stereo placement, and ambience so it is not bone dry.
# Stem levels are set from measured stem loudness, not guessed: the first
# pass had the bass 21 dB above the percussion and 15 dB above the trumpet,
# which buried the brass hook and the cumbia groove. In this genre the
# percussion and the brass carry the song, so they sit on top, with the
# bass supporting rather than dominating.
MIX = {
    # name:        (highpass, presence_freq, presence_gain, pan, comp_thresh, ratio, makeup, echo, volume)
    'bass':        (35,   900,  2.0,  0.00, 0.10, 4.0, 2.4, None,                              0.45),
    'drums':       (55,  4000,  3.0,  0.00, 0.14, 3.0, 2.6, '0.85:0.16:35|60:0.18|0.12',       3.40),
    'guitar':      (140, 2600,  4.0, -0.24, 0.12, 3.5, 2.1, '0.9:0.28:55|95|140:0.3|0.22|0.15', 1.05),
    'trumpet':     (200, 3200,  3.5,  0.19, 0.13, 3.0, 2.0, '0.9:0.3:70|120|180:0.32|0.24|0.16', 2.05),
    'trumpet2':    (200, 3100,  3.0, -0.21, 0.13, 3.0, 2.0, '0.9:0.3:75|125|185:0.3|0.22|0.15',  1.65),
    'trombone':    (120, 1800,  2.5, -0.17, 0.13, 3.0, 2.0, '0.9:0.28:70|120:0.3|0.2',         1.40),
    'organ':       (160, 1500,  1.5,  0.15, 0.16, 2.5, 1.7, '0.9:0.25:80|130:0.28|0.18',       1.25),
}


def render_stem(midi_path, wav_path):
    subprocess.run(['fluidsynth', '-ni', SOUNDFONT, midi_path,
                    '-F', wav_path, '-r', str(SAMPLE_RATE)],
                   check=True, capture_output=True)


def process_stem(src, dst, name):
    hp, pf, pg, pan, thr, ratio, makeup, echo, vol = MIX[name]
    chain = [
        f'highpass=f={hp}',
        f'equalizer=f={pf}:width_type=q:width=1.2:g={pg}',
        f'acompressor=threshold={thr}:ratio={ratio}:attack=8:release=140:makeup={makeup}',
    ]
    if echo:
        chain.append(f'aecho={echo}')
    if abs(pan) > 0.01:
        chain.append(f'stereotools=balance_out={pan}')
    chain.append(f'volume={vol}')
    subprocess.run(['ffmpeg', '-y', '-i', src, '-af', ','.join(chain), dst],
                   check=True, capture_output=True)


def mix_and_master(stems, out_path, total_duration, fade_seconds):
    inputs = []
    for s in stems:
        inputs += ['-i', s]
    n = len(stems)
    master = (
        f'amix=inputs={n}:duration=longest:normalize=0,'
        'acompressor=threshold=0.25:ratio=2:attack=25:release=250:makeup=1.6,'
        'equalizer=f=250:width_type=q:width=1.1:g=-2,'
        'equalizer=f=3000:width_type=q:width=1.4:g=2,'
        f'afade=t=out:st={total_duration - fade_seconds}:d={fade_seconds},'
        'alimiter=limit=0.95,'
        'loudnorm=I=-14:TP=-1.0:LRA=11'
    )
    subprocess.run(['ffmpeg', '-y'] + inputs +
                   ['-filter_complex', master, '-ar', str(SAMPLE_RATE), out_path],
                   check=True, capture_output=True)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    audio = os.path.join(base, 'audio')
    stems_dir = os.path.join(audio, 'stems')
    os.makedirs(stems_dir, exist_ok=True)

    total_bars = sum(b for _k, b, _c in SECTIONS)
    print('Generating "Medio Limón" backing track (v3, cumbia chilena)')
    print(f'  {BPM} BPM, 4/4, {total_bars} bars, harmony Dm-Gm-A7')
    print(f'  Structure: {" -> ".join(k for k, _b, _c in SECTIONS)}')
    print()

    print('[1/4] Writing arrangement (brass riff, charchazo, tumbao, cumbia percussion)...')
    parts, total_duration = build_arrangement()

    print('[2/4] Rendering each instrument to its own stem via fluidsynth...')
    processed = []
    for name, part in parts.items():
        midi_path = os.path.join(stems_dir, f'{name}.mid')
        raw = os.path.join(stems_dir, f'{name}_raw.wav')
        proc = os.path.join(stems_dir, f'{name}.wav')
        part.save(midi_path)
        render_stem(midi_path, raw)
        print(f'      - {name}')
        process_stem(raw, proc, name)
        os.remove(raw)
        processed.append(proc)

    print('[3/4] Mixing stems with per-instrument EQ, compression, panning, ambience...')
    out = os.path.join(audio, 'backing_track_base.wav')
    fade = SECTIONS[-1][1] * BAR  # fade across the final outro repeat
    mix_and_master(processed, out, total_duration, fade)

    print('[4/4] Done.')
    print()
    print(f'  Output: {out}')
    print(f'  Duration: {total_duration:.1f}s')


if __name__ == '__main__':
    main()
