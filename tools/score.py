#!/usr/bin/env python3
"""Lead-sheet engraver shared by every song in the album.

Why the score is built from the composition and not from the MIDI stems:
a direct MIDI-to-notation dump of these arrangements would be unreadable.
The stems are deliberately humanized - strokes land 8ms early, notes ring
for 0.92 of their nominal length, crowd layers drift - and a notation
program has to quantize all of that into something, so it produces a page
of tied thirty-second notes and nested tuplets that represents the
performance but not the piece.

What a registration needs, and what a musician reading it needs, is the
opposite: the composition itself. So each song declares its structure,
harmony, melody and lyrics, and this module engraves that.

Pitched instruments get pitched notation. Slash notation is for parts with
no pitch - the drum kit - or for a part whose voicing the player is meant
to choose. Where the source knows exactly which notes the guitar plays,
writing slashes instead would be throwing the music away: it says "there is
a bar here" and nothing else. So the guitar is written as real noteheads,
either as the chord voicing it strums (with cross noteheads for the damped
strokes) or as the melodic figure it plays, and only the percussion keeps
the rhythm-only notation it is meant for.

Output per song, into its `partitura/` folder:
  <slug>.ly        LilyPond source (the thing under version control)
  <slug>.pdf       engraved score, for printing and for the DPI
  <slug>.musicxml  interchange format, opens in MuseScore/Finale/Sibelius
"""

import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field

# LilyPond note spelling. Melodies are written as (step, octave, duration)
# where octave 4 is the one containing middle C, so the source reads the
# way a musician would say it out loud.
_LY_OCT = {0: ",,,", 1: ",,", 2: ",", 3: "", 4: "'", 5: "''", 6: "'''", 7: "''''"}


def _q(text):
    """LilyPond string literals: no stray backslashes, no double quotes."""
    return text.replace("\\", "").replace('"', "'")


_SHARP = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
_FLAT = ["c", "des", "d", "ees", "e", "f", "ges", "g", "aes", "a", "bes", "b"]


def ly_midi(n, flats=False):
    """MIDI number to LilyPond pitch. 60 -> c'.

    Melodic instruments get real noteheads at real pitches. Slash notation
    belongs to instruments with no pitch (the drum kit) or to a part the
    player is expected to voice themselves; writing a guitar that way when
    the exact voicing is known in the source throws the music away.
    """
    table = _FLAT if flats else _SHARP
    return f"{table[n % 12]}{_LY_OCT[n // 12 - 1]}"


def _ly_pitch(name, octave):
    """'Bb', 4 -> 'bes''. LilyPond spells flats -es and sharps -is."""
    step = name[0].lower()
    acc = name[1:]
    acc = acc.replace("b", "es").replace("#", "is")
    if step in "ae" and acc.startswith("es"):
        acc = acc[1:]          # aes not aees, ees not eees
    return f"{step}{acc}{_LY_OCT[octave]}"


def _ly_chord(sym):
    """'Bbm7' -> 'bes1:m7'. Chord symbols as a player would write them."""
    m = re.match(r"^([A-G][b#]?)(.*)$", sym)
    if not m:
        raise ValueError(f"chord symbol not understood: {sym!r}")
    root, qual = m.group(1), m.group(2)
    step = root[0].lower() + root[1:].replace("b", "es").replace("#", "is")
    if root[0] in "AE" and root[1:2] == "b":
        step = root[0].lower() + "es"
    table = {
        "": "", "m": ":m", "min": ":m", "m7": ":m7", "7": ":7",
        "maj7": ":maj7", "M7": ":maj7", "sus2": ":sus2", "sus4": ":sus4",
        "dim": ":dim", "aug": ":aug", "6": ":6", "m6": ":m6",
        "9": ":9", "m9": ":m9", "add9": ":5.9", "m7b5": ":m7.5-",
    }
    if qual not in table:
        raise ValueError(f"chord quality not supported: {sym!r}")
    return f"{step}1{table[qual]}"


