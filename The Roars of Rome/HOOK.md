# The Roars of Rome: cómo potenciar el hook sin perder la esencia

Pregunta del autor: ¿cómo hacer que en ~5 segundos la gente note que quiere seguir
escuchando, sin perder lo esencial de la canción? La investigación la hicieron
agentes de IA leyendo la web. **Los datos con fuente van marcados; las propuestas
de abajo son de la IA y no están aplicadas al audio.**

## Lo esencial que no se toca (según lo dicho por el autor)

- Etérea, con las gotas flotando (`pam pam pa pam pam pam`).
- 3/4 como vals, 80 BPM, centro en Mi (Mi frigio), el pulso negra-negra-silencio.
- La melodía de piano Mi Re Si · Mi Re Do Sol Fa Mi.
- Crece de a poco, como un rugido, algo estilo Hans Zimmer.
- La letra y la voz (incluido el "Ooh Oooh oOOOooh") las canta el autor.

## Qué dice la evidencia

**Estudios y datos**

- Análisis de datos de Spotify (Paul Lamere, 2014): el **24 %** de las reproducciones
  se saltan en los primeros 5 s y el **35 %** en los primeros 30 s. Es de un solo
  analista, con datos no publicados por Spotify y de hace más de diez años.
  ([The Skip](https://musicmachinery.com/2014/05/02/the-skip/))
- Léveillé Gauvin (*Musicae Scientiae*, 2017), top 10 de Billboard 1986-2015: las
  intros pasaron de más de 20 s a mediados de los 80 a unos 5 s hoy, y el tempo
  subió ~8 %. ([OSU](https://news.osu.edu/has-music-streaming-killed-the-instrumental-intro/))
- Jakubowski y otros (2016), 3 000 participantes: los *earworms* (melodías que se
  pegan) tienen **contornos melódicos más comunes**, **intervalos menos comunes** y
  **tempo más rápido** que otras canciones. ([resumen](https://neurosciencenews.com/song-stuck-in-head-5423/amp/))
- Margulis, *On Repeat* (2014): la repetición aumenta el disfrute (fuente de prensa,
  no el paper). Burgoyne y otros (ISMIR 2013): el reconocimiento de segmentos
  varía; la gente predice mal qué recordará.

**No confirmado:** la cifra "el oyente decide en 5 s" (atribuida a NYU, solo por un
blog); cifras de saltos por género; "intros de 5 a 15 s" como regla.

**Opiniones de blogs** (no estudios): abrir con el motivo principal reducido,
filtrar un fragmento del estribillo y abrir el filtro, empezar con "versión
despojada" del hook. Sirven como ideas, no como prueba.

## Qué hacen canciones parecidas (con fuente, solo lo confirmado)

- **AURORA, *Runaway***: producción escasa con efectos de gotas de agua, chirridos y
  transiciones de viento (Wikipedia); piano que termina antes del primer verso
  (resumen de búsqueda de Song Exploder, no verificado).
- **Enya, *Orinoco Flow***: casi sin sintetizadores; la voz de Enya apilada hace de
  pad; ensamble de cuerdas en vivo y timbales (The Ringer); reverb Lexicon 224XL
  (Sound on Sound, 1989).
- **Of Monsters and Men, *Little Talks***: riff de piano/acordeón, diálogo entre las
  dos voces, coro con mucha reverb (Wikipedia, USA Today).
- **Vangelis, *Chariots of Fire***: piano acústico con Yamaha CS-80 sobre pulso
  electrónico y percusión.
- **Sigur Rós, *Hoppípolla***: arranca con piano, entra la batería y las cuerdas,
  voz muy doblada; crece hacia metales.
- **Hans Zimmer, *Time***: termina con una versión mínima del tema en piano.
- **Mecano, Skott, Björk, Bon Iver, Florence, Lorde**: no se encontró análisis de
  sus aperturas.

**Síntesis (inferencia de la IA, no estudio):** en estos casos el gancho no es un
evento fuerte sino una **textura reconocible en la primera escena**: un timbre
propio (CS-80, voz apilada, piano), un motivo corto que vuelve y una dinámica que
se abre sin acelerar. Eso encaja con la esencia de esta canción.

## Cómo abre hoy la canción (v10)

- Durante los primeros 18 s solo hay gotas, pulso y pad (el pad entra en el segundo
  9). El nivel es bajo y casi plano (RMS ~0,02, contra ~0,06 en los versos).
- La melodía de piano, lo más reconocible, entra recién en el segundo 18 (y como
  "fantasma", bajo, bajo los versos); suena plena en el segundo 54 (interludio).
- El patrón de gotas ya está en el segundo 0, pero con poca presencia.
- Rasgos a favor de ser pegadiza (Jakubowski): contorno descendente por grados
  conjuntos. En contra: tempo lento (80 BPM), con nada que haya que cambiar.

## Opciones (propuestas de la IA) y cuánto tocan la esencia

| # | Idea | Qué cambia | Riesgo para la esencia |
|---|---|---|---|
| 1 | **Gotas como firma desde el segundo 0**: subir su presencia y afinar su timbre (más cristalino) para que sean la "marca" | Nivel y timbre de las gotas en la intro | Bajo: ya es parte de la esencia |
| 2 | **Intro más corta**: de 8 a 4 compases (~9 s en vez de 18 s) | Estructura | Medio-bajo: se acerca a la tendencia de intros cortas; el "ooh" tiene menos espacio |
| 3 | **Abrir con el motivo en piano**: los primeros dos compases ya tienen Mi y Re (la melodía) antes de las gotas | Orden de entrada | Medio: la melodía suena antes que el resto del mundo sonoro |
| 4 | **Nivel inicial más alto**: la intro hoy es casi 3 veces más baja que los versos | Mezcla | Bajo, pero conviene cuidar el "crece de a poco" |
| 5 | **Un adelanto del hook al inicio** (flash de 1 compás de la melodía + silencio, y luego la intro) | Estructura | Medio-alto: es un truco de apertura que cambia la sensación de la intro |
| 6 | **El "Ooh" del autor entre los 2 y 5 s** (lo cantas tú) | Posición de la voz | Bajo: ya estaba previsto abrir con él; solo habría que adelantarlo |
| 7 | **Repetir la melodía más veces** en la canción (Margulis) | Más frases de piano en versos | Bajo-medio |

**Lo que menos recomienda la evidencia:** poner el coro o un golpe fuerte al segundo
0. Eso contradiría "crece de a poco" y no es lo que hacen las canciones parecidas.

## Sugerencia de prueba

Probar por separado, en A/B contra la v10, con tu oído como juez:

- **A**: 1 + 4 (gotas con más presencia y nivel inicial más alto).
- **B**: A + 2 (más la intro de 4 compases).
- **C**: A + 3 (más el motivo de piano desde el inicio).

Ninguna de esas se ha generado todavía.

## Pruebas generadas (v11, v12, v13)

El autor aceptó la sugerencia de prueba. Se agregó `--hook a|b|c` a `build_song.py`
(requiere `--long`), todas con el piano en negras y sustain 1,6 como la v10:

| Versión | `--hook` | Qué cambia respecto a la v10 | Duración |
|---|---|---|---|
| v11 | `a` | Gotas con más presencia (nivel inicial ×1,5 que baja a ×1 en el compás 8), timbre más cristalino (parcial agudo corto en cada gota), pulso ×1,3 al inicio y el pad entra desde el compás 1-3 | 3:01 |
| v12 | `b` | A, con los 4 primeros compases de la intro recortados | 2:52 |
| v13 | `c` | A, con el motivo de piano (Mi, Re, Si...) desde el compás 0 | 3:01 |

Nivel medio (RMS) de los primeros 5 s: v10 0,023; A 0,037; B 0,043; C 0,069. Por
comparación, en la v10 los versos rondan 0,06. Ojo: el timbre más cristalino de A
se aplica a todas las gotas de la canción, no solo a la intro.

Comandos: `python build_song.py --waltz --piano --rhythm one --center e --sustain 1.6 --long --bpm 80 --hook a|b|c`.

No se han oído; falta que el autor elija o combine.

## v14: las tres ideas juntas + crescendo en el puente

Pedido del autor: combinar A, B y C y que **fluya algo más**, para que tenga potencial
viral sin perder identidad. Se agregó `--hook abc`:

- **A + B + C:** gotas con más presencia y timbre cristalino, intro recortada 4
  compases (empieza 9 s adentro) y el motivo de piano (Mi Re Si · Mi Re Do Sol Fa Mi)
  desde el primer compás que se escucha. Como B recorta el inicio, la frase de piano
  se movió al compás 4 y termina al llegar el verso 1 (por eso el verso 1 no lleva su
  frase "fantasma"; sí la llevan los demás versos).
- **Fluir (interpretación de la IA):** en el puente, el pad, la marimba, las gotas
  agudas y el timbal crecen hasta el compás de silencio; después entra el coro. Se
  subió el nivel de marimba y arpegio en el verso 1 y el subgrave en el interludio
  para que el nivel no baje tanto entre secciones.
- Duración 2:52. Nivel de los primeros 5 s: 0,064 (la v10 tenía 0,023). Nivel por
  sección, aproximado: intro 0,065 · verso 1 0,057 · verso 2 0,075 · interludio 0,070
  · puente 0,060 · coro 0,102 · verso 3 0,077 · coro 2 0,105 · outro 0,048.
- No se garantiza "viral": nada de lo investigado lo asegura; esto solo aplica lo
  que la evidencia sugiere sobre los primeros segundos y la repetición del motivo.

Comando: `python build_song.py --waltz --piano --rhythm one --center e --sustain 1.6 --long --bpm 80 --hook abc`.
