#!/usr/bin/env python3
"""
Mirror Cry -- Automated Song Builder (MIDI + FluidSynth + DSP)
Cold wave moderno a 156 BPM, en E menor (Em - C - Am - B).
Batería motorik (bombo en los 4 tiempos, hi-hat abierto a contratiempo),
bajo galopante, guitarra con arpegios en grupos de 3 semicorcheas,
riff de sintetizador con eco, acordes distorsionados en el coro y un
corte seco antes del coro.

Funciona al clonar el repo: ver README.md de esta carpeta.
Uso: python build_song.py
"""
import glob
import os
import random
import re
import shutil
import subprocess
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

SR = 44100
TICKS_PER_BEAT = 480
BPM = 156

# Todas las rutas son relativas a este archivo, no a donde se ejecute el comando.
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSIONS_DIR = os.path.join(PROJECT_DIR, "versions")
REPO_SOUNDFONTS_DIR = os.path.join(os.path.dirname(PROJECT_DIR), "soundfonts")

GM_KICK, GM_SNARE = 36, 38
GM_HAT_C, GM_HAT_O, GM_CRASH = 42, 46, 49

# Tonalidad: Mi menor (Em - C - Am - B). El B mayor es la dominante armónica.
PROGRESSION = ["Em", "C", "Am", "B"]
BASS_ROOT = {"Em": 40, "C": 36, "Am": 33, "B": 35}
ARP = {  # raíz, tercera, quinta, octava
    "Em": [64, 67, 71, 76],
    "C":  [60, 64, 67, 72],
    "Am": [57, 60, 64, 69],
    "B":  [59, 63, 66, 71],
}
POWER = {  # quinta y octava para acordes distorsionados
    "Em": [52, 59, 64],
    "C":  [48, 55, 60],
    "Am": [45, 52, 57],
    "B":  [47, 54, 59],
}

# Estructura: el puente termina con un compás de silencio (solo un bombo).
# drums: motor (verso) / drive (intro, puente, outro) / full (coro)
# bass: gallop / eighths   guitar: none / arp / strum   synth: True/False
def sec(name, bars, drums, bass, guitar, synth, **kw):
    return dict(name=name, bars=bars, drums=drums, bass=bass,
                guitar=guitar, synth=synth, **kw)

SECTIONS = [
    sec("intro",   8, "drive", "gallop",  "arp",   True),
    sec("verse1a", 8, "motor", "eighths", "arp",   True),
    sec("verse1b", 8, "motor", "gallop",  "arp",   True),
    sec("verse2a", 8, "motor", "gallop",  "arp",   True),
    sec("verse2b", 8, "motor", "eighths", "arp",   True),
    sec("inter",   8, "drive", "gallop",  "arp",   True),
    sec("verse3a", 8, "motor", "eighths", "arp",   True),
    sec("verse3b", 8, "motor", "gallop",  "arp",   True),
    sec("bridge1", 8, "drive", "gallop",  "arp",   True),
    sec("bridge2", 4, "drive", "gallop",  "arp",   True, has_drop=True),
    sec("chorus1a", 8, "full", "gallop",  "strum", True),
    sec("chorus1b", 8, "full", "gallop",  "strum", True),
    sec("chorus2a", 8, "full", "gallop",  "strum", True),
    sec("chorus2b", 8, "full", "gallop",  "strum", True),
    sec("outro",   8, "drive", "gallop",  "arp",   True, ending=True),
]

