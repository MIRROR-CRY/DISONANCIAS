#!/usr/bin/env python3
"""Partitura de "Kicking Stones" (track 1), deducida DEL MÁSTER.

Esta es la única canción del disco que está terminada y masterizada, así
que es la única donde se puede saber qué se cantó de verdad y no solo qué
se pensaba cantar. Y resulta que no son lo mismo.

Los nombres de sección de `build_song.py` registran la intención del
arreglo cuando se construyó, en mayo. El máster registra lo que se grabó.
Cruzando `lyrics_with_timestamps.txt` contra los compases, cuatro no
calzan:

  build_song.py   lo que de verdad hay ahí
  -------------   ---------------------------------------------
  rapfaster1      Verso 1 cantado normal. Nunca se grabó ningún rap.
  rapfaster2      Verso 2, igual.
  chorus1         Nadie canta. Es un interludio instrumental.
  verse1          EL CORO. La sección más importante del tema estaba
                  etiquetada como verso.

Además el máster dura 135.2s y `build_song.py` genera 124.9s: la pista
final tiene unos seis compases más de los que produce el generador, señal
de que se editó después de generarla.

Por eso esta partitura no importa SECTIONS del generador como hacen las
otras tres. Toma la forma de los timestamps del máster, que es el único
documento que describe la obra tal como existe. Para el registro en el DPI
eso no es un detalle: lo que se inscribe es la grabación que hay, no la
que se planeó.
"""

import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "..", "tools"))

from score import SongSpec, GrooveCell, sections_from_timestamps, render

BPM = 146
PROGRESSION = ["Am", "F", "G", "Em"]
MASTER = os.path.join(BASE, "final_master", "KickingStonesv5.mp3")

# Medido directamente del MIDI de la version masterizada
# (versions/v5/midi/): la guitarra toca cuatro corcheas al principio del
# compas y calla la segunda mitad; el bajo va en 1 y 3; la bateria lleva
# bombo en 1 y 3, caja en 2 y 4 y charles en todas las corcheas.
# La guitarra de esta cancion NO rasguea: toca un motivo melodico
# descendente, E4-D4-C4-A3, tomado de write_guitar_midi() en build_song.py y
# confirmado contra el MIDI de la version masterizada. En las secciones
# "sparse" suena un compas de por medio, en las llenas todos los compases.
MOTIVO = [(64, 0.5), (62, 0.5), (60, 0.5), (57, 1.0)]
GUITARRA = [(0, "hit"), (0.5, "hit"), (1, "hit"), (1.5, "hit")]
SOLO_PAD = [(0, "hit")]
# Donde la guitarra suena en todos los compases (coros y outro).
DENSAS = {"Coro", "Coro 2", "Post-Coro", "Outro"}

LABELS = {
    "Intro": "Intro", "Verse": "Verso", "Pre-Chorus": "Pre-Coro",
    "Chorus": "Coro", "Bridge": "Puente", "Post-Chorus": "Post-Coro",
    "Outro": "Outro", "Instrumental": "Instrumental",
}


def es(name):
    """'Verse 2' -> 'Verso 2'. El numero puede venir del sheet o de una
    repeticion detectada, y en los dos casos se conserva."""
    if name in LABELS:
        return LABELS[name]
    m = re.match(r"^(.+?) (\d+)$", name)
    if m and m.group(1) in LABELS:
        return f"{LABELS[m.group(1)]} {m.group(2)}"
    return name
SECTION_NOTES = {
    "Intro": "solo pad",
    "Verse 1": "voz y bajo",
    "Verse 2": "voz y bajo",
    "Verse": "voz y bajo",
    "Pre-Chorus": "entra batería y guitarra",
    "Chorus": "todo",
    "Bridge": "hablado, batería mínima",
    "Post-Chorus": "respuesta doblada",
    "Outro": "entra la guitarra solista",
}


