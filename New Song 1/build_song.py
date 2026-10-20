#!/usr/bin/env python3
"""
New Song 1 -- backing track builder (render continuo, un solo MIDI por
instrumento, sin cortes entre secciones).

La clave del render continuo: se escribe UN solo MIDI por instrumento que
abarca toda la cancion (con silencio en las secciones donde ese instrumento
no toca). FluidSynth renderiza cada instrumento en una sola pasada. No hay
nada que pegar: el audio es una sola toma por construccion.

Diferencias vs. Second Floor (Kicking Stones):
  - Tonalidad: D menor (vs A menor)
  - Progresion: Dm-Bb-C-Am (i-VI-VII-v, una cuarta mas abajo)
  - Motivo guitarra: ascendente F3-G3-A3-C4 (vs descendente E4-D4-C4-A3)
  - BPM: 138 (mas pesado, mas lento)
  - Estructura: sin Rap/Faster; doble Verse + Pre-Chorus de 12 compases
  - Lead: escala D menor natural con random walk (mismo principio que KS)

Principios de produccion heredados de Second Floor:
  - Drum machine estilo 808/909: kick+snare+hi-hats, patron simple y repetitivo
  - Fill de bateria en el ultimo compas de cada seccion (pickup hacia la siguiente)
  - Crash en el primer beat de la seccion siguiente si tiene bateria
  - Nota de anticipacion del bajo antes de que entre tras una ausencia
  - Bajo distorsionado (tanh drive=5), reverb variable por nota
  - Guitarra limpia con chorus + reverb variable por nota
  - Pad oscuro sostenido (GM 90 Pad 4 choir), un acorde por compas
  - Humanizacion: jitter de timing +-12 ticks, velocity +-10
  - Check de continuidad al final: ningun punto debe caer a un hoyo de energia
"""
import os
import re
import subprocess
import random
import numpy as np
from scipy.io import wavfile
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

SR = 44100
TICKS_PER_BEAT = 480

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSIONS_DIR = os.path.join(PROJECT_DIR, "versions")
SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

random.seed(7)

# General MIDI drum map
GM_KICK = 36
GM_SNARE = 38
GM_HIHAT_CLOSED = 42
GM_HIHAT_OPEN = 46
GM_CRASH = 49
GM_OVERDRIVEN_GUITAR = 29

# D natural minor: i=Dm, VI=Bb, VII=C, v=Am
# Raices bajo: D1=26, Bb0=22, C1=24, A0=21
ROOTS_MIDI = {"D": 26, "Bb": 22, "C": 24, "A": 21}

# Dm: D3 F3 A3 = 50 53 57
# Bb: Bb2 D3 F3 = 46 50 53
# C:  C3 E3 G3  = 48 52 55
# Am: A2 C3 E3  = 45 48 52
CHORD_TONES_MIDI = {
    "D":  [50, 53, 57],
    "Bb": [46, 50, 53],
    "C":  [48, 52, 55],
    "A":  [45, 48, 52],
}
PROGRESSION = ["D", "Bb", "C", "A"]

BPM = 138
TIMING_JITTER_TICKS = 12
VELOCITY_JITTER = 10

# Motivo guitarra ascendente F3-G3-A3-C4
F3, G3, A3_n, C4 = 53, 55, 57, 60
GUITAR_MOTIF = [(F3, 0.5), (G3, 0.5), (A3_n, 0.75), (C4, 0.75)]