# Ondas de volumen: cada instrumento toca la canción completa en un solo MIDI
# y su presencia es una curva (compás, nivel) suavizada. Los instrumentos
# entran y salen como oleadas, sin cortes entre secciones (como Second Floor).
# Compases: intro 0-8 (hook), v1 8-24, v2 24-40, interludio 40-48 (vuelve el
# hook), v3 48-64, puente 64-76, coro1 76-92, coro2 92-108, outro 108-116.
LEVELS = {
    "drums":  [(0, 0.75), (8, 0.8), (72, 0.9), (76, 1.0), (116, 1.0)],
    "bass":   [(0, 0), (1.5, 0), (2.5, 0.9), (8, 1.0), (116, 1.0)],
    "bass_dbl": [(0, 0), (1.5, 0), (2.5, 0.9), (8, 1.0), (116, 1.0)],
    "bass_sub": [(0, 0), (1.5, 0), (2.5, 0.9), (8, 1.0), (116, 1.0)],
    "guitar": [(0, 0), (3.5, 0), (5, 0.8), (7.5, 0.8), (9.5, 0), (25, 0), (27, 0.75),
               (39, 0.75), (41, 0.85), (47, 0.85), (49.5, 0), (65, 0), (67, 0.8),
               (75, 0.8), (76, 1.0), (116, 1.0)],
    "synth":  [(0, 0), (3.5, 0), (5.5, 0.6), (7.5, 0.6), (9.5, 0), (37, 0), (39, 0.45),
               (41, 0.9), (47, 0.9), (49.5, 0), (65, 0), (68, 0.9), (76, 1.0),
               (116, 1.0)],
    # lead: el hook. Abre la canción, vuelve en el interludio y es la melodía
    # del coro y del final.
    "lead":   [(0, 1.0), (7.5, 1.0), (9.5, 0), (15, 0), (17, 0.18), (23, 0.18),
               (24.5, 0), (31, 0), (33, 0.18), (39, 0.18), (39.5, 0), (41, 1.0),
               (47, 1.0), (49.5, 0), (55, 0), (57, 0.18), (63, 0.18), (64.5, 0),
               (76, 0), (77, 0.75), (107.5, 0.75), (109, 1.0), (116, 1.0)],
    # silbido western: frases lentas en los versos B y el puente; al final
    # recita el arranque del hook sobre la cola.
    "whistle": [(0, 0), (15, 0), (17, 0.8), (23, 0.8), (24.5, 0), (31, 0), (33, 0.8),
                (39, 0.8), (40.5, 0), (55, 0), (57, 0.8), (71, 0.8), (73, 0),
                (116, 0), (116.2, 1.0)],
    "pad":    [(0, 0.25), (4, 1.0), (8, 0.5), (24, 0.35), (36, 0.7), (41, 0.9),
               (48, 0.4), (64, 0.6), (72, 1.0), (76, 0.6), (108, 0.8), (114, 1.0),
               (116, 1.0)],
}


def envelope(name, n_samples):
    """Curva de volumen por muestra: interpolación suave (smoothstep) entre puntos."""
    bar = 4 * 60.0 / BPM * SR
    pts = LEVELS[name]
    x = np.arange(n_samples) / bar
    env = np.zeros(n_samples)
    xs = [p[0] for p in pts]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        m = (x >= x0) & (x < x1)
        t = (x[m] - x0) / (x1 - x0)
        env[m] = y0 + (y1 - y0) * (t * t * (3 - 2 * t))
    env[x >= xs[-1]] = pts[-1][1]
    return env


GAINS = {"drums": 1.25, "bass": 0.56, "bass_dbl": 0.22, "bass_sub": 0.14, "guitar": 0.70, "synth": 0.50, "lead": 0.62, "whistle": 0.45, "pad": 0.35}
PAN = {"drums": 0.5, "bass": 0.5, "bass_dbl": 0.5, "bass_sub": 0.5, "guitar": 0.5, "synth": 0.5, "lead": 0.5, "whistle": 0.5, "pad": 0.5}


# ---------- DEPENDENCIAS EXTERNAS (FluidSynth + SoundFont) ----------

INSTALL_HELP = """
No se encontró {what}.

Instalación rápida:
  Linux / WSL : sudo apt install fluidsynth fluid-soundfont-gm
  macOS       : brew install fluid-synth
  Windows     : choco install fluidsynth   (o usa WSL)
  Python      : pip install -r requirements.txt

Más detalle en README.md de esta carpeta.
"""


def find_fluidsynth():
    exe = shutil.which("fluidsynth")
    if exe:
        return exe
    for p in (r"C:\tools\fluidsynth\bin\fluidsynth.exe",
              r"C:\ProgramData\chocolatey\bin\fluidsynth.exe",
              "/opt/homebrew/bin/fluidsynth",
              "/usr/local/bin/fluidsynth"):
        if os.path.isfile(p):
            return p
    sys.exit(INSTALL_HELP.format(what="el programa 'fluidsynth'"))


