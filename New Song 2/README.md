# New Song 2: propuesta musical v1

Base instrumental etérea con **pocos sonidos a propósito**, para ir armando la
idea de a poco. Misma estructura de trabajo que Mirror Cry (secciones en
compases + curvas de presencia por instrumento), pero sintetizada con numpy puro:
no necesita FluidSynth ni SoundFont.

Escuchar: `new_song_2_base_v1.mp3` (2:13). Se regenera con `python build_song.py`
(requiere numpy; ffmpeg opcional para el mp3). Cada ejecución crea una versión
nueva en `versions/vN/` (mix + stems por instrumento, no se sube a git).

> Todo lo musical de abajo es **propuesta de la IA** para probar, no decisiones
> del autor. Tempo, tonalidad y progresión se pueden cambiar en las constantes
> del inicio de `build_song.py`.

## Parámetros propuestos

| Parámetro | Valor | Por qué |
|---|---|---|
| Compás | 3/4 | 6 corcheas por compás = los 6 golpes del patrón |
| Tempo | 60 BPM | Lento y flotante; *Runaway* de AURORA va a ~58 BPM |
| Tonalidad | La menor | Misma tonalidad de *Runaway* (según su partitura citada) |
| Progresión | Am - F - C - G | Un acorde por compás, ciclo de 4 compases |
| Duración | 44 compases (~2:12) | Cabe una letra de dos versos y coro |

## Patrón de gotas

La idea del autor: **pam, pam, pa, pam, pam, pam**. Cada compás tiene 6 corcheas y
cada una es una gota: la tercera ("pa") es más corta y suave. Cada gota cae en una
nota del acorde (raíz, tercera, quinta, octava), con pequeñas variaciones de
tiempo, volumen y afinación, y en un punto distinto del campo estéreo, más un eco
ping-pong y reverb larga para que floten.

Pregunta abierta del autor sin resolver: si esto es un 6/8 o un patrón que se
desfasa sobre 4/4. Acá se probó como compás fijo de 3/4.

## Estructura

| Sección | Compases | Qué suena |
|---|---|---|
| Intro | 0-8 | Solo gotas; el pad asoma en el compás 5 |
| Verso 1 | 8-16 | Gotas + pad |
| Verso 2 | 16-24 | + sub grave desde el compás 18 |
| Interludio | 24-28 | El pad se va; queda el eco de las gotas (el "respiro") |
| Coro | 28-36 | Todo: pad abierto, gotas agudas, sub y timbal grave desde el compás 32 |
| Outro | 36-44 | Todo se desvanece hasta una sola gota |

## Instrumentos (todos sintetizados)

| Instrumento | Descripción |
|---|---|
| `drops` | Gota: seno con glissando ascendente corto y caída exponencial |
| `drops_hi` | Gotas una octava arriba, más cortas; solo en el coro |
| `pad` | Acordes de senos con leve desafinación L/R para dar ancho |
| `sub` | Fundamental grave que sigue la progresión |
| `timbal` | Golpe grave y suave en el tiempo 1 de cada compás, solo en el coro |

No hay voz, melodía ni letra todavía: ese es el siguiente paso.

## Siguientes pasos posibles

1. Escuchar y ajustar: tempo, qué tan "gota" suena, cuánta reverb.
2. Probar la progresión Am-F-C-G contra otras (más modal, p. ej. Am-G-F-G).
3. Agregar una voz con capas tipo AURORA/Enya (por ahora, melodía guía).
4. Incorporar un instrumento acústico (violín como Skott, glockenspiel como Of
   Monsters and Men) o folk de Chile.
5. Escribir la letra desde el contexto sistémico (ver `REFERENCIAS.md` e
   `INVESTIGACION_NORDICOS_Y_CHILE.md`).
