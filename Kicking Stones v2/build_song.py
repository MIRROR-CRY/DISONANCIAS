#!/usr/bin/env python3
"""
Kicking Stones v2 -- song builder (MIDI + SoundFont rendering, versioned,
section-based).

Writes a MIDI file per instrument PER SECTION, renders each through
fluidsynth with a General MIDI SoundFont (real sampled instruments), then
concatenates all sections into the full song. Every run creates a NEW
version folder under versions/ (v1, v2, ...) instead of overwriting the
previous one.

Each version contains:
  sections/<name>/stems/*.wav   -- per-instrument stems for that section
  sections/<name>/midi/*.mid    -- the MIDI for that section
  sections/<name>/mix.wav       -- that section's own mix
  mix.wav                       -- the full song, all sections concatenated

Sections follow the structure in lyrics/README.md:
  Intro > Verse1 > Rap/Faster > Pre-Chorus > Chorus > Verse2 > Bridge >
  Chorus > Outro
Not every section uses every instrument, and Rap/Faster runs at a higher
BPM -- see SECTIONS below. A minor throughout; the Am-F-G-Em progression
continues seamlessly across sections via a running bar offset.

See ficha_tecnica.md for the production concept (drum machine, dirty
bass, chorus/reverb guitar, dark pads).
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

PROJECT_DIR = "musica/Kicking Stones v2"
VERSIONS_DIR = os.path.join(PROJECT_DIR, "versions")
SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

random.seed(42)  # reproducible humanization

# General MIDI drum map (channel 10 / index 9)
GM_KICK = 36
GM_SNARE = 38
GM_HIHAT_CLOSED = 42
GM_HIHAT_OPEN = 46
GM_CRASH = 49
GM_OVERDRIVEN_GUITAR = 29  # a grittier, higher-register timbre than the clean rhythm guitar

# A minor: i - VI - VII - v, one chord per bar, cycling continuously
# across sections via each section's `bar_offset`.
ROOTS_MIDI = {"A": 33, "F": 29, "G": 31, "E": 28}  # A1, F1, G1, E1
CHORD_TONES_MIDI = {
    "A": [57, 60, 64],   # A3 C4 E4  (Am)
    "F": [53, 57, 60],   # F3 A3 C4  (F)
    "G": [55, 59, 62],   # G3 B3 D4  (G)
    "E": [52, 55, 59],   # E3 G3 B3  (Em)
}
PROGRESSION = ["A", "F", "G", "E"]

# Humanization amounts
TIMING_JITTER_TICKS = 12   # up to ~25ms of drift at 150 BPM
VELOCITY_JITTER = 10       # +/- this much velocity variation

# ---------- song structure ----------
# instruments: subset of {"drums", "bass", "guitar", "pad"}
# drum_density: "full" (kick+snare+hihats), "sparse" (kick only, for the
#   spoken-word Bridge), "driving" (kick+snare on every beat, Rap/Faster)
# bass_pattern: "half" (root on beats 1&3, the default groove) or
#   "quarter" (root on every beat, more frantic -- Rap/Faster)
# guitar_density: "sparse" (accent every other bar) or "full" (every bar)
# Tempo: 146 BPM, not the earlier 150. Measured directly from the user's own
# mastered Rap/Faster vocal demo (vocals/mastered_reference/rap_faster_mastered.mp3):
# that recording is exactly the 8 bars (32 beats) we already sized the
# rapfaster sections to, at a real duration of 13.15s -- 32*60/13.15 = 145.96
# BPM. 150 was close ("casi perfecto") but not exact; 146 is what the
# vocalist is actually singing to. One fixed tempo for the whole song, same
# as always -- see the double-time note above about how "faster" sections
# vary subdivision, never BPM.
SECTIONS = [
    {"name": "intro",      "bars": 4, "bpm": 146, "instruments": ["pad"]},
    {"name": "rapfaster1", "bars": 8, "bpm": 146, "instruments": ["bass"],
     "bass_pattern": "quarter"},
    {"name": "rapfaster2", "bars": 8, "bpm": 146, "instruments": ["bass"],
     "bass_pattern": "quarter"},
    {"name": "prechorus",  "bars": 8, "bpm": 146, "instruments": ["drums", "bass", "guitar", "pad"],
     "drum_density": "full", "bass_pattern": "half", "guitar_density": "sparse"},
    {"name": "chorus1",    "bars": 8, "bpm": 146, "instruments": ["drums", "bass", "guitar", "pad"],
     "drum_density": "full", "bass_pattern": "half", "guitar_density": "full"},
    {"name": "verse1",     "bars": 12, "bpm": 146, "instruments": ["drums", "bass", "guitar", "pad"],
     "drum_density": "full", "bass_pattern": "half", "guitar_density": "sparse"},
    {"name": "bridge",     "bars": 4, "bpm": 146, "instruments": ["drums", "pad"],
     "drum_density": "sparse"},
    {"name": "chorus2",    "bars": 8, "bpm": 146, "instruments": ["drums", "bass", "guitar", "pad"],
     "drum_density": "full", "bass_pattern": "half", "guitar_density": "full"},
    {"name": "chorus3",    "bars": 8, "bpm": 146, "instruments": ["drums", "bass", "guitar", "pad"],
     "drum_density": "full", "bass_pattern": "half", "guitar_density": "full"},
    {"name": "outro",      "bars": 8, "bpm": 146, "instruments": ["drums", "guitar", "pad", "lead"],
     "drum_density": "sparse", "guitar_density": "sparse"},
]

CROSSFADE_SEC = 0.45  # real overlap between sections, not just a de-click --
# >= one beat at 150bpm (0.4s) so the overlap reliably spans into the next
# section's first hit instead of fading through dead air first


def ticks(beats):
    return int(beats * TICKS_PER_BEAT)


def tick_to_sec(tick, bpm):
    return tick / TICKS_PER_BEAT * (60.0 / bpm)


def humanize_tick(tick, amount=TIMING_JITTER_TICKS):
    return max(0, tick + random.randint(-amount, amount))


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


# ---------- MIDI writers (all take n_bars/bpm/bar_offset explicitly) ----------

def write_drum_midi(path, n_bars, bpm, density="full", humanize=True):
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))

    events = []
    for bar in range(n_bars):
        bar_start = bar * ticks(4)

        def add_hit(beat_pos, note, vel):
            t = bar_start + ticks(beat_pos)
            if humanize:
                t = humanize_tick(t)
                vel = humanize_velocity(vel)
            events.append((t, note, vel, True))
            events.append((t + 20, note, 0, False))

        if density == "sparse":
            # bridge: just a slow kick heartbeat, no snare/hihat -- leaves
            # room for the spoken-word sample
            add_hit(0, GM_KICK, 90)
        elif density == "driving":
            # rap/faster: kick+snare on every beat, no hihats -- blunt and frantic
            for beat in range(4):
                add_hit(beat, GM_KICK, 100)
                add_hit(beat, GM_SNARE, 95)
        else:  # "full"
            add_hit(0, GM_KICK, 100)
            add_hit(2, GM_KICK, 100)
            add_hit(1, GM_SNARE, 105)
            add_hit(3, GM_SNARE, 105)
            for eighth in range(8):
                is_last = (bar % 2 == 1 and eighth == 7)
                note = GM_HIHAT_OPEN if is_last else GM_HIHAT_CLOSED
                add_hit(eighth * 0.5, note, 75)

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, note, vel, on in events:
        delta = max(0, tick - last_tick)
        track.append(Message("note_on" if on else "note_off",
                              note=note, velocity=vel, time=delta, channel=9))
        last_tick = max(last_tick, tick)

    mid.save(path)


def pitch_bend_value(cents, bend_range_semitones=2.0):
    """Convert cents of detune to a 14-bit MIDI pitch bend value (-8192..8191)."""
    semitone_range = bend_range_semitones * 100.0
    return int(max(-8192, min(8191, round(cents / semitone_range * 8192))))


def write_bass_midi(path, n_bars, bpm, bar_offset=0, pattern="half",
                     humanize=True, intonation_wobble=True):
    """Dirty bass with humanization (timing/velocity drift) plus a subtle
    pitch-bend wobble per note (micro-detuning, like an imprecise real
    finger/string) instead of a perfectly locked pitch. `pattern` controls
    hit density: "half" (root on beats 1&3, the normal groove) or "quarter"
    (root on every beat, for the more frantic Rap/Faster section)."""
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    track.append(Message("program_change", program=34, time=0, channel=1))  # Electric Bass (picked)

    beat_positions = (0, 1, 2, 3) if pattern == "quarter" else (0, 2)
    hit_dur_beats = 0.9 if pattern == "quarter" else 1.9

    events = []
    note_windows_sec = []

    for bar in range(n_bars):
        bar_start = bar * ticks(4)
        chord = PROGRESSION[(bar + bar_offset) % len(PROGRESSION)]
        note = ROOTS_MIDI[chord]
        for beat_pos in beat_positions:
            start = bar_start + ticks(beat_pos)
            dur = ticks(hit_dur_beats)
            vel = 110
            if humanize:
                start = humanize_tick(start)
                dur += random.randint(-15, 15)
                vel = humanize_velocity(vel)
            end = start + dur

            events.append((start, "on", note, vel))

            if intonation_wobble:
                depth_cents = random.uniform(3.0, 9.0)
                phase = random.uniform(0, 2 * np.pi)
                rate = random.uniform(1.5, 3.5)
                n_points = 10
                for i in range(n_points):
                    frac = i / (n_points - 1)
                    t = start + int(frac * dur)
                    wobble = np.sin(2 * np.pi * rate * frac + phase)
                    drift = random.uniform(-1.5, 1.5)
                    cents = wobble * depth_cents + drift
                    events.append((t, "bend", pitch_bend_value(cents), None))
                events.append((end, "bend", 0, None))

            events.append((end, "off", note, 0))
            note_windows_sec.append((tick_to_sec(start, bpm), tick_to_sec(end, bpm)))

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, kind, value, vel in events:
        delta = max(0, tick - last_tick)
        if kind == "on":
            track.append(Message("note_on", note=value, velocity=vel, time=delta, channel=1))
        elif kind == "off":
            track.append(Message("note_off", note=value, velocity=0, time=delta, channel=1))
        else:
            track.append(Message("pitchwheel", pitch=value, time=delta, channel=1))
        last_tick = max(last_tick, tick)

    mid.save(path)
    return note_windows_sec


def write_guitar_midi(path, n_bars, bpm, density="sparse", humanize=True):
    """Clean electric guitar, dark minor melodic phrases. `density` controls
    how often the motif plays: "sparse" (every other bar -- comes and goes,
    the default) or "full" (every bar -- for the Chorus, more present)."""
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    track.append(Message("program_change", program=27, time=0, channel=2))  # Electric Guitar (clean)

    A3, C4, D4, E4 = 57, 60, 62, 64
    motif = [(E4, 0.5), (D4, 0.5), (C4, 0.5), (A3, 1.0)]  # descending, dark

    if density == "full":
        accent_bars = list(range(n_bars))
    else:
        accent_bars = [b for b in range(n_bars) if b % 2 == 1]

    events = []
    note_windows_sec = []

    for bar in accent_bars:
        bar_start = bar * ticks(4)
        pos = 0.0
        for note, dur_beats in motif:
            start = bar_start + ticks(pos)
            dur = ticks(dur_beats * 0.85)
            vel = 85
            if humanize:
                start = humanize_tick(start, amount=8)
                dur += random.randint(-10, 10)
                vel = humanize_velocity(vel, amount=8)
            end = start + dur
            events.append((start, "on", note, vel))
            events.append((end, "off", note, 0))
            note_windows_sec.append((tick_to_sec(start, bpm), tick_to_sec(end, bpm)))
            pos += dur_beats

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, kind, note, vel in events:
        delta = max(0, tick - last_tick)
        track.append(Message("note_on" if kind == "on" else "note_off",
                              note=note, velocity=vel, time=delta, channel=2))
        last_tick = max(last_tick, tick)

    mid.save(path)
    return note_windows_sec


def write_pad_midi(path, n_bars, bpm, bar_offset=0, humanize=True):
    """Dark atmospheric synth pad: full sustained chords, one per bar,
    following the same Am-F-G-Em progression as the bass."""
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    track.append(Message("program_change", program=90, time=0, channel=3))  # Pad 4 (choir)

    events = []
    note_windows_sec = []

    for bar in range(n_bars):
        bar_start = bar * ticks(4)
        chord = PROGRESSION[(bar + bar_offset) % len(PROGRESSION)]
        for note in CHORD_TONES_MIDI[chord]:
            start = bar_start
            dur = ticks(4)
            vel = 55
            if humanize:
                start = humanize_tick(start, amount=6)
                vel = humanize_velocity(vel, amount=6)
            end = start + dur
            events.append((start, "on", note, vel))
            events.append((end, "off", note, 0))
        note_windows_sec.append((tick_to_sec(bar_start, bpm), tick_to_sec(bar_start + ticks(4), bpm)))

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, kind, note, vel in events:
        delta = max(0, tick - last_tick)
        track.append(Message("note_on" if kind == "on" else "note_off",
                              note=note, velocity=vel, time=delta, channel=3))
        last_tick = max(last_tick, tick)

    mid.save(path)
    return note_windows_sec


# ---------- rendering (fluidsynth) ----------

def render_midi_to_wav(midi_path, wav_path):
    # -R 0 -C 0: disable fluidsynth's OWN built-in reverb/chorus DSP. We
    # apply our own (chorus_effect, per_note_variable_reverb) in Python, so
    # the synth's defaults were stacking a second, much longer, uncontrolled
    # tail on top -- that's what was leaving several seconds of near-silence
    # at the end of every section before the next one started.
    subprocess.run([
        "fluidsynth", "-ni", SOUNDFONT, midi_path,
        "-F", wav_path, "-r", str(SR), "-g", "1.0", "-R", "0", "-C", "0"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def distort(samples, drive=4.0):
    return np.tanh(samples * drive) / np.tanh(drive)


def chorus_effect(signal, rate_hz=0.4, depth_ms=6.0, base_delay_ms=18.0, mix=0.45, sr=SR):
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
    starts_samples = sorted(int(s * sr) for s, _ in note_windows_sec)
    boundaries = starts_samples + [len(dry)]
    out = np.zeros(len(dry) + int(sr * 1.0))
    for i in range(len(boundaries) - 1):
        seg_start, seg_end = boundaries[i], boundaries[i + 1]
        if seg_end <= seg_start:
            continue
        segment = dry[seg_start:seg_end]
        decay = random.uniform(0.15, 0.4)
        mix = random.uniform(0.15, 0.35)
        wet = convolve_reverb(segment, decay=decay, mix=mix)
        end = min(seg_start + len(wet), len(out))
        out[seg_start:end] += wet[:end - seg_start]
    return out[:len(dry)] if len(out) >= len(dry) else pad_to(out, len(dry))


def load_wav_mono(path):
    sr, data = wavfile.read(path)
    if data.ndim > 1:
        data = data.mean(axis=1)
    return data.astype(np.float32) / 32768.0


def peak_normalize(samples, peak=0.9):
    cur_peak = np.max(np.abs(samples))
    return samples / cur_peak * peak if cur_peak > 0 else samples


def write_wav(samples, path):
    wavfile.write(path, SR, (np.clip(samples, -1.0, 1.0) * 32767).astype(np.int16))
    print(f"    guardado: {path}")


def sum_mix(tracks_with_gains, path, headroom_peak=0.98, length=None):
    if length is None:
        length = max(len(t) for t, _ in tracks_with_gains) if tracks_with_gains else 0
    mix = np.zeros(length)
    for track, gain in tracks_with_gains:
        mix[:len(track)] += pad_to(track, length) * gain
    peak = np.max(np.abs(mix)) if length else 0
    if peak > headroom_peak:
        mix = mix * (headroom_peak / peak)
        print(f"    mezcla atenuada {headroom_peak/peak:.2f}x para evitar clipping (pico era {peak:.2f})")
    if path:
        write_wav(mix, path)
    return mix


def pad_to(a, n):
    if len(a) < n:
        return np.pad(a, (0, n - len(a)))
    return a[:n]


def trim_trailing_silence(audio, threshold=0.02, keep_tail_sec=0.35, sr=SR):
    """Cuts off the long dead tail left after the last audible content
    (natural release + our own reverb decaying below `threshold`), keeping
    only a short, deliberate `keep_tail_sec` of decay -- so sections don't
    end in several seconds of near-total silence before the next one
    starts."""
    above = np.where(np.abs(audio) > threshold)[0]
    if len(above) == 0:
        return audio
    last = above[-1] + int(sr * keep_tail_sec)
    return audio[:min(last, len(audio))]


# ---------- gains (predictable because every track is peak-normalized first) ----------
GAINS = {"drums": 1.0, "bass": 0.75, "guitar": 0.5, "pad": 0.35, "lead": 0.55}


def render_section(section, bar_offset, out_dir):
    name = section["name"]
    n_bars = section["bars"]
    bpm = section["bpm"]
    instruments = section["instruments"]

    stems_dir = os.path.join(out_dir, "stems")
    midi_dir = os.path.join(out_dir, "midi")
    os.makedirs(stems_dir, exist_ok=True)
    os.makedirs(midi_dir, exist_ok=True)

    print(f"  seccion '{name}': {n_bars} compases @ {bpm} BPM, instrumentos: {instruments}")

    processed = {}  # name -> (audio, gain)
    length = 0

    if "drums" in instruments:
        midi_path = os.path.join(midi_dir, "drums.mid")
        write_drum_midi(midi_path, n_bars, bpm, density=section.get("drum_density", "full"))
        raw = os.path.join(stems_dir, "_drums_raw.wav")
        render_midi_to_wav(midi_path, raw)
        drums = load_wav_mono(raw)
        os.remove(raw)
        processed["drums"] = drums
        length = max(length, len(drums))

    if "bass" in instruments:
        midi_path = os.path.join(midi_dir, "bass.mid")
        windows = write_bass_midi(midi_path, n_bars, bpm, bar_offset=bar_offset,
                                   pattern=section.get("bass_pattern", "half"))
        raw = os.path.join(stems_dir, "_bass_raw.wav")
        render_midi_to_wav(midi_path, raw)
        bass = load_wav_mono(raw)
        os.remove(raw)
        bass = distort(bass, drive=5.0)
        bass = per_note_variable_reverb(bass, windows)
        processed["bass"] = bass
        length = max(length, len(bass))

    if "guitar" in instruments:
        midi_path = os.path.join(midi_dir, "guitar.mid")
        windows = write_guitar_midi(midi_path, n_bars, bpm, density=section.get("guitar_density", "sparse"))
        raw = os.path.join(stems_dir, "_guitar_raw.wav")
        render_midi_to_wav(midi_path, raw)
        guitar = load_wav_mono(raw)
        os.remove(raw)
        guitar = chorus_effect(guitar)
        guitar = per_note_variable_reverb(guitar, windows)
        processed["guitar"] = guitar
        length = max(length, len(guitar))

    if "pad" in instruments:
        midi_path = os.path.join(midi_dir, "pad.mid")
        windows = write_pad_midi(midi_path, n_bars, bpm, bar_offset=bar_offset)
        raw = os.path.join(stems_dir, "_pad_raw.wav")
        render_midi_to_wav(midi_path, raw)
        pad = load_wav_mono(raw)
        os.remove(raw)
        pad = per_note_variable_reverb(pad, windows)
        processed["pad"] = pad
        length = max(length, len(pad))

    # normalize what's present, save stems, build this section's own mix
    tracks_with_gains = []
    for inst, audio in processed.items():
        norm = peak_normalize(pad_to(audio, length))
        write_wav(norm, os.path.join(stems_dir, f"{inst}.wav"))
        tracks_with_gains.append((norm, GAINS[inst]))

    section_mix = sum_mix(tracks_with_gains, None, length=length)
    section_mix = trim_trailing_silence(section_mix)
    write_wav(section_mix, os.path.join(out_dir, "mix.wav"))
    return section_mix


def crossfade_concat(chunks, fade_secs, sr=SR):
    """Concatenates audio chunks with an equal-power crossfade at each
    boundary. `fade_secs` gives one fade duration per boundary (len(chunks)-1)
    -- boundaries between very different arrangements (e.g. full band into a
    sparse section) get a longer fade so the density change reads as a
    transition instead of a cut, not just a de-click.

    Equal-power (sin/cos) curves, not a linear ramp: a linear fade sums two
    signals whose combined gain dips below either one alone around the
    midpoint (-6dB or worse), which is audible as a hollow "hole" right at
    the splice -- especially here, where both edges are already quiet
    (decaying tail into a rising attack). The sin/cos curves keep total
    energy closer to constant through the overlap so the transition reads
    as smooth blending rather than a dip. The fade is also long enough to
    span at least one beat, so it reliably catches the next section's first
    hit inside the overlap instead of fading through dead air first."""
    if not chunks:
        return np.zeros(0)
    out = chunks[0].copy()
    for chunk, fade_sec in zip(chunks[1:], fade_secs):
        fade_n = int(sr * fade_sec)
        if len(out) >= fade_n and len(chunk) >= fade_n and fade_n > 0:
            t = np.linspace(0, np.pi / 2, fade_n)
            fade_out = np.cos(t)
            fade_in = np.sin(t)
            overlap = out[-fade_n:] * fade_out + chunk[:fade_n] * fade_in
            out = np.concatenate([out[:-fade_n], overlap, chunk[fade_n:]])
        else:
            out = np.concatenate([out, chunk])
    return out


def section_density(section):
    """Rough 0-4 'how full is this section' score, used to size the
    crossfade at each boundary -- a bigger jump gets a longer blend."""
    score = len(section["instruments"])
    if section.get("drum_density") == "sparse":
        score -= 0.5
    if section.get("guitar_density") == "full":
        score += 0.5
    return score


def boundary_fade_sec(a, b, base=CROSSFADE_SEC, max_fade=0.9):
    """Longer crossfade when the arrangement changes a lot between two
    consecutive sections (e.g. full band -> sparse bridge), shorter when
    it's a similar-density transition."""
    diff = abs(section_density(a) - section_density(b))
    return min(max_fade, base + diff * 0.15)