@dataclass
class Section:
    """One formal section. `chords` is one symbol per bar, cycled to `bars`."""
    name: str
    bars: int
    chords: list
    lyrics: str = ""          # one syllable group per word, space separated
    melody: list = field(default_factory=list)   # [(pitch|'r', octave, dur)]
    note: str = ""            # printed above the staff
    # The section's actual rhythmic figure, as [(beat, kind)] where beat is
    # the position inside the bar counting from 0 and kind is "hit" for a
    # struck chord or "mute" for a damped percussive stroke. Written out in
    # the section's first bar; the rest of the section repeats it with the
    # percent sign, which is how a chart says "same figure, new chord".
    rhythm: list = field(default_factory=list)
    # A fixed melodic figure, [(midi, duration in beats)], played once per
    # bar. This is what a guitar that plays a riff actually does, as opposed
    # to one that strums the chord of the moment.
    figure: list = field(default_factory=list)
    # True when the figure plays on every other bar rather than every bar.
    figure_alternates: bool = False


@dataclass
class Motif:
    """A short quoted figure printed on its own staff after the chart.

    Some material in these songs is a motif rather than a section: a riff
    that surfaces here and there, or a phrase quoted from elsewhere. Forcing
    it into the main staff would mean padding it to whole bars it does not
    occupy, so it gets its own small system with its own time signature.
    """
    label: str
    melody: list
    time_sig: str = "4/4"
    key: str = "c \\major"
    note: str = ""


@dataclass
class GrooveCell:
    """One bar of the actual groove, written out per instrument.

    A chord chart tells a player WHAT harmony and WHEN it changes. It does
    not tell them how the thing feels, and for these songs the feel IS the
    style: the paseo lives in its damped offbeat, the indie-folk lives in
    the stomps and claps, and no amount of chord symbols carries either.
    So the groove goes at the top of the page as a real bar of notation,
    once, and the chart underneath says "like this".

    `guitar` and `bass` are [(beat, kind)] like Section.rhythm; `bass_notes`
    optionally gives pitches. `drums` is [(beat, [drum names])] using
    LilyPond drum names (bd, sn, hh, hho, cymc, tamb, ...).
    """
    label: str = "Groove"
    note: str = ""
    guitar: list = field(default_factory=list)
    guitar_name: str = "Guit."
    bass: list = field(default_factory=list)
    bass_notes: list = field(default_factory=list)
    bass_name: str = "Bajo"
    drums: list = field(default_factory=list)
    drums_name: str = "Perc."


@dataclass
class SongSpec:
    title: str
    subtitle: str
    composer: str
    key: str                  # e.g. 'c \\major', 'a \\minor'
    bpm: int
    time_sig: str
    sections: list
    slug: str
    tagline: str = ""
    copyright: str = ""
    staff_name: str = ""
    footer_notes: list = field(default_factory=list)
    # [(section label, [lines])] - printed after the score. A lead sheet only
    # sets lyrics under the staff where the vocal melody is actually written
    # out; under slash notation the syllables would line up with nothing.
    lyrics_text: list = field(default_factory=list)
    motifs: list = field(default_factory=list)
    groove: object = None
    # {chord symbol: [midi notes]} - the actual voicing the part plays. When
    # present, the chart writes real stacked noteheads at those pitches
    # instead of slashes.
    voicings: dict = field(default_factory=dict)
    flats: bool = False       # spell accidentals as flats (flat keys)


def _bars_of(sec):
    """Chord symbols expanded to one per bar."""
    return [sec.chords[i % len(sec.chords)] for i in range(sec.bars)]


