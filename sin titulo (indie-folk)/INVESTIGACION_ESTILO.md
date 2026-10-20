# Investigación de estilo: indie-folk stomp-clap (The Lumineers)

Apuntes previos a componer nada. Se investiga primero por la lección que dejó
"Medio Limón": doce versiones de backing track perseguiendo un sonido que yo
estaba improvisando, cuando los acordes, el compás y la instrumentación reales
estaban documentados y a una búsqueda de distancia.

---

## La referencia: "Ho Hey" (The Lumineers, 2012)

| Dato | Valor |
|---|---|
| Tempo | **79 BPM** |
| Tonalidad | **Do mayor** |
| Compás | 4/4 |
| Género | Folk rock / indie folk |
| Acordes | C, F, Am, Em, G |
| Progresión de apertura | **C - F - C - Am** |
| Producción | Ryan Hadlock |
| Estudio | Bear Creek Studio, Woodinville, Washington |

**Todos los acordes son de posición abierta, sin cejilla.** Eso no es un detalle
menor: es parte del sonido. Las cuerdas al aire suenan más abiertas y resonantes
que las mismas notas con cejilla.

### Ojo con el tempo
79 BPM es lento sobre el papel y la canción no se siente lenta. Mismo fenómeno
que en Medio Limón: lo que da la sensación de movimiento no es el número sino
dónde caen los golpes y cuánta actividad hay. Acá el motor son las pisadas y las
palmas, no el tempo.

### Los gritos
Los "Ho!" y "Hey!" nacieron como recurso en vivo, para llamar la atención del
público en los shows. O sea que el gancho del tema no es melódico ni armónico:
es una interjección rítmica pensada para que la gente la conteste.

---

## La banda

| Miembro | Rol |
|---|---|
| Wesley Schultz | Voz, guitarra |
| Jeremiah Fraites | Batería, percusión |
| Neyla Pekarek | Cello, voz (2010-2018) |

En gira suman violín (Lauren Jacobson) y bajo (Byron Isaacs).

El grupo se describe a sí mismo como "una amalgama de rock acústico de pisada y
palmada que hincha el corazón, pop clásico y folk de porche". Elementos de roots,
chamber pop y country alternativo. **Evitan deliberadamente la producción
electrónica** habitual del pop mainstream.

---

## Lo más importante: cómo está hecho el stomp-clap

Del desglose de la mezcla de "Ho Hey" publicado en *Sound on Sound*:

```
1  voz principal
2  dos pistas de coros
1  guitarra acústica
1  mandolina
1  cello
4  pistas de batería
7  pistas de pisadas, percusión y palmas
```

**Siete pistas de pisadas y palmas.** Grabadas en la sala en vivo de Bear Creek,
capturadas con un Neumann M49.

Esto es lo central del estilo y lo más fácil de errar: el stomp-clap no es *un*
elemento en el arreglo, es un **muro de capas humanas grabadas en una sala con
micrófono de ambiente**. El carácter viene de que son varias personas, en un
espacio real, sin cuadrar exacto entre ellas. Una palmada sola y cuantizada no
se parece en nada, por buena que sea la muestra.

Si se genera por código, la consecuencia práctica es: **muchas capas de palmadas
y pisadas, cada una con su propio desfase y su propia velocidad, más reverb de
sala compartida**, no una sola pista de palmas repetida.

Instrumentos a considerar que no estaban en ninguna canción del álbum hasta
ahora: **mandolina** y **cello** (el cello sí se usó en Medio Limón, pero como
color de fondo, no como voz melódica).

---

## Qué rol cumpliría en el álbum

Según `ALBUM_CONCEPT.md`, leyendo el álbum como si fuera una sola canción:

```
Kicking Stones  → el verso   (rápido, crítica social hacia afuera)
Rescue Us       → el bridge  (rompe el ritmo, autocrítica hacia adentro)
Medio Limón     → tropipop en español, quiebre de idioma
esta canción    → el chorus  (el momento comunitario, el alivio colectivo)
```

El contraste que tendría que dar: después de la crítica hacia afuera y la
autocrítica hacia adentro, algo que se cante en grupo. Por eso el estilo calza
con el rol: los "Ho!" y "Hey!" existen precisamente para que el público conteste.

---

## Los tres recursos pedidos

### 1. Crescendo

El principio es simple y estructural: **empezar con instrumentación mínima e ir
sumando capas**. Un arreglo típico del género abre con guitarra acústica y voz
suave, y va agregando percusión y cuerdas que crecen hacia el coro.

Lo que se repite en la literatura del género: los versos se mantienen bajos, se
abre en el coro, y se vuelve a la intimidad en el puente. **El arco dinámico es
lo que hace que los detalles chicos se sientan grandes.** Si todo está al mismo
nivel de intensidad, nada destaca.

