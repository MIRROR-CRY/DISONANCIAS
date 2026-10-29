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

## v14 (ajuste): el compás del drop ya no es silencio total

Reporte del autor: el silencio total antes del coro suena incómodo (awkward) frente al
de Mirror Cry. Diagnóstico: en Mirror Cry el último compás del puente es el "drop
silencioso" donde **queda el bombo**, no un corte a cero; aquí el compás 39 se
multiplicaba por 0 y se cortaba también la cola de la reverb de golpe.

Cambio (compás 39 del largo, afecta a todas las versiones `--long` al regenerarlas):

- Todo se **agacha a 0,15** (en vez de 0), con bajada de 0,3 s y subida de 0,12 s al
  entrar el coro: queda como un susurro, con las colas de reverb.
- El **timbal queda fuera del recorte**: es el "bombo" que sigue sonando, como en
  Mirror Cry.
- Nivel medio medido: compás 38 0,080 · compás 39 0,033 · compás 40 (coro) 0,110.

Si sigue sonando raro, alternativas: bajar menos (0,3), dejar solo una gota en vez del
timbal, o un crescendo sin ningún hueco.

## v14 y v15: el drop antes del coro, como en Mirror Cry

Reporte del autor: el corte en 1:18 (compás 39) sigue sonando raro. Se midió Mirror Cry
(v13) y se buscaron técnicas (Faderpro, Lyric Assistant; el resto de las fuentes dio 403 o
estaba truncado).

**Lo que hace Mirror Cry (medido):** un solo golpe de bombo en el tiempo 1; el sonido cae
de ~0,10 a ~0,01 en ~0,3 s; ~1,2 s de casi silencio total (≈ 3 tiempos a 156 BPM); el
coro entra de golpe, en el tiempo 1, más fuerte que antes (de ~0,001 a 0,09-0,14), con
platillo y todos los instrumentos a la vez. Antes del corte viene su parte más intensa.

**Por qué el nuestro seguía raro (hipótesis):**

- La pausa duraba 2,25 s (un compás a 80 BPM), casi el doble que en Mirror Cry, en una
  canción lenta.
- Agachaba todo a 0,15: suena a bajón de volumen, no a corte.
- No había un golpe claro que marcara el tiempo 1 ni un impacto al entrar al coro.

**Lo que dicen las fuentes (poca evidencia):** de unos "pocos tiempos" a un compás de
silencio (Faderpro); "un tiempo de silencio" que termina justo en el tiempo 1 del coro
(Lyric Assistant); dejar un golpe o un "bass boom" (Faderpro); cortar las colas de
reverb juntas en la misma posición (snippet de MusicRadar, no confirmado); un lift
tardío o un riser más fuerte que el coro son errores comunes. No se encontró nada
sobre pausas en canciones lentas, ternarias o sin batería.

**Cambios (`--drop mc|short`):**

| Versión | Qué pasa en el compás 39 |
|---|---|
| v14 `--drop mc` | Golpe de timbal fuerte en el tiempo 1 (×1,3), todo lo demás se corta seco a 0,55 s con una bajada de 0,3 s; ~1,4 s de casi silencio; el coro entra en el tiempo 1 con un timbal aún más fuerte (×1,4) |
| v15 `--drop short` | El golpe y todo el sonido siguen ~1,2 s (casi 2 tiempos), y solo el último tiempo (~0,75 s) queda en silencio |

Nivel medido en ventanas de 0,25 s desde el compás 39: v14 0,17 → 0,02 → 0,01 → coro
0,19; v15 0,17 → ~0,09 por ~1 s → 0,02 → coro 0,19.

Todo el material se corta junto (colas de reverb y eco incluidas); el timbal queda
fuera del corte para que su golpe y cola suenen enteros.

Comando: `python build_song.py --waltz --piano --rhythm one --center e --sustain 1.6 --long --bpm 80 --hook abc --drop mc|short`.

## v16: más fuerza (`--power`)

Reporte del autor: "quizá le falta más fuerza aún" (se interpretó como el drop y la entrada al
coro). Con `--power` (requiere `--hook abc`):

- **Capa `impact`:** golpe grave en el compás 39 (el drop), **swell inverso** (ruido que se
  abre más un tono en Mi) en el último segundo del silencio, que lo llena de tensión, y un
  golpe fuerte + "platillo" sintético al entrar a cada coro (compases 40 y 64).
- **Coros con más cuerpo:** bajo ×1,35, subgrave ×1,3, timbal ×1,25 y gotas agudas ×1,2.
- **Limitador suave** (`tanh` sobre el percentil 99,9): antes, los golpes del timbal
  fijaban el pico y la normalización bajaba el volumen de todo lo demás.
- Efecto medido: volumen medio (RMS) de toda la mezcla de 0,10 a 0,20, es decir **unos
  6 dB más fuerte**; en el coro 1 pasa de 0,10 a 0,20 y en el compás del drop el golpe llega
  a 0,31 contra 0,17. Al comparar con las versiones anteriores hay que igualar el volumen,
  porque más volumen por sí solo ya suena a "más fuerza". Para eso se envió un fragmento a
  mismo volumen.

Comando: `python build_song.py --waltz --piano --rhythm one --center e --sustain 1.6 --long --bpm 80 --hook abc --drop mc --power`.

## v16 (ajuste): swell más suave