def sections_from_timestamps(path, bpm, progression, phrase=4, notes=None,
                             instrumental_label="Instrumental",
                             total_seconds=None):
    """Derive the form from WHERE THE VOCAL ACTUALLY LANDS, not from the
    generator's section names.

    The names inside a backing-track generator record what the arrangement
    was meant to be when it was built. The master records what was sung.
    Those drift: in "Kicking Stones" the parts named `rapfaster1/2` ended up
    holding ordinary sung verses (no rap was ever recorded), the part named
    `verse1` is where the chorus is actually sung, and the part named
    `chorus1` has no vocal on it at all.

    A score has to describe the recording, because the recording is the work.
    So this reads the timestamped lyric sheet, snaps each section's entry to
    the nearest phrase boundary (these songs move in four-bar phrases, so a
    singer coming in a beat early is a pickup, not a new bar count), and
    names the sections the way the lyric sheet does.

    Returns (sections, report) - the report lists every place the derived
    form disagrees with what you would have gotten from the generator, so
    the discrepancy is visible instead of silently resolved.
    """
    bar = 4 * 60 / bpm
    entries, current = [], None
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        m = re.match(r"^\[(.+?)\]\s*$", line)
        if m:
            current = m.group(1)
            continue
        t = re.match(r"^\d+\.\s*\[(\d+):(\d+)\]\s*\(([\d.]+)s\)\s*(.*)$", line)
        if t and current:
            start = int(t.group(1)) * 60 + int(t.group(2))
            entries.append((current, start, start + float(t.group(3)), t.group(4)))
    if not entries:
        raise ValueError(f"no timestamped lines found in {path}")

    # First bar of each named block, snapped to the phrase grid.
    starts, seen = [], set()
    for name, start, _end, _text in entries:
        if name in seen:
            continue                      # a repeated block gets numbered below
        seen.add(name)
    order, last = [], None
    for name, start, _end, _text in entries:
        if name != last:
            order.append([name, start])
            last = name
    bounds = []
    for name, start in order:
        first_bar = int(round(start / (phrase * bar))) * phrase + 1
        bounds.append([name, max(1, first_bar)])

    # An intro, and any stretch with no vocal, is its own section.
    if bounds[0][1] > 1:
        bounds.insert(0, ["Intro", 1])
    end_bar = int(round(entries[-1][2] / (phrase * bar))) * phrase
    if total_seconds:
        # The score is as long as the master. Rounding the last vocal up to a
        # phrase can overshoot the actual end of the recording, and a score
        # that runs past the record is describing a different take.
        end_bar = min(end_bar, int(total_seconds / bar))
    bounds.append([None, max(end_bar, bounds[-1][1] + phrase) + 1])

    def mk(label, b0, b1, note):
        out.append(Section(
            name=label, bars=b1 - b0,
            chords=[progression[(b0 - 1 + k) % len(progression)]
                    for k in range(b1 - b0)],
            note=note))
        report.append(f"c.{b0}-{b1 - 1}  ({b1 - b0} c.)  {label}")

    counts, out, report = {}, [], []
    for i in range(len(bounds) - 1):
        name, b0 = bounds[i]
        b1 = bounds[i + 1][1]
        if b1 - b0 <= 0:
            continue
        counts[name] = counts.get(name, 0) + 1
        label = name if counts[name] == 1 else f"{name} {counts[name]}"

        # Where does the last syllable of this block actually stop? If whole
        # phrases go by after it, that stretch is an instrumental section and
        # gets printed as one, instead of being padded onto the sung part.
        ends = [e for n, _s, e, _t in entries if n == name and
                b0 <= int(round(_s / (phrase * bar))) * phrase + 1 < b1 + phrase]
        sung_to = b1
        if ends and name != "Intro":
            sung_to = int(round(max(ends) / (phrase * bar))) * phrase + 1
            sung_to = min(max(sung_to, b0 + phrase), b1)
        if b1 - sung_to >= phrase:
            mk(label, b0, sung_to, (notes or {}).get(name, ""))
            mk(instrumental_label, sung_to, b1, "sin voz")
        else:
            mk(label, b0, b1, (notes or {}).get(name, ""))
    return out, report


_DUR_NAMES = {4.0: "1", 3.0: "2.", 2.0: "2", 1.5: "4.", 1.0: "4",
              0.75: "8.", 0.5: "8", 0.25: "16"}


def _dur(beats):
    """Nearest writable duration at or below `beats`."""
    for d in sorted(_DUR_NAMES, reverse=True):
        if d <= beats + 1e-6:
            return _DUR_NAMES[d], d
    return "16", 0.25