def find_soundfont():
    """Orden: variable SOUNDFONT > soundfonts/ del repo > sistema > pretty_midi."""
    env = os.environ.get("SOUNDFONT")
    if env:
        if os.path.isfile(env):
            return env
        sys.exit(f"SOUNDFONT apunta a un archivo que no existe: {env}")

    candidates = []
    for d in (os.path.join(PROJECT_DIR, "soundfonts"), REPO_SOUNDFONTS_DIR):
        candidates += sorted(glob.glob(os.path.join(d, "*.sf2")))
    candidates += [
        "/usr/share/sounds/sf2/FluidR3_GM.sf2",
        "/usr/share/soundfonts/FluidR3_GM.sf2",
        "/usr/share/sounds/sf2/default-GM.sf2",
        "/usr/share/soundfonts/default.sf2",
        "/opt/homebrew/share/soundfonts/default.sf2",
        "/usr/local/share/soundfonts/default.sf2",
        os.path.expanduser("~/soundfonts/FluidR3_GM.sf2"),
        os.path.expanduser("~/.fluidsynth/default_sound_font.sf2"),
        r"C:\ProgramData\soundfonts\default.sf2",
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p

    # Fallback incluido en el paquete pip "pretty_midi" (TimGM6mb, ~6 MB).
    try:
        import pretty_midi
        bundled = os.path.join(os.path.dirname(pretty_midi.__file__), "TimGM6mb.sf2")
        if os.path.isfile(bundled):
            print("  [aviso] usando el SoundFont ligero de pretty_midi; "
                  "para mejor calidad instala fluid-soundfont-gm.")
            return bundled
    except ImportError:
        pass

    sys.exit(INSTALL_HELP.format(what="ningún SoundFont (.sf2)"))


def ticks(beats):
    return int(beats * TICKS_PER_BEAT)


def next_version_dir():
    os.makedirs(VERSIONS_DIR, exist_ok=True)
    existing = [d for d in os.listdir(VERSIONS_DIR) if re.fullmatch(r"v\d+", d)]
    nums = [int(d[1:]) for d in existing] if existing else [0]
    v = max(nums) + 1
    path = os.path.join(VERSIONS_DIR, f"v{v}")
    os.makedirs(path)
    return path, v





# ---------- GENERADORES MIDI ----------

def bar_iter():
    """Rinde (sección, índice de compás en la sección, compás absoluto)."""
    n = 0
    for s in SECTIONS:
        for i in range(s["bars"]):
            yield s, i, n
            n += 1


def is_drop(s, i):
    return s.get("has_drop") and i == s["bars"] - 1


# Humanización: ninguna nota suena exactamente igual a la anterior.
# Varían el momento (microretrasos), la velocidad, la duración y la afinación
# (pitch bend de pocos cents). Las notas simultáneas (acordes) comparten
# desfase y afinación para que suenen como una sola mano.
rng = random.Random(42)
HUMAN = {  # canal: (jitter de tiempo en ticks, jitter de velocidad, cents)
    9: (6, 8, 0),    # batería: más justa
    1: (8, 6, 4),    # bajo
    2: (12, 10, 8),  # guitarra
    3: (10, 8, 10),  # sintetizador
    5: (8, 8, 8),    # lead (hook)
    6: (14, 8, 6),   # silbido
    4: (14, 4, 12),  # pad
}
_human_cache = {}


def human(channel, start_beat):
    key = (channel, round(start_beat, 4))
    if key not in _human_cache:
        t, v, c = HUMAN[channel]
        _human_cache[key] = (rng.randint(-t, t), rng.randint(-v, v),
                             rng.uniform(-c, c))
    return _human_cache[key]


def write_track(path, program, channel, events):
    """events: (tick, nota, velocidad, on). Un MIDI continuo por instrumento."""
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(BPM), time=0))
    if program is not None:
        track.append(Message("program_change", program=program, time=0, channel=channel))
    events = [e if len(e) == 5 else (*e, 0.0) for e in events]
    events.sort(key=lambda e: (e[0], e[3]))  # note_off antes de note_on
    last = 0
    for tick, note, vel, on, cents in events:
        if on and cents:
            bend = int(max(-8191, min(8191, cents / 100.0 * 8191 / 2)))  # rango ±2 semitonos
            track.append(Message("pitchwheel", pitch=bend,
                                 time=max(0, tick - last), channel=channel))
            last = max(last, tick)
        track.append(Message("note_on" if on else "note_off", note=note,
                             velocity=vel, time=max(0, tick - last), channel=channel))
        last = max(last, tick)
    mid.save(path)


def note(ev, start_beat, dur_beats, pitch, vel, channel):
    dt, dv, cents = human(channel, start_beat)
    start = max(0, ticks(start_beat) + dt)
    end = max(start + 1, ticks(start_beat + dur_beats) + dt + rng.randint(-8, 8))
    vel = max(1, min(127, vel + dv + rng.randint(-3, 3)))
    ev.append((start, pitch, vel, True, cents))
    ev.append((end, pitch, 0, False))