# Estructura de la cancion
SECTIONS = [
    {"name": "intro",     "bars": 4,  "instruments": ["pad"]},
    {"name": "verse1",    "bars": 8,  "instruments": ["drums", "bass"],
     "drum_density": "full", "bass_pattern": "half"},
    {"name": "verse2",    "bars": 8,  "instruments": ["drums", "bass", "guitar"],
     "drum_density": "full", "bass_pattern": "half", "guitar_density": "sparse"},
    {"name": "prechorus", "bars": 12, "instruments": ["drums", "bass", "guitar", "pad"],
     "drum_density": "full", "bass_pattern": "half", "guitar_density": "sparse"},
    {"name": "chorus1",   "bars": 8,  "instruments": ["drums", "bass", "guitar", "pad"],
     "drum_density": "full", "bass_pattern": "quarter", "guitar_density": "full"},
    {"name": "verse3",    "bars": 8,  "instruments": ["drums", "bass", "guitar", "pad"],
     "drum_density": "full", "bass_pattern": "half", "guitar_density": "sparse"},
    {"name": "bridge",    "bars": 4,  "instruments": ["drums", "pad"],
     "drum_density": "sparse"},
    {"name": "chorus2",   "bars": 8,  "instruments": ["drums", "bass", "guitar", "pad"],
     "drum_density": "full", "bass_pattern": "quarter", "guitar_density": "full"},
    {"name": "outro",     "bars": 8,  "instruments": ["drums", "pad", "lead"],
     "drum_density": "sparse"},
]

GAINS = {"drums": 1.0, "bass": 0.75, "guitar": 0.50, "pad": 0.35, "lead": 0.55}

# Escala D menor natural para el lead del outro
# D3 E3 F3 G3 A3 Bb3 C4 D4 E4 F4 G4 A4 D5
D_MINOR_SCALE = [50, 52, 53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 74]

# Tonos del acorde por grado (semitono relativo a D=50) para atraer el lead
CHORD_TONE_SEMITONES = {
    "D":  {0, 3, 7},   # D F A
    "Bb": {-4, 0, 3},  # Bb D F
    "C":  {-2, 2, 5},  # C E G
    "A":  {-5, -2, 2}, # A C E
}


def ticks(beats):
    return int(beats * TICKS_PER_BEAT)


def tick_to_sec(tick):
    return tick / TICKS_PER_BEAT * (60.0 / BPM)


def humanize_tick(t, amount=TIMING_JITTER_TICKS):
    return max(0, t + random.randint(-amount, amount))


def humanize_velocity(base, amount=VELOCITY_JITTER):
    return max(1, min(127, base + random.randint(-amount, amount)))


def next_version_dir():
    os.makedirs(VERSIONS_DIR, exist_ok=True)
    existing = [d for d in os.listdir(VERSIONS_DIR) if re.fullmatch(r"v\d+", d)]
    nums = [int(d[1:]) for d in existing] if existing else [0]
    v = max(nums) + 1
    path = os.path.join(VERSIONS_DIR, f"v{v}")
    os.makedirs(path)
    return path, v


def pitch_bend_value(cents, bend_range_semitones=2.0):
    semitone_range = bend_range_semitones * 100.0
    return int(max(-8192, min(8191, round(cents / semitone_range * 8192))))


# ── MIDI CONTINUOS ──────────────────────────────────────────────────────────