def rhythm_bar(onsets, beats_per_bar=4):
    """One bar of real rhythm notation from a list of (beat, kind).

    This replaces the four identical slashes per bar that the first version
    printed everywhere. Four slashes in every bar of every song say nothing
    beyond "there is a bar here": they are the notational equivalent of a
    placeholder. A chart earns its keep by showing the figure the player
    actually plays, and then saying "again" instead of redrawing it.

    "hit" gets a slash notehead, "mute" gets a cross, which is the standard
    way to write a damped percussive stroke.
    """
    if not onsets:
        return "b'4 b'4 b'4 b'4"
    onsets = sorted(onsets, key=lambda o: o[0])
    out, cursor = [], 0.0
    for i, (beat, kind) in enumerate(onsets):
        if beat - cursor > 1e-6:                      # silence before the hit
            gap = beat - cursor
            while gap > 1e-6:
                name, taken = _dur(gap)
                out.append(f"r{name}")
                gap -= taken
            cursor = beat
        nxt = onsets[i + 1][0] if i + 1 < len(onsets) else beats_per_bar
        name, taken = _dur(max(0.25, nxt - beat))
        if kind == "mute":
            out.append("\\once \\override NoteHead.style = #'cross "
                       f"b'{name}")
        else:
            out.append(f"b'{name}")
        cursor = beat + taken
    while beats_per_bar - cursor > 1e-6:
        name, taken = _dur(beats_per_bar - cursor)
        out.append(f"r{name}")
        cursor += taken
    return " ".join(out)


def _drum_bar(onsets, beats_per_bar=4):
    """A bar of drum notation from [(beat, [names])]."""
    if not onsets:
        return ""
    onsets = sorted(onsets, key=lambda o: o[0])
    out, cursor = [], 0.0
    for i, (beat, names) in enumerate(onsets):
        while beat - cursor > 1e-6:
            name, taken = _dur(beat - cursor)
            out.append(f"r{name}")
            cursor += taken
        nxt = onsets[i + 1][0] if i + 1 < len(onsets) else beats_per_bar
        name, taken = _dur(max(0.25, nxt - beat))
        body = names[0] if len(names) == 1 else "<" + " ".join(names) + ">"
        out.append(f"{body}{name}")
        cursor = beat + taken
    while beats_per_bar - cursor > 1e-6:
        name, taken = _dur(beats_per_bar - cursor)
        out.append(f"r{name}")
        cursor += taken
    return " ".join(out)


def _groove_block(g, spec):
    if g is None:
        return ""
    staves = []
    if g.guitar:
        staves.append(
            '\\new RhythmicStaff \\with {'
            ' instrumentName = \\markup { \\fontsize #-3 "' + _q(g.guitar_name) + '" }'
            ' } { \\improvisationOn ' + rhythm_bar(g.guitar) + ' }')
    if g.bass:
        if g.bass_notes:
            toks, cursor = [], 0.0
            for (beat, _k), (pitch, octv) in zip(sorted(g.bass), g.bass_notes):
                while beat - cursor > 1e-6:
                    nm, taken = _dur(beat - cursor)
                    toks.append(f"r{nm}")
                    cursor += taken
                idx = sorted(g.bass).index((beat, _k))
                nxt = (sorted(g.bass)[idx + 1][0] if idx + 1 < len(g.bass) else 4)
                nm, taken = _dur(max(0.25, nxt - beat))
                toks.append(f"{_ly_pitch(pitch, octv)}{nm}")
                cursor = beat + taken
            body = "\\clef bass " + " ".join(toks)
            staves.append(
                '\\new Staff \\with { instrumentName = \\markup { \\fontsize #-3 "'
                + _q(g.bass_name) + '" } } { ' + body + ' }')
        else:
            staves.append(
                '\\new RhythmicStaff \\with { instrumentName = \\markup { \\fontsize #-3 "'
                + _q(g.bass_name) + '" } } { \\improvisationOn '
                + rhythm_bar(g.bass) + ' }')
    if g.drums:
        staves.append(
            '\\new DrumStaff \\with { instrumentName = \\markup { \\fontsize #-3 "'
            + _q(g.drums_name) + '" } } \\drummode { ' + _drum_bar(g.drums) + ' }')
    if not staves:
        return ""
    return ("\n\\pageBreak\n\\markup \\column {\n"
            '  \\line { \\bold \\fontsize #2 "' + _q(g.label) + '" }\n'
            + ('  \\vspace #0.4\n  \\wordwrap-string #"' + _q(g.note) + '"\n'
               if g.note else "")
            + "  \\vspace #0.6\n}\n"
            + "\\score {\n  \\new StaffGroup <<\n    " + "\n    ".join(staves)
            + "\n  >>\n  \\layout {\n"
            + "    indent = 2.2\\cm\n"
            + "    \\context { \\Score\n"
            + "      \\override StaffGrouper.staff-staff-spacing ="
            + " #'((basic-distance . 6) (minimum-distance . 5) (padding . 0.5))\n"
            + "      \\override SystemStartBar.collapse-height = #1\n"
            + "    }\n  }\n}\n")


