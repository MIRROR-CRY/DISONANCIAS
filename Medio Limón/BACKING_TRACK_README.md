# Backing Track - Medio Limón

## Estilo
**Tropipop**: vallenato cruzado con pop moderno. Referencias definidas con el
autor, ambas de Carlos Vives y del mismo álbum (*Corazón Profundo*, producido
por Vives y Andrés Castro):

| Referencia | Tonalidad | Tempo |
|---|---|---|
| "Volví a Nacer" | Fa mayor | 97 BPM |
| "Cuando nos volvamos a encontrar" (con Marc Anthony) | Re bemol mayor | 102 BPM |

Perfil acordado:

| Dimensión | Valor |
|---|---|
| Producción | Moderna y limpia, pocas capas |
| Qué manda | La voz, con poco atrás |
| Ánimo | Alegre pero tierna, no eufórica |
| Acordeón | Presente como color, no protagonista |
| Metales | Ninguno |

## Archivo generado
**Ubicación**: `audio/backing_track_base.wav` (y `.mp3` como copia liviana)
**Duración**: 164s (2:44) + cola de reverb
**Tempo**: 105.5 BPM, compás de 4 tiempos, Fa mayor
**Armonía**: tomada de las referencias, no inventada (ver abajo)

## Armonía: de dónde sale cada progresión

Las versiones anteriores usaban un I-V-vi-IV genérico de pop que yo inventé.
Eso es lo que hacía que no se pareciera a las referencias, más allá del tempo.
Buscadas las cifras reales, las dos comparten dos recursos que no estaban:

- **El cuarto grado menor prestado**: Bbm en "Volví a Nacer", Fm en "Cuando nos
  volvamos a encontrar". El giro Bb → Bbm → F es el color agridulce del estilo.
- **Dominantes secundarias y cadenas ii-V hacia grados que no son la tónica**:
  E7 → Am y C7 → F en la segunda referencia.

Progresiones de esta canción, en Fa:

```
intro     F - Bb - Dm - C                      (intro literal de "Volví a Nacer")
verso     F - C - Dm - A7 - Bb - F - Gm - C    (A7 es dominante secundaria hacia Dm)
pre-coro  Gm - C - Gm - C7                     (cadena ii-V)
coro      F - Dm - Bb - Bbm - F - C - Bb - C   (el cuarto menor prestado)
```

## Lo que costó llegar acá: el tempo y el empuje

Diez versiones se fueron en esto, y hubo tres causas distintas, no una.

**1. Dónde cae el bombo.** Con el bombo solo en 1 y 3, el pulso que uno marca
con el pie es la mitad del tempo nominal. A 102 BPM eso daba 51 por minuto:
se sentía lenta aunque el número no lo pareciera. Ahora el bombo marca los
cuatro tiempos, así que el pulso percibido es 105.

**2. Una regla mal aplicada.** El vallenato se escribe en 2/4, y sobre esa base
reescribí todo al doble de velocidad. Pero **el paseo es la excepción del
folclor: se cuadra en cuatro tiempos**. Aplicar la regla del 2/4 justo al aire
de las referencias disparó la versión y quedó demasiado rápida.

**3. La causa de fondo: faltaba el apagado.** Aun con el tempo correcto seguía
arrastrando, y no era cosa de velocidad. En el rasgueo del paseo, donde la
partitura muestra un silencio **se golpean las cuerdas apagadas con la mano
derecha**, generando un sonido percutido. Todas las versiones anteriores
tocaban acordes limpios sostenidos, sin un solo golpe apagado. Un acorde
sostenido no empuja hacia adelante a ninguna velocidad.

El patrón que se toca ahora:

```
  1         &          2         &          3         &          4         &
  bajo      ataque     apagado   ataque     bajo      ataque     apagado   ataque
  (pulgar)  ascendente percutido ascendente (quinta)  ascendente percutido ascendente
```

Nota sobre medir el tempo: el pulso se puede contar al doble o al cuádruple y
sigue siendo válido, así que el número solo no dice nada. El valor de acá salió
de un conteo a cronómetro del autor sobre la referencia (22 pulsos en 12.49s =
105.7/min), y la pista mide 105.5.

## Historial de versiones

