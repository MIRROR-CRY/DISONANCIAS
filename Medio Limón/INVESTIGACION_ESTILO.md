# Investigación de estilo: vallenato, paseo y tropipop

Apuntes de lo que se fue averiguando mientras se construía la base de "Medio
Limón". Se anota acá para no volver a improvisar sobre cosas que tienen
respuesta documentada, y porque varias de estas cosas explican errores
concretos que costaron versiones enteras.

---

## 1. Los aires del vallenato

El vallenato clásico se organiza en cuatro **aires** (tipos de sensación
rítmica):

| Aire | Carácter | Tempo |
|---|---|---|
| **Paseo** | Lírico y versátil, el más grabado hoy | 90-115 BPM (comercial y cruces pop: 112-118) |
| Merengue | Vivo y saltarín (no confundir con el dominicano) | — |
| Puya | El más rápido y virtuoso | — |
| Son | El más lento, sentimental | — |

**Las referencias de esta canción son paseos.** El paseo se describe como
alegre, algo romántico, tocado en tresillos y con armonía estricta.

### El compás: la excepción que costó dos versiones

Cada aire tiene su propio compás, y la versión corta que se repite por ahí
("el vallenato va en 2/4") es falsa:

| Aire | Compás |
|---|---|
| **Paseo** | 2/4 escrito, pero **se cuadra y se siente en cuatro tiempos** |
| Son | 2/4 |
| Merengue | **6/8** |
| Puya | **6/8** |

O sea: el paseo no es la excepción frente a un folclor entero en 2/4. Es uno
de los dos aires binarios, y los otros dos ni siquiera son binarios, son
ternarios. Lo que sí es cierto, y es lo que importa acá, es que **el paseo se
cuadra en cuatro**.

Esto no es un detalle académico. Al aplicar la regla general del 2/4 al paseo,
la versión v7/v8 de esta canción reescribió todo al doble de velocidad y quedó
inservible. La regla existe, pero no aplica justamente al aire que estábamos
haciendo.

---

## 2. El trío instrumental

El vallenato tradicional se toca con tres instrumentos que no necesitan
amplificación:

- **Acordeón diatónico de tres hileras** (31 botones en la mano derecha, tres
  lengüetas por nota). Lleva la melodía y los riffs. Viene en afinaciones ADG,
  GCF y BbEbAb. La mano izquierda hace pasajes de bajo extendidos.
- **Caja vallenata**: tambor pequeño de un solo parche, se sujeta entre las
  rodillas y se toca con las manos desnudas. Da los acentos secos.
- **Guacharaca**: palo de madera acanalado que se raspa con un tenedor
  metálico. Es la columna rítmica continua.

### Caja vallenata
Los tres patrones rítmicos principales son **"el adominicao"**, **"el rodado"**
y **"los tres golpes"** (este último asociado a Domingo 'Mingo' Pimentel). La
velocidad a la que se dan los golpes es lo que define qué aire se está
interpretando.

Patrón básico documentado: **golpe grave en el tiempo 1, palmada en el tiempo 2
(contratiempo), doble palmada sincopada antes del 3.**

### Guacharaca
Raspado continuo, constante, sin pausas. Es lo que sostiene el movimiento hacia
adelante en todas las variedades de vallenato y cumbia. Densidad real: **unos
siete raspados por segundo** (semicorcheas a este tempo). A la mitad de esa
densidad el groove pierde empuje.

---

## 3. El rasgueo de guitarra del paseo

Esto resultó ser lo más importante de toda la investigación, y explica por qué
la canción sonaba pesada sin importar a qué tempo se pusiera.

**Donde la partitura muestra un silencio, no se hace silencio: se golpean las
cuerdas apagadas con la mano derecha para que toquen el diapasón, generando un
sonido percutido.** Un apagado (golpe percutido) reemplaza una corchea ligada.

La técnica base: tocar el bajo con el pulgar e inmediatamente hacer un ataque
ascendente, para conseguir un movimiento fluido. El acompañamiento combina
**bajos, rasgueos, síncopas y apagados**.

```
  1         &          2         &          3         &          4         &
  bajo      ataque     apagado   ataque     bajo      ataque     apagado   ataque
  (pulgar)  ascendente percutido ascendente (quinta)  ascendente percutido ascendente
```

Existen tres variantes: **paseo clásico**, **paseo romántico a un bajo** y
**paseo romántico a dos bajos**. Para una canción romántica tipo Vives, la
familia "romántico" es la que corresponde.

---

## 4. El bajo

- El patrón del paseo tiene **bajo principal y bajo secundario**, con cambios de
  articulación entre ellos.
- **La síncopa característica se logra colocando una ligadura entre dos
  compases**: el bajo se anticipa y se ata por encima de la línea divisoria.
  Esa anticipación es lo que tira hacia adelante.
- Es recurrente usar **la octava superior de la tónica** para darle carácter
  más rítmico al acompañamiento.
- La marcación de los bajos es "una por cada tres, y a veces, dependiendo de la
  pieza, dos por una".

---

## 5. Armonía de las referencias

Ninguna de estas progresiones se inventó: salen de las cifras publicadas.

**"Volví a Nacer"** (Fa mayor, 97 BPM)
```
intro    F - Bb - Dm - C - F - Bb
acordes  F, C, Dm, Bb y Bbm
```

**"Cuando nos volvamos a encontrar"** (original en Re bemol; las cifras se
publican en Do con cejilla al primer traste, 102 BPM)
```
intro    C - G - Am - F - Fm - Csus2 - G
verso    C - G - Am - E   ·   F - C   ·   Dm - Dm/F - G
coro     G - G7 - C   ·   Bm7b5 - E7 - Am   ·   Gm - C7 - F   ·   Dm7 - G
```