Reporte del autor: le gusta más, pero el sonido raro, que asume es el swell, domina demasiado.
Cambios al swell inverso: volumen de 0,8 a 0,3 (menos de la mitad), ruido de 0,6 a 0,2, y el
tono pasa de Mi4 + Mi5 (agudo) a Mi4 + Mi3 (grave y más suave). El golpe del drop y la entrada
al coro quedan igual.

Si sigue molestando, siguientes pasos: bajarlo más, quitarlo (solo queda el golpe) o acortarlo
a medio segundo.

## v16 (ajuste): silencio más corto

Reporte del autor: el silencio es muy largo. Se pasó a `--drop short` (ver arriba): el golpe del
compás 39 sostiene casi 2 tiempos (1,2 s) y el silencio baja de ~1,4 s a ~0,75 s (un tiempo,
como sugería la fuente de "un tiempo de silencio"). Nivel medido en ventanas de 0,25 s desde
el golpe: 0,35 · 0,35 · 0,31 · 0,32 · 0,24 · 0,16 · 0,07 · 0,05 · 0,04 y entonces el coro a 0,41.
Con el swell suave llenando la parte final, el hueco real es de aprox. medio segundo a 0,75 s.

Si todavía es largo: bajar `keep` y `down` a (1,35 s; 0,2 s) para dejar ~0,5 s, o quitar el
hueco y dejar solo el golpe con un corte de reverb.

Comando recomendado: `python build_song.py --waltz --piano --rhythm one --center e --sustain 1.6 --long --bpm 80 --hook abc --drop short --power`.

## v16 (ajuste): swell casi inaudible

Reporte del autor: bajarle más al sonido raro. El volumen del swell pasa de 0,3 a 0,1 (un tercio),
con el mismo ruido bajo y tono grave. Quedan sin cambios el golpe, el silencio corto (~0,75 s) y
la entrada al coro. Si aún se oye, el siguiente paso es quitarlo del todo.

## v16 (ajuste): el "sonido raro" no era el swell, era el pad

El autor aclaró: el sonido parece una flauta pequeña, está justo antes del coro y suena muy fuerte
al final. Se apagó el swell por completo (`add(swell, ..., 0.0)`) y el sonido seguía.

Análisis del audio (compases 38-39): la energía está concentrada en graves (<200 Hz: 78 a 91 %,
el golpe del timbal a ~41 Hz y el subgrave) y las notas de la zona media son **165, 198 y 245 Hz**,
es decir **Mi3, Sol3 y Si3 = el acorde de Mi menor del pad**. El pad son senos con un segundo
armónico: suena a flauta. Y en el puente subía a nivel 1,0 justo hasta el compás del drop
(el crescendo), así que llegaba más fuerte exactamente antes del corte.

Cambio: el pad llega al compás 39 a 0,5 (antes 1,0) y vuelve a 1,0 en el coro. Banda media
(150 a 800 Hz) justo antes del golpe: de 48 % a 34 % de la energía. Si el flauteo persiste, los
siguientes sospechosos son el piano sostenido, la marimba y las gotas agudas del puente.

## v16 (ajuste): golpe del drop más suave, swell de vuelta

El autor sospecha que el sonido raro puede ser el "golpe fuerte" del drop (no el swell ni el
pad) y pidió: menos fuerte, que se funda más rápido, y volver a poner el swell.

- **Golpe grave del drop** (`_boom` en el compás 39): volumen de 1,0 a 0,5 y caída más rápida
  (constante de 0,55 s a 0,28 s; largo de 1,6 s a 1,0 s).
- **Timbal en el compás 39:** de ×1,3 a ×0,9. El timbal de la entrada al coro queda en ×1,4.
- **Swell** vuelve, a 0,2 (antes 0,3 y luego 0,1). El pad sigue más bajo en el puente (0,5).
- Nivel medido en ventanas de 0,25 s desde 0,5 s antes del golpe: 0,18 · 0,18 · **0,30** · 0,27 ·
  0,23 · 0,24 · 0,18 · 0,12 · 0,04 · 0,03 · 0,02 · coro **0,41**. (Antes, con golpe fuerte: pico
  ~0,35 y sostén ~0,32.)
- "O mejor al final" del mensaje del autor no quedó claro (¿que el golpe vaya más cerca del
  coro?). Se dejó la posición del golpe en el tiempo 1 del compás 39; falta aclararlo.

## v16-v18 (ajuste): tres opciones de golpe en el drop

El autor confirmó que el problema no era el swell, pero el golpe seguía sonando mal. Se agregó
`--hit boom|tight|none` y se generaron las tres, idénticas salvo por el golpe del compás 39:

| Versión | `--hit` | Qué suena en el tiempo 1 del compás 39 |
|---|---|---|
| v16 | `none` | Nada extra (sin boom ni timbal); queda solo el corte del resto de la banda |
| v17 | `tight` | Golpe corto y seco de ~0,35 s: un "tok" de 110-200 Hz con clic, sin cola grave |
| v18 | `boom` | El golpe grave de 38-95 Hz con timbal (la versión anterior) |

Hipótesis de por qué el golpe grave suena mal: un seno puro muy grave con deslizamiento de tono
suena a "bwong" o a bombo sin ataque, y en audífonos pequeños queda como un zumbido (el análisis
mostró un pico a ~41 Hz y otro a ~85 Hz). Falta confirmar con el oído del autor cuál es mejor.

Comando: `python build_song.py --waltz --piano --rhythm one --center e --sustain 1.6 --long --bpm 80 --hook abc --drop short --power --hit none|tight|boom`.
