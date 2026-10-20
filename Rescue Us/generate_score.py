#!/usr/bin/env python3
"""Lead sheet for "Rescue Us" (track 2).

The structure is imported from the backing-track generator so the page and
the audio cannot drift apart. One point of translation: that generator
measures sections in SECONDS, because it is a synthesis script, with one
chord every 2.0s. Two seconds is one bar of 4/4 at 120, so the score
converts seconds to bars once, here, and notates the piece the way it is
actually felt.

Unlike the other three, this song has a written melody: the Gen Alpha
Melody is the hook and it runs unbroken from the first bar to the last.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from score import SongSpec, Section, Motif, render
import generate_backing_track as src

SEC_PER_BAR = src.CHORD_DURATION          # 2.0s, one chord per bar
BPM = int(round(4 * 60 / SEC_PER_BAR))    # 120

PROGRESSION = ["Dm", "G", "C", "F"]

# The Gen Alpha Melody: scale degrees 4 - 7 - 3 - 6, one pillar note per
# chord, held. In C that is F - B - E - A, which is what the generator
# synthesises, in one octave: F4 rises a tritone to B4, falls a fifth to E4,
# rises a fourth to A4. (An earlier comment here described it as falling
# twice. That would need B and A an octave down, and is not what is written
# or what the audio plays.) Each pillar note is the THIRD of its chord.
GEN_ALPHA = [("F", 4), ("B", 4), ("E", 4), ("A", 4)]

SECTION_NOTES = {
    "intro": "sirena de ambulancia antes del primer compás",
    "verse": "despojado, la voz manda",
    "pre_chorus": "construye",
    "chorus": "hook completo",
    "bridge": "entra el cello",
    "chorus_final": "versión más grande, sirena al cerrar",
}


def melody_for(bars, start_bar):
    """The hook, phase-locked to the chord loop, one whole note per bar."""
    return [(GEN_ALPHA[(start_bar + i) % 4][0],
             GEN_ALPHA[(start_bar + i) % 4][1], 1) for i in range(bars)]


sections, bar_cursor = [], 0
for kind, seconds in src.SECTIONS:
    bars = int(round(seconds / SEC_PER_BAR))
    sections.append(Section(
        name=kind, bars=bars,
        chords=[PROGRESSION[(bar_cursor + i) % 4] for i in range(bars)],
        melody=melody_for(bars, bar_cursor),
        note=SECTION_NOTES.get(kind, "")))
    bar_cursor += bars

spec = SongSpec(
    title="Rescue Us",
    subtitle="track 2  ·  antes titulada 36@24",
    composer="Emmanuel Ángel Blue Norambuena Sepúlveda",
    key="c \\major",
    bpm=BPM,
    time_sig="4/4",
    slug="rescue_us",
    copyright="© Emmanuel Ángel Blue Norambuena Sepúlveda. Todos los derechos reservados.",
    staff_name="Melodía",
    tagline="",
    sections=sections,
    motifs=[
        Motif(label="Motivo: cita de 'Dame Luz' (Nicole)",
              note="Aparece de forma espontánea en coros y puente, en guitarra aguda. "
                   "Cinco tiempos, cruza la línea divisoria, por eso va aparte y sin "
                   "indicación de compás. ATENCIÓN: es una cita de una obra ajena. "
                   "No forma parte de lo que se registra como propio.",
              melody=[("A", 4, 4), ("A", 4, 8), ("G", 4, 8), ("F", 4, 4),
                      ("A", 4, 8), ("B", 4, 8), ("C", 5, 4)]),
    ],
    footer_notes=[
        "La melodía escrita es la Gen Alpha Melody: grados 4-7-3-6 de la escala, "
        "en Do mayor F-B-E-A. Cada nota pilar es la TERCERA de su acorde. "
        "Contorno real: sube un tritono, baja una quinta, sube una cuarta.",
        "Esta melodía está escrita en redondas porque así la sintetiza el generador: "
        "es un pedal armónico, no el gancho rítmico definitivo. Cuando exista la línea "
        "vocal cantada habrá que transcribirla y reemplazar estas redondas.",
        "Armonía Dm-G-C-F: es un ciclo completo de quintas descendentes, ii-V-I-IV en "
        "Do mayor. Hay una V-I auténtica (G a C) en cada vuelta.",
        "Pero la pieza nunca cadencia en el tónico: empieza en Dm, termina en F, y las "
        "ocho secciones entran en Dm. La armadura de Do mayor describe el contenido; "
        "el énfasis está en Re. Es deliberado, y es lo que produce la sensación de "
        "bucle sin descanso.",
        "Las secciones se distinguen por instrumentación y densidad, no por cambio "
        "armónico.",
        "El generador mide las secciones en segundos porque sintetiza audio. "
        "2.0s por acorde equivale a un compás de 4/4 a 120.",
        "La línea vocal se canta sobre esta base y todavía no está transcrita. "
        "La letra va al final de esta partitura.",
    ],
    lyrics_text=[
        ("Verse 1", ["Bright, clear eyes... no fear in them",
                     "Light brown hair, drifts up to me",
                     "A voice that's calm, a steady hand",
                     "A smile that doesn't lie at all"]),
        ("Verse 2", ["Funny, but not trying hard",
                     "Smart enough to win the fight",
                     "Kind to strangers, kind to me",
                     "Ambitious, but still has time"]),
        ("Chorus", ["You'll rescue me", "I'll rescue you",
                    "Please, dear God", "Rescue us all"]),
    ],
)

if __name__ == "__main__":
    render(spec, os.path.dirname(os.path.abspath(__file__)))