def build_drums_midi(path):
    ev = []
    for s, i, n in bar_iter():
        b0 = n * 4.0
        last_bar = i == s["bars"] - 1
        if is_drop(s, i):
            note(ev, b0, 0.1, GM_KICK, 115, 9)
            continue
        style = s["drums"]
        # Bombo en los 4 tiempos (motorik), caja en 2 y 4
        for beat in range(4):
            note(ev, b0 + beat, 0.1, GM_KICK, 108 if beat % 2 == 0 else 92, 9)
        for beat in (1, 3):
            note(ev, b0 + beat, 0.1, GM_SNARE, 112, 9)
        # Hi-hat: cerrado en corcheas, abierto a contratiempo (drive/full)
        if style == "full":
            for k in range(16):  # semicorcheas
                note(ev, b0 + k * 0.25, 0.1, GM_HAT_C, 82 if k % 4 == 0 else 54, 9)
            for beat in range(4):
                note(ev, b0 + beat + 0.5, 0.2, GM_HAT_O, 80, 9)
        elif style == "drive":
            for k in range(8):
                if k % 2 == 1:
                    note(ev, b0 + k * 0.5, 0.25, GM_HAT_O, 78, 9)
                else:
                    note(ev, b0 + k * 0.5, 0.1, GM_HAT_C, 70, 9)
        else:  # motor: hi-hat cerrado sobrio en negras con relleno de corchea
            for k in range(8):
                note(ev, b0 + k * 0.5, 0.1, GM_HAT_C, 72 if k % 2 == 0 else 48, 9)
        if i == 0 and style == "full":
            note(ev, b0, 1.5, GM_CRASH, 100, 9)
        # Relleno al final de cada sección (caja en semicorcheas en el 4º tiempo)
        if last_bar and s.get("ending"):
            # redoble en crescendo: caja en semicorchas durante los últimos 2 tiempos
            for k in range(8):
                note(ev, b0 + 2 + k * 0.25, 0.1, GM_SNARE, 70 + k * 8, 9)
        elif last_bar:
            for k in range(4):
                note(ev, b0 + 3 + k * 0.25, 0.1, GM_SNARE, 85 + k * 10, 9)
    if SECTIONS[-1].get("ending"):
        end = sum(x["bars"] for x in SECTIONS) * 4.0
        note(ev, end, 6.0, GM_CRASH, 127, 9)
        note(ev, end, 0.2, GM_KICK, 127, 9)
        note(ev, end, 0.2, GM_SNARE, 120, 9)
    write_track(path, None, 9, ev)


def build_bass_dbl_midi(path):
    """Doblaje del bajo: las mismas notas (y la misma humanización) una octava
    arriba y con un timbre de sintetizador, para dar presencia en los medios."""
    src = MidiFile(os.path.join(os.path.dirname(path), "bass.mid"))
    for tr in src.tracks:
        for msg in tr:
            if msg.type in ("note_on", "note_off"):
                msg.note += 12
            elif msg.type == "program_change":
                msg.program = 38  # Synth Bass 1
    src.save(path)


def synth_sub(midi_path, tail_s=9):
    """Capa de sub: senoidal en la fundamental de cada nota del bajo (más una
    segunda armónica suave para que se perciba también en parlantes chicos)."""
    notes = [(m.time, m.note, m.type == "note_on" and m.velocity > 0)
             for m in _abs_messages(MidiFile(midi_path))]
    end_s = max(t for t, _, _ in notes) + tail_s
    out = np.zeros(int(end_s * SR))
    active = {}
    for t, nt, on in notes:
        if on:
            active[nt] = t
        elif nt in active:
            t0, t1 = active.pop(nt), t
            i0, i1 = int(t0 * SR), int((t1 + 0.06) * SR)
            x = np.arange(i1 - i0) / SR
            f = 440.0 * 2 ** ((nt - 69) / 12.0)
            wave = np.sin(2 * np.pi * f * x) + 0.25 * np.sin(4 * np.pi * f * x)
            env = np.minimum(1.0, x / 0.008) * np.minimum(1.0, np.maximum(0.0, (t1 + 0.06 - t0 - x)) / 0.06)
            out[i0:i1] += wave * env
    return out


def _abs_messages(mid):
    """Mensajes con tiempo absoluto en segundos (un solo track de tempo fijo)."""
    sec_per_tick = bpm2tempo(BPM) / 1e6 / mid.ticks_per_beat
    t = 0
    for msg in mid.tracks[0]:
        t += msg.time
        if msg.type in ("note_on", "note_off"):
            msg.time = t * sec_per_tick
            yield msg


def build_bass_midi(path):
    """Galope: corchea + dos semicorcheas por tiempo, con octava en el último tiempo."""
    ev = []
    for s, i, n in bar_iter():
        if is_drop(s, i):
            continue
        b0 = n * 4.0
        root = BASS_ROOT[PROGRESSION[n % 4]]
        for beat in range(4):
            top = 12 if beat == 3 and i % 2 == 1 else 0
            if s["bass"] == "gallop":
                note(ev, b0 + beat, 0.45, root, 106, 1)
                note(ev, b0 + beat + 0.5, 0.2, root + top, 88, 1)
                note(ev, b0 + beat + 0.75, 0.2, root + top, 96, 1)
            else:
                note(ev, b0 + beat, 0.45, root, 104, 1)
                note(ev, b0 + beat + 0.5, 0.4, root, 90, 1)
    if SECTIONS[-1].get("ending"):  # golpe final: Mi grave sostenido
        end = sum(x["bars"] for x in SECTIONS) * 4.0
        note(ev, end, 7.0, 28, 127, 1)
        note(ev, end, 7.0, 40, 110, 1)
    write_track(path, 34, 1, ev)