| Versión | Qué era | Por qué no |
|---|---|---|
| v1 | Vallenato con acordeón, 100 BPM | MIDI cuantizado, sin mezcla, sonaba a caja de ritmos |
| v2 | Igual a 116 BPM con jitter aleatorio | El jitter uniforme no es humanización: suena desordenado, no humano |
| v3 | Nueva cumbia chilena (Chico Trujillo) | Ya sonaba a música real, pero rama equivocada del género |
| v4 | Cumbia sonora clásica (Sonora Palacios) | Bien ejecutada, pero no era esta canción. Guardada en `musica/ideas/` |
| v5-v6 | Tropipop a 97 y 102 BPM | Estilo correcto, seguía sintiéndose lenta |
| v7-v8 | Reescrita en 2/4 | Regla mal aplicada: el paseo va en 4 tiempos. Quedó demasiado rápida |
| v9 | Vuelta a armonía normal | Mejor, pero la guitarra seguía sin apagados |
| v10 | Rasgueo real del paseo | Mejor empuje, pero la armonía seguía siendo inventada |
| v11 | Acordes e instrumentos de las referencias | El bajo seguía tocando raíces planas |
| **v12** | **Bajo con la síncopa anticipada del estilo** | **Actual** |

## Instrumentación
Tomada de los créditos del álbum de referencia (*Corazón Profundo*): acordeón
(Egidio Cuadrado, John Lozano), caja vallenata (Alfredo Rosado), guacharaca
(Eder Polo), guitarra / órgano Hammond B3 / teclados (Andrés Castro), más bajo,
cello, batería y bombardino. Renderizado con FluidR3_GM.

El bombardino queda pendiente: está en los discos, pero se dejó fuera porque el
perfil acordado pedía nada de metales.


| Instrumento | GM | Rol |
|---|---|---|
| Guitarra acústica | 25 | La columna: bajo con pulgar en 1 y 3, ataques ascendentes en los contratiempos |
| Guitarra muteada | 28 | Los apagados percutidos en 2 y 4 — el motor del rasgueo |
| Acordeón | 21 | Figuras derivadas del acorde en curso (no una melodía fija, así no choca con el Bbm ni el A7), respuestas cortas en el hueco entre frases |
| Guitarra eléctrica limpia | 27 | Solo acentos, en los coros |
| Órgano Hammond | 16 | Cama armónica. Los discos de referencia usan un B3, no un piano de cola |
| Cello | 42 | Color grave sostenido en los coros; el álbum de referencia tiene cello |
| Bajo | 33 | Bajo principal en 1, octava superior de la tónica en el "y" de 2, bajo secundario (quinta) en 3, y la raíz del acorde siguiente anticipada en el "y" de 4 ligada sobre el compás |
| Percusión | — | Bombo en los 4 tiempos, guacharaca en semicorcheas (~7/s), caja vallenata (grave en 1, palmada en 2, doble palmada sincopada antes del 3), palmas en coros |

## Principio del arreglo
La voz manda, así que **los versos van despojados**: guitarra, bajo y percusión,
sin piano ni eléctrica. El acordeón no toca por debajo de la voz — responde en
el último compás de cada frase, en el hueco entre líneas cantadas.

## Balance de mezcla (medido)
Los niveles se fijan midiendo los stems, no a ojo.
```
acústica   -35.0 dB   ← la columna, adelante
drums      -36.0 dB
bajo       -38.1 dB   ← apoya, no domina
apagado    -42.4 dB   ← percusión del rasgueo
acordeón   -43.2 dB   ← color
cello      -43.2 dB   ← calidez en coros
órgano     -46.0 dB   ← cama Hammond
eléctrica  -46.0 dB   ← acentos
```

## Control de calidad (medido)
```
Tempo detectado:       105.5 BPM                      ✓
Pulso de bombo:        105.5/min (conteo del autor: 105.7)  ✓
Acorde cada:           2.27s = 4 pulsos               ✓ relación normal
Densidad de eventos:   5.8/s                          ✓
Pico:                  -1.03 dBFS                      ✓
Loudness:              -14 LUFS                        ✓
```

## Estructura
```
intro        4 compases   (acordeón + guitarra, presenta el hook)
verso        8 compases   (despojado, espacio para la voz)
pre-coro     4 compases   (acordeón ascendente, construye)
coro         8 compases   (todo, vuelve el hook)
coro         8 compases
verso       12 compases   (para las 6 líneas del segundo verso)
pre-coro     4 compases
coro         8 compases
outro        8 compases
outro        8 compases   (con fade)
```

## Pendiente
- Probar el bombardino: está en los créditos del disco de referencia pero se
  dejó fuera por el "nada de metales" del perfil. Su rol es melódico grave, muy
  distinto al de las trompetas que se rechazaron en la v3/v4.
- Los patrones exactos de la caja (adominicao, rodado, tres golpes) solo están
  explicados en video; la caja acá usa el patrón básico documentado en texto.

Ver `INVESTIGACION_ESTILO.md` para los apuntes completos de estilo con fuentes.

## Regenerar
```bash
python3 generate_backing_track.py
```

---
**Última versión**: v12, 2026-09-22