def build_continuous_drum_midi(path, humanize=True):
    """Bateria continua con fill de snare en el ultimo compas de cada seccion
    (pickup natural hacia la siguiente parte) y crash en el beat 1 de la
    seccion siguiente si tiene bateria."""
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(BPM), time=0))

    events = []
    abs_bar = 0

    for idx, section in enumerate(SECTIONS):
        next_section = SECTIONS[idx + 1] if idx + 1 < len(SECTIONS) else None

        if "drums" not in section["instruments"]:
            abs_bar += section["bars"]
        else:
            density = section.get("drum_density", "full")
            for local_bar in range(section["bars"]):
                bar_start = abs_bar * ticks(4)
                is_last_bar = (local_bar == section["bars"] - 1)

                def add_hit(beat_pos, note, vel, h=humanize):
                    t = bar_start + ticks(beat_pos)
                    v = vel
                    if h:
                        t = humanize_tick(t)
                        v = humanize_velocity(vel)
                    events.append((t, note, v, True))
                    events.append((t + 20, note, 0, False))

                if density == "sparse":
                    add_hit(0, GM_KICK, 85)
                    add_hit(2, GM_KICK, 75)
                else:  # "full"
                    add_hit(0, GM_KICK, 100)
                    add_hit(2, GM_KICK, 95)
                    add_hit(1, GM_SNARE, 105)
                    if is_last_bar:
                        # fill: snare en semicorcheas del beat 4 (pickup)
                        for i, sub in enumerate([0.0, 0.25, 0.5, 0.75]):
                            add_hit(3 + sub, GM_SNARE, 92 + i * 8)
                    else:
                        add_hit(3, GM_SNARE, 100)
                    for eighth in range(8):
                        if is_last_bar and eighth >= 6:
                            continue  # espacio para el fill
                        is_last_hat = (local_bar % 2 == 1 and eighth == 7)
                        note = GM_HIHAT_OPEN if is_last_hat else GM_HIHAT_CLOSED
                        add_hit(eighth * 0.5, note, 72)
                abs_bar += 1

        # crash en el downbeat de la siguiente seccion si tiene bateria
        if next_section is not None and "drums" in next_section["instruments"]:
            crash_tick = abs_bar * ticks(4)
            events.append((crash_tick, GM_CRASH, 110, True))
            events.append((crash_tick + 20, GM_CRASH, 0, False))

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for t, note, vel, on in events:
        delta = max(0, t - last_tick)
        track.append(Message("note_on" if on else "note_off",
                              note=note, velocity=vel, time=delta, channel=9))
        last_tick = max(last_tick, t)
    mid.save(path)


def build_continuous_bass_midi(path, humanize=True):
    """Bajo continuo. Cuando el bajo esta ausente y la siguiente seccion lo
    tiene, toca una nota de anticipacion (root del siguiente acorde, ultimo
    octavo del compas anterior) para que la entrada no sea fria."""
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(BPM), time=0))
    track.append(Message("program_change", program=34, time=0, channel=1))

    events = []
    note_windows_sec = []

    def emit_note(start, dur, note, vel):
        end = start + dur
        events.append((start, "on", note, vel))
        depth_cents = random.uniform(3.0, 8.0)
        phase = random.uniform(0, 2 * np.pi)
        rate = random.uniform(1.5, 3.0)
        for i in range(10):
            frac = i / 9
            t = start + int(frac * dur)
            wobble = np.sin(2 * np.pi * rate * frac + phase)
            cents = wobble * depth_cents + random.uniform(-1.0, 1.0)
            events.append((t, "bend", pitch_bend_value(cents), None))
        events.append((end, "bend", 0, None))
        events.append((end, "off", note, 0))
        note_windows_sec.append((tick_to_sec(start), tick_to_sec(end)))

    abs_bar = 0
    for idx, section in enumerate(SECTIONS):
        next_section = SECTIONS[idx + 1] if idx + 1 < len(SECTIONS) else None

        if "bass" not in section["instruments"]:
            if next_section is not None and "bass" in next_section["instruments"]:
                # nota de anticipacion: ultimo octavo del ultimo compas
                pickup_bar_start = (abs_bar + section["bars"] - 1) * ticks(4)
                next_chord = PROGRESSION[(abs_bar + section["bars"]) % len(PROGRESSION)]
                start = pickup_bar_start + ticks(3.5)
                if humanize:
                    start = humanize_tick(start)
                emit_note(start, ticks(0.4), ROOTS_MIDI[next_chord], 88)
            abs_bar += section["bars"]
            continue

        pattern = section.get("bass_pattern", "half")
        beat_positions = (0, 1, 2, 3) if pattern == "quarter" else (0, 2)
        hit_dur_beats = 0.9 if pattern == "quarter" else 1.9

        for _ in range(section["bars"]):
            bar_start = abs_bar * ticks(4)
            chord = PROGRESSION[abs_bar % len(PROGRESSION)]
            note = ROOTS_MIDI[chord]
            for beat_pos in beat_positions:
                start = bar_start + ticks(beat_pos)
                dur = ticks(hit_dur_beats)
                vel = 108
                if humanize:
                    start = humanize_tick(start)
                    dur += random.randint(-15, 15)
                    vel = humanize_velocity(vel)
                emit_note(start, dur, note, vel)
            abs_bar += 1

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for t, kind, value, vel in events:
        delta = max(0, t - last_tick)
        if kind == "on":
            track.append(Message("note_on", note=value, velocity=vel, time=delta, channel=1))
        elif kind == "off":
            track.append(Message("note_off", note=value, velocity=0, time=delta, channel=1))
        else:
            track.append(Message("pitchwheel", pitch=value, time=delta, channel=1))
        last_tick = max(last_tick, t)
    mid.save(path)
    return note_windows_sec