def build_guitar_midi(path):
    """arp: arpegio limpio con acento cada 3 semicorcheas. strum: acordes con distorsión."""
    ev = []
    pattern = [0, 1, 2, 1, 2, 1, 0, 1, 0, 1, 2, 1, 2, 3, 2, 1]
    for s, i, n in bar_iter():
        if is_drop(s, i):
            continue
        b0 = n * 4.0
        ch = PROGRESSION[n % 4]
        if s["guitar"] == "arp":
            tones = [t - 12 for t in ARP[ch]]
            for k, idx in enumerate(pattern):
                note(ev, b0 + k * 0.25, 0.3, tones[idx], 92 if k % 3 == 0 else 64, 2)
        else:
            for k in range(8):
                for p in POWER[ch]:
                    note(ev, b0 + k * 0.5, 0.45, p, 100 if k % 2 == 0 else 84, 2)
    clean = any(s["guitar"] == "arp" for s in SECTIONS)
    if SECTIONS[-1].get("ending"):  # golpe final: acorde de Mi menor abierto
        end = sum(x["bars"] for x in SECTIONS) * 4.0
        for p in (40, 47, 52, 59, 64, 71):
            note(ev, end, 7.0, p, 118, 2)
    write_track(path, 27 if clean else 29, 2, ev)


def build_synth_midi(path):
    """Riff agudo y frío con ritmo sincopado, eco de corchea con puntillo."""
    ev = []
    rhythm = [(0.0, 3, 0.6), (0.75, 2, 0.6), (1.5, 1, 0.4), (2.0, 2, 0.9), (3.0, 3, 0.9)]
    for s, i, n in bar_iter():
        if is_drop(s, i):
            continue
        b0 = n * 4.0
        tones = [t - 12 for t in ARP[PROGRESSION[n % 4]]]
        for pos, idx, dur in rhythm:
            note(ev, b0 + pos, dur, tones[idx], 86, 3)
    if SECTIONS[-1].get("ending"):  # nota aguda larga, el eco la deja sonando
        end = sum(x["bars"] for x in SECTIONS) * 4.0
        note(ev, end, 7.0, 64, 100, 3)
        note(ev, end, 7.0, 71, 80, 3)
    write_track(path, 81, 3, ev)


def build_lead_midi(path):
    """El hook: motivo de 4 compases que sigue los acordes. Mismo ritmo en los
    primeros tres compases y una escalera ascendente en el B que empuja a repetir."""
    ev = []
    cell = [(0.0, 2, 0.5), (0.5, 2, 0.5), (1.0, 3, 1.0), (2.0, 2, 0.5),
            (2.5, 1, 0.5), (3.0, 2, 1.0)]
    climb = [(0.0, 2, 0.5), (0.5, 3, 0.5), (1.0, 2, 0.5), (1.5, 1, 0.5),
             (2.0, 0, 0.5), (2.5, 1, 0.5), (3.0, 2, 0.5), (3.5, 3, 0.5)]
    for s, i, n in bar_iter():
        if is_drop(s, i):
            continue
        b0 = n * 4.0
        ch = PROGRESSION[n % 4]
        tones = list(ARP[ch])  # una octava más grave: mood oscuro
        for pos, idx, dur in (climb if ch == "B" else cell):
            if n in (40, 108) and pos < 2.0:
                continue  # silencio de dos tiempos: el hook se hace esperar
            tone = tones[idx]
            if ch != "B" and pos == 1.0:
                tone = tones[1] + 12  # salto característico (décima) en la nota larga
            note(ev, b0 + pos, dur, tone, 98 if pos in (0.0, 1.0) else 84, 5)
    if SECTIONS[-1].get("ending"):
        end = sum(x["bars"] for x in SECTIONS) * 4.0
        note(ev, end, 7.0, 76, 105, 5)
        note(ev, end, 7.0, 71, 95, 5)
    write_track(path, 80, 5, ev)


