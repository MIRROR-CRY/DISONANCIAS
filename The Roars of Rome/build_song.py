#!/usr/bin/env python3
"""The Roars of Rome: base instrumental etérea (gotas flotando).

Propuesta v1, a propósito con pocos sonidos para ir armando la idea de a poco.
3/4 a 60 BPM, La menor (Am - F - C - G), 44 compases (~2:12).

Sintesis con numpy puro (sin FluidSynth ni SoundFont): gotas, pad, sub y timbal.
Estructura y curvas de presencia (LEVELS) siguen el esquema de Mirror Cry.

Uso:  python build_song.py                    v1: solo etereo, 60 BPM
      python build_song.py --cold --bpm 100   v2: suma capa coldwave en 3/4
      python build_song.py --waltz --bpm 80   v3: sin bateria; marimba + sintetizador
                                              de pulso (negra, negra, silencio)
(necesita numpy; ffmpeg opcional para el mp3)
"""
import argparse
import os
import shutil
import subprocess
import wave

import numpy as np

_ap = argparse.ArgumentParser()
_ap.add_argument("--bpm", type=int, default=60)
_ap.add_argument("--cold", action="store_true",
                 help="agrega la capa coldwave (bombo, caja, hi-hat, bajo galopante, arpegio)")
_ap.add_argument("--waltz", action="store_true",
                 help="sin bateria: marimba en 3/4 + sintetizador negra, negra, silencio")
_ap.add_argument("--piano", action="store_true",
                 help="agrega la melodia de piano de 9 notas (Mi Re Si, Mi Re Do Sol Fa Mi)")
_ap.add_argument("--rhythm", choices=["dotted", "one"], default="dotted",
                 help="con --piano: duracion de las 6 ultimas notas (negra con puntillo o una negra)")
_ap.add_argument("--sustain", type=float, default=1.0,
                 help="con --piano: factor de pedal/sustain (1 = seco, 3 = notas que se funden)")
_ap.add_argument("--long", action="store_true",
                 help="version larga (~3:00, 80 compases) con las partes de Mirror Cry; requiere --waltz")
_ap.add_argument("--hook", choices=["a", "b", "c", "abc"], default=None,
                 help="con --long, pruebas de hook: a = gotas con mas presencia y nivel inicial mas alto; "
                      "b = a + intro de 4 compases; c = a + motivo de piano desde el compas 0; "
                      "abc = las tres ideas juntas, con un crescendo en el puente para que fluya")
_ap.add_argument("--center", choices=["a", "e"], default="a",
                 help="centro tonal: a = La menor (Am F C G); e = Mi frigio (Em F G Am | Em F Em Em)")
ARGS = _ap.parse_args()

SR = 44100
BPM = ARGS.bpm
COLD = ARGS.cold
WALTZ = ARGS.waltz
PIANO = ARGS.piano
LONG = ARGS.long
HOOK = ARGS.hook
if HOOK and not ARGS.long:
    _ap.error("--hook requiere --long")
if LONG and not WALTZ:
    _ap.error("--long requiere --waltz")
BEATS = 3                      # compas de 3/4
BAR_S = BEATS * 60.0 / BPM     # 3 s por compas
EIGHTH = 60.0 / BPM / 2        # 0.5 s; el patron de gotas son 6 corcheas por compas
SEED = 7

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSIONS_DIR = os.path.join(PROJECT_DIR, "versions")

# Progresion: un acorde por compas, ciclo de 4 compases.
PROGRESSION = ["Am", "F", "C", "G"]
if ARGS.center == "e":
    # Mi frigio (E F G A B C D): i, bII, bIII, iv. En el compas 7 vuelve al Em
    # justo cuando la melodia resuelve Fa -> Mi.
    PROGRESSION = ["Em", "F", "G", "Am", "Em", "F", "Em", "Em"]
# raiz, tercera, quinta, octava (notas MIDI) para las gotas
DROP_NOTES = {
    "Am": [69, 72, 76, 81],
    "F":  [65, 69, 72, 77],
    "C":  [64, 67, 72, 76],
    "G":  [62, 67, 71, 74],
    "Em": [64, 67, 71, 76],
}
PAD_NOTES = {"Am": [57, 60, 64], "F": [53, 57, 60], "C": [55, 60, 64], "G": [50, 55, 59], "Em": [52, 55, 59]}
BASS_ROOT = {"Am": 33, "F": 29, "C": 36, "G": 31, "Em": 28}

