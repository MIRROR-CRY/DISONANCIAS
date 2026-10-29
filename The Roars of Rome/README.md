# The Roars of Rome: propuesta musical

_(Antes llamada "New Song 2"; renombrada por el autor.)_

Base instrumental etérea con **pocos sonidos a propósito**, para ir armando la
idea de a poco. Misma estructura de trabajo que Mirror Cry (secciones en
compases + curvas de presencia por instrumento), pero sintetizada con numpy puro:
no necesita FluidSynth ni SoundFont.

Escuchar: `the_roars_of_rome_base_v1.mp3` (2:13). Se regenera con `python build_song.py`
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
no se sube a git) o `the_roars_of_rome_base_vN.mp3` (sí se sube).

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

## v4 y v5: melodía de piano (aclaración del autor)

El autor aclaró: las notas **Mi4 Re4 Si3** duran **un compás cada una**; el resto
(**Mi4 Re4 Do4 Sol4 Fa4 Mi4**) va en **negra y media (negra con puntillo) o dos
negras**. Y esto es la **melodía**, no la armonía: la armonía es el sintetizador de
pulso (**negra, negra, silencio**) que ya estaba en la v3.

| Versión | Rítmica de las 6 últimas notas | Frase |
|---|---|---|
| v4 `--rhythm dotted` | negra con puntillo (1,5 tiempos): dos por compás, caen exactas en las barras | 3 + 3 = 6 compases + 2 de respiro |
| v5 `--rhythm two` | dos negras (2 tiempos): 2 contra 3, cruzan la barra de compás | 3 + 4 = 7 compases + 1 de respiro |

Las dos caben en una frase de 8 compases (el largo de las secciones). Se repite en
el verso 1 (compás 8), verso 2 (16), coro (28) y outro (36, más suave). Entre
frases queda el pulso, las gotas y el resto de la base.

Notas sobre la armonía (Am F C G, un acorde por compás): en la v4 la frase cae
Mi4/Am, Re4/F, Si3/C, Mi4-Re4/G, Do4-Sol4/Am, Fa4-Mi4/F. Todas las notas caben en
La menor; el Si sobre C es la séptima mayor y el Mi sobre F también (color "maj7").

**Bemoles**: no hacen falta. Criterio del autor: un bemol solo se agrega si una nota
lo necesita para encajar en la escala y sonar bien, nunca de adorno. Todas las
notas de la melodía ya pertenecen a La menor natural, así que no se usa ninguno
(se quitó la opción `--flat`).

Cómo generar: `python build_song.py --waltz --piano --rhythm dotted|two --bpm 80`.
El piano es sintetizado (armónicos con caída rápida y pedal). No se pudo escuchar:
la duración y el solape se verificaron por el código, no de oído.

## v6 y v7: centro en Mi (Mi frigio)

Observación del autor: como la melodía vuelve tanto a Mi, siente que la escala tiene
**centro en Mi**. Es correcto, y explica por qué no hacen falta bemoles: las notas
**Mi Re Si Mi Re Do Sol Fa Mi**, sin alteraciones, son **Mi frigio** (Mi Fa Sol La Si
Do Re): Mi = 1.º, Fa = ♭2, Sol = ♭3, Si = 5.º, Do = ♭6, Re = ♭7. Los bemoles están
dentro del modo. La frase termina **Fa → Mi** (♭2 → 1.º), la cadencia frigia
clásica, la que da el color "español/andaluz" (conecta con *Hijo de la Luna*).

Con la armonía anterior (Am F C G) esa melodía se oía en La menor, con el Mi como
quinta. Para que el centro sea Mi se cambió la progresión (`--center e`), 8 compases:

| Compás | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Acorde | Em | F | G | Am | Em | F | Em | Em |
| Melodía (v6, puntillo) | Mi | Re | Si | Mi Re | Do Sol | Fa Mi | (respiro) | (respiro) |

- La melodía cae sobre notas del acorde (Mi/Em, Si/G como tercera, Fa/F como
  fundamental) y el **Fa→Mi del compás 6 resuelve en el Em del compás 7**.
- La progresión reinicia al empezar cada sección, para que cada frase empiece
  en el Em.
- Elección de la IA (no del autor): Em F G Am | Em F Em Em (i, ♭II, ♭III, iv). Hay
  más opciones frigias (p. ej. Em-F alternando, o un pedal de Mi).

Generar: `python build_song.py --waltz --piano --rhythm dotted|two --center e --bpm 80`.
Las v4/v5 (centro en La) quedan para comparar.

## Descartado: dos negras. Nueva opción: una negra

