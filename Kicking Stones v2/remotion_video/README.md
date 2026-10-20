# Kicking Stones - Remotion Video

Video profesional generado con código para "Kicking Stones" en inglés.

## Features

- **Arquitectura abstracta** generada con SVG/Canvas - edificios grises abandonados
- **Sincronización de letras** frame-by-frame con `lyrics_timing.json`
- **Animaciones dinámicas** - palabras transforman, aparecen/desaparecen
- **Efectos visuales** sincronizados con música

## Instalación

```bash
npm install
```

## Desarrollo

```bash
npm start
```

Abre http://localhost:3000 para ver preview en tiempo real.

## Render

```bash
npm run build:video
```

Genera MP4 en `out/` folder.

## Estructura

- `src/Video.tsx` - Composición principal, sincronización con audio
- `src/components/AbstractArchitecture.tsx` - Geometría urbana abstracta
- `src/components/AnimatedWords.tsx` - Sistema de animación de palabras
- `src/utils/lyrics.ts` - Utilidades para cargar/parsear lyrics

## Audio

Necesita:
- `../final_master/KickingStonesv5.mp3` - Audio track
- `../lyrics_timing.json` - Timing de letras (ya exists)

## Customización

Edita `AbstractArchitecture.tsx` para cambiar:
- Formas de edificios
- Colores (paleta gris)
- Animaciones
- Opacity/efectos

Edita `AnimatedWords.tsx` para cambiar:
- Posición de palabras
- Animación (scale, rotation, fade)
- Tamaño de fuente