# Patron de la idea: pam, pam, pa, pam, pam, pam. El "pa" (indice 2) es mas
# corto y suave. Cada numero indica a que nota del acorde cae la gota.
PATTERN_DEGREE = [2, 1, 0, 1, 2, 3]
PATTERN_VEL = [1.0, 0.85, 0.45, 0.9, 0.8, 0.95]
PATTERN_LEN = [1.0, 1.0, 0.45, 1.0, 1.0, 1.0]

# Estructura: (nombre, compases)
SECTIONS = [
    ("intro", 8),       # solo gotas; el pad asoma al final
    ("verse1", 8),      # gotas + pad
    ("verse2", 8),      # + sub
    ("interlude", 4),   # el pad se va; queda el eco de las gotas
    ("chorus", 8),      # todo: timbal, gotas altas, pad abierto
    ("outro", 8),       # se desvanece hasta una sola gota
]
if LONG:
    # Mismas partes que Mirror Cry: intro, versos, interludio, puente con el compas
    # final en silencio, dos coros, verso 3 despues del coro, outro. 80 compases a
    # 80 BPM en 3/4 = 3:00.
    SECTIONS = [
        ("intro", 8),        # gotas + pulso + pad (el autor pone aqui su voz)
        ("verse1", 8),
        ("verse2", 8),
        ("interlude", 8),    # la melodia de piano sola con el pulso
        ("bridge", 8),       # se vacia; el ultimo compas queda en silencio total
        ("chorus1", 16),
        ("verse3", 8),
        ("chorus2", 8),
        ("outro", 8),        # todo se desvanece hasta una gota
    ]
TOTAL_BARS = sum(b for _, b in SECTIONS)
SECTION_STARTS = [sum(b for _, b in SECTIONS[:i]) for i in range(len(SECTIONS))]

# Presencia por instrumento: (compas, nivel), interpolado linealmente.
LEVELS = {
    "drops":   [(0, 0.7), (8, 1.0), (28, 0.8), (36, 1.0), (40, 0.6), (43, 0.2), (44, 0.0)],
    "drops_hi": [(0, 0), (28, 0), (30, 0.8), (36, 0.8), (38, 0), (44, 0)],
    "pad":     [(0, 0), (5, 0), (8, 0.7), (24, 0.8), (27, 0), (28, 0.3), (32, 1.0),
                (36, 1.0), (40, 0.6), (44, 0.0)],
    "sub":     [(0, 0), (16, 0), (18, 0.8), (27, 0.8), (28, 0), (32, 0.8),
                (36, 0.8), (40, 0), (44, 0)],
    "timbal":  [(0, 0), (31.9, 0), (32, 1.0), (36, 1.0), (36.1, 0), (44, 0)],
}
if COLD:
    LEVELS.update({
        "kick":  [(0, 0), (27, 0), (28, 1), (36, 1), (40, 0), (44, 0)],
        "snare": [(0, 0), (27, 0), (28, 1), (36, 1), (40, 0), (44, 0)],
        "bass_cold": [(0, 0), (27, 0), (28, 1), (36, 1), (40, 0), (44, 0)],
        "hat":   [(0, 0), (16, 0), (18, 0.4), (27, 0.4), (28, 1), (36, 1), (40, 0), (44, 0)],
        "arp":   [(0, 0), (20, 0), (22, 0.5), (28, 0.8), (36, 0.8), (40, 0), (44, 0)],
    })
if WALTZ:
    LEVELS.update({
        # el sintetizador acompana toda la cancion
        "pulse":   [(0, 1.0), (40, 1.0), (44, 0.0)],
        "marimba": [(0, 0), (6, 0), (8, 0.5), (24, 0.5), (28, 1.0), (36, 1.0),
                    (40, 0.4), (44, 0)],
        "bass_cold": [(0, 0), (27, 0), (28, 1), (36, 1), (40, 0), (44, 0)],
        "arp":   [(0, 0), (20, 0), (22, 0.5), (28, 0.8), (36, 0.8), (40, 0), (44, 0)],
    })
if PIANO:
    LEVELS["piano"] = [(0, 0), (7.9, 0), (8, 0.9), (36, 0.9), (40, 0.5), (44, 0)]
