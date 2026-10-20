# Backing Track - Generated Base for Rescue Us

## Overview

This backing track was generated using Python synthesis to create a complete musical foundation for vocal recording. It features:

- **Gen Alpha Melody** (F-B-E-A pattern)
- **Harmonic accompaniment** (Dm-G-C-F progression)
- **Bass line** (root notes following the chords)
- **Spontaneous Dame Luz moments** (melodic interjections)

## Generated File

**Location**: `audio/backing_track_base.wav`
**Duration**: 120 seconds (2:00), structured in distinct sections (see below)
**Sample Rate**: 44,100 Hz (CD quality)
**Format**: WAV (uncompressed)

With the ambulance siren intro/outro (`backing_track_with_intro.wav`): 130 seconds (2:10). The outro fade was removed on request: the final chorus now cuts straight into the siren instead of fading out first, and the Gen Alpha melody keeps the exact same tone/octave in every chorus (the earlier version doubled it an octave up on the last chorus, which made it sound "off" compared to the rest).

## Real Bass Arpeggio (non-synthetic)

`add_bass_arpeggio.py` adds an **acoustic bass** layer using real sampled audio instead of a synthesized waveform: a MIDI arpeggio (following the same Dm-G-C-F progression) rendered through `fluidsynth` with the **FluidR3_GM** soundfont (GM program 32, Acoustic Bass — actual recorded upright bass samples, not a sine/triangle oscillator like the rest of the track).

Density and velocity vary per section, same principle as the rest of the arrangement:

```
intro:        silent (lets the pad breathe)
verse:        sparse — root/fifth half notes, quiet
pre_chorus:   building — quarter-note arpeggio
chorus:       full eighth-note arpeggio, louder
bridge:       just a held root note, very quiet (breakdown)
chorus_final: full eighth-note arpeggio, loudest
```

The rendered bass (`audio/bass_arpeggio_render.wav`) is mixed under the synth layers at 60% gain so it sits underneath rather than fighting with the Gen Alpha melody.

## Real Cello in the Bridge (non-synthetic)

`add_strings.py` adds a **cello** line (GM program 42, real sampled low strings via FluidR3_GM) exactly during the bridge section (80s-96s) — the moment the Gen Alpha melody ("ni-ni-ni-ni") drops out. Instead of leaving that space just to chords + a Dame Luz hit, a sustained cello line holds the root of each chord (Dm-G-C-F) through the breakdown, giving it a real, warm low-string texture. Mixed in at 70% gain.

## Loudness Normalization (no section sounds quieter than another)

`normalize_loudness.py` runs last. It measures the RMS (perceived loudness) of each section and scales every section to match a common target level, with a short crossfade at each boundary to avoid clicks. Arrangement density still varies section to section (sparse verse vs full chorus), but the overall volume no longer drops in the quieter sections — the intro and bridge in particular were much quieter in level (not just in arrangement) before this step, and are now brought up to match the rest of the track.

Full re-run order if regenerating from scratch:

```bash
python3 generate_backing_track.py   # synth layers (melody, chords, pads, Dame Luz)
python3 add_bass_arpeggio.py        # mixes the real acoustic bass on top
python3 add_strings.py              # mixes the real cello into the bridge
python3 normalize_loudness.py       # MUST run last - equalizes loudness across sections
```

## Song Structure (v2 — section-based)

The first version was one flat loop with no dynamic contrast. This version
gives every section a distinct role, so the Gen Alpha hook actually lands
as a hook instead of just repeating at constant volume throughout:

```
  0s -   8s : intro        (soft chords only, sets the mood)
  8s -  24s : verse        (sparse — chords + bass, melody almost silent)
 24s -  32s : pre_chorus   (melody enters, building)
 32s -  48s : chorus       (full arrangement — the hook at full volume + Dame Luz hit)
 48s -  64s : verse        (back to sparse)
 64s -  80s : chorus       (full arrangement again)
 80s -  96s : bridge       (pattern breaks — no bass, spotlight on Dame Luz melody)
 96s - 120s : chorus_final (biggest version — same melody tone as other choruses)
```

No separate outro section: the final chorus cuts straight into the
ambulance siren for a more abrupt, "brusco" transition (matches the
"emergency" framing better than a fade-out would). This also lengthened
the track (120s core, 130s with the siren intro/outro) versus the
original flat-loop version, as a side effect of giving each section
room to breathe.

## Track Composition

### 1. Gen Alpha Melody (F-B-E-A)
- **Role**: The hypnotic, repeating melodic hook
- **Sound**: Triangle wave (soft, synthesized)
- **Pattern**: Loops continuously F → B → E → A
- **Effect**: Creates the yearning, circular quality
- **Volume**: -12dB (moderate presence)

### 2. Harmonic Accompaniment (Dm-G-C-F)
- **Role**: The emotional/harmonic anchor
- **Chords**: D minor → G major → C major → F major
- **Duration per chord**: 2 seconds
- **Sound**: Mixed sine waves
- **Volume**: -18dB (background support)
- **Effect**: Smooth progression that never fully "resolves"

### 3. Bass Line
- **Role**: Low-end foundation and harmonic confirmation
- **Notes**: D₂ → G₂ → C₂ → F₂ (root notes of each chord)
- **Duration per note**: 2 seconds
- **Sound**: Sine wave (pure tone)
- **Volume**: -14dB (supporting)

### 4. Dame Luz Moments
- **Role**: Spontaneous melodic interjections
- **Appearances**: At 8s, 24s, 48s, 72s, 96s
- **Melody**: Simplified contour based on "oh dame dame dame luz"
- **Notes**: A → A → G → F → A → B → C
- **Sound**: Triangle wave (matched to Gen Alpha)
- **Volume**: -10dB (becomes prominent in moments)

## How to Use

### For Vocal Recording:
1. Open `backing_track_base.wav` in your DAW (Audacity, GarageBand, etc.)
2. Create a new audio track for vocals
3. Record your vocal performance on top
4. The Gen Alpha pattern will serve as a constant reference point
5. The Dame Luz moments provide rhythmic/melodic anchors for phrasing

### Timing Reference:
- **Gen Alpha note duration**: 0.5 seconds per note
- **Chord changes**: Every 2 seconds
- **BPM**: 100 (matches the tempo)

## For Further Editing

The `generate_backing_track.py` script can be modified to:
- Change the total duration (`DURATION_TOTAL`)
- Adjust volumes of individual tracks
- Modify the Gen Alpha pattern or chord progression
- Add more Dame Luz appearances
- Change BPM (beats per minute)
- Switch instruments/waveforms

## Quality Notes

- All synthesis is done digitally (no external samples)
- No post-processing applied yet (EQ, compression, reverb can be added later)
- Designed for vocal recording (not a finished mix)
- Compatible with all major DAWs

## Next Steps

1. Listen to `backing_track_base.wav` to familiarize yourself with the pattern
2. Identify which Dame Luz moments feel right for your vocals
3. Record vocals in your DAW
4. Consider adding production elements (EQ, compression, effects)
5. Export final mix

---

**Generated**: 2026-09-18
**Generator**: `generate_backing_track.py`
**Status**: Ready for vocal recording
