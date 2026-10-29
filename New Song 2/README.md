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

## ¿Coldwave en 3/4, como un vals? (consideración)

**Respuesta corta: sí se puede, y hay poco precedente, lo que lo hace distintivo.**
No es una certeza de la investigación sino una lectura de lo encontrado.

### Qué dicen las fuentes

- **Solo hay un ejemplo sólido** de la familia post-punk/gótica en 3/4: *Melt!*
  (Siouxsie and the Banshees, 1982), según la página Ethereal wave de Wikipedia.
  Es post-punk gótico, no coldwave estricto.
- **Indicios más débiles**: la misma página tiene una muestra de audio "en vals"
  de Cocteau Twins (ethereal wave) sin asignarla a una canción con partitura, y
  una base colaborativa (GetSongBPM) lista *Theft, and Wandering Around Lost* de
  Cocteau Twins en 3/4 a 149 BPM. No son partituras.
- **No se encontró ningún coldwave confirmado en 3/4 ni 6/8.** Joy Division,
  Xmal Deutschland, Minimal Compact, Asylum Party, Kas Product, The Cure
  (*Disintegration*) y Bauhaus no tienen compás confirmado en las fuentes leídas.
  Esto puede ser una laguna de la búsqueda más que una ausencia real.
- Más cerca de nuestro caso: *Hijo de la Luna* (Mecano), synth-pop/new wave en
  3/4 según una sola fuente.

### Cómo se adaptaría el sonido de Mirror Cry (inferencia, sin fuente)

El corazón del coldwave de Mirror Cry es el bajo galopante en corcheas sobre una
batería motorik, a 156 BPM. En 3/4 eso se puede conservar así:

| Elemento | Mirror Cry (4/4) | Vals frío (3/4) propuesto |
|---|---|---|
| Acentos | 1 y 3 fuertes | 1 fuerte, 2 y 3 más suaves (esquema estándar del 3/4) |
| Bombo / caja | bombo 1-3, caja 2-4 | bombo en 1, caja o hi-hat en 2 y/o 3 |
| Hi-hat | corcheas | 6 corcheas por compás (ya es el pulso de las gotas) |
| Bajo | galope de corcheas | corcheas con la raíz en el 1; o tresillos para el galope |
| Guitarra | arpegio con chorus | arpegio de 6 corcheas por compás, frío y con eco |

Un efecto buscado: el patrón de gotas de la idea (`pam pam pa pam pam pam`) ya son
6 corcheas por compás, así que **el coldwave en 3/4 y las gotas comparten la
misma rejilla**. La batería y el bajo podrían ser el "esqueleto" que marca el
vals, y las gotas la capa etérea encima.

### Riesgo / decisiones abiertas

- Un tempo rápido (>130) en 3/4 se oye como vals vienés o jig; el coldwave en
  ternario funciona mejor ~90-120 BPM (a verificar al oído, sin fuente).
- ¿Un solo carácter (frío y pulsante) o dos secciones (versos etéreos a 60 BPM,
  coro con motor coldwave)? Se puede probar como contraste entre secciones.

### Siguiente paso posible

Una variante `v2` de `build_song.py` con batería y bajo coldwave en 3/4 (bombo
en 1, hi-hat en corcheas, bajo galopante) en el coro, para comparar contra la v1
puramente etérea. Falta tu visto bueno y decidir el tempo.

## v2: vals coldwave (hecha)

`python build_song.py --cold --bpm 100`. Misma base de la v1 a **100 BPM**, más una
capa coldwave en 3/4 (propuesta de la IA, tempo elegido por la IA sin escuchar):

| Capa | Dónde | Qué hace |
|---|---|---|
| `kick` | coro | Bombo en el tiempo 1 |
| `snare` | coro | Caja seca en los tiempos 2 y 3 |
| `hat` | desde el compás 18 (suave), coro a pleno | 6 corcheas por compás, acento en el 1 |
| `bass_cold` | coro | Bajo galopante: la raíz en cada corchea, saturado |
| `arp` | desde el compás 22 | Arpegio frío pulsado con eco ping-pong |

