# Backing Track - Medio Limón

## Estilo
**Cumbia sonora chilena clásica** (linaje Sonora Palacios / Tommy Rey): la
cumbia brillante de intro de teleserie. No es la nueva cumbia de Chico Trujillo
(más cruda y con ska), ni vallenato.

El rasgo que define el estilo, según la propia historia del género: Sonora
Palacios **sacó el llamador colombiano del contratiempo y lo puso en el tiempo**,
con un cencerro marcando los cuatro tiempos del compás. Ese cambio es lo que hizo
la cumbia chilena bailable "para tiesos y cumbiancheros", y es el motor rítmico
de este arreglo. El formato instrumental viene de la Sonora Matancera cubana:
trompetas armonizadas al frente + percusión afrolatina.

## Archivo generado
**Ubicación**: `audio/backing_track_base.wav`
**Duración**: 133s (2:13) + cola de reverb
**Tempo**: 130 BPM, 4/4. El bombo pega en 1 y 3, o sea un pulso percibido de
**65 por minuto** — que era la velocidad pedida. (En v3 el tempo nominal era 102
con bombo en 1 y 3, lo que daba un pulso de 51: por eso se sentía lenta aunque
el número no lo pareciera.)
**Armonía**: C - Am - F - G7, en mayor. Se pasó de Re menor a Do mayor porque la
letra es celebratoria y la cumbia sonora clásica tiende a brillante.

## Historial de versiones

**v1 (rechazada)**: vallenato con acordeón, 100 BPM, MIDI cuantizado renderizado
en un solo pase mono y seco. Sonaba a caja de ritmos.

**v2 (rechazada)**: subió a 116 BPM y agregó jitter aleatorio. El jitter uniforme
no es humanización: suena desordenado, no humano. Seguía siendo vallenato y
seguía sin mezcla.

**v3 (rechazada)**: ya sonaba a música de verdad, pero apuntaba a la rama
equivocada del género (nueva cumbia tipo Chico Trujillo en vez de cumbia sonora)
y el pulso percibido era de 51/min, demasiado lento. Sus cuatro correcciones de
base se conservan:

1. **Género corregido**: cumbia chilena en vez de vallenato — metales, charchazo,
   güira, tumbao. El acordeón pasa a segundo plano.
2. **Humanización real**: en vez de ruido aleatorio, se modela cómo toca una banda
   de verdad — desfases *consistentes* por rol (el bajo adelanta ~11ms, los metales
   se atrasan ~14-18ms, la percusión es el ancla), swing en los contratiempos
   (5.5% del pulso), velocidades según la estructura de acentos musicales, y solo
   un ruido gaussiano pequeño encima (σ=7ms).
3. **Mezcla real**: cada instrumento se renderiza a su propio stem y recibe su
   cadena propia (EQ, compresión, paneo, ambiente). Esta es la causa más grande
   de que la música programada suene falsa, y en v1/v2 no existía.
4. **Gancho melódico**: riff de metales de 4 compases que abre la canción y vuelve
   en cada coro. v1/v2 eran solo acordes, sin melodía.

**v4 (actual)**: reorienta el estilo a cumbia sonora clásica. Cambios:
cencerro en los cuatro tiempos (el sello del género), 130 BPM, Do mayor, dos
trompetas armonizadas a tercera diatónica (formato sonora) en vez de una, riff
nuevo más brillante, y se elimina el acordeón (la sonora clásica no lo usa).

## Instrumentación (FluidR3_GM, samples reales)
| Instrumento | GM | Rol |
|---|---|---|
| Trompeta 1 | 56 | Riff principal (el gancho) |
| Trompeta 2 | 56 | Armonía a tercera diatónica bajo el lead |
| Trombón | 57 | Puntúa la raíz del acorde |
| Guitarra limpia | 27 | Charchazo: acordes cortos en los 4 contratiempos |
| Bajo eléctrico | 33 | Tumbao: raíz en 1, quinta en el "y" de 2, raíz en 3, nota de paso en el "y" de 4 |
| Órgano | 18 | Pegamento armónico (solo en secciones llenas) |
| Percusión | — | **Cencerro en los 4 tiempos (el sello)**, bombo en 1 y 3, caja en 4, side-stick en 2, güira en corcheas continuas, congas en los "y" de 2 y 4, fills de timbal |

## Balance de mezcla
Los niveles se fijaron **midiendo los stems**, no a ojo. El primer intento tenía
el bajo 21 dB sobre la percusión y 15 dB sobre la trompeta, lo que enterraba el
riff de metales y el groove. Balance final medido:

```
trompeta 1 -36.0 dB   ← el gancho, arriba
bajo       -37.0 dB
percusión  -37.3 dB   ← mueve la cumbia
guitarra   -38.1 dB
trompeta 2 -40.3 dB   ← armonía
trombón    -44.8 dB   ← apoyo
órgano     -47.5 dB   ← textura
```

## Control de calidad (medido)
```
Tempo detectado:       129.2 BPM (objetivo 130)      ✓
Pulso de bombo:        65 por minuto                 ✓ la velocidad pedida
Balance frecuencial:   graves 19%, low-mid 15%, medios 25%,
                       presencia 25%, agudos 12%     ✓ (v1 tenía 65% en graves)
Ancho estéreo:         44.1%                          ✓
Pérdida al sumar mono: -0.77 dB                       ✓ sin cancelación de fase
Pico:                  -1.2 dBFS                       ✓ sin clipping
Loudness:              -14 LUFS (estándar streaming)   ✓
```

## Estructura
```
intro       8 compases  (riff de metales, banda completa)
verse       8 compases  (guitarra + bajo + percusión, deja espacio a la voz)
pre_chorus  4 compases  (swell de metales ascendente, construye)
chorus      8 compases  (todo, vuelve el riff)
chorus      8 compases
verse       8 compases
pre_chorus  4 compases
chorus      8 compases
outro       8 compases
outro       8 compases  (con fade-out estilo 80s)
```

## Regenerar
```bash
python3 generate_backing_track.py
```
Escribe los stems en `audio/stems/` y la mezcla final en `audio/backing_track_base.wav`.

---
**Última versión**: v4, 2026-09-22
