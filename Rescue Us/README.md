# Rescue Us — Decisiones de diseño

Este documento registra el *por qué* detrás de las decisiones creativas del proyecto, siguiendo el mismo formato usado en `Kicking Stones v2/README.md`. Ver `GEN_ALPHA_MELODY_ANALYSIS.md` y `GEN_ALPHA_MELODY_HOW_TO_PLAY.md` para la teoría musical, `BACKING_TRACK_README.md` para el detalle técnico del audio generado, y `ALBUM_CONCEPT.md` (carpeta padre `musica/`) para cómo esta canción se posiciona dentro del álbum conceptual junto a "Kicking Stones".

## Nombre anterior: "36@24 (36 at 24)"

Esta canción se llamó originalmente **"36@24 (36 at 24)"**, título tomado de la primera línea de letra escrita ("36, 36, not 20 not six-seven, just 36") cruzado con la edad real del autor (24) al momento de componer. Se renombró a **"Rescue Us"** porque, al simplificar la estructura de la canción a Verse 1 - Verse 2 - Chorus, se eliminó el Pre-Chorus que mencionaba el "36" — dejando el título sin ninguna conexión textual con la letra final. "Rescue Us" en cambio es una frase literal del hook ("You'll rescue me / I'll rescue you / please dear God / rescue us all"), por lo que sí tiene anclaje directo en la canción.

## Origen del proyecto

Nace como contraparte de "Kicking Stones": si esa canción es catarsis **externa** (crítica social), esta nace pensada como catarsis **interna** (autocrítica personal). La idea inicial fue simple: tomar la melodía de **"Dame Luz" de Nicole** en guitarra aguda como base, y usar la **melodía GenZ/Gen Alpha** (el patrón viral identificado por el musicólogo danés Carl E. Martin) como armonía.

## El Gen Alpha Melody: de curiosidad viral a herramienta compositiva

En julio-agosto 2026, un reportaje de NPR ("Do You Recognize the 'Gen Alpha Melody'?") documentó el hallazgo de Carl E. Martin: un patrón de 4 notas pilares presente en cientos de canciones pop desde 2010 (Clairo "Sofia", Rosé & Bruno Mars "APT.", Lewis Capaldi "Forever", Coldplay "Viva la Vida"). El patrón se describe en grados de escala **4°-7°-3°-6°**, que en Do Mayor corresponde a **Fa-Si-Mi-La (F-B-E-A)**.

Proceso de identificación del patrón exacto:
1. Primer intento (intuición del usuario, sin referencia externa): "Re-Do-Mi-Re" — movimiento correcto (baja-sube-baja) pero notas incorrectas.
2. El usuario, consciente de tener oído poco entrenado, pidió explícitamente **verificar con fuentes externas** en vez de confiar en la intuición.
3. Búsqueda web confirmó la transcripción exacta de Carl E. Martin: **F-B-E-A**, con estructura de "pregunta" (Fa→Si, tritono descendente) y "respuesta" (Mi→La, quinta descendente).
4. El usuario aportó una fuente adicional (captura de una respuesta de otro asistente) con los acordes de acompañamiento sugeridos: **Dm-G-C-F**, que terminaron siendo la base armónica del backing track.

Esto quedó documentado en detalle en `GEN_ALPHA_MELODY_ANALYSIS.md` (teoría) y `GEN_ALPHA_MELODY_HOW_TO_PLAY.md` (guía práctica de ejecución, con transposiciones a otras tonalidades).

## "Dame Luz" (Nicole): la melodía madre

Investigación de acordes reales de la canción original (Chordify, Cifra Club, e-chords): **tonalidad Eb Mayor**, 130 BPM. El outro repite "oh dame dame dame luz" sobre los acordes **D# A# Cm G#** (Ab-Eb-Bbm-Eb en notación de bemoles). Esta progresión del final es la que se tomó como referencia para las "apariciones espontáneas" de la melodía dentro del backing track: no es un sample de la canción original, sino una recreación sintetizada inspirada en su contorno melódico y armónico.

## Generación del backing track: mismo enfoque que Kicking Stones, otra herramienta

El usuario pidió explícitamente replicar el enfoque de "generar todo con código" usado en Kicking Stones v2 (ahí, Remotion para video; acá, síntesis de audio en Python). Se descartó usar samples reales de "Dame Luz" — la instrucción fue clara: **tomar la referencia armónica/melódica, no samplear literalmente**.