Esto también responde a lo de "que tenga partes como corresponde": las partes no
se distinguen solo por acordes distintos, se distinguen por **cuántos elementos
están sonando**.

### 2. Voces comunales (gang vocals)

Lo documentado sobre cómo se graban:

- El objetivo es **sonar como un grupo de gente común, no como cantantes
  profesionales**. La recomendación explícita es permitirse ser un poco
  desprolijo.
- **Al menos 4 capas, idealmente 6 pistas por parte**, con tonos y acentos
  vocales distintos en cada una.
- Panear fuerte: una toma a la izquierda, otra a la derecha.
- Variar la distancia al micrófono entre tomas. Con un grupo real, se pone un
  condensador cardioide de frente a los monitores y de espaldas a la fuente,
  lo que da una sensación más suelta y "rowdy".

Converge exactamente con el hallazgo de las siete pistas de pisadas y palmas de
"Ho Hey": **el carácter está en la cantidad de capas y en su imperfección**, no
en la calidad de una toma sola.

#### Precisión del autor: no es un coro, es una multitud que crece

La idea no es un coro que entra y se mantiene, sino **cada vez más gente**: una
voz, después unas pocas, después muchas. Coro de estadio, no coro profesional.
O sea que el doblaje de voces **es el mecanismo del crescendo**, no un adorno
que se agrega encima de él.

Implicación para el arreglo: la cantidad de voces es un parámetro que sube a lo
largo de la canción, no un ajuste fijo.

```
Verso 1      1 voz
Coro 1       2-3 voces
Verso 2      1-2 voces (baja, pero ya no vuelve a estar sola del todo)
Coro 2       5-6 voces
Coro final   máximo, suena a multitud
```

#### Por qué doblar mal es lo correcto acá

Hay una diferencia técnica que importa, y que este proyecto ya vivió en carne
propia: al intentar doblar la voz en "Rescue Us" el resultado sonaba hueco y
con flanger, por el desfase entre tomas.

En un **doblaje al unísono** ese desfase es un defecto: dos tomas casi idénticas
y levemente corridas se cancelan entre sí y producen el efecto de peine.

En un **coro de multitud pasa lo contrario**: el desfase y la desafinación entre
voces es justamente lo que hace que se lean como personas distintas. Un grupo de
gente cantando nunca está afinado ni sincronizado.

Si se genera por código, la consecuencia práctica es que cada voz agregada
necesita:
- su propio desfase temporal (decenas de milisegundos, no unos pocos)
- su propia desviación de afinación (unos cuantos cents arriba o abajo)
- su propio timbre y su propia intensidad
- posición distinta en el estéreo

Copiar la misma toma veinte veces suena más fuerte, pero sigue sonando a una
sola persona. **La dispersión es el efecto.**

### 3. Modulación de tono ("truck driver's gear change")

Nombre técnico del recurso: subir la canción de tono cerca del final.

- Se sube **un semitono o un tono entero**, en un corte estructural, típicamente
  **antes del último coro**.
- **No necesita acorde pivote**: se sube todo y listo. La alternativa más suave
  es usar el acorde de séptima dominante de la tonalidad nueva como puente.
- **Nunca vuelve a la tonalidad original y nunca modula hacia abajo.** El único
  camino es hacia arriba.
- Suele ir seguido de repetición del coro y fade.
- El efecto buscado es exactamente el que se pidió: una sensación de urgencia y
  de resolución, "como doblar la última curva hacia la recta final".

Advertencia honesta de las fuentes: es un recurso tan usado que se volvió un
cliché de balada romántica. Funciona, pero se nota. Usarlo a conciencia.

> **Decidido: por ahora no va modulación.** Se deja registrada como idea
> barajada, para retomarla solo si al escuchar la canción armada se siente que
> le falta ese empujón. Ver "Decisiones tomadas" al final.

**Dato importante: "Ho Hey" NO modula.** Se mantiene en Do mayor de principio a
fin, coro final incluido. La sensación de potencia al final de esa canción viene
íntegramente del crescendo y de la acumulación de capas (pisadas, palmas, voces),
no de un cambio de tonalidad.

O sea que la modulación sería un recurso **agregado** respecto de la referencia,
no copiado de ella. Puede hacerse igual, pero conviene saber que la referencia
logra ese efecto por otra vía: pura densidad.

---

## Estructura propuesta

Juntando las tres cosas, con las partes diferenciadas por densidad:

```
Intro        guitarra acústica sola
Verso 1      guitarra + voz principal              (mínimo)
Pre-coro     entra la pisada
Coro 1       + palmas + primeras voces comunales   (primera apertura)
Verso 2      baja, pero conserva la pisada
Pre-coro     + cello
Coro 2       más capas de palmas y de voces
Puente       se cae todo: voz y palmas, lo más íntimo
             → acá va la modulación (subir un tono)
Coro final   tonalidad nueva, todas las capas      (máximo)
Outro        repetición y fade
```

