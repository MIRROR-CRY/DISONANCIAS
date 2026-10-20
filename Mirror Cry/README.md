# Mirror Cry

Base instrumental coldwave / post-punk. 156 BPM, Mi menor (Em, C, Am, B), 116 compases.
Se genera con MIDI + FluidSynth + DSP en Python.

## Estructura

Intro (8) > Verse 1 (8) > Verse 2 (8) > Verse 3 (8) > Bridge (8, último compás en silencio) > Chorus 1 (8) > Chorus 2 (8) > Outro (8)

Cada instrumento toca la canción completa en un solo MIDI y su presencia es una onda de volumen (`LEVELS` en `build_song.py`): entran y salen suavemente, sin cortes entre secciones.

Humanización: cada nota varía levemente en momento, velocidad, duración y afinación (±pocos cents), con semilla fija para que sea reproducible.

Final: el clímax se sostiene hasta el último compás, con redoble de caja y un golpe final de toda la banda en Em (platillo largo). La cola decae con reverb y eco naturales, con un fade suave de 2 s, sin corte seco.

Instrumentos: batería, bajo galopante con distorsión, guitarra arpegiada con acentos cada 3 semicorcheas (acordes distorsionados en el coro), riff de sintetizador con eco, pad oscuro.

## Cómo generarla desde un clon limpio

```bash
git clone https://github.com/eanorambuena/Emma-HQ.git
cd "Emma-HQ/MIRROR-CRY_DISONANCIAS/Mirror Cry"

# 1. Programa FluidSynth (el sintetizador)
sudo apt install fluidsynth fluid-soundfont-gm   # Linux / WSL
# brew install fluid-synth                        # macOS
# choco install fluidsynth                        # Windows (o usa WSL)

# 2. Librerías de Python
pip install -r requirements.txt

# 3. Generar
python build_song.py
```

El resultado queda en `versions/vN/mix.wav`, con los stems por instrumento en `versions/vN/stems/` y los MIDI en `versions/vN/midi/`. Cada ejecución crea una versión nueva. La carpeta `versions/` no se sube a git.

## Cómo encuentra el SoundFont

El repo no incluye ningún `.sf2` (FluidR3_GM pesa 148 MB y GitHub no lo acepta). El script busca, en este orden:

1. Variable de entorno `SOUNDFONT` con la ruta a un `.sf2`.
2. Carpeta `soundfonts/` junto al script o en `MIRROR-CRY_DISONANCIAS/soundfonts/`.
3. Rutas del sistema (`/usr/share/sounds/sf2/FluidR3_GM.sf2` y equivalentes en macOS y Windows).
4. El SoundFont ligero que trae el paquete `pretty_midi` (TimGM6mb, 6 MB). Suena más plano, sirve para que funcione siempre.

Para el sonido del resto del álbum usa FluidR3_GM (`fluid-soundfont-gm` en Debian/Ubuntu).

Si falta FluidSynth o no hay ningún SoundFont, el script termina con un mensaje que explica qué instalar.

## v6: duración y hook

Duración ~3:04 (116 compases a 156 BPM): versos de 16 compases, interludio de 8, puente de 12 y dos coros de 16, para alcanzar a cantar.

Hook: un instrumento nuevo (`lead`, onda cuadrada con eco) toca un motivo de 4 compases que sigue los acordes. Suena desde el primer golpe, vuelve en el interludio antes del verso 3, es la melodía bajo los coros y cierra el final. Los versos quedan sin él para que el regreso se sienta como premio.

## v7: referencia western y final con el hook

Se agrega la música western como referencia (Morricone, spaghetti western), dentro del cold wave moderno: el bajo galopante ya evoca el trote, y ahora hay un silbido solitario (`whistle`) con frases lentas de 4 compases en la segunda mitad de los versos y en el puente, y un leve trémolo de guitarra tipo twang.

Final: el hook completo suena en los últimos compases, el golpe final suma sus notas, y tras el golpe el silbido recita el arranque del hook (Si, Si, Mi) sobre la cola.

## v8: balance de volumen

Ajustes leves de `GAINS`, sin tocar arreglos ni LEVELS:

| Elemento | Antes | Ahora | Motivo |
|----------|-------|-------|--------|
| drums | 1.00 | 1.25 | La batería quedaba muy atrás del bajo (RMS 0.05 vs 0.235) |
| bass | 0.80 | 0.66 | Dominaba toda la mezcla y tapaba al resto |
| guitar | 0.62 | 0.70 | Más presencia en estrofas y estribillos |
| synth | 0.45 | 0.50 | Se perdía bajo la guitarra |
| lead | 0.55 | 0.62 | El hook debe destacar en intro, interludio y outro |
| whistle, pad | sin cambio | | Ya estaban en buen nivel |

## Archivos por versión

`versions/vN/` guarda los MIDI y los stems (un WAV por instrumento) de cada render. Los números coinciden con `mirror_cry_base_vN`. Están las versiones v7 y v8; las anteriores se generaron en sesiones previas y solo se conservan sus mezclas finales en la raíz. El siguiente render crea `versions/v9`.