def build_whistle_midi(path):
    """Silbido western: una frase de 4 compases (un acorde por compás) con
    notas largas, como la voz solitaria de un spaghetti western."""
    ev = []
    phrase = {
        "Em": [(0.0, 79, 0.25, 70), (0.5, 83, 3.3, 84)],
        "C":  [(0.0, 84, 2.0, 82), (2.0, 79, 1.9, 76)],
        "Am": [(0.0, 81, 1.5, 82), (1.5, 76, 0.5, 70), (2.0, 81, 1.9, 80)],
        "B":  [(0.0, 78, 1.0, 82), (1.0, 75, 1.0, 76), (2.0, 71, 1.9, 84)],
    }
    for s, i, n in bar_iter():
        if is_drop(s, i):
            continue
        for pos, p, dur, vel in phrase[PROGRESSION[n % 4]]:
            note(ev, n * 4.0 + pos, dur, p, vel, 6)
    if SECTIONS[-1].get("ending"):  # cita el inicio del hook (Si, Si, Mi) en la cola
        end = sum(x["bars"] for x in SECTIONS) * 4.0
        note(ev, end + 1.5, 0.5, 83, 90, 6)
        note(ev, end + 2.0, 0.5, 83, 90, 6)
        note(ev, end + 2.5, 3.0, 88, 100, 6)
    write_track(path, 78, 6, ev)


def build_pad_midi(path):
    ev = []
    for s, i, n in bar_iter():
        if is_drop(s, i):
            continue
        b0 = n * 4.0
        for p in ARP[PROGRESSION[n % 4]][:3]:
            note(ev, b0, 3.9, p - 24, 52, 4)
    if SECTIONS[-1].get("ending"):
        end = sum(x["bars"] for x in SECTIONS) * 4.0
        for p in (40, 52, 55, 59):
            note(ev, end, 7.5, p, 70, 4)
    write_track(path, 89, 4, ev)


def render_fluidsynth(fluidsynth, soundfont, midi_p, wav_p):
    r = subprocess.run([
        fluidsynth, "-ni", soundfont, midi_p,
        "-F", wav_p, "-r", str(SR), "-g", "1.0", "-R", "0", "-C", "0"
    ], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.isfile(wav_p):
        sys.exit(f"FluidSynth falló al renderizar {os.path.basename(midi_p)}:\n{r.stderr or r.stdout}")


def distort(samples, drive=4.0):
    return np.tanh(samples * drive) / np.tanh(drive)


def chorus(signal, rate=0.6, depth_ms=5.0, delay_ms=20.0, mix=0.5, phase=0.0):
    n = len(signal)
    t = np.arange(n) / SR
    delays = (delay_ms + depth_ms * np.sin(2 * np.pi * rate * t + phase)) * SR / 1000.0
    idx = np.arange(n) - delays
    valid = idx >= 0
    delayed = np.zeros(n)
    delayed[valid] = np.interp(idx[valid], np.arange(n), signal)
    return signal * (1.0 - mix) + delayed * mix


def load_wav(p):
    _, d = wavfile.read(p)
    if d.ndim > 1:
        d = d.mean(axis=1)
    return d.astype(np.float32) / 32768.0


def pad_to(a, n):
    return np.pad(a, (0, max(0, n - len(a))))[:n]




def echo(signal, beats=0.75, feedback=0.38, taps=4, mix=0.45):
    """Eco sincronizado al tempo (corchea con puntillo)."""
    d = int(beats * 60.0 / BPM * SR)
    out = signal.copy()
    gain = mix
    for t in range(1, taps + 1):
        out[t * d:] += signal[:len(signal) - t * d] * gain
        gain *= feedback
    return out


def reverb(signal, seconds=1.8, mix=0.28):
    rng = np.random.default_rng(7)
    n = int(seconds * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (0.35 * SR))
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = fftconvolve(signal, ir)[:len(signal)]
    return signal * (1 - mix) + wet * mix


def to_stereo(signal):
    return np.stack([signal, signal], axis=1)


def chorus_st(st, **kw):
    """Chorus con el LFO en contrafase entre canales: ensancha la imagen."""
    return np.stack([chorus(st[:, 0], phase=0.0, **kw),
                     chorus(st[:, 1], phase=np.pi, **kw)], axis=1)


def pingpong(st, beats=0.75, feedback=0.38, taps=4, mix=0.45):
    """Eco sincronizado al tempo que rebota entre izquierda y derecha."""
    d = int(beats * 60.0 / BPM * SR)
    mono = st.mean(axis=1)
    out = st.copy()
    gain = mix
    for t in range(1, taps + 1):
        out[t * d:, t % 2] += mono[:len(mono) - t * d] * gain
        gain *= feedback
    return out


def reverb_st(st, seconds=1.8, mix=0.28):
    """Reverb con una respuesta distinta por canal (colas descorrelacionadas)."""
    n = int(seconds * SR)
    out = np.empty_like(st)
    for ch, seed in enumerate((7, 11)):
        rng = np.random.default_rng(seed)
        ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (0.35 * SR))
        ir /= np.sqrt(np.sum(ir ** 2))
        wet = fftconvolve(st[:, ch], ir)[:len(st)]
        out[:, ch] = st[:, ch] * (1 - mix) + wet * mix
    return out