def build_lilypond(spec):
    chord_tokens, melody_tokens, lyric_tokens = [], [], []
    has_melody = any(s.melody for s in spec.sections)

    for si, sec in enumerate(spec.sections):
        label = sec.name.replace("_", " ").title()
        # The section name and its annotation go inside ONE rehearsal mark,
        # stacked. Attaching the annotation to a note instead would put it in
        # the lane the chord symbols already occupy, and would not attach at
        # all in the slash-notation sections, which begin with a command
        # rather than with a note.
        if sec.note:
            inner = (f'\\column {{ \\box \\bold "{_q(label)}" '
                     f'\\italic \\fontsize #-2 "{_q(sec.note)}" }}')
        else:
            inner = f'\\box \\bold "{_q(label)}"'
        mark = f'\\mark \\markup {inner} '

        bars = _bars_of(sec)
        first = True
        for ch in bars:
            tok = _ly_chord(ch)
            chord_tokens.append(tok)
            first = False

        if sec.melody:
            melody_tokens.append(mark)
            for pitch, octv, dur in sec.melody:
                if pitch == "r":
                    melody_tokens.append(f"r{dur}")
                else:
                    melody_tokens.append(f"{_ly_pitch(pitch, octv)}{dur}")
        elif sec.figure:
            # A fixed melodic figure: the guitar plays a riff, so the riff is
            # what goes on the staff, at its real pitches.
            melody_tokens.append(mark)
            for bi in range(len(bars)):
                if sec.figure_alternates and bi % 2 == 0:
                    melody_tokens.append("r1")
                    continue
                total = 0.0
                for midi, beats in sec.figure:
                    name, taken = _dur(beats)
                    melody_tokens.append(f"{ly_midi(midi, spec.flats)}{name}")
                    total += taken
                while 4 - total > 1e-6:
                    name, taken = _dur(4 - total)
                    melody_tokens.append(f"r{name}")
                    total += taken

        elif spec.voicings:
            # The part strums chords and the exact voicing is known, so the
            # notes go on the staff. A damped stroke keeps its pitches and
            # gets cross noteheads, which is how a muted strum is written.
            melody_tokens.append(mark)
            for ch in bars:
                notes = spec.voicings.get(ch)
                if not notes:
                    raise ValueError(f"{spec.title}: falta el voicing de {ch!r}")
                stack = "<" + " ".join(ly_midi(n, spec.flats) for n in notes) + ">"
                onsets = sorted(sec.rhythm or [(0, "hit")], key=lambda o: o[0])
                cursor = 0.0
                for i, (beat, kind) in enumerate(onsets):
                    while beat - cursor > 1e-6:
                        nm, taken = _dur(beat - cursor)
                        melody_tokens.append(f"r{nm}")
                        cursor += taken
                    nxt = onsets[i + 1][0] if i + 1 < len(onsets) else 4
                    nm, taken = _dur(max(0.25, nxt - beat))
                    if kind == "mute":
                        melody_tokens.append(
                            "\\once \\override NoteHead.style = #'cross "
                            f"{stack}{nm}")
                    else:
                        melody_tokens.append(f"{stack}{nm}")
                    cursor = beat + taken
                while 4 - cursor > 1e-6:
                    nm, taken = _dur(4 - cursor)
                    melody_tokens.append(f"r{nm}")
                    cursor += taken

        else:
            # Nothing pitched is known for this part, so it stays a rhythm
            # chart: the figure once, then the percent sign.
            melody_tokens.append(mark + "\\improvisationOn")
            cell = rhythm_bar(sec.rhythm)
            melody_tokens.append(cell)
            if len(bars) > 1:
                melody_tokens.append(
                    f"\\repeat percent {len(bars) - 1} {{ {cell} }}")
            melody_tokens.append("\\improvisationOff")

        if sec.lyrics:
            lyric_tokens.append(sec.lyrics)

    notes_block = ""
    if spec.footer_notes:
        items = "\n".join(
            f'    \\line {{ \\bold "{i + 1}." \\wordwrap-string #"{_q(t)}" }}'
            for i, t in enumerate(spec.footer_notes))
        notes_block = f"""
\\pageBreak
\\markup \\column {{
  \\line {{ \\bold \\fontsize #1 "Notas" }}
  \\vspace #0.4
{items}
}}
"""

    groove_block = _groove_block(spec.groove, spec)

    motif_blocks = ""
    for mo in spec.motifs:
        toks = " ".join(f"r{d}" if p == "r" else f"{_ly_pitch(p, o)}{d}"
                        for p, o, d in mo.melody)
        motif_blocks += (
            "\n\\markup \\vspace #1.6\n"
            "\\markup \\column {\n"
            '  \\line { \\bold \\fontsize #1 "' + _q(mo.label) + '" }\n'
            + ('  \\vspace #0.4\n  \\wordwrap-string #"' + _q(mo.note) + '"\n'
               if mo.note else "")
            + "  \\vspace #0.4\n}\n"
            + "\\score {\n  \\new Staff { \\key " + mo.key
            + " \\cadenzaOn " + toks
            + ' \\bar "|." }\n  \\layout { }\n}\n')

    lyrics_page = ""
    if spec.lyrics_text:
        blocks = []
        for label, lines in spec.lyrics_text:
            rows = "\n".join(
                '      \\line { \\wordwrap-string #"' + _q(l) + '" }'
                for l in lines)
            blocks.append(
                "\\markup \\column {\n"
                "  \\vspace #0.8\n"
                '  \\line { \\bold \\fontsize #1 "' + _q(label) + '" }\n'
                "  \\vspace #0.3\n" + rows + "\n}")
        lyrics_page = ("\n\\pageBreak\n\\markup \\vspace #0.5\n"
                       '\\markup { \\bold \\fontsize #3 "Letra" }\n'
                       + "\n".join(blocks) + "\n")

    lyric_block = ""
    if lyric_tokens:
        joined = "\n    ".join(lyric_tokens)
        lyric_block = f"""
      \\new Lyrics \\lyricsto "mel" {{
    {joined}
      }}
"""

    return f"""\\version "2.24.0"
\\header {{
  title = "{spec.title}"
  subtitle = "{spec.subtitle}"
  composer = "{spec.composer}"
  copyright = "{spec.copyright}"
  tagline = "{spec.tagline}"
}}

\\paper {{
  #(set-paper-size "a4")
  top-margin = 12\\mm
  bottom-margin = 12\\mm
  ragged-bottom = ##t
  ragged-last-bottom = ##t
}}

theChords = \\chordmode {{
  {' '.join(chord_tokens)}
}}

theMelody = {{
  \\key {spec.key}
  \\time {spec.time_sig}
  \\tempo 4 = {spec.bpm}
  {' '.join(melody_tokens)}
  \\bar "|."
}}

\\score {{
  <<
    \\new ChordNames {{ \\theChords }}
    \\new Staff = "main" \\with {{
      instrumentName = \\markup {{ \\fontsize #-2.5 "{spec.staff_name}" }}
    }} <<
      \\new Voice = "mel" {{ \\theMelody }}
    >>{lyric_block}
  >>
  \\layout {{
    \\context {{ \\Score
      \\override RehearsalMark.self-alignment-X = #LEFT
      \\override RehearsalMark.padding = #3.0
      barNumberVisibility = #(every-nth-bar-number-visible 4)
      \\override BarNumber.break-visibility = #'#(#f #t #t)
    }}
    \\context {{ \\Staff
      \\override TextScript.padding = #1.4
      \\override TextScript.outside-staff-priority = #250
    }}
    \\context {{ \\ChordNames
      \\override ChordName.padding = #0.8
    }}
  }}
}}
{groove_block}{motif_blocks}{notes_block}{lyrics_page}
"""