def build_continuous_guitar_midi(path, humanize=True):
    """Guitarra continua con motivo ascendente F3-G3-A3-C4."""
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(BPM), time=0))
    track.append(Message("program_change", program=27, time=0, channel=2))

    events = []
    note_windows_sec = []
    abs_bar = 0

    for section in SECTIONS:
        if "guitar" not in section["instruments"]:
            abs_bar += section["bars"]
            continue
        density = section.get("guitar_density", "sparse")
        for local_bar in range(section["bars"]):
            play = density == "full" or local_bar % 2 == 0
            if play:
                bar_start = abs_bar * ticks(4)
                pos = 0.0
                for note, dur_beats in GUITAR_MOTIF:
                    start = bar_start + ticks(pos)
                    dur = ticks(dur_beats * 0.85)
                    vel = 80
                    if humanize:
                        start = humanize_tick(start, amount=8)
                        dur += random.randint(-10, 10)
                        vel = humanize_velocity(vel, amount=8)
                    end = start + dur
                    events.append((start, "on", note, vel))
                    events.append((end, "off", note, 0))
                    note_windows_sec.append((tick_to_sec(start), tick_to_sec(end)))
                    pos += dur_beats
            abs_bar += 1

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for t, kind, note, vel in events:
        delta = max(0, t - last_tick)
        track.append(Message("note_on" if kind == "on" else "note_off",
                              note=note, velocity=vel, time=delta, channel=2))
        last_tick = max(last_tick, t)
    mid.save(path)
    return note_windows_sec


def build_continuous_pad_midi(path, humanize=True):
    """Pad continuo. Un acorde sostenido por compas, siguiendo la progresion."""
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(BPM), time=0))
    track.append(Message("program_change", program=90, time=0, channel=3))

    events = []
    note_windows_sec = []
    abs_bar = 0

    for section in SECTIONS:
        if "pad" not in section["instruments"]:
            abs_bar += section["bars"]
            continue
        for _ in range(section["bars"]):
            bar_start = abs_bar * ticks(4)
            chord = PROGRESSION[abs_bar % len(PROGRESSION)]
            for note in CHORD_TONES_MIDI[chord]:
                start = bar_start
                dur = ticks(4)
                vel = 52
                if humanize:
                    start = humanize_tick(start, amount=6)
                    vel = humanize_velocity(vel, amount=6)
                end = start + dur
                events.append((start, "on", note, vel))
                events.append((end, "off", note, 0))
            note_windows_sec.append((tick_to_sec(bar_start), tick_to_sec(bar_start + ticks(4))))
            abs_bar += 1

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for t, kind, note, vel in events:
        delta = max(0, t - last_tick)
        track.append(Message("note_on" if kind == "on" else "note_off",
                              note=note, velocity=vel, time=delta, channel=3))
        last_tick = max(last_tick, t)
    mid.save(path)
    return note_windows_sec


def _closest_scale_index(target_note, scale):
    return min(range(len(scale)), key=lambda i: abs(scale[i] - target_note))