# ---------- ESCENA ESPACIAL (3D) ----------
# Cada voz recibe una trayectoria por compás: azimut (-1 izquierda, 1 derecha),
# profundidad (0 adelante, 1 atrás) y elevación (-1 abajo, 1 arriba). Son los
# mismos sonidos de siempre, solo ubicados y movidos en el espacio. Batería,
# bajo y sub quedan fijos al frente como ancla.
BAR_S = 4 * 60.0 / BPM


def _orbit(b, period, phase=0.0):
    """Vuelta completa alrededor del oyente: adelante, derecha, atrás, izquierda."""
    th = 2 * np.pi * b / period + phase
    return np.sin(th), (1 - np.cos(th)) / 2


def _scene_guitar(b):
    return -0.75 + 0.10 * np.sin(2 * np.pi * b / 16), 0.15, 0.0


def _scene_synth(b):
    return 0.75 + 0.10 * np.sin(2 * np.pi * b / 12 + 1.0), 0.25, 0.0


def _scene_lead(b):
    # el hook llega desde el fondo en la intro y después se queda adelante, arriba
    depth = 0.1 + 0.8 * np.clip(1 - b / 8.0, 0, 1)
    return 0.35 * np.sin(2 * np.pi * b / 8), depth, 0.35


def _scene_whistle(b):
    az, depth = _orbit(b, 8.0)
    return 0.9 * az, 0.1 + 0.75 * depth, 0.5


def _scene_pad(b):
    return 0.5 * np.sin(2 * np.pi * b / 24), 0.55, 0.35


def _scene_bass_dbl(b):
    return 0.3 * np.sin(2 * np.pi * b / 20 + 2.0), 0.2, -0.3


SCENE = {"guitar": _scene_guitar, "synth": _scene_synth, "lead": _scene_lead,
         "whistle": _scene_whistle, "pad": _scene_pad, "bass_dbl": _scene_bass_dbl}


def spatialize(st, fn):
    """Ubica una señal estéreo en el espacio siguiendo las curvas de `fn`.
    Diferencia de tiempo entre oídos (ITD) y de nivel, oscurecimiento y atenuación
    hacia atrás, y brillo/oscuridad para arriba/abajo. Aproximación sin HRTF."""
    n = len(st)
    kr = 200  # las curvas se calculan a 200 Hz y se interpolan por muestra
    tb = np.arange(0, n / SR, 1.0 / kr)
    vals = fn(tb / BAR_S)
    t_all = np.arange(n) / SR
    az, depth, elev = (np.interp(t_all, tb, np.broadcast_to(np.asarray(v, float), tb.shape))
                       for v in vals)
    mid = (st[:, 0] + st[:, 1]) / 2
    side = (st[:, 0] - st[:, 1]) / 2
    lp = sosfilt(butter(2, 2000, "lowpass", fs=SR, output="sos"), mid)
    hp = sosfilt(butter(2, 4000, "highpass", fs=SR, output="sos"), mid)
    m = (mid * (1 - depth) + lp * depth) * (1 - 0.3 * depth)       # atrás: más oscuro y bajo
    m = m + 0.6 * np.maximum(elev, 0) * hp - 0.5 * np.maximum(-elev, 0) * (m - lp)
    ang = (az + 1) * np.pi / 4                                    # ley de potencia constante
    idx = np.arange(n)
    itd = 0.0007 * SR                                             # ~0.7 ms entre oídos
    m_l = np.interp(idx - np.maximum(az, 0) * itd, idx, m)
    m_r = np.interp(idx - np.maximum(-az, 0) * itd, idx, m)
    sw = 0.6                                                      # conserva la amplitud del chorus
    return np.stack([m_l * np.cos(ang) * np.sqrt(2) + side * sw,
                     m_r * np.sin(ang) * np.sqrt(2) - side * sw], axis=1)


