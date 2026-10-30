# lipsync

Herramienta estándar para sincronizar a mano una letra con su canción, palabra por palabra.

- Artifact publicado: https://claude.ai/artifact/VuZsxyN2MJVGCZZR39dsjm
- Fuente: `lipsync.template.html` (placeholders `__AUDIO__` data-URI y `__LYRICS__`). Para otra canción, reemplazar ambos y republicar.

## Uso
1. Cargar audio (selector) y pegar la letra con `[Sección]` en su línea, un verso por línea.
2. **Calibrar** reacción una vez (10 beeps).
3. Play y tocar **TAP** (o Espacio) justo cuando empieza cada palabra. Tocar una palabra la re-marca. `↶` deshace.
4. Exportar JSON (`<cancion>_timing.json`), SRT por palabra, o **Guardar para Claude** (doc `lipsync/<cancion>` en la db).

## Formato JSON
`{song, reactionOffsetMs, sections:[{section, lines:[{text,start,end,words:[{text,start,end,_tagged}]}]}]}` (segundos). Los builders de video (`build_tiktok.py`, `build_lyrics.py`) deben leer este formato.

## Biblioteca de canciones

El selector "Biblioteca" carga cada canción con su audio y letra:

- **Mirror Cry** (Bandcamp, sin tiempos: se sincroniza a mano).
- **Kicking Stones (EN)** y **(ES)**, con los tiempos del antiguo Editor de Timing ya precargados (editables).

La plantilla usa los placeholders `__MC__` (audio data-URI), `__KS__` (audio data-URI) y `__LIB__` (JSON de la biblioteca).

## GitHub Pages

`index.html` es la versión estática (audio en `audio/`, biblioteca en `library.json`). Con Pages activado desde `main` / raíz: https://mirror-cry.github.io/DISONANCIAS/lipsync/ . Descarga JSON/SRT con un enlace normal; "Guardar para Claude" solo existe dentro de claude.ai.