## v9: hook inolvidable

- Salto característico: en la nota larga del hook (tiempo 2 de cada compás, salvo el B) ahora sube a la décima en vez de la octava.
- Silencio de dos tiempos antes de que el hook vuelva (inicio del interludio y del outro).
- Hook fantasma (nivel bajo) en los versos 2 a 4, además del coro (que ya lo llevaba a 0.75).

## v10: mood grave

Casi todo baja de registro y solo el silbido queda agudo, como contraste. No se tocaron silbido, bajo, batería ni la guitarra distorsionada (strum).

- Lead: el hook baja una octava (`tones = list(ARP[ch])`). Las dos notas del final pasan de 88 y 83 a 76 y 71.
- Synth: baja una octava (`t - 12`). Las notas del final pasan de 76 y 83 a 64 y 71.
- Pad: baja una octava más (`p - 24`) y sube un poco su velocity (de 48 a 52).
- Guitarra (arpegio): se probó `t - 24`, pero caía en MIDI 33 a 52, chocando con el bajo y bajo el rango real de la guitarra (quedaba turbio). Se mantiene en `t - 12`, igual que la v9.
- Medición contra la v9: pico 0.808 (≤ 0.95), RMS 0.1458 (v9: 0.1456) y centroide espectral 2514 Hz (v9: 2577 Hz), es decir, más oscura.
- El siguiente render crea `versions/v14`.

## v11: bajo más grave

Igual que la v10, pero el bajo baja una octava más (raíces de A0 a E1; el golpe final pasa de 28 y 40 a 16 y 28).

- Pico 0.790, RMS 0.1441 y centroide de la mezcla 2501 Hz (v10: 0.808, 0.1458 y 2514 Hz).
- Centroide del bajo 503 Hz (v10: 610 Hz). La energía del bajo bajo 100 Hz sube de 9 % a 53 %.
- Riesgo: la fundamental queda bajo 45 Hz y en parlantes chicos casi no se oye.

## v12: estéreo real y bajo de vuelta a la v10

La v11 se sintió demasiado grave, así que el bajo vuelve al registro de la v10 (la v11 queda como referencia). Además la mezcla era casi mono: cada instrumento se renderizaba en mono y los efectos también, por lo que solo el panning los separaba (correlación L/R de 0.970).

- Chorus con el LFO en contrafase entre canales (guitarra, lead, silbido y pad).
- Eco ping-pong sincronizado al tempo, que rebota entre izquierda y derecha (guitarra, synth, lead y silbido).
- Reverb con una respuesta distinta por canal, de modo que las colas queden descorrelacionadas.
- Bajo y batería siguen centrados; los stems ahora son WAV estéreo.
- Medición: correlación L/R 0.875 (v10: 0.970), pico 0.783, RMS 0.1401 y centroide por canal 2524 Hz (v10: 2510 Hz, v9: 2573 Hz).

## v13: bajo gigante y mezcla 3D

El bajo no necesitaba ser más grave sino llenar el espacio, así que se le suman dos capas (mismas notas y misma humanización que el bajo base) y se mueven las voces en el espacio.

**Bajo con presencia (sin subir el volumen)**
- `bass_sub`: senoidal en la fundamental de cada nota, con una segunda armónica suave. Es el retumbe, y queda centrado.
- `bass_dbl`: las mismas notas una octava arriba, con timbre de sintetizador, saturadas, filtradas bajo 140 Hz y abiertas en estéreo (chorus en contrafase y reverb). El grave queda al centro y los medios llenan los lados.
- Ganancias: bajo base 0.66 a 0.56, `bass_dbl` 0.22 y `bass_sub` 0.14, para que el nivel total no suba.

**Escena espacial** (los mismos sonidos, solo ubicados y movidos)
- Cada voz sigue una trayectoria por compás: azimut, profundidad y elevación (`SCENE` y `spatialize` en `build_song.py`).
- Izquierda y derecha: balance de potencia constante más una diferencia de tiempo entre oídos de hasta 0.7 ms.
- Atrás: más oscuro (pasa bajos) y un poco más bajo de nivel.
- Arriba y abajo: se realzan o se apagan los agudos. Es una aproximación, sin HRTF.
- Guitarra a la izquierda (con un vaivén lento) y synth a la derecha.
- Lead: llega desde el fondo en la intro y después se queda adelante y arriba, con un balanceo suave.
- Silbido: da vueltas alrededor del oyente (adelante, derecha, atrás, izquierda) cada 8 compases, arriba.
- Pad: respira detrás y arriba. `bass_dbl`: ligeramente abajo.
- Batería, bajo y sub quedan fijos al frente, como ancla. Se escucha mejor con auriculares.

**Medición** (v12 entre paréntesis)
- Pico 0.735 (0.783), RMS 0.1337 (0.1447) y centroide por canal 2613 Hz (2524 Hz). Sube un poco por el realce de agudos de las voces "arriba".
- Correlación L/R 0.814 (0.875).
- Energía de 30 a 80 Hz: 13.2 % (7.0 %).