Dos decisiones que quedan de esto:
- El puente es el punto más bajo del arco, justo antes del más alto. Ese
  contraste es lo que hace que el coro final pegue, más que el volumen absoluto.
- La modulación cae en el corte estructural entre el puente y el coro final,
  que es donde la documentación dice que va.

---

## Fuentes

- [Ho Hey - Wikipedia](https://en.wikipedia.org/wiki/Ho_Hey)
- [Inside Track: The Lumineers - Sound on Sound](https://www.soundonsound.com/techniques/inside-track-lumineers)
- [The Lumineers Members, Gear & Sound - Equipboard](https://equipboard.com/band/the-lumineers)
- [The Lumineers (album) - Wikipedia](https://en.wikipedia.org/wiki/The_Lumineers_(album))
- [Key & BPM for Ho Hey - Tunebat](https://tunebat.com/Info/Ho-Hey-The-Lumineers/1jdNcAD8Ir58RlsdGjJJdx)
- [Ho Hey Chords - Ultimate Guitar](https://tabs.ultimate-guitar.com/tab/the-lumineers/ho-hey-chords-1047662)
- [A Beginner's Guide to Indie Folk Music Production](https://eliottglinnaudio.com/blog/a-beginner-s-guide-to-indie-folk-music-production)
- [Dynamic Builds and Drops: Advanced Techniques](https://mysticalankar.com/blogs/blog/dynamic-builds-and-drops-advanced-techniques)
- [Recording gang vocals - Gearspace](https://gearspace.com/board/so-much-gear-so-little-time/866177-recording-gang-vocals.html)
- [How To Layer Vocals Like A Pro](https://twisbyrecords.com/post/how-to-layer-vocals-like-a-pro/)
- [Truck Driver's Gear Change - TV Tropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/TruckDriversGearChange)
- [The Truck Driver's Gear Shift - Musical U](https://www.musical-u.com/learn/the-truck-drivers-gear-shift/)
- [Master modulation - MusicRadar](https://www.musicradar.com/news/how-to-use-key-changes-songwriting-music-theory)

---

## Decisiones tomadas

**Sin modulación de tono, por ahora.** El empujón del final lo carga el
crecimiento de la multitud de voces, que es como lo resuelve la referencia.
Subir un tono antes del último coro sería un segundo empujón encima del primero.

Queda barajada como idea: si al escuchar la canción armada se siente que le
falta, se prueba. Es un cambio barato de hacer después — se sube todo un tono en
el último coro y listo, no necesita acorde pivote.

**Las voces se doblan como multitud real**, con dispersión de tiempo y de
afinación entre capas, no como copias limpias de una misma toma.

---

## Pendiente
- **De qué trata la canción**: sin definir.
- **El grito**: el equivalente al "Ho!" y "Hey!". Es lo primero que habría que
  encontrar, porque la estructura se cuelga de él.
- Letra.
- Confirmar si el arreglo lleva mandolina (está en la referencia) o si se deja
  fuera por coherencia con el resto del álbum.

## Nota sobre las referencias

Hay una sola referencia para esta canción: **"Ho Hey" de The Lumineers**. El
dictado por voz la ha transcrito de varias formas distintas a lo largo de la
conversación ("Jauge", "Hope Halo", "Couch"), pero siempre se trata de la misma
canción. Ante un nombre que no calce con nada conocido, asumir que es una
referencia ya mencionada antes de buscarla como si fuera nueva.

---
**Creado**: 2026-09-22


---

## Correcciones a este documento

**2026-09-23.** Dos datos de producción estaban mal y se corrigieron:

- Decía que "Ho Hey" lo produjo **Julius Gatuma**. Falso. El álbum debut de
  The Lumineers (2012), "Ho Hey" incluida, lo produjo **Ryan Hadlock**, que
  además es dueño del estudio donde se grabó.
- Decía que las pisadas y palmas se grabaron en la sala en vivo de
  **Fairfax**. Falso: fue en **Bear Creek Studio**, en Woodinville,
  Washington. Hadlock los llevó ahí después de escuchar su maqueta en SXSW,
  y la grabación tomó entre dos semanas y media y tres.

El origen del error fue tomar un crédito de producción de un agregador sin
verificarlo contra una fuente primaria. Queda anotado porque es exactamente
el error que este documento existe para evitar.

Fuentes: [The Lumineers (álbum) - Wikipedia](https://en.wikipedia.org/wiki/The_Lumineers_(album)),
[Ryan Hadlock: Producing The Lumineers - Music Connection](https://www.musicconnection.com/ryan-hadlock-producing-lumineers/),
[Bear Creek Studio - Wikipedia](https://en.wikipedia.org/wiki/Bear_Creek_Studio)