# ---------- continuous full-song rendering (no cross-section concatenation) ----------
#
# render_section() above renders each section as an INDEPENDENT audio file,
# which is then glued to its neighbors with a crossfade. That's fine for
# inspecting one section in isolation, but any crossfade -- however well
# tuned -- is fundamentally patching over a seam that shouldn't exist: the
# two sides were never the same performance. Because every section in this
# song shares one fixed tempo (150 BPM, checked at the top of
# build_continuous_song), we can instead write ONE continuous MIDI timeline
# per instrument spanning the whole song (silent during sections where that
# instrument isn't used) and render each through fluidsynth ONCE. There is
# then nothing to glue: the audio is one uninterrupted performance by
# construction, so there is no seam left for a crossfade to fix.

def _assert_uniform_bpm():
    bpms = {s["bpm"] for s in SECTIONS}
    if len(bpms) != 1:
        raise ValueError(
            f"continuous rendering assumes one fixed tempo across the whole "
            f"song, found {bpms} -- see the double-time note in this file's "
            f"module docstring before adding a tempo change."
        )
    return bpms.pop()


def build_continuous_drum_midi(path, humanize=True):
    """Continuous drums for the whole song, PLUS actual musical transition
    devices at every section boundary instead of relying on a fade:
      - a snare fill on the last beat of a section's last bar (build-up
        into whatever comes next, silence included -- ends the phrase with
        motion instead of stopping mid-groove);
      - a crash on beat 1 of the next section's first bar, when that next
        section also has drums, to mark the arrival.
    This is what makes a boundary read as one idea moving forward rather
    than two clips blended together -- the composition itself signals the
    change, so there's nothing left that needs smoothing in the mix."""
    bpm = _assert_uniform_bpm()
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))

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

                def add_hit(beat_pos, note, vel):
                    t = bar_start + ticks(beat_pos)
                    v = vel
                    if humanize:
                        t = humanize_tick(t)
                        v = humanize_velocity(vel)
                    events.append((t, note, v, True))
                    events.append((t + 20, note, 0, False))

                if density == "sparse":
                    add_hit(0, GM_KICK, 90)
                elif density == "driving":
                    for beat in range(4):
                        add_hit(beat, GM_KICK, 100)
                        add_hit(beat, GM_SNARE, 95)
                else:  # "full"
                    add_hit(0, GM_KICK, 100)
                    add_hit(2, GM_KICK, 100)
                    add_hit(1, GM_SNARE, 105)
                    if is_last_bar:
                        # snare fill on beat 4 (sixteenths, ramping up) instead
                        # of the usual single hit -- a pickup into the next
                        # section rather than a flat stop
                        for i, sub in enumerate([0.0, 0.25, 0.5, 0.75]):
                            add_hit(3 + sub, GM_SNARE, 95 + i * 8)
                    else:
                        add_hit(3, GM_SNARE, 105)
                    for eighth in range(8):
                        if is_last_bar and eighth >= 6:
                            continue  # leave room for the beat-4 fill above
                        is_last_hat = (local_bar % 2 == 1 and eighth == 7)
                        note = GM_HIHAT_OPEN if is_last_hat else GM_HIHAT_CLOSED
                        add_hit(eighth * 0.5, note, 75)
                abs_bar += 1

        if next_section is not None and "drums" in next_section["instruments"]:
            crash_tick = abs_bar * ticks(4)
            events.append((crash_tick, GM_CRASH, 110, True))
            events.append((crash_tick + 20, GM_CRASH, 0, False))

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, note, vel, on in events:
        delta = max(0, tick - last_tick)
        track.append(Message("note_on" if on else "note_off",
                              note=note, velocity=vel, time=delta, channel=9))
        last_tick = max(last_tick, tick)
    mid.save(path)