if LONG:
    # inicio de cada seccion: intro 0, v1 8, v2 16, interludio 24, puente 32,
    # coro1 40, v3 56, coro2 64, outro 72, fin 80
    LEVELS = {
        "drops":   [(0, 0.85), (8, 1.0), (32, 1.0), (38, 0.6), (40, 1.0), (72, 1.0), (79, 0.3), (80, 0.0)],
        "drops_hi": [(0, 0), (39.9, 0), (40, 0.8), (55.9, 0.8), (56, 0), (63.9, 0), (64, 0.8),
                     (71.9, 0.8), (72, 0), (80, 0)],
        "pad":     [(0, 0), (4, 0), (8, 0.7), (24, 0.9), (32, 0.4), (40, 1.0), (56, 0.7),
                    (64, 1.0), (72, 1.0), (80, 0.0)],
        "sub":     [(0, 0), (16, 0), (18, 0.8), (23.9, 0.8), (24, 0), (32, 0), (40, 0.9), (56, 0.5),
                    (64, 0.9), (72, 0.6), (80, 0)],
        "timbal":  [(0, 0), (40, 0), (40.1, 1.0), (55.9, 1.0), (56, 0), (64, 0), (64.1, 1.0),
                    (71.9, 1.0), (72, 0), (80, 0)],
        "pulse":   [(0, 1.0), (79, 1.0), (80, 0.0)],
        "marimba": [(0, 0), (6, 0), (8, 0.5), (16, 0.6), (24, 0.5), (32, 0.3), (40, 1.0),
                    (56, 0.5), (64, 1.0), (72, 0.5), (80, 0)],
        "bass_cold": [(0, 0), (39.9, 0), (40, 1.0), (55.9, 1.0), (56, 0), (63.9, 0), (64, 1.0),
                      (71.9, 1.0), (72, 0), (80, 0)],
        "arp":     [(0, 0), (16, 0), (18, 0.5), (24, 0.5), (32, 0.3), (40, 0.8), (56, 0.4),
                    (64, 0.8), (72, 0.4), (80, 0)],
        # piano: fantasma bajo los versos, pleno en interludio y coros (como el hook de Mirror Cry)
        "piano":   [(0, 0), (7.9, 0), (8, 0.35), (23.9, 0.35), (24, 0.7), (31.9, 0.7), (32, 0),
                    (39.9, 0), (40, 1.0), (55.9, 1.0), (56, 0.35), (63.9, 0.35), (64, 1.0),
                    (71.9, 1.0), (72, 0.7), (80, 0)],
    }
    GATES = [(39.0, 40.0)]     # compas de silencio total antes del coro
    if HOOK:
        # A: gotas con mas presencia y nivel inicial mas alto; el pad y el pulso suben antes
        LEVELS["drops"] = [(0, 1.5), (6, 1.2)] + LEVELS["drops"][1:]
        LEVELS["pad"] = [(0, 0), (1, 0), (3, 0.6), (8, 0.7)] + LEVELS["pad"][3:]
        LEVELS["pulse"] = [(0, 1.3), (8, 1.0), (79, 1.0), (80, 0.0)]
        if HOOK == "c":
            # C: el motivo de piano (Mi, Re, Si...) suena desde el compas 0
            LEVELS["piano"] = [(0, 0.9), (7.9, 0.9)] + LEVELS["piano"][2:]
        if HOOK == "abc":
            # A + B + C. B recorta los 4 primeros compases, asi que el motivo de piano
            # empieza en el compas 4 (el primer compas que se escucha). Termina en el
            # compas 9, por eso no hay frase fantasma en el verso 1.
            LEVELS["piano"] = [(0, 0), (3.9, 0), (4, 0.7), (8.9, 0.7), (9, 0.35)] + LEVELS["piano"][3:]
            # Para que fluya: crescendo en el puente (pad, marimba, gotas agudas y
            # timbal crecen hasta el compas de silencio) antes de entrar al coro.
            LEVELS["pad"] = [(0, 0), (1, 0), (3, 0.6), (8, 0.7), (24, 0.9), (32, 0.4),
                             (38.9, 1.0), (40, 1.0), (56, 0.7), (64, 1.0), (72, 1.0), (80, 0)]
            LEVELS["drops"] = [(0, 1.3), (6, 1.1), (8, 1.0)] + LEVELS["drops"][2:]
            LEVELS["arp"] = [(0, 0), (8, 0), (10, 0.4), (24, 0.6), (32, 0.4), (40, 0.8), (56, 0.4),
                             (64, 0.8), (72, 0.4), (80, 0)]
            LEVELS["sub"] = [(0, 0), (16, 0), (18, 0.8), (23.9, 0.8), (24, 0.6), (31.9, 0.6), (32, 0),
                             (40, 0.9), (56, 0.5), (64, 0.9), (72, 0.6), (80, 0)]
            LEVELS["marimba"] = [(0, 0.3), (8, 0.65), (16, 0.7), (24, 0.6), (32, 0.3), (38.9, 0.9),
                                 (40, 1.0), (56, 0.5), (64, 1.0), (72, 0.5), (80, 0)]
            LEVELS["drops_hi"] = [(0, 0), (35, 0), (38.9, 0.8), (40, 0.8), (55.9, 0.8), (56, 0),
                                  (63.9, 0), (64, 0.8), (71.9, 0.8), (72, 0), (80, 0)]
            LEVELS["timbal"] = [(0, 0), (36, 0), (38.9, 0.8), (40, 1.0), (55.9, 1.0), (56, 0),
                                (64, 0), (64.1, 1.0), (71.9, 1.0), (72, 0), (80, 0)]
