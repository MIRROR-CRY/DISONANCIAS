# Instrucciones: Subir a GitHub

## Paso 1: Crear la organización

1. Ve a github.com/organizations/new
2. Nombre: `Void Child`
3. Descripción: "VOID CHILD — Composer from San Borja, Santiago"
4. Plan: Free
5. Crear

## Paso 2: Crear el repositorio

1. En la organización Void Child, haz clic en "New repository"
2. Nombre: `Disonancias`
3. Descripción: "A four-track concept album about lies and cognitive dissonance"
4. Visibilidad: **Public**
5. NO inicializar con README (ya lo tenemos)
6. Crear repositorio

## Paso 3: Conectar y subir desde esta carpeta

Desde tu terminal (en esta carpeta `/tmp/disonancias-repo`):

```bash
cd /tmp/disonancias-repo

# Configurar remote
git remote add origin https://github.com/void-child/disonancias.git

# Renombrar branch a main (opcional pero recomendado)
git branch -M main

# Agregar todos los archivos
git add .

# Commit inicial
git commit -m "feat: initial release of DISONANCIAS album

Complete creative record:
- Code-generated backing tracks (custom Python generators)
- Vocal recordings and analysis
- Visual assets (album cover)
- Strategic positioning documents
- Full transparency on process

Album structure: Verse → Bridge → Verse → Chorus
Theme: Examination of lies at four scales (political, personal, inherited, collective)
Distribution: Bandcamp-first, then Spotify via RouteNote"

# Subir a GitHub
git push -u origin main
```

## Paso 4: Configurar README en GitHub

GitHub debería mostrar el README.md automáticamente. Si no:
1. Refresh la página del repo
2. El README debería aparecer en la sección principal

## Paso 5: Agregar tópicos (tags)

En GitHub, sección "About":
- Tags recomendadas: `music`, `album`, `code-composition`, `experimental`, `independent`

## Paso 6: Hacer README editable

Opcionalmente, en el README de GitHub puedes añadir:
- Link a Bandcamp (cuando esté listo)
- Link a redes sociales (cuando esté listo)

---

¿Preguntas? Todo está listo en `/tmp/disonancias-repo`.