def build_continuous_bass_midi(path, humanize=True, intonation_wobble=True):
    """Continuous bass, plus a pickup note: when a section without bass is
    followed by one that has it, a single anticipation note (the upcoming
    chord's root, on the last 8th of the last bar) plays before the new
    section actually starts -- the entrance is announced a beat early
    instead of just appearing cold on the downbeat."""
    bpm = _assert_uniform_bpm()
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    track.append(Message("program_change", program=34, time=0, channel=1))

    events = []
    note_windows_sec = []

    def emit_note(start, dur, note, vel):
        end = start + dur
        events.append((start, "on", note, vel))
        if intonation_wobble:
            depth_cents = random.uniform(3.0, 9.0)
            phase = random.uniform(0, 2 * np.pi)
            rate = random.uniform(1.5, 3.5)
            n_points = 10
            for i in range(n_points):
                frac = i / (n_points - 1)
                t = start + int(frac * dur)
                wobble = np.sin(2 * np.pi * rate * frac + phase)
                drift = random.uniform(-1.5, 1.5)
                cents = wobble * depth_cents + drift
                events.append((t, "bend", pitch_bend_value(cents), None))
            events.append((end, "bend", 0, None))
        events.append((end, "off", note, 0))
        note_windows_sec.append((tick_to_sec(start, bpm), tick_to_sec(end, bpm)))

    abs_bar = 0
    for idx, section in enumerate(SECTIONS):
        next_section = SECTIONS[idx + 1] if idx + 1 < len(SECTIONS) else None

        if "bass" not in section["instruments"]:
            if next_section is not None and "bass" in next_section["instruments"]:
                pickup_bar_start = (abs_bar + section["bars"] - 1) * ticks(4)
                next_chord = PROGRESSION[(abs_bar + section["bars"]) % len(PROGRESSION)]
                start = pickup_bar_start + ticks(3.5)
                if humanize:
                    start = humanize_tick(start)
                emit_note(start, ticks(0.4), ROOTS_MIDI[next_chord], 90)
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
                vel = 110
                if humanize:
                    start = humanize_tick(start)
                    dur += random.randint(-15, 15)
                    vel = humanize_velocity(vel)
                emit_note(start, dur, note, vel)
            abs_bar += 1

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, kind, value, vel in events:
        delta = max(0, tick - last_tick)
        if kind == "on":
            track.append(Message("note_on", note=value, velocity=vel, time=delta, channel=1))
        elif kind == "off":
            track.append(Message("note_off", note=value, velocity=0, time=delta, channel=1))
        else:
            track.append(Message("pitchwheel", pitch=value, time=delta, channel=1))
        last_tick = max(last_tick, tick)
    mid.save(path)
    return note_windows_sec