else:
    GATES = []
GAINS = {"piano": 0.45, "pulse": 0.24, "marimba": 0.5, "kick": 0.7, "snare": 0.35, "bass_cold": 0.4, "hat": 0.16, "arp": 0.3,
         "drops": 0.55, "drops_hi": 0.22, "pad": 0.30, "sub": 0.40, "timbal": 0.55}
PAN = {"drops": 0.0, "drops_hi": 0.0, "pad": 0.0, "sub": 0.0, "timbal": 0.0}


def midi_hz(n):
    return 440.0 * 2 ** ((n - 69) / 12.0)


def level_curve(name, n_samples):
    pts = LEVELS[name]
    xs = np.array([p[0] for p in pts]) * BAR_S * SR
    ys = np.array([p[1] for p in pts])
    return np.interp(np.arange(n_samples), xs, ys)


def chord_at_bar(bar):
    """La progresion reinicia al empezar cada seccion (asi cada frase empieza en el acorde 1)."""
    start = 0
    for b in SECTION_STARTS:
        if b <= bar:
            start = b
    return PROGRESSION[(bar - start) % len(PROGRESSION)]


def bar_start(bar):
    return int(bar * BAR_S * SR)


# ---------------------------------------------------------------- sintesis

def drop(freq, vel, length_scale, rng, hi=False):
    """Una gota: seno con glissando ascendente corto y caida exponencial."""
    dur = (0.28 if hi else 0.6) * length_scale + 0.05
    t = np.arange(int(dur * SR)) / SR
    glide = 1.0 + 0.32 * np.exp(-t / 0.035)          # el tono sube hacia la nota
    freq = freq * (1 + rng.uniform(-0.003, 0.003))   # leve variacion natural
    phase = 2 * np.pi * np.cumsum(freq * glide) / SR
    tau = (0.07 if hi else 0.14) * (0.5 + 0.5 * length_scale)
    env = np.exp(-t / tau)
    env *= np.minimum(1.0, t / 0.002)                # ataque suave, sin click
    body = np.sin(phase) + 0.18 * np.sin(2 * phase + 0.3)
    if HOOK:   # parcial agudo y corto: gota mas cristalina, mas reconocible
        body = body + 0.22 * np.sin(3.01 * phase) * np.exp(-t / 0.05)
    return body * env * vel


def render_drops(hi=False):
    rng = np.random.default_rng(SEED + (1 if hi else 0))
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros((n, 2))
    for bar in range(TOTAL_BARS):
        notes = DROP_NOTES[chord_at_bar(bar)]
        for i in range(6):
            degree = PATTERN_DEGREE[i]
            pitch = notes[degree] + (12 if hi else 0)
            t0 = bar * BAR_S + i * EIGHTH + rng.uniform(-0.006, 0.006)
            vel = PATTERN_VEL[i] * rng.uniform(0.9, 1.0)
            g = drop(midi_hz(pitch), vel, PATTERN_LEN[i], rng, hi)
            s = max(0, int(t0 * SR))
            seg = g[: n - s]
            # cada gota cae en un punto distinto del campo estereo
            pos = rng.uniform(-0.7, 0.7)
            out[s:s + len(seg), 0] += seg * np.sqrt((1 - pos) / 2)
            out[s:s + len(seg), 1] += seg * np.sqrt((1 + pos) / 2)
    return out