### Los dos recursos que comparten

1. **Cuarto grado menor prestado**: Bbm en la primera, Fm en la segunda. El
   giro IV → iv → I (Bb → Bbm → F) es el color agridulce del estilo.
2. **Dominantes secundarias y cadenas ii-V hacia grados que no son la tónica**:
   E7 → Am, C7 → F, Bm7b5 - E7 - Am.

Un I-V-vi-IV de pop genérico no tiene ninguno de los dos. Esa fue la razón de
fondo por la que las primeras versiones no se parecían a las referencias,
independiente del tempo y del groove.

---

## 6. Producción: el álbum de referencia

Ambas referencias son de *Corazón Profundo* (Carlos Vives, 2013), producido por
Carlos Vives y Andrés Castro, con Castro también como ingeniero de grabación.
Grabado entre Henson Recording Studios (Los Ángeles), On the Groove Studio
(Miami), Audiovision Estudios (Bogotá) y Le Dune Studios (Bolonia).

| Instrumento | Músico |
|---|---|
| Acordeón | Egidio Cuadrado, John Lozano |
| Caja vallenata | Alfredo Rosado |
| Guacharaca | Eder Polo |
| Guitarra, órgano Hammond B3, teclados | Andrés Castro |
| Bajo, cello, batería, bombardino | — |

Dos cosas que corrigieron el arreglo: el teclado es un **Hammond B3**, no un
piano de cola, y **hay cello** en el disco. El **bombardino** también está, y
queda como posibilidad pendiente.

Sobre Egidio Cuadrado: fue Rey del Festival de la Leyenda Vallenata en 1985 en
categoría profesional. El guitarrista Teto Ocampo lo describió como alguien que
tenía "la teoría del vallenato" sin formación musical formal, y que el resto de
los músicos tenía que aprender su vocabulario.

**Tropipop** es el nombre del género de estos cruces: vallenato colombiano
cruzado con pop.

---

## 7. Sobre medir el tempo

El pulso se puede contar al doble, al cuádruple o a cualquier múltiplo y sigue
siendo válido: la misma canción admite contar 60 o 120. Por eso **el número
solo no dice nada** — lo que importa es el pulso efectivo, cómo se escucha.

Lo que sí sirve como dato duro es un conteo contra cronómetro: en esta canción
el tempo se fijó desde un conteo del autor sobre la referencia (22 pulsos en
12.49 segundos = 105.7 por minuto), y después se verificó midiendo la pista
generada (105.5).

Lo que hace que un tempo dado se sienta rápido o lento no es el número sino
tres cosas distintas:
1. **Dónde cae el bombo** (en 1 y 3 el pulso percibido es la mitad del nominal)
2. **Cada cuántos pulsos cambia el acorde** (lo normal en pop es cada cuatro)
3. **Si hay apagados percutidos o solo acordes sostenidos**

---

## Fuentes

- [Vallenato - Wikipedia](https://en.wikipedia.org/wiki/Vallenato)
- [Caja vallenata - Wikipedia](https://en.wikipedia.org/wiki/Caja_vallenata)
- [Guacharaca - Wikipedia](https://en.wikipedia.org/wiki/Guacharaca)
- [Vallenato en guitarra: ritmo y rasgueo paso a paso - clasesdeguitarra.com.co](https://clasesdeguitarra.com.co/como-tocar-vallenato-guia-paso-a-paso/)
- [How to Make Vallenato Music - BeatKey](https://beatkey.app/how-to-make-vallenato-music)
- [Volví a Nacer - Cifra Club](https://www.cifraclub.com/vives-carlos/volvi-a-nacer/)
- [Cuando nos volvamos a encontrar - acordesdcanciones.com](https://acordesdcanciones.com/carlos-vives-cuando-nos-volvamos-a-encontrar-ft-marc-anthony/)
- [Corazón Profundo - Discogs](https://www.discogs.com/release/14784763-Carlos-Vives-Coraz%C3%B3n-Profundo)
- [Egidio Cuadrado - Festival Vallenato](https://festivalvallenato.com/egidio-cuadrado-el-acordeonero-que-ha-llevado-la-musica-vallenata-alrededor-del-mundo/)
- [Traducción de paseos vallenatos empleando el piano - Universidad de Antioquia](https://bibliotecadigital.udea.edu.co/server/api/core/bitstreams/b4b8ebf7-2743-4e45-aec6-10ca3ea12058/content)

---

## Pendiente de investigar
- Patrones exactos de la caja (adominicao, rodado, tres golpes): la explicación
  detallada está en video, no en texto accesible.
- Qué toca exactamente el acordeón en las introducciones y rellenos del paseo:
  tampoco hay descripción técnica en texto.
- Rol del bombardino en este repertorio.

## Correcciones a este documento

**2026-09-23.** La sección del compás decía que "el vallenato se escribe en
2/4" y que "el paseo es la excepción de todo el folclor". La segunda mitad
es falsa: solo el son comparte el 2/4 con el paseo, mientras que **el
merengue vallenato y la puya van en 6/8**, que es métrica ternaria. La tabla
de arriba reemplaza esa afirmación.

Importa porque esa media verdad es la que costó las versiones v7 y v8: si el
dato hubiera estado completo desde el principio, nunca se habría aplicado
una "regla general del 2/4" que no existe.

Fuente: [Paseo, puya, merengue y son, los aires clásicos del vallenato - El Tiempo](https://www.eltiempo.com/cultura/musica-y-libros/paseo-puya-merengue-y-son-los-aires-clasicos-del-vallenato-647537)

---
**Última actualización**: 2026-09-23