def build_continuous_guitar_midi(path, humanize=True):
    bpm = _assert_uniform_bpm()
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    track.append(Message("program_change", program=27, time=0, channel=2))

    A3, C4, D4, E4 = 57, 60, 62, 64
    motif = [(E4, 0.5), (D4, 0.5), (C4, 0.5), (A3, 1.0)]

    events = []
    note_windows_sec = []
    abs_bar = 0
    for section in SECTIONS:
        if "guitar" not in section["instruments"]:
            abs_bar += section["bars"]
            continue
        density = section.get("guitar_density", "sparse")
        for local_bar in range(section["bars"]):
            play = density == "full" or local_bar % 2 == 1
            if play:
                bar_start = abs_bar * ticks(4)
                pos = 0.0
                for note, dur_beats in motif:
                    start = bar_start + ticks(pos)
                    dur = ticks(dur_beats * 0.85)
                    vel = 85
                    if humanize:
                        start = humanize_tick(start, amount=8)
                        dur += random.randint(-10, 10)
                        vel = humanize_velocity(vel, amount=8)
                    end = start + dur
                    events.append((start, "on", note, vel))
                    events.append((end, "off", note, 0))
                    note_windows_sec.append((tick_to_sec(start, bpm), tick_to_sec(end, bpm)))
                    pos += dur_beats
            abs_bar += 1

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, kind, note, vel in events:
        delta = max(0, tick - last_tick)
        track.append(Message("note_on" if kind == "on" else "note_off",
                              note=note, velocity=vel, time=delta, channel=2))
        last_tick = max(last_tick, tick)
    mid.save(path)
    return note_windows_sec