def render_pad():
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros((n, 2))
    t_full = np.arange(n) / SR
    fade = int(1.2 * SR)
    for bar in range(TOTAL_BARS):
        s = bar_start(bar)
        e = min(n, bar_start(bar + 1) + fade)
        t = t_full[s:e]
        env = np.ones(len(t))
        a = min(fade, len(t))
        env[:a] *= np.linspace(0, 1, a) ** 2
        env[-a:] *= np.linspace(1, 0, a) ** 2
        for k, note in enumerate(PAD_NOTES[chord_at_bar(bar)]):
            for det, ch in ((-0.15, 0), (0.15, 1)):   # leve desafinado L/R: ancho
                f = midi_hz(note) * 2 ** (det / 12.0)
                wave_ = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t)
                out[s:e, ch] += wave_ * env * 0.3
    return out


def render_sub():
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros(n)
    t_full = np.arange(n) / SR
    fade = int(0.8 * SR)
    for bar in range(TOTAL_BARS):
        s = bar_start(bar)
        e = min(n, bar_start(bar + 1) + fade)
        t = t_full[s:e]
        env = np.ones(len(t))
        a = min(fade, len(t))
        env[:a] *= np.linspace(0, 1, a)
        env[-a:] *= np.linspace(1, 0, a)
        f = midi_hz(BASS_ROOT[chord_at_bar(bar)])
        out[s:e] += np.sin(2 * np.pi * f * t) * env
    return np.stack([out, out], axis=1)


def render_timbal():
    """Timbal grave y suave en el tiempo 1 de cada compas."""
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros(n)
    t = np.arange(int(1.4 * SR)) / SR
    for bar in range(TOTAL_BARS):
        f0 = midi_hz(BASS_ROOT[chord_at_bar(bar)] + 12)
        sweep = 1.0 + 0.6 * np.exp(-t / 0.05)
        phase = 2 * np.pi * np.cumsum(f0 * sweep) / SR
        hit = np.sin(phase) * np.exp(-t / 0.35) * np.minimum(1.0, t / 0.004)
        s = bar_start(bar)
        seg = hit[: n - s]
        out[s:s + len(seg)] += seg
    return np.stack([out, out], axis=1)


# ----------------------------------------------- capa coldwave en 3/4 (--cold)

def _stereo(x):
    return np.stack([x, x], axis=1)


def render_kick():
    """Bombo en el tiempo 1 de cada compas (el 'boom' del vals)."""
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros(n)
    t = np.arange(int(0.35 * SR)) / SR
    phase = 2 * np.pi * np.cumsum(45 + 90 * np.exp(-t / 0.04)) / SR
    hit = np.sin(phase) * np.exp(-t / 0.12) * np.minimum(1.0, t / 0.002)
    for bar in range(TOTAL_BARS):
        s = bar_start(bar)
        out[s:s + len(hit)] += hit[: n - s]
    return _stereo(out)


def render_snare():
    """Caja seca en los tiempos 2 y 3 (el 'chick chick')."""
    rng = np.random.default_rng(SEED + 11)
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros(n)
    t = np.arange(int(0.18 * SR)) / SR
    for bar in range(TOTAL_BARS):
        for beat, vel in ((1, 0.8), (2, 1.0)):
            noise = rng.standard_normal(len(t))
            tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.03)
            hit = (noise * 0.6 + tone) * np.exp(-t / 0.05) * vel
            s = bar_start(bar) + int(beat * 60.0 / BPM * SR)
            seg = hit[: n - s]
            out[s:s + len(seg)] += seg
    return _stereo(out)


def render_hat():
    """Hi-hat en las 6 corcheas del compas, acentuando el tiempo 1."""
    rng = np.random.default_rng(SEED + 12)
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros(n)
    t = np.arange(int(0.05 * SR)) / SR
    for bar in range(TOTAL_BARS):
        for i in range(6):
            noise = np.diff(rng.standard_normal(len(t) + 1))   # pasa-altos simple
            vel = 1.0 if i == 0 else (0.45 if i % 2 == 0 else 0.7)
            hit = noise * np.exp(-t / 0.012) * vel
            s = bar_start(bar) + int(i * EIGHTH * SR)
            seg = hit[: n - s]
            out[s:s + len(seg)] += seg
    return _stereo(out)