`generate_backing_track.py` sintetiza 4 capas con NumPy + SciPy (sin librerías de audio externas, sin samples):
- **Gen Alpha Melody** (F-B-E-A en loop, onda triangular, la columna hipnótica constante)
- **Acordes** (Dm-G-C-F, ondas seno superpuestas, el ancla armónica)
- **Bajo** (raíces D-G-C-F, onda seno pura)
- **Apariciones de Dame Luz** (contorno melódico simplificado inspirado en "oh dame dame luz", en momentos puntuales: 8s, 24s, 48s, 72s, 96s)

Cada nota usa envolvente ADSR para sonar natural en vez de un tono sintético plano. Resultado: 2 minutos, 44.1kHz, listo para grabar voz encima.

**Reacción del usuario al escuchar el resultado**: "es una canción muy distinta a la que yo te pedí, pero me encantó" — el resultado se desvió de la intención original (algo más cercano a "Dame Luz" con adornos de Gen Alpha) y terminó siendo su propia pieza, que el usuario decidió conservar tal cual en vez de corregir hacia el plan original.

## La sirena de ambulancia: enmarcado sonoro

Idea del usuario: agregar un sonido real de sirena de ambulancia grabada (no sintetizada) al inicio, con timbre similar al synth ya usado. Intentos de descarga automática (Pixabay, Wikimedia Commons, Freesound, YouTube) fallaron por política de red del entorno (egress bloqueado a dominios externos) — limitación de infraestructura, no técnica. El usuario subió directamente el archivo ("SONIDO DE AMBULANCIA (SIRENA DE EMERGENCIA) — LA BIBLIOTECA DEL SONIDO ASMR").

Instrucción explícita: **no modificar nada del backing track ya generado**, solo anteponer/agregar la sirena. Se extrajeron los primeros 5s (tras detectar 3.5s de silencio inicial en el archivo fuente) para el inicio, y los últimos 5s para el final — la canción queda enmarcada por la sirena en ambos extremos, subrayando la idea de "emergencia" que conecta con el tema de autocrítica/catarsis personal.

Resultado final: **130 segundos** = 5s sirena (intro) + 120s backing track original intacto + 5s sirena (outro).

## Letra: primer verso

Única línea escrita hasta ahora: *"36, 36, not 20 not six-seven, just 36"* — referencia cultural directa al meme viral "6-7" de 2025, jugando con la idea de afirmar una identidad/edad/número propio frente a la presión de encajar en categorías ajenas (conecta temáticamente con la autocrítica del track).

## El título: "Rescue Us"

Título elegido directamente a partir de esa primera línea de letra: el "36" que se repite y se afirma ("not 20, not six-seven, just 36") se cruza con el "24" (edad real del autor al momento de componer). El formato "@" evoca una marca de tiempo/ubicación ("36 en el momento 24" o "36 a los 24") — la tensión entre una cifra que se insiste como identidad propia y la edad real desde la que se canta, coherente con el eje de autocrítica/introspección del track.

## Tema central: la dificultad de encontrar el amor hoy

El "36" se define como **36 requisitos/casillas que debe cumplir la persona ideal** ("thirty six boxes to check"). La canción trata sobre lo difícil que es encontrar pareja en la actualidad, cuando todos buscan un ideal inalcanzable y, en algunos casos (autocrítica explícita del autor), se cargan demasiados requisitos sobre esa búsqueda. La intención es que sea una canción con la que mucha gente se sienta identificada: no es una queja externa (como en Kicking Stones), sino una autocrítica honesta sobre las propias exigencias al buscar el amor.

Esto conecta directamente con el "@" del título: 36 casillas que marcar, a los 24 años.

## Estado del proyecto

- ✅ Teoría del Gen Alpha Melody documentada y verificada con fuentes externas
- ✅ Acordes reales de "Dame Luz" identificados (Eb Mayor, outro en Ab-Eb-Bbm-Eb)
- ✅ Backing track generado por código (Python/NumPy), 2 min, 4 capas sintetizadas
- ✅ Sirena de ambulancia integrada al inicio y al final (grabación real proporcionada por el usuario)
- ✅ Álbum conceptual definido: Kicking Stones (catarsis externa) → esta canción (catarsis interna, puente)
- ✅ Título definido: "Rescue Us"
- ⏳ Letra: solo primera línea escrita
- ⏳ Grabación vocal sobre el backing track

Ver `BACKING_TRACK_README.md` para el detalle técnico del audio y `ALBUM_CONCEPT.md` (en `musica/`) para el arco narrativo del álbum.