El autor descartó las seis últimas notas en **dos negras** y pidió probar con **una
negra** (`--rhythm one`): una nota por tiempo, tres por compás, así que las seis
ocupan 2 compases y la frase queda en 3 + 2 = **5 compases** (más 3 de respiro en
el bloque de 8). Opciones vigentes: `dotted` (negra con puntillo) y `one` (negra).

Generar la mezcla: `python build_song.py --waltz --piano --rhythm one --center e --bpm 80`
(v5 en esta tanda de archivos). Las versiones antiguas con dos negras se eliminaron.

## v7: mezcla con puntillo y pulso más etéreo

Pedido del autor: mezcla completa con la melodía en **negra con puntillo**, y el
sintetizador negra, negra, silencio más etéreo porque sonaba "muy encima" de los
demás sonidos. Cambios al `pulse`:

- Solo fundamental y un segundo armónico suave (antes 4 armónicos, más brillante).
- Ataque de 60 ms y salida de 250 ms (antes 10 y 30 ms): el acorde se asoma en
  vez de golpear.
- Ganancia de 0.28 a 0.17 y más reverb (mezcla 0.6, cola de 2.5 s).
- Consecuencia: la reverb llena un poco más el silencio del tiempo 3; sigue
  habiendo hueco, pero más suave.

Comando: `python build_song.py --waltz --piano --rhythm dotted --center e --sustain 2 --bpm 80`
(piano con sustain 2, elección de la IA; el autor pidió sustain para el piano solo).

## v8: piano más etéreo, pulso menos etéreo

Pedido del autor tras la v7 (se interpretó "tero" como "etéreo"):

- **Piano**: martillo más lento (15 ms), menos armónicos agudos, eco ping-pong,
  reverb más larga y más presente (mezcla 0.7, cola de 4.5 s), sustain 3.
- **Pulso**: de vuelta hacia más presencia, a medio camino entre la v3 y la v7:
  ataque 30 ms, salida 120 ms, cuatro armónicos suavizados y ganancia 0.24
  (v3: 0.28; v7: 0.17), reverb 0.4.

Comando: `python build_song.py --waltz --piano --rhythm dotted --center e --sustain 3 --bpm 80`.

## v9: versión larga (~3:00), partes como Mirror Cry

Pedido del autor: la letra se esboza aparte y **no debe cambiar la base sonora**; lo
que falta es extender la canción a unos 3 minutos para desarrollar todas las partes
como en Mirror Cry, y que **empiece con "Ooh Oooh oOOOooh"** (sonidos de "u").

> **Regla del autor:** la letra y la voz no afectan la base sonora y no se agregan a
> ella; las canta el autor. La base es solo instrumental y deja el espacio.
> (Una primera versión incluía un "ooh" sintetizado como marcador; se eliminó.)

Se agregó `--long` (requiere `--waltz`): 80 compases a 80 BPM en 3/4 = **3:01**. La
base musical (gotas, pad, marimba, pulso, piano, Mi frigio) es la de la v8.

| Sección | Compases | Qué pasa |
|---|---|---|
| Intro | 0-8 | Gotas + pulso; el pad entra en el compás 4. Espacio para el "Ooh Oooh oOOOooh" que canta el autor |
| Verso 1 | 8-16 | Gotas, pad, marimba suave; piano "fantasma" (nivel bajo) |
| Verso 2 | 16-24 | + sub y arpegio; piano fantasma |
| Interludio | 24-32 | La melodía de piano sola con el pulso (el "hook") |
| Puente | 32-40 | Se vacía; **el compás 39 queda en silencio total** (como el corte de Mirror Cry) |
| Coro 1 | 40-56 | Todo: gotas agudas, timbal, bajo, piano pleno, dos frases |
| Verso 3 | 56-64 | Baja la energía (después del coro, como en la última versión de Mirror Cry) |
| Coro 2 | 64-72 | Vuelve todo |
| Outro | 72-80 | Todo se desvanece hasta una gota |

- La progresión (Em F G Am | Em F Em Em) reinicia al empezar cada sección, así que
  cada frase de piano empieza en el Em.
- Los versos quedan con espacio para cantar (8 compases ≈ 18 s cada uno). Si hacen
  falta versos más largos, se pueden duplicar a 16 compases.
- La estructura de partes y los niveles de cada instrumento son propuesta de la IA,
  modelada sobre `SECTIONS` y `LEVELS` de Mirror Cry.

Comando: `python build_song.py --waltz --piano --rhythm dotted --center e --sustain 3 --long --bpm 80`