def render_bass_cold():
    """Bajo galopante: la raiz en cada corchea, saturado y con el 1 acentuado."""
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros(n)
    L = int(EIGHTH * 0.9 * SR)
    t = np.arange(L) / SR
    for bar in range(TOTAL_BARS):
        f = midi_hz(BASS_ROOT[chord_at_bar(bar)] + 12)
        env = np.exp(-t / 0.25) * np.minimum(1.0, t / 0.004)
        tone = np.tanh(3.0 * (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2 * f * t)))
        for i in range(6):
            s = bar_start(bar) + int(i * EIGHTH * SR)
            seg = (tone * env * (1.0 if i == 0 else 0.7))[: n - s]
            out[s:s + len(seg)] += seg
    return _stereo(out)


def render_arp():
    """Arpegio frio de 6 corcheas por compas, pulsado (sin sustain)."""
    rng = np.random.default_rng(SEED + 13)
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros((n, 2))
    L = int(0.5 * SR)
    t = np.arange(L) / SR
    order = [0, 1, 2, 1, 2, 1]
    for bar in range(TOTAL_BARS):
        notes = DROP_NOTES[chord_at_bar(bar)]
        for i in range(6):
            f = midi_hz(notes[order[i]] - 12)
            pluck = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2 * f * t)
                     + 0.25 * np.sin(2 * np.pi * 3 * f * t)) * np.exp(-t / 0.12)
            s = bar_start(bar) + int(i * EIGHTH * SR)
            seg = pluck[: n - s]
            pan = -0.5 if i % 2 == 0 else 0.5
            out[s:s + len(seg), 0] += seg * np.sqrt((1 - pan) / 2)
            out[s:s + len(seg), 1] += seg * np.sqrt((1 + pan) / 2)
    return out


# ------------------------------------- vals sin bateria (--waltz)

def _marimba_hit(freq, length=0.5):
    """Marimba: madera con ataque corto y un parcial agudo (~4x) que cae rapido."""
    t = np.arange(int(length * SR)) / SR
    body = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.22)
    over = 0.35 * np.sin(2 * np.pi * 4 * freq * t) * np.exp(-t / 0.04)
    return (body + over) * np.minimum(1.0, t / 0.001)


def render_marimba():
    """Acompanamiento de vals: raiz grave en el 1 y acorde mas agudo en 2 y 3."""
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros((n, 2))
    beat = 60.0 / BPM
    for bar in range(TOTAL_BARS):
        ch = chord_at_bar(bar)
        notes = DROP_NOTES[ch]
        plan = [(0, BASS_ROOT[ch] + 24, 1.0, -0.2),
                (1, notes[1] - 12, 0.6, 0.35),
                (2, notes[2] - 12, 0.6, -0.35)]
        for b, pitch, vel, pan in plan:
            hit = _marimba_hit(midi_hz(pitch)) * vel
            s = bar_start(bar) + int(b * beat * SR)
            seg = hit[: n - s]
            out[s:s + len(seg), 0] += seg * np.sqrt((1 - pan) / 2)
            out[s:s + len(seg), 1] += seg * np.sqrt((1 + pan) / 2)
    return out


def render_pulse():
    """Sintetizador del vals: negra, negra, silencio de negra, en cada compas."""
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros((n, 2))
    beat = 60.0 / BPM
    L = int(beat * 0.8 * SR)             # corta: deja oir el silencio del tiempo 3
    t = np.arange(L) / SR
    # ataque lento y salida larga: el acorde "se asoma" en vez de golpear
    env = np.minimum(1.0, t / 0.03) * np.minimum(1.0, (t[-1] - t) / 0.12)
    for bar in range(TOTAL_BARS):
        tones = [m + 12 for m in PAD_NOTES[chord_at_bar(bar)]]
        for b in (0, 1):                 # tiempos 1 y 2; el 3 queda en silencio
            s = bar_start(bar) + int(b * beat * SR)
            for note in tones:
                for det, ch in ((-0.1, 0), (0.1, 1)):
                    f = midi_hz(note) * 2 ** (det / 12.0)
                    # fundamental y tres armonicos: mas presencia que antes
                    w = sum(np.sin(2 * np.pi * k * f * t) / k ** 1.5 for k in (1, 2, 3, 4))
                    out[s:s + L, ch] += w * env * 0.25
    return out


