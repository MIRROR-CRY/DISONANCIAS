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