def _m21_chord(sym):
    """music21 spells flats with '-', not 'b'.

    This mattered more than it looks: the first version passed 'Bb' and
    'Bbm' straight through, music21 raised, and a bare `except: pass`
    swallowed it. Medio Limon silently lost 19 of its 76 chords - every
    borrowed iv in the piece - and the file still looked plausible.
    """
    m = re.match(r"^([A-G])(b|#)?(.*)$", sym)
    if not m:
        raise ValueError(f"chord symbol not understood: {sym!r}")
    root, acc, qual = m.group(1), m.group(2) or "", m.group(3)
    return root + acc.replace("b", "-") + qual


def _musicxml(spec, out_dir):
    """MusicXML alongside the PDF, so the score opens in notation software.

    This carries the same content as the PDF - chords, melody, lyrics,
    section names, tempo - rather than a skeleton of empty bars. It is the
    machine-readable copy of the work, so anything missing here is missing
    from the registration.
    """
    try:
        from music21 import (stream, harmony, note as m21note, meter,
                             key as m21key, tempo, metadata, expressions)
    except ImportError:
        return None, []

    dropped = []
    sc = stream.Score()
    sc.metadata = metadata.Metadata(title=spec.title, composer=spec.composer)
    part = stream.Part()
    part.partName = spec.staff_name or "Lead"

    beats_per_bar = int(spec.time_sig.split("/")[0])
    bar_no = 0
    first = True
    for sec in spec.sections:
        chords = _bars_of(sec)
        # The melody is a flat stream of (pitch, octave, duration); walk it
        # bar by bar so the notes land in the measure they belong to.
        mel = list(sec.melody)
        mi = 0
        for bi, ch in enumerate(chords):
            bar_no += 1
            m = stream.Measure(number=bar_no)
            if first:
                m.append(meter.TimeSignature(spec.time_sig))
                tonic, mode = spec.key.replace("\\", "").split()
                m.append(m21key.Key(tonic.upper() if mode == "major" else tonic.lower()))
                m.append(tempo.MetronomeMark(number=spec.bpm))
                first = False
            if bi == 0:
                m.insert(0, expressions.RehearsalMark(
                    sec.name.replace("_", " ").title()))
            try:
                m.insert(0, harmony.ChordSymbol(_m21_chord(ch)))
            except Exception as exc:
                dropped.append(f"{ch} (c.{bar_no}): {exc}")
            filled = 0.0
            while mi < len(mel) and filled < beats_per_bar:
                pitch, octv, dur = mel[mi]
                ql = 4.0 / dur
                if filled + ql > beats_per_bar:
                    break
                n = (m21note.Rest() if pitch == "r"
                     else m21note.Note(f"{pitch.replace('b', '-')}{octv}"))
                n.quarterLength = ql
                m.append(n)
                filled += ql
                mi += 1
            if filled < beats_per_bar:
                r = m21note.Rest()
                r.quarterLength = beats_per_bar - filled
                m.append(r)
            part.append(m)
    sc.append(part)
    path = os.path.join(out_dir, f"{spec.slug}.musicxml")
    sc.write("musicxml", fp=path)
    return path, dropped


def render(spec, song_dir):
    out_dir = os.path.join(song_dir, "partitura")
    os.makedirs(out_dir, exist_ok=True)
    ly_path = os.path.join(out_dir, f"{spec.slug}.ly")
    with open(ly_path, "w") as fh:
        fh.write(build_lilypond(spec))

    res = subprocess.run(
        ["lilypond", "--pdf", "-o", os.path.join(out_dir, spec.slug), ly_path],
        capture_output=True, text=True)
    pdf = os.path.join(out_dir, f"{spec.slug}.pdf")
    if res.returncode != 0 or not os.path.exists(pdf):
        raise RuntimeError(f"lilypond failed for {spec.title}:\n{res.stderr[-2500:]}")

    xml, dropped = _musicxml(spec, out_dir)
    if dropped:
        # Never silently. A chord missing from the machine-readable copy is a
        # chord missing from the registration.
        raise RuntimeError(f"{spec.title}: acordes perdidos en el MusicXML: "
                           + "; ".join(dropped))
    total_bars = sum(s.bars for s in spec.sections)
    print(f"  {spec.title}: {total_bars} compases -> {os.path.basename(pdf)}"
          + (f" + {os.path.basename(xml)}" if xml else ""))
    return pdf