def main():
    fluidsynth = find_fluidsynth()
    soundfont = find_soundfont()

    version_dir, v = next_version_dir()
    midi_dir = os.path.join(version_dir, "midi")
    stems_dir = os.path.join(version_dir, "stems")
    os.makedirs(midi_dir, exist_ok=True)
    os.makedirs(stems_dir, exist_ok=True)

    print(f"Generando Mirror Cry v{v} ({BPM} BPM, E menor, cold wave)...")
    print(f"  FluidSynth: {fluidsynth}")
    print(f"  SoundFont : {soundfont}")

    builders = {"drums": build_drums_midi, "bass": build_bass_midi,
                "bass_dbl": build_bass_dbl_midi, "bass_sub": None,
                "guitar": build_guitar_midi, "synth": build_synth_midi,
                "lead": build_lead_midi, "whistle": build_whistle_midi, "pad": build_pad_midi}
    audio = {}
    for name, build in builders.items():
        mid_p = os.path.join(midi_dir, f"{name}.mid")
        if name == "bass_sub":
            sig = synth_sub(os.path.join(midi_dir, "bass.mid"))
        else:
            build(mid_p)
            raw_p = os.path.join(midi_dir, f"_{name}_raw.wav")
            render_fluidsynth(fluidsynth, soundfont, mid_p, raw_p)
            sig = load_wav(raw_p)
            os.remove(raw_p)
            sig = np.concatenate([sig, np.zeros(int(9 * SR))])  # espacio para la cola final

        if name == "bass":
            sig = to_stereo(distort(sig, drive=4.0))  # bajo centrado
        elif name == "bass_dbl":
            # medios saturados, filtrados y abiertos en estéreo: el grave queda
            # centrado y el bajo "llena" los lados
            sig = sosfilt(butter(2, 140, "highpass", fs=SR, output="sos"), distort(sig, drive=6.0))
            sig = reverb_st(chorus_st(to_stereo(sig), rate=0.35, depth_ms=7.0, mix=0.5),
                            seconds=1.2, mix=0.15)
        elif name == "bass_sub":
            sig = to_stereo(sig)
        elif name == "drums":
            sig = to_stereo(sig)
        elif name == "guitar":
            if any(s["guitar"] == "strum" for s in SECTIONS):
                sig = distort(sig, drive=2.2)
            trem = 1.0 - 0.18 * (0.5 + 0.5 * np.sin(2 * np.pi * 5.2 * np.arange(len(sig)) / SR))
            sig = pingpong(chorus_st(to_stereo(sig * trem), rate=0.8, depth_ms=6.0, mix=0.5))
            sig = reverb_st(sig, mix=0.2)
        elif name == "synth":
            sig = reverb_st(pingpong(to_stereo(distort(sig, drive=1.8)), mix=0.5), mix=0.3)
        elif name == "lead":
            sig = reverb_st(pingpong(chorus_st(to_stereo(distort(sig, drive=1.6)),
                                               rate=0.5, mix=0.3), mix=0.4), mix=0.25)
        elif name == "whistle":
            sig = reverb_st(pingpong(chorus_st(to_stereo(sig), rate=0.4, depth_ms=3.0, mix=0.25),
                                     beats=1.5, mix=0.5), seconds=2.8, mix=0.4)
        elif name == "pad":
            sig = reverb_st(chorus_st(to_stereo(sig), rate=0.3, depth_ms=8.0, mix=0.4), seconds=2.5, mix=0.4)

        peak = np.max(np.abs(sig))
        sig = sig / peak if peak > 0 else sig
        sig = sig * envelope(name, len(sig))[:, None]
        audio[name] = spatialize(sig, SCENE[name]) if name in SCENE else sig

    length = max(len(s) for s in audio.values())
    mix = np.zeros((length, 2))
    for name, sig in audio.items():
        stem = np.pad(sig, ((0, max(0, length - len(sig))), (0, 0)))[:length] * GAINS[name]
        wavfile.write(os.path.join(stems_dir, f"{name}.wav"), SR,
                      (np.clip(stem, -1.0, 1.0) * 32767).astype(np.int16))
        pan = PAN[name]
        mix[:, 0] += stem[:, 0] * np.cos(pan * np.pi / 2)
        mix[:, 1] += stem[:, 1] * np.sin(pan * np.pi / 2)

    # recorta el silencio sobrante y cierra con un fundido largo de la cola
    loud = np.where(np.max(np.abs(mix), axis=1) > 0.002)[0]
    length = min(length, loud[-1] + SR)
    mix = mix[:length]
    tail = int(2.0 * SR)
    mix[-tail:] *= np.linspace(1.0, 0.0, tail)[:, None] ** 2

    mix = np.tanh(mix * 0.9)  # limitador suave
    m_peak = np.max(np.abs(mix))
    if m_peak > 0.95:
        mix = mix * (0.95 / m_peak)

    out = os.path.join(version_dir, "mix.wav")
    wavfile.write(out, SR, (np.clip(mix, -1.0, 1.0) * 32767).astype(np.int16))
    print(f"Listo: {out} ({length / SR:.1f}s)")


if __name__ == "__main__":
    main()