def build_continuous_lead_midi(path, humanize=True):
    """Lead overdriven con random walk sobre la escala D menor natural.
    En los beats fuertes (1 y 3) se atrae al tono del acorde actual para
    que siga la progresion en vez de vagar libre."""
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(BPM), time=0))
    track.append(Message("program_change", program=GM_OVERDRIVEN_GUITAR, time=0, channel=4))

    events = []
    note_windows_sec = []
    dur_choices = [0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 1.0]
    abs_bar = 0
    scale_idx = len(D_MINOR_SCALE) // 2

    for section in SECTIONS:
        if "lead" not in section["instruments"]:
            abs_bar += section["bars"]
            continue
        for _ in range(section["bars"]):
            bar_start = abs_bar * ticks(4)
            chord = PROGRESSION[abs_bar % len(PROGRESSION)]
            pos_beats = 0.0
            while pos_beats < 4.0:
                if random.random() < 0.12:
                    pos_beats += random.choice([0.25, 0.5])
                    continue
                on_strong = pos_beats in (0.0, 2.0)
                if on_strong and random.random() < 0.6:
                    # atraer hacia el tono del acorde actual
                    offset = random.choice(list(CHORD_TONE_SEMITONES[chord]))
                    target = 50 + offset  # D3 = 50 como raiz
                    scale_idx = _closest_scale_index(target, D_MINOR_SCALE)
                else:
                    step = random.choice([-3, -2, -1, -1, 1, 1, 2, 3])
                    scale_idx = max(0, min(len(D_MINOR_SCALE) - 1, scale_idx + step))
                note = D_MINOR_SCALE[scale_idx]
                dur_beats = min(random.choice(dur_choices), 4.0 - pos_beats)
                start = bar_start + ticks(pos_beats)
                dur = ticks(dur_beats * 0.85)
                vel = 82
                if humanize:
                    start = humanize_tick(start, amount=10)
                    vel = humanize_velocity(vel, amount=10)
                end = start + dur
                events.append((start, "on", note, vel))
                events.append((end, "off", note, 0))
                note_windows_sec.append((tick_to_sec(start), tick_to_sec(end)))
                pos_beats += dur_beats
            abs_bar += 1

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for t, kind, note, vel in events:
        delta = max(0, t - last_tick)
        track.append(Message("note_on" if kind == "on" else "note_off",
                              note=note, velocity=vel, time=delta, channel=4))
        last_tick = max(last_tick, t)
    mid.save(path)
    return note_windows_sec


# ── AUDIO ───────────────────────────────────────────────────────────────────