def build_continuous_pad_midi(path, humanize=True):
    bpm = _assert_uniform_bpm()
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
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
                vel = 55
                if humanize:
                    start = humanize_tick(start, amount=6)
                    vel = humanize_velocity(vel, amount=6)
                end = start + dur
                events.append((start, "on", note, vel))
                events.append((end, "off", note, 0))
            note_windows_sec.append((tick_to_sec(bar_start, bpm), tick_to_sec(bar_start + ticks(4), bpm)))
            abs_bar += 1

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, kind, note, vel in events:
        delta = max(0, tick - last_tick)
        track.append(Message("note_on" if kind == "on" else "note_off",
                              note=note, velocity=vel, time=delta, channel=3))
        last_tick = max(last_tick, tick)
    mid.save(path)
    return note_windows_sec


# A natural minor scale (root A), spanning just over two octaves, used for
# the improvised lead solo below -- degrees at semitone offsets 0,2,3,5,7,8,10
A_NATURAL_MINOR_OFFSETS = [0, 2, 3, 5, 7, 8, 10]
LEAD_SCALE = [69 + 12 * octv + off for octv in (0, 1) for off in A_NATURAL_MINOR_OFFSETS] + [69 + 24]

CHORD_TONE_SEMITONES = {  # relative to A, for pulling the solo back to consonance on strong beats
    "A": {0, 3, 7}, "F": {8, 0, 5}, "G": {10, 2, 7}, "E": {7, 11, 4},
}


