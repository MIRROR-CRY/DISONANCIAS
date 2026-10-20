#!/usr/bin/env python3
"""Lead sheet for the untitled indie-folk track.

The structure and harmony are imported from the backing-track generator
rather than retyped, so the score cannot drift out of sync with the audio:
change SECTIONS there and the page changes here.

The song has no vocal melody or lyrics yet, so every section is a chord
chart. That is the honest state of the piece, and it is also what a
session player would be handed for a groove like this.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from score import SongSpec, Section, GrooveCell, render
import generate_backing_track as src

# Los cuatro patrones de mano derecha que toca el generador (STRUM_PATTERNS).
# Las secciones despojadas usan los sueltos, las llenas los densos, que es lo
# que hace el codigo al elegir por velocidad.
DENSO   = [(0, "hit"), (0.5, "hit"), (1, "hit"), (1.5, "hit"),
           (2, "hit"), (2.5, "hit"), (3, "hit"), (3.5, "hit")]
MEDIO   = [(0, "hit"), (0.5, "hit"), (1.5, "hit"),
           (2, "hit"), (2.5, "hit"), (3, "hit"), (3.5, "hit")]
SUELTO  = [(0, "hit"), (1, "hit"), (1.5, "hit"), (2, "hit"), (3, "hit"), (3.5, "hit")]

RITMO = {
    "intro": SUELTO, "verse": SUELTO, "pre_chorus": MEDIO,
    "chorus": DENSO, "bridge": SUELTO, "chorus_final": DENSO, "outro": DENSO,
}

SECTION_NOTES = {
    "intro": "solo guitarra acústica",
    "verse": "despojado",
    "pre_chorus": "entran palmas",
    "chorus": "entra el bajo, cello y pisadas",
    "bridge": "punto más bajo del arco",
    "chorus_final": "todo: 3 pisadas + 4 palmas + arpegio",
    "outro": "fade lineal de 4 compases",
}

spec = SongSpec(
    title="Sin titulo",
    subtitle="indie-folk  ·  track 4",
    composer="Emmanuel Ángel Blue Norambuena Sepúlveda",
    key="c \\major",
    bpm=src.BPM,
    time_sig="4/4",
    slug="sin_titulo_indie_folk",
    copyright="© Emmanuel Ángel Blue Norambuena Sepúlveda. Todos los derechos reservados.",
    staff_name="Guitarra",
    tagline="",
    voicings={k: v["gtr"] for k, v in src.CHORDS.items()},
    sections=[
        Section(name=kind, bars=bars, chords=cycle,
                note=SECTION_NOTES.get(kind, ""),
                rhythm=RITMO.get(kind, SUELTO))
        for kind, bars, cycle in src.SECTIONS
    ],
    groove=GrooveCell(
        label="El groove: pisadas y palmas",
        note="El estilo no está en la guitarra, está acá. Pisadas en 1 y 3, palmas "
             "en 2 y 4, y en las secciones más llenas las palmas empiezan a rellenar "
             "el contratiempo. No es una pista copiada más fuerte: son tres capas de "
             "pisadas y cuatro de palmas, cada una con su desfase propio de unos 10ms "
             "y su lugar en el estéreo. La dispersión entre capas ES el efecto.",
        guitar=DENSO, guitar_name="Guit.",
        drums=[(0, ["bd"]), (1, ["hc"]), (2, ["bd"]), (3, ["hc"]), (3.5, ["hc"])],
        drums_name="Pisadas/palmas"),
    footer_notes=[
        "Sin melodía vocal ni letra todavía: la canción está en etapa de base. "
        "Todas las secciones van como cifrado rítmico.",
        "Acordes en POSICIÓN ABIERTA, sin cejilla. Referencia: 'Ho Hey' de The "
        "Lumineers (79 BPM, Do mayor, C-F-C-Am).",
        "Sin modulación: el crecimiento del final es por acumulación de capas, no por "
        "cambio de tono, igual que en la referencia.",
        "El estilo son las pisadas y palmas, no la guitarra: tres capas de pisadas y "
        "cuatro de palmas, que entran de a poco. Pisadas en 1 y 3, palmas en 2 y 4. "
        "No están en pentagrama todavía y es lo que más falta en esta hoja.",
        "Las secciones se distinguen por densidad, no solo por armonía. "
        "El puente es el punto más bajo justo antes del punto más alto.",
    ],
)

if __name__ == "__main__":
    render(spec, os.path.dirname(os.path.abspath(__file__)))
