# Análisis de las tomas vocales limpias

Qué se puede y qué no se puede transcribir de las grabaciones de voz sola,
medido y no estimado a ojo.

## Qué hay

| Archivo | Duración | Contenido |
|---|---|---|
| `reference_takes/verse1_part1_take1.m4a` | 3.80s | Una línea del verso 1 |
| `mastered_reference/rap_faster_mastered.mp3` | 13.15s | Los 8 compases de la sección rápida |

Las dos son **voz sola**, confirmado: el detector de tono encuentra una línea
monofónica coherente en el 69-76% de los frames, en registro grave masculino.
No hay batería ni bajo encima.

Entre las dos suman **17 segundos de una canción de 135**, o sea el 13%.

## Las tomas están 30 cents bajas

| Archivo | Afinación respecto de La=440 |
|---|---|
| `verse1_part1_take1` | **-31 cents** |
| `rap_faster_mastered` | **-27 cents** |
| `final_master/KickingStonesv5.mp3` | +2 cents |

El máster está afinado; las tomas de voz no. Casi un tercio de semitono es
suficiente para que redondear las frecuencias al semitono más cercano, sin
corregir primero, mande como un tercio de las notas a la nota equivocada. El
transcriptor mide el desvío por archivo y lo resta antes de nada.

## El problema de fondo: la entrega es declamada, no cantada

Esto es lo que impide escribir una melodía, y no es un defecto de la
grabación ni del detector.

| | Frames en meseta (altura sostenida) | Tiempo dentro de ±20 cents de un semitono |
|---|---|---|
| `verse1_part1_take1` | 43% | **37%** |
| `rap_faster_mastered` | 44% | **32%** |
| Máster (tiene guitarra afinada, de referencia) | 59% | 50% |

Una voz cantada se posa en alturas discretas y se queda ahí: mesetas con
vibrato alrededor de una nota. Una voz declamada se desliza de forma continua
y no se posa en ninguna parte.

Estas tomas pasan **solo un tercio del tiempo cerca de una altura definible**.
Las consecuencias se ven directo en la salida del transcriptor:

- Desviación media del semitono: **24-29 cents**. Muchas notas caen a +49 o
  -45 cents, o sea exactamente entre dos semitonos: redondearlas es tirar
  una moneda.
- Solo el **54-56% de las notas extraídas cae dentro de La menor**. Una
  melodía cantada en La menor debería dar 85-95%. Aparecen La#, Do#, Re# y
  Sol#, que no pertenecen a la tonalidad; no son cromatismos deliberados,
  son el redondeo de un glissando.

**Conclusión:** escribir esas notas en la partitura sería inventar una
melodía que nadie está cantando. La altura no está indefinida por falta de
técnica de análisis: está indefinida porque la interpretación es declamada,
que para una canción de crítica es una decisión expresiva legítima.

## Lo que sí es dato firme

- **El registro**: la voz vive entre **La2 y Do#3**, centrada en La#2/Si2.
- **El ritmo**: las entradas de sílaba están bien definidas y, para la
  canción entera, ya están medidas en `lyrics_timing.json`.
- **El contorno**: sube y baja de forma consistente, aunque sin posarse.

Eso se notaría como **parlato** (cabezas de nota en cruz sobre una línea,
con indicación de registro), que es la convención estándar para una voz
declamada, y no como una melodía con alturas.

## Herramienta

`musica/tools/transcribe_vocal.py`. Corrige la afinación de la toma, segmenta
por onsets (no por estabilidad de altura: la primera versión agrupaba una
línea entera en una sola nota porque la mediana móvil se arrastra con la voz)
y toma la mediana del centro de cada nota, no la media, para que el ataque
deslizado no arrastre la altura.

Un detalle que costó encontrar: `voiced_prob` de pyin tiene **mediana 0.01**
en estas tomas aunque el detector entregue una f0 usable en el 70% de los
frames. Filtrar por esa probabilidad a 0.55 descartaba el 96% de los frames
buenos y la primera corrida no encontró casi ninguna nota. Hay que filtrar
por la bandera `voiced`, no por la probabilidad.

---
**Fecha**: 2026-09-23