def _closest_scale_index(target_note):
    return min(range(len(LEAD_SCALE)), key=lambda i: abs(LEAD_SCALE[i] - target_note))


def build_continuous_lead_midi(path, humanize=True):
    """A semi-random ('improvised') melodic solo over A natural minor,
    active only in sections listing 'lead' -- currently just the Outro.
    A random walk through the scale, gently pulled toward the current
    chord's tones on strong beats (beat 1 and 3) so it still tracks the
    Am-F-G-Em progression instead of wandering freely, with occasional
    rests so it reads as phrased rather than a constant stream of notes."""
    bpm = _assert_uniform_bpm()
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    track.append(Message("program_change", program=GM_OVERDRIVEN_GUITAR, time=0, channel=4))

    events = []
    note_windows_sec = []
    dur_choices = [0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.75, 1.0]

    abs_bar = 0
    scale_idx = len(LEAD_SCALE) // 2
    for section in SECTIONS:
        if "lead" not in section["instruments"]:
            abs_bar += section["bars"]
            continue
        for _ in range(section["bars"]):
            bar_start = abs_bar * ticks(4)
            chord = PROGRESSION[abs_bar % len(PROGRESSION)]
            pos_beats = 0.0
            while pos_beats < 4.0:
                on_strong_beat = pos_beats in (0.0, 2.0)
                if random.random() < 0.12:
                    # a rest -- keeps the solo phrased, not a wall of notes
                    pos_beats += random.choice([0.25, 0.5])
                    continue
                if on_strong_beat and random.random() < 0.6:
                    # pull toward a chord tone for consonance on the strong beat
                    target_offset = random.choice(list(CHORD_TONE_SEMITONES[chord]))
                    target_note = 69 + target_offset
                    scale_idx = _closest_scale_index(target_note)
                else:
                    step = random.choice([-3, -2, -1, -1, 1, 1, 2, 3])
                    scale_idx = max(0, min(len(LEAD_SCALE) - 1, scale_idx + step))
                note = LEAD_SCALE[scale_idx]
                dur_beats = min(random.choice(dur_choices), 4.0 - pos_beats)
                start = bar_start + ticks(pos_beats)
                dur = ticks(dur_beats * 0.85)  # slight gap between notes, not fully legato
                vel = 80
                if humanize:
                    start = humanize_tick(start, amount=10)
                    vel = humanize_velocity(vel, amount=10)
                end = start + dur
                events.append((start, "on", note, vel))
                events.append((end, "off", note, 0))
                note_windows_sec.append((tick_to_sec(start, bpm), tick_to_sec(end, bpm)))
                pos_beats += dur_beats
            abs_bar += 1

    events.sort(key=lambda e: e[0])
    last_tick = 0
    for tick, kind, note, vel in events:
        delta = max(0, tick - last_tick)
        track.append(Message("note_on" if kind == "on" else "note_off",
                              note=note, velocity=vel, time=delta, channel=4))
        last_tick = max(last_tick, tick)
    mid.save(path)
    return note_windows_sec