def render_midi_to_wav(midi_path, wav_path):
    subprocess.run([
        "fluidsynth", "-ni", SOUNDFONT, midi_path,
        "-F", wav_path, "-r", str(SR), "-g", "1.0", "-R", "0", "-C", "0"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def distort(samples, drive=4.5):
    return np.tanh(samples * drive) / np.tanh(drive)


def chorus_effect(signal, rate_hz=0.35, depth_ms=7.0, base_delay_ms=20.0, mix=0.40, sr=SR):
    n = len(signal)
    t = np.arange(n) / sr
    delay_samples = (base_delay_ms + depth_ms * np.sin(2 * np.pi * rate_hz * t)) * sr / 1000.0
    idx = np.arange(n) - delay_samples
    valid = idx >= 0
    delayed = np.zeros(n)
    delayed[valid] = np.interp(idx[valid], np.arange(n), signal)
    return signal * (1 - mix) + delayed * mix


def convolve_reverb(segment, decay, mix):
    tail_len = int(SR * 1.0)
    ir = np.random.randn(tail_len) * np.exp(-np.arange(tail_len) / (SR * decay))
    ir[0] = 1.0
    wet = np.convolve(segment, ir)
    out = np.zeros(len(segment) + tail_len)
    out[:len(segment)] += segment
    out[:len(wet)] += wet * mix
    return out


def per_note_variable_reverb(dry, note_windows_sec, sr=SR):
    if not note_windows_sec:
        return dry
    starts = sorted(int(s * sr) for s, _ in note_windows_sec)
    boundaries = starts + [len(dry)]
    out = np.zeros(len(dry) + int(sr * 1.0))
    for i in range(len(boundaries) - 1):
        seg_start, seg_end = boundaries[i], boundaries[i + 1]
        if seg_end <= seg_start:
            continue
        segment = dry[seg_start:seg_end]
        decay = random.uniform(0.12, 0.35)
        mix = random.uniform(0.15, 0.30)
        wet = convolve_reverb(segment, decay=decay, mix=mix)
        end = min(seg_start + len(wet), len(out))
        out[seg_start:end] += wet[:end - seg_start]
    return out[:len(dry)] if len(out) >= len(dry) else np.pad(out, (0, len(dry) - len(out)))


def load_wav_mono(path):
    sr, data = wavfile.read(path)
    if data.ndim > 1:
        data = data.mean(axis=1)
    return data.astype(np.float32) / 32768.0


def peak_normalize(samples, peak=0.9):
    cur = np.max(np.abs(samples))
    return samples / cur * peak if cur > 0 else samples


def write_wav(samples, path):
    wavfile.write(path, SR, (np.clip(samples, -1.0, 1.0) * 32767).astype(np.int16))
    print(f"    guardado: {path}")


def pad_to(a, n):
    return np.pad(a, (0, n - len(a))) if len(a) < n else a[:n]


def sum_mix(tracks_with_gains, path, headroom_peak=0.96, length=None):
    if length is None:
        length = max(len(t) for t, _ in tracks_with_gains) if tracks_with_gains else 0
    mix = np.zeros(length)
    for track, gain in tracks_with_gains:
        mix[:len(track)] += pad_to(track, length) * gain
    peak = np.max(np.abs(mix)) if length else 0
    if peak > headroom_peak:
        mix *= headroom_peak / peak
        print(f"    atenuado {headroom_peak/peak:.2f}x (pico {peak:.2f})")
    if path:
        write_wav(mix, path)
    return mix


def trim_trailing_silence(audio, threshold=0.02, keep_tail_sec=1.0, sr=SR):
    above = np.where(np.abs(audio) > threshold)[0]
    if len(above) == 0:
        return audio
    last = above[-1] + int(sr * keep_tail_sec)
    return audio[:min(last, len(audio))]


# ── CHECK DE CONTINUIDAD ───────────────────────────────────────────────────

def check_boundary_continuity(mix, sr=SR, win_sec=0.05, context_sec=1.0,
                               drop_ratio=0.20, neighbor_floor=0.01):
    """Detecta hoyos de energia en la mezcla: si un punto cae por debajo de
    drop_ratio * los vecinos en ambos lados, es una costura audible."""
    win = int(win_sec * sr)
    hop = win // 2
    rms, times = [], []
    for i in range(0, max(0, len(mix) - win), hop):
        w = mix[i:i + win]
        rms.append(np.sqrt(np.mean(w.astype(np.float64) ** 2)))
        times.append(i / sr)
    rms = np.array(rms)
    times = np.array(times)
    ctx_n = max(1, int(context_sec / (hop / sr)))

    flagged = []
    for i in range(ctx_n, len(rms) - ctx_n - 1):
        before = np.mean(rms[i - ctx_n:i])
        after = np.mean(rms[i + 1:i + 1 + ctx_n])
        floor = min(before, after)
        if floor < neighbor_floor:
            continue
        if rms[i] < floor * drop_ratio:
            flagged.append(times[i])

    if not flagged:
        return True, ["  check de continuidad: OK (sin hoyos de energia)"]

    runs = []
    start = prev = flagged[0]
    for t in flagged[1:]:
        if t - prev > (hop / sr) * 1.5:
            runs.append((start, prev))
            start = t
        prev = t
    runs.append((start, prev))

    lines = [f"  ADVERTENCIA: hoyo de energia detectado en {s:.2f}s-{e:.2f}s" for s, e in runs]
    return False, lines


# ── RENDER CONTINUO ────────────────────────────────────────────────────────

def build_continuous_song(version_dir):
    midi_dir = os.path.join(version_dir, "full_song_midi")
    os.makedirs(midi_dir, exist_ok=True)
    print("  render continuo (una sola toma por instrumento)...")

    processed = {}
    length = 0

    # Bateria
    p = os.path.join(midi_dir, "drums.mid")
    build_continuous_drum_midi(p)
    raw = os.path.join(midi_dir, "_drums_raw.wav")
    render_midi_to_wav(p, raw)
    drums = load_wav_mono(raw); os.remove(raw)
    processed["drums"] = drums; length = max(length, len(drums))

    # Bajo
    p = os.path.join(midi_dir, "bass.mid")
    bass_wins = build_continuous_bass_midi(p)
    raw = os.path.join(midi_dir, "_bass_raw.wav")
    render_midi_to_wav(p, raw)
    bass = load_wav_mono(raw); os.remove(raw)
    bass = distort(bass, drive=5.0)
    bass = per_note_variable_reverb(bass, bass_wins)
    processed["bass"] = bass; length = max(length, len(bass))

    # Guitarra
    p = os.path.join(midi_dir, "guitar.mid")
    guitar_wins = build_continuous_guitar_midi(p)
    raw = os.path.join(midi_dir, "_guitar_raw.wav")
    render_midi_to_wav(p, raw)
    guitar = load_wav_mono(raw); os.remove(raw)
    guitar = chorus_effect(guitar)
    guitar = per_note_variable_reverb(guitar, guitar_wins)
    processed["guitar"] = guitar; length = max(length, len(guitar))

    # Pad
    p = os.path.join(midi_dir, "pad.mid")
    pad_wins = build_continuous_pad_midi(p)
    raw = os.path.join(midi_dir, "_pad_raw.wav")
    render_midi_to_wav(p, raw)
    pad_audio = load_wav_mono(raw); os.remove(raw)
    pad_audio = per_note_variable_reverb(pad_audio, pad_wins)
    processed["pad"] = pad_audio; length = max(length, len(pad_audio))

    # Lead
    p = os.path.join(midi_dir, "lead.mid")
    lead_wins = build_continuous_lead_midi(p)
    raw = os.path.join(midi_dir, "_lead_raw.wav")
    render_midi_to_wav(p, raw)
    lead = load_wav_mono(raw); os.remove(raw)
    lead = distort(lead, drive=3.0)
    lead = chorus_effect(lead, base_delay_ms=24.0)
    lead = per_note_variable_reverb(lead, lead_wins)
    processed["lead"] = lead; length = max(length, len(lead))

    tracks_with_gains = []
    gained = {}
    for inst, audio in processed.items():
        norm = peak_normalize(pad_to(audio, length))
        track = norm * GAINS[inst]
        gained[inst] = track
        tracks_with_gains.append((norm, GAINS[inst]))

    full_mix = sum_mix(tracks_with_gains, None, length=length)
    full_mix = trim_trailing_silence(full_mix, keep_tail_sec=1.2)

    # stems alineados al mix final
    stems_dir = os.path.join(version_dir, "stems")
    os.makedirs(stems_dir, exist_ok=True)
    for inst, t in gained.items():
        write_wav(pad_to(t, len(full_mix)), os.path.join(stems_dir, f"{inst}.wav"))

    return full_mix


# ── MAIN ────────────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(SOUNDFONT):
        print(f"ERROR: SoundFont no encontrado en {SOUNDFONT}")
        print("Instalar con: sudo apt install fluid-soundfont-gm")
        return

    out_dir, v = next_version_dir()
    print(f"Nueva cancion v{v} → {out_dir}")

    full_mix = build_continuous_song(out_dir)
    peak_normalize(full_mix)

    out_path = os.path.join(out_dir, "mix.wav")
    write_wav(full_mix, out_path)

    passed, lines = check_boundary_continuity(full_mix)
    for line in lines:
        print(line)
    if not passed:
        print("  Re-revisar las transiciones si se escuchan cortes.")

    duration = len(full_mix) / SR
    print(f"\nListo! Duracion: {duration:.1f}s ({duration/60:.1f} min)")
    print(f"Archivo: {out_path}")


if __name__ == "__main__":
    main()
