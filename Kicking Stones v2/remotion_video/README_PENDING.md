# Kicking Stones - Remotion Video (Professional Version)

Abstract lyric video with ruins/fragments aesthetic for English release.

## ✅ Completed

- Project structure (React + Remotion)
- AbstractArchitecture component (geometric building shapes)
- RuinsText component (fragmented, glitch-effect text)
- CracksLayer component (animated deterioration)
- Video composition (Audio sync, word-by-word timing)
- GitHub Action for CI/CD rendering
- Lyrics timing integration from `lyrics_timing.json`

## ⏳ Pending Tasks

### 1. **Install Dependencies & Test**
```bash
npm install
npm start  # Preview at localhost:3000
npm run build:video  # Render to MP4
```

### 2. **Enhance RuinsText Component**
- [ ] Add more glitch layers (RGB chromatic aberration)
- [ ] Implement text "falling" animation
- [ ] Add pixelation effect on text
- [ ] Vary opacity/decay per word

### 3. **Improve CracksLayer**
- [ ] More organic crack patterns (Perlin noise)
- [ ] Dust particle effects
- [ ] Debris floating animation
- [ ] Vignette darkening effect

### 4. **Visual Effects**
- [ ] Audio-reactive effects (beat detection)
- [ ] Distortion wave effect
- [ ] Color grade (desaturated, cold tones)
- [ ] Fade/transition between sections

### 5. **Performance Optimization**
- [ ] Optimize SVG renders
- [ ] Reduce draw calls
- [ ] Test rendering speed

### 6. **Final Render**
- [ ] Test full 2min video render
- [ ] Quality check
- [ ] Export final MP4

## Architecture

```
src/
├── index.ts                   # Entry point
├── Video.tsx                  # Main composition
└── components/
    ├── AbstractArchitecture.tsx  # Building geometry
    ├── RuinsText.tsx            # Fragmented text
    └── CracksLayer.tsx          # Decay/damage
```

## Key Files

- `../lyrics_timing.json` - Word-level timing data (synced with audio)
- `../final_master/KickingStonesv5.mp3` - Audio track
- `src/Video.tsx` - Links everything together

## Notes

- Remotion renders frame-by-frame (slower than real-time)
- 2min video @ 24fps = ~3000 frames
- Render time: ~10-20 minutes depending on effects complexity
- All text is data-driven from `lyrics_timing.json`

## Next Steps

1. Run `npm install` locally
2. Test with `npm start`
3. Implement missing effects one-by-one
4. Render and iterate
5. Final MP4 export when satisfied

---

**Español:**
Video profesional para lanzamiento en inglés.
Tema: Arquitectura deteriorada, ruinas urbanas, fragmentación.
Estética: Texto roto entre grietas, efectos glitch, geometría quebrada.