def build_continuous_song(version_dir):
    """Renders the whole song as one uninterrupted performance per
    instrument (see the module note above `_assert_uniform_bpm`), then mixes
    them down. This is the authoritative full mix.wav for the version --
    render_section()'s per-section files remain useful for stems/vocal-sync
    work but are no longer glued together for the final mix."""
    midi_dir = os.path.join(version_dir, "full_song_midi")
    os.makedirs(midi_dir, exist_ok=True)

    print("  render continuo (una sola toma por instrumento, sin cortes entre secciones)...")

    processed = {}
    length = 0

    drum_midi = os.path.join(midi_dir, "drums.mid")
    build_continuous_drum_midi(drum_midi)
    raw = os.path.join(midi_dir, "_drums_raw.wav")
    render_midi_to_wav(drum_midi, raw)
    drums = load_wav_mono(raw)
    os.remove(raw)
    processed["drums"] = drums
    length = max(length, len(drums))

    bass_midi = os.path.join(midi_dir, "bass.mid")
    bass_windows = build_continuous_bass_midi(bass_midi)
    raw = os.path.join(midi_dir, "_bass_raw.wav")
    render_midi_to_wav(bass_midi, raw)
    bass = load_wav_mono(raw)
    os.remove(raw)
    bass = distort(bass, drive=5.0)
    bass = per_note_variable_reverb(bass, bass_windows)
    processed["bass"] = bass
    length = max(length, len(bass))

    guitar_midi = os.path.join(midi_dir, "guitar.mid")
    guitar_windows = build_continuous_guitar_midi(guitar_midi)
    raw = os.path.join(midi_dir, "_guitar_raw.wav")
    render_midi_to_wav(guitar_midi, raw)
    guitar = load_wav_mono(raw)
    os.remove(raw)
    guitar = chorus_effect(guitar)
    guitar = per_note_variable_reverb(guitar, guitar_windows)
    processed["guitar"] = guitar
    length = max(length, len(guitar))

    pad_midi = os.path.join(midi_dir, "pad.mid")
    pad_windows = build_continuous_pad_midi(pad_midi)
    raw = os.path.join(midi_dir, "_pad_raw.wav")
    render_midi_to_wav(pad_midi, raw)
    pad = load_wav_mono(raw)
    os.remove(raw)
    pad = per_note_variable_reverb(pad, pad_windows)
    processed["pad"] = pad
    length = max(length, len(pad))

    if any("lead" in s["instruments"] for s in SECTIONS):
        lead_midi = os.path.join(midi_dir, "lead.mid")
        lead_windows = build_continuous_lead_midi(lead_midi)
        raw = os.path.join(midi_dir, "_lead_raw.wav")
        render_midi_to_wav(lead_midi, raw)
        lead = load_wav_mono(raw)
        os.remove(raw)
        lead = distort(lead, drive=2.5)  # a little grit, distinct from the clean rhythm guitar
        lead = chorus_effect(lead, base_delay_ms=24.0)  # wider/longer delay -- more "solo", less "rhythm part"
        lead = per_note_variable_reverb(lead, lead_windows)
        processed["lead"] = lead
        length = max(length, len(lead))

    tracks_with_gains = []
    gained = {}
    for inst, audio in processed.items():
        norm = peak_normalize(pad_to(audio, length))
        track = norm * GAINS[inst]
        gained[inst] = track
        tracks_with_gains.append((norm, GAINS[inst]))

    full_mix = sum_mix(tracks_with_gains, None, length=length)
    full_mix = trim_trailing_silence(full_mix, keep_tail_sec=1.0)  # only the song's own ending

    # full-song stems, gain-matched to the mix and trimmed to the same final
    # length -- these sum back to (approximately) full_mix, so they line up
    # sample-for-sample if imported together into an external editor
    stems_dir = os.path.join(version_dir, "stems")
    os.makedirs(stems_dir, exist_ok=True)
    for inst, track in gained.items():
        write_wav(pad_to(track, len(full_mix)), os.path.join(stems_dir, f"{inst}.wav"))

    return full_mix