A 100 BPM la canción dura 1:20 (la v1, a 60 BPM, dura 2:13), así que las gotas
suenan más rápidas y menos "flotando". Para comparar, la v1 sigue siendo la
referencia etérea pura. Ambas se escuchan como `.wav` (`versions/vN/mix.wav`,
no se sube a git) o `new_song_2_base_vN.mp3` (sí se sube).

## v3: vals sin batería (marimba + sintetizador de pulso)

`python build_song.py --waltz --bpm 80`. Feedback del autor sobre la v2: le gustan
las gotas, no le gustó la batería; propone usar otra percusión (marimba) y que un
sintetizador acompañe toda la canción con **negra, negra, silencio de negra** en
cada compás para que se sienta más 3/4.

- Se quitan bombo, caja y hi-hat.
- `pulse` (sintetizador): acorde en el tiempo 1 y en el 2, silencio en el 3, en
  cada compás, de principio a fin. Notas cortas para que el silencio se oiga; la
  reverb deja una cola, así que el tiempo 3 queda más suave, no totalmente mudo.
- `marimba`: la raíz grave en el 1 y notas del acorde en el 2 y el 3 (el
  "boom-chick-chick" del vals), con eco ping-pong. Entra suave en los versos y
  llena en el coro.
- Se mantienen el bajo galopante y el arpegio de la v2 (el autor no los criticó;
  se pueden quitar).
- 80 BPM es elección de la IA, un punto medio entre la v1 (60) y la v2 (100).

## v4 y v5: piano con el motivo del autor

Idea del autor: la armonía puede ser un piano con **Mi4 Re4 Si3 · Mi4 Re4 Do4 ·
Sol4 Fa4 Mi4** ("algo así"), y quizá algunas notas bemoles. Se pidió ordenar los
intervalos manteniendo la idea.

### Lectura del motivo

Son tres células de tres notas, cada una cayendo por grados y con un salto hacia
arriba entre una y otra:

| Compás | Acorde | Notas | Intervalos |
|---|---|---|---|
| 1 | Am | Mi4 Re4 Si3 | 2.ª mayor ↓, 3.ª menor ↓ |
| 2 | F | Mi4 Re4 Do4 | 2.ª mayor ↓, 2.ª mayor ↓ (salto 4.ª justa ↑ desde el Si3) |
| 3 | C | Sol4 Fa4 Mi4 | 2.ª mayor ↓, 2.ª menor ↓ (salto 5.ª justa ↑ desde el Do4) |
| 4 | G | Re4 largo | sostenido, deja respirar antes de repetir |

- **Todas las notas ya caben en La menor** (no hacen falta alteraciones): el Si
  sobre Am es una novena, el Mi sobre F es una séptima mayor (color "maj7"), y
  Sol-Fa-Mi sobre C es quinta-cuarta-tercera. Se dejaron los intervalos de la idea
  original sin cambios (**v4**).
- El motivo calza justo con la progresión Am-F-C-G de 4 compases: tres grupos de
  tres notas y un cuarto compás de reposo. Cae una nota por tiempo del 3/4, y el
  tiempo 3 coincide con el silencio del sintetizador de pulso, así que
  el piano responde donde el pulso calla.

### Dónde entra el bemol (v5)

El Si3 pasa a **Si♭3**: la tonalidad se vuelve La frigio (La Si♭ Do Re Mi Fa Sol),
el modo "español/andaluz", que además conecta con *Hijo de la Luna* y su leyenda
gitana. Efectos: el Re→Si♭ baja una 3.ª mayor (en vez de menor) y el Si♭→Mi
sube un **tritono**, un intervalo duro, de tensión. Rozará con el La y el Mi del
acorde. Es disonancia a propósito (el álbum se llama DISONANCIAS), pero si es
demasiado, la v4 es el respaldo.

Se probó solo un bemol por ser el único que cabe sin chocar de frente con el
acorde de Do (Mi♭ sobre C chocaría con el Mi del pad). Si el autor tenía en mente
otros bemoles, hay que decir cuáles.

### Cómo generar

- v4: `python build_song.py --waltz --piano --bpm 80`
- v5: `python build_song.py --waltz --piano --flat --bpm 80`

El piano entra en el compás 8 (verso 1) y suena hasta el final. Es un piano
sintetizado (armónicos con caída rápida y pedal); la verificación de las notas se
hizo por el código y por análisis de frecuencias, no de oído.