# ------------------------------------------------ melodia de piano (--piano)

# Melodia del autor: Mi4 Re4 Si3 (un compas cada una) y despues Mi4 Re4 Do4 Sol4
# Fa4 Mi4. La armonia es el sintetizador de pulso (negra, negra, silencio).
# --rhythm dotted: las 6 ultimas con negra con puntillo (1.5 tiempos): dos por
#                  compas, caen exactas en las barras.
# --rhythm one:    las 6 ultimas con una negra (1 tiempo): tres por compas, una
#                  por tiempo; ocupan 2 compases. (Se descarto la opcion de dos
#                  negras.)
MELODY_PITCHES = [64, 62, 59, 64, 62, 60, 67, 65, 64]
PHRASE_BARS = [8, 16, 28, 36]      # verso 1, verso 2, coro, outro (frase de 8 compases)
if LONG:
    PHRASE_BARS = [8, 16, 24, 40, 48, 56, 64, 72]
    if HOOK == "c":
        PHRASE_BARS = [0] + PHRASE_BARS
    if HOOK == "abc":
        PHRASE_BARS = [4] + PHRASE_BARS[1:]     # sin la frase del verso 1 (compas 8)


def melody_events():
    """(inicio en tiempos, midi, duracion en tiempos) de una frase."""
    tail = 1.5 if ARGS.rhythm == "dotted" else 1.0
    ev, t = [], 0.0
    for i, m in enumerate(MELODY_PITCHES):
        d = 3.0 if i < 3 else tail
        ev.append((t, m, d))
        t += d
    return ev


def _piano_note(freq, length, vel, sustain=1.0):
    t = np.arange(int(length * SR)) / SR
    out = np.zeros(len(t))
    for k, amp, tau in ((1, 1.0, 1.1), (2, 0.5, 0.7), (3, 0.12, 0.45), (4, 0.06, 0.28),
                        (5, 0.03, 0.2), (6, 0.02, 0.15)):
        out += amp * np.sin(2 * np.pi * k * freq * (1 + 0.0003 * k * k) * t) * np.exp(-t / (tau * sustain))
    out *= np.minimum(1.0, t / 0.015)          # martillo muy suave
    out *= np.minimum(1.0, (t[-1] - t) / 0.3)   # la nota se apaga al entrar la siguiente
    return out * vel


def render_piano():
    rng = np.random.default_rng(SEED + 21)
    n = int((TOTAL_BARS * BAR_S + 8) * SR)
    out = np.zeros((n, 2))
    beat = 60.0 / BPM
    for start_bar in PHRASE_BARS:
        for t0, midi, d in melody_events():
            vel = rng.uniform(0.9, 1.0)
            note = _piano_note(midi_hz(midi), d * beat + 0.3, vel, ARGS.sustain)
            s0 = max(0, int((start_bar * BAR_S + t0 * beat + rng.uniform(-0.008, 0.008)) * SR))
            seg = note[: n - s0]
            out[s0:s0 + len(seg), 0] += seg * 0.8
            out[s0:s0 + len(seg), 1] += seg * 0.8
    return out


GATE_FLOOR = 0.15   # en el compas del "drop" todo baja a este nivel, no a cero


def gate_curve(n):
    """Compas del drop (como en Mirror Cry, que deja solo el bombo): todo se agacha pero
    sigue sonando bajito, con bajada y subida suaves; el timbal queda fuera."""
    g = np.ones(n)
    down, up = int(0.3 * SR), int(0.12 * SR)
    for a, b in GATES:
        i0, i1 = int(a * BAR_S * SR), int(b * BAR_S * SR)
        g[i0:i1] = GATE_FLOOR
        g[i0 - down:i0] = np.linspace(1, GATE_FLOOR, down)
        g[i1 - up:i1] = np.linspace(GATE_FLOOR, 1, up)
    return g


# ---------------------------------------------------------------- efectos