def master_seconds():
    """La partitura dura lo que dura el disco, no lo que dura el script."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", MASTER], capture_output=True, text=True, check=True)
        return float(out.stdout.strip())
    except Exception:
        return None


sections, form = sections_from_timestamps(
    os.path.join(BASE, "lyrics_with_timestamps.txt"),
    bpm=BPM, progression=PROGRESSION, phrase=4,
    notes=SECTION_NOTES, instrumental_label="Instrumental",
    total_seconds=master_seconds())

# Los rótulos del sheet vienen en inglés; en la partitura van en español.
for sec in sections:
    sec.name = es(sec.name)
    if sec.name in ("Intro",):
        sec.rhythm = SOLO_PAD
    else:
        sec.figure = MOTIVO
        sec.figure_alternates = sec.name not in DENSAS


def read_lyrics():
    path = os.path.join(BASE, "lyrics")
    blocks, label, lines = [], None, []
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = re.match(r"^\[(.+?)\]\s*$", line.strip())
        if m:
            if label and lines:
                blocks.append((label, lines))
            label, lines = es(m.group(1)), []
        elif line.strip():
            lines.append(line.strip())
    if label and lines:
        blocks.append((label, lines))
    return blocks


spec = SongSpec(
    title="Kicking Stones",
    subtitle="track 1  ·  apertura del álbum",
    composer="Emmanuel Ángel Blue Norambuena Sepúlveda",
    copyright="© Emmanuel Ángel Blue Norambuena Sepúlveda. Todos los derechos reservados.",
    staff_name="Guitarra",
    key="a \\minor",
    bpm=BPM,
    time_sig="4/4",
    slug="kicking_stones",
    tagline="",
    sections=sections,
    groove=GrooveCell(
        label="El groove",
        note="Medido del MIDI de la versión masterizada, no reconstruido de oído. "
             "La guitarra no rasguea: toca un motivo melódico descendente, "
             "Mi-Re-Do-La, en la primera mitad del compás. Ese hueco en la segunda "
             "mitad es lo que deja respirar al tema a 146. En versos y pre-coro "
             "suena un compás de por medio; en coros y outro, todos. El bajo marca "
             "1 y 3.",
        guitar=GUITARRA, guitar_name="Guit.",
        bass=[(0, "hit"), (2, "hit")],
        bass_notes=[("A", 1), ("A", 1)], bass_name="Bajo",
        drums=[(0, ["bd", "hh"]), (0.5, ["hh"]), (1, ["sn", "hh"]), (1.5, ["hh"]),
               (2, ["bd", "hh"]), (2.5, ["hh"]), (3, ["sn", "hh"]), (3.5, ["hh"])],
        drums_name="Batería"),
    footer_notes=[
        "La forma de esta hoja está deducida del máster, cruzando los tiempos de "
        "entrada de cada línea cantada contra los compases. No sale de los nombres "
        "de sección del generador, que registran la intención del arreglo y no lo "
        "que terminó grabándose.",
        "En concreto: las partes que el generador llama 'rapfaster' llevan versos "
        "cantados normales, nunca se grabó rap ahí; la que llama 'chorus1' no tiene "
        "voz y acá va como Instrumental; y la que llama 'verse1' es el coro.",
        "Progresión i - VI - VII - v en La menor (Am - F - G - Em), un acorde por "
        "compás, sin una sola alteración accidental en toda la obra. Las secciones "
        "se distinguen por instrumentación y densidad, no por armonía.",
        "Tempo único de 146 para toda la canción. 146 no es un número elegido sino "
        "medido: la maqueta vocal cubre 8 compases (32 tiempos) en 13.15s.",
        "El outro lleva guitarra solista sobre la escala de La menor natural. Es una "
        "parte improvisada sobre la armonía, no una melodía fija, por eso no va escrita.",
        "La línea vocal todavía no está transcrita; la letra va al final de esta hoja "
        "con los tiempos de entrada del máster. Existe además una versión en español "
        "de la letra, en el archivo lyrics_es.",
    ],
    lyrics_text=read_lyrics(),
)

if __name__ == "__main__":
    print("  Forma deducida del máster:")
    for row in form:
        print(f"     {row}")
    render(spec, BASE)
