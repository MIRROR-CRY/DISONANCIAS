#!/usr/bin/env python3
"""New Song 2: base instrumental etérea (gotas flotando).

Propuesta v1, a propósito con pocos sonidos para ir armando la idea de a poco.
3/4 a 60 BPM, La menor (Am - F - C - G), 44 compases (~2:12).

Sintesis con numpy puro (sin FluidSynth ni SoundFont): gotas, pad, sub y timbal.
Estructura y curvas de presencia (LEVELS) siguen el esquema de Mirror Cry.

Uso:  python build_song.py     (necesita numpy; ffmpeg opcional para el mp3)
"""
import os
import shutil
import subprocess
import wave

import numpy as np

SR = 44100
BPM = 60
BEATS = 3                      # compas de 3/4
BAR_S = BEATS * 60.0 / BPM     # 3 s por compas
EIGHTH = 60.0 / BPM / 2        # 0.5 s; el patron de gotas son 6 corcheas por compas
SEED = 7

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSIONS_DIR = os.path.join(PROJECT_DIR, "versions")

# Progresion: un acorde por compas, ciclo de 4 compases.
PROGRESSION = ["Am", "F", "C", "G"]
# raiz, tercera, quinta, octava (notas MIDI) para las gotas
DROP_NOTES = {
    "Am": [69, 72, 76, 81],
    "F":  [65, 69, 72, 77],
    "C":  [64, 67, 72, 76],
    "G":  [62, 67, 71, 74],
}
PAD_NOTES = {"Am": [57, 60, 64], "F": [53, 57, 60], "C": [55, 60, 64], "G": [50, 55, 59]}
BASS_ROOT = {"Am": 33, "F": 29, "C": 36, "G": 31}

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
TOTAL_BARS = sum(b for _, b in SECTIONS)

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
GAINS = {"drops": 0.55, "drops_hi": 0.22, "pad": 0.30, "sub": 0.40, "timbal": 0.55}
PAN = {"drops": 0.0, "drops_hi": 0.0, "pad": 0.0, "sub": 0.0, "timbal": 0.0}


def midi_hz(n):
    return 440.0 * 2 ** ((n - 69) / 12.0)


def level_curve(name, n_samples):
    pts = LEVELS[name]
    xs = np.array([p[0] for p in pts]) * BAR_S * SR
    ys = np.array([p[1] for p in pts])
    return np.interp(np.arange(n_samples), xs, ys)


def chord_at_bar(bar):
    return PROGRESSION[bar % len(PROGRESSION)]


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
    stems = {}
    for name, st in raw.items():
        if name in ("drops", "drops_hi", "pad", "timbal"):
            st = reverb(st, seconds=4.0 if name == "pad" else 3.0,
                        mix=0.45 if name != "timbal" else 0.3)
        st = st * level_curve(name, len(st))[:, None] * GAINS[name]
        stems[name] = st
        write_wav(os.path.join(vdir, "stems", f"{name}.wav"), st / max(1e-9, np.abs(st).max()) * 0.9)
    mix = sum(stems.values())
    mix = mix[: int((TOTAL_BARS * BAR_S + 1) * SR)]   # 1 s tras el ultimo compas
    peak = np.abs(mix).max()
    mix = mix / peak * 0.8
    wav_path = os.path.join(vdir, "mix.wav")
    write_wav(wav_path, mix)
    rms = float(np.sqrt(np.mean(mix ** 2)))
    print(f"v{version}: {len(mix) / SR:.1f} s, pico {np.abs(mix).max():.3f}, RMS {rms:.4f}")
    if shutil.which("ffmpeg"):
        mp3 = os.path.join(PROJECT_DIR, f"new_song_2_base_v{version}.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
                        "-b:a", "192k", mp3], check=True)
        print("mp3:", mp3)


if __name__ == "__main__":
    main()
