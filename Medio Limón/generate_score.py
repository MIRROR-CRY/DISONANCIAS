#!/usr/bin/env python3
"""Lead sheet for "Medio Limon" (track 3, la unica en espanol).

Estructura y armonia importadas del generador, no retipeadas: si cambia
SECTIONS alla, cambia la pagina aca.

La armonia de esta cancion no se invento. Sale de las cifras publicadas de
las dos referencias (Carlos Vives, "Volvi a Nacer" y "Cuando nos volvamos a
encontrar"), y los dos recursos que la definen estan anotados abajo: el
cuarto grado menor prestado y las dominantes secundarias.
"""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from score import SongSpec, Section, Motif, GrooveCell, render
import generate_backing_track as src

# El rasgueo real del paseo, tal como lo toca el generador:
#   1      &        2        &        3      &        4        &
#   bajo   ataque   APAGADO  ataque   bajo   ataque   APAGADO  ataque
PASEO = [(0, "hit"), (0.5, "hit"), (1, "mute"), (1.5, "hit"),
         (2, "hit"), (2.5, "hit"), (3, "mute"), (3.5, "hit")]
# La intro entra mas suelta, solo los bajos y el ultimo ataque.
INTRO_RASGUEO = [(0, "hit"), (2, "hit"), (3.5, "hit")]

SECTION_NOTES = {
    "intro": "acordeón presenta el hook",
    "verse": "despojado: guitarra, bajo y percusión",
    "pre_chorus": "acordeón ascendente",
    "chorus": "entra todo",
    "outro": "coro x2 con fade-out",
}


def read_lyrics():
    """La letra vive en lyrics/lyrics.txt, no duplicada aca."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "lyrics", "lyrics.txt")
    blocks, label, lines = [], None, []
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = re.match(r"^\[(.+?)\](.*)$", line.strip())
        if m:
            if label and lines:
                blocks.append((label, lines))
            label = (m.group(1) + m.group(2)).strip()
            lines = []
        elif line.strip():
            lines.append(line.strip())
    if label and lines:
        blocks.append((label, lines))
    # El outro repite el coro entero; en la partitura basta la indicacion.
    return [(l, ls) for l, ls in blocks if not l.lower().startswith("outro")]


spec = SongSpec(
    title="Medio Limón",
    subtitle="tropipop  ·  track 3  ·  antes titulada Patio de los Naranjos",
    composer="Emmanuel Ángel Blue Norambuena Sepúlveda",
    key="f \\major",
    bpm=int(round(src.BPM)),
    time_sig="4/4",
    slug="medio_limon",
    copyright="© Emmanuel Ángel Blue Norambuena Sepúlveda. Todos los derechos reservados.",
    staff_name="Guitarra",
    tagline="",
    flats=True,
    # Los voicings exactos que toca el generador, no una version idealizada.
    voicings={k: v["gtr"] for k, v in src.CHORDS.items()},
    sections=[Section(name=kind, bars=bars, chords=cycle,
                      note=SECTION_NOTES.get(kind, ""),
                      rhythm=PASEO if kind != "intro" else INTRO_RASGUEO)
              for kind, bars, cycle in src.SECTIONS],
    groove=GrooveCell(
        label="El rasgueo del paseo",
        note="Esto es lo que hace que suene a paseo y no a cumbia. La cabeza "
             "en cruz es el apagado: la mano derecha golpea las cuerdas apagadas "
             "contra el diapasón y suena percutido, no afinado. Donde la partitura "
             "mostraría un silencio, se golpea. El bajo anticipa la raíz del acorde "
             "siguiente en el 'y' del tiempo 4, ligada sobre la línea divisoria: esa "
             "síncopa es la que tira hacia adelante. La guacharaca raspa semicorcheas "
             "sin parar, unas siete por segundo.",
        guitar=PASEO, guitar_name="Guit.",
        bass=[(0, "hit"), (1.5, "hit"), (2, "hit"), (3.5, "hit")],
        bass_notes=[("F", 2), ("F", 3), ("C", 3), ("Bb", 2)],
        bass_name="Bajo",
        drums=[(0, ["bd", "cabasa"]), (0.25, ["cabasa"]), (0.5, ["cabasa"]),
               (0.75, ["cabasa"]), (1, ["bd", "sn", "cabasa"]), (1.25, ["cabasa"]),
               (1.5, ["cabasa"]), (1.75, ["cabasa"]), (2, ["bd", "cabasa"]),
               (2.25, ["cabasa"]), (2.5, ["cabasa"]), (2.75, ["cabasa"]),
               (3, ["bd", "sn", "cabasa"]), (3.25, ["cabasa"]), (3.5, ["cabasa"]),
               (3.75, ["cabasa"])],
        drums_name="Caja/guach."),
    footer_notes=[
        "Aire: paseo vallenato, en cuatro tiempos. Ojo que la frase corriente 'el "
        "vallenato va en 2/4' es falsa: el son va en 2/4, pero el merengue y la puya "
        "van en 6/8. El paseo se escribe en 2/4 y se cuadra en cuatro.",
        "El rasgueo no toca acordes sostenidos: donde la partitura muestra silencio "
        "se golpean las cuerdas apagadas con la mano derecha. Ese golpe percutido en "
        "2 y 4 es el motor del ritmo, sin él la canción arrastra a cualquier tempo.",
        "Bbm en el coro es el cuarto grado menor prestado: Bb - Bbm - F es IV - iv - I. "
        "Ese giro agridulce sale de las cifras de las referencias, no es invención.",
        "A7 en el compás 4 del verso es V7/vi, pero NO resuelve a Dm: el Dm ya pasó en "
        "el compás 3 y el A7 va a Bb. Es una resolución deceptiva a IV, o si se prefiere "
        "leerlo local, un acorde cromático de paso con el bajo subiendo La - Si bemol.",
        "El bajo anticipa la raíz del acorde siguiente en el 'y' del tiempo 4, "
        "ligada sobre la línea divisoria. Esa síncopa es la que tira hacia adelante. "
        "No está cifrada en esta hoja: va escrita en el generador de audio.",
        "Tempo: 105.5. Viene de un conteo del autor sobre la referencia, 22 pulsos en "
        "12.49s. Ojo que 22 pulsos son 21 intervalos, o sea 100.9 por minuto; según "
        "cómo se contó, el tempo real está entre 101 y 106 y queda por confirmar.",
        "La línea vocal se canta sobre esta base y todavía no está transcrita.",
        "La canción termina en C, o sea en dominante, con fade-out. Es deliberado: "
        "no resuelve.",
    ],
    lyrics_text=read_lyrics(),
)

if __name__ == "__main__":
    render(spec, os.path.dirname(os.path.abspath(__file__)))