# ---------- TDD-style objective check: no section boundary may dip ----------

def check_boundary_continuity(mix, sr=SR, win_sec=0.05, context_sec=1.0,
                               drop_ratio=0.20, neighbor_floor=0.01):
    """Fails the build if any point has a sudden local energy hole: quieter
    than `drop_ratio` times BOTH its preceding and following `context_sec`
    of audio, with those neighbors themselves clearly audible. This is
    local-context comparison, not a global threshold -- an earlier version
    compared against the whole song's median RMS and flagged the (correctly)
    quiet pad-only Intro as a false positive, because a section that's quiet
    throughout by arrangement looks the same as a splice artifact under a
    single global level. A real seam is quiet audio surrounded on both sides
    by louder audio; a deliberately sparse section is quiet on both sides
    too, and this test only flags the former. Returns (passed, report_lines).
    Run this after every change to the song-assembly code before calling it
    done."""
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
    for i in range(len(rms)):
        if i - ctx_n < 0 or i + 1 + ctx_n > len(rms):
            continue  # no full context at the very start/end (song's own fade-in/out, not a seam)
        before = np.mean(rms[i - ctx_n:i])
        after = np.mean(rms[i + 1:i + 1 + ctx_n])
        floor = min(before, after)
        if floor < neighbor_floor:
            continue  # neighbors are quiet too (a sparse section, not a hole between loud content)
        if rms[i] < floor * drop_ratio:
            flagged.append(times[i])

    runs = []
    if flagged:
        start = prev = flagged[0]
        for t in flagged[1:]:
            if t - prev > hop / sr * 1.5:
                runs.append((start, prev))
                start = t
            prev = t
        runs.append((start, prev))

    lines = [f"local-context dip scan: window={win_sec*1000:.0f}ms, context={context_sec:.1f}s each side, "
             f"flags a window under {drop_ratio*100:.0f}% of BOTH neighbors' average level"]
    if runs:
        lines.append(f"FAIL: {len(runs)} real seam(s)/hole(s) found (quiet, flanked by audible content both sides):")
        for a, b in runs:
            lines.append(f"    {a:.2f}s - {b:.2f}s (dur {b-a:.2f}s)")
    else:
        lines.append("PASS: no point in the mix is a local hole between two louder passages -- "
                      "any quiet stretches found are deliberately sparse sections, not broken splices.")
    return (len(runs) == 0), lines


def render_song():
    version_dir, v = next_version_dir()
    sections_dir = os.path.join(version_dir, "sections")

    print(f"Renderizando version v{v} en {version_dir} ...")

    # per-section files: kept for stems / isolated vocal-sync preview work
    bar_offset = 0
    for section in SECTIONS:
        out_dir = os.path.join(sections_dir, section["name"])
        render_section(section, bar_offset, out_dir)
        bar_offset += section["bars"]

    # the actual song: one continuous take per instrument, no seams to glue
    full_mix = build_continuous_song(version_dir)

    write_wav(full_mix, os.path.join(version_dir, "mix.wav"))
    print(f"Version v{v} lista: {len(SECTIONS)} secciones, {len(full_mix)/SR:.1f}s totales.")

    passed, report = check_boundary_continuity(full_mix)
    print("  --- chequeo de continuidad (TDD) ---")
    for line in report:
        print(f"  {line}")
    if not passed:
        print("  ADVERTENCIA: el chequeo de continuidad FALLO -- revisar antes de dar la version por buena.")

    return version_dir


if __name__ == "__main__":
    render_song()