def reverb(st, seconds=3.5, mix=0.4, seed=SEED):
    """Reverb por convolucion con ruido decreciente; una respuesta por canal."""
    rng = np.random.default_rng(seed)
    n_ir = int(seconds * SR)
    t = np.arange(n_ir) / SR
    out = np.zeros_like(st)
    size = 1 << int(np.ceil(np.log2(len(st) + n_ir)))
    for ch in range(2):
        ir = rng.standard_normal(n_ir) * np.exp(-t / (seconds / 4.5))
        k = 64                                  # suaviza: cola mas oscura
        ir = np.convolve(ir, np.ones(k) / k, mode="same")
        ir /= np.sqrt(np.sum(ir ** 2))
        wet = np.fft.irfft(np.fft.rfft(st[:, ch], size) * np.fft.rfft(ir, size), size)
        out[:, ch] = wet[: len(st)]
    return st * (1 - mix) + out * mix


def pingpong(st, beats=0.75, feedback=0.4, taps=5, mix=0.5):
    """Eco que rebota entre izquierda y derecha, sincronizado al tempo."""
    d = int(beats * 60.0 / BPM * SR)
    wet = np.zeros_like(st)
    for k in range(1, taps + 1):
        g = mix * feedback ** (k - 1)
        src = st[:, 0] if k % 2 else st[:, 1]
        dst = 1 if k % 2 else 0
        off = k * d
        if off < len(st):
            wet[off:, dst] += src[: len(st) - off] * g
    return st + wet


# ---------------------------------------------------------------- mezcla

def next_version_dir():
    os.makedirs(VERSIONS_DIR, exist_ok=True)
    n = 1
    while os.path.exists(os.path.join(VERSIONS_DIR, f"v{n}")):
        n += 1
    d = os.path.join(VERSIONS_DIR, f"v{n}")
    os.makedirs(os.path.join(d, "stems"))
    return d, n


def write_wav(path, st):
    pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    vdir, version = next_version_dir()
    raw = {
        "drops": pingpong(render_drops(False)),
        "drops_hi": pingpong(render_drops(True), beats=1.5, feedback=0.5),
        "pad": render_pad(),
        "sub": render_sub(),
        "timbal": render_timbal(),
    }
    if COLD:
        raw.update({"kick": render_kick(), "snare": render_snare(),
                    "hat": render_hat(), "bass_cold": render_bass_cold(),
                    "arp": pingpong(render_arp(), beats=1.5, feedback=0.35)})
    if WALTZ:
        raw.update({"pulse": render_pulse(), "marimba": pingpong(render_marimba(), beats=1.5, feedback=0.3),
                    "bass_cold": render_bass_cold(),
                    "arp": pingpong(render_arp(), beats=1.5, feedback=0.35)})
    if PIANO:
        raw["piano"] = pingpong(render_piano(), beats=1.5, feedback=0.35, mix=0.12)
    stems = {}
    for name, st in raw.items():
        if name in ("drops", "drops_hi", "pad", "timbal", "arp", "snare", "marimba", "pulse", "piano"):
            st = reverb(st, seconds=(4.5 if name == "pad" else 3.0) if name in ("pad", "piano") else (2.5 if name == "pulse" else 3.0),
                        mix=0.5 if name in ("piano",) else (0.4 if name == "pulse" else (0.45 if name != "timbal" else 0.3)))
        st = st * level_curve(name, len(st))[:, None] * GAINS[name]
        if GATES and name != "timbal":
            st = st * gate_curve(len(st))[:, None]
        stems[name] = st
        write_wav(os.path.join(vdir, "stems", f"{name}.wav"), st / max(1e-9, np.abs(st).max()) * 0.9)
    mix = sum(stems.values())
    mix = mix[: int((TOTAL_BARS * BAR_S + 1) * SR)]   # 1 s tras el ultimo compas
    if HOOK in ("b", "abc"):
        mix = mix[int(4 * BAR_S * SR):]               # B: se saltan los 4 primeros compases de la intro
    peak = np.abs(mix).max()
    mix = mix / peak * 0.8
    wav_path = os.path.join(vdir, "mix.wav")
    write_wav(wav_path, mix)
    rms = float(np.sqrt(np.mean(mix ** 2)))
    print(f"v{version}: {len(mix) / SR:.1f} s, pico {np.abs(mix).max():.3f}, RMS {rms:.4f}")
    if shutil.which("ffmpeg"):
        mp3 = os.path.join(PROJECT_DIR, f"the_roars_of_rome_base_v{version}.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
                        "-b:a", "192k", mp3], check=True)
        print("mp3:", mp3)


if __name__ == "__main__":
    main()
