# Cumbia sonora — idea guardada para una canción futura

## Qué es esto

Una base de **cumbia sonora chilena** (linaje Sonora Palacios / Tommy Rey, la
cumbia brillante de intro de teleserie) generada íntegramente por código:
arreglo, interpretación humanizada, y mezcla con EQ/compresión/paneo por
instrumento.

Nació como intento de backing track para "Medio Limón", pero esa
canción va por otro lado. Se guarda acá porque el resultado quedó bueno por sí
mismo y merece ser el punto de partida de otra canción, no morir como descarte.

## Archivos

| Archivo | Qué es |
|---|---|
| `cumbia_sonora_v4.wav` | La pista, 2:13, mezclada y masterizada |
| `generate_cumbia_sonora.py` | El generador completo. Semilla fija (7), así que regenera exactamente la misma pista |
| `PRODUCCION.md` | Toda la documentación técnica: estilo, instrumentación, balance medido, control de calidad |

## Ficha rápida

- **Tempo**: 130 BPM, 4/4 (pulso de bombo percibido: 65/min)
- **Tonalidad**: Do mayor
- **Armonía**: C - Am - F - G7
- **Duración**: 2:13
- **Instrumentos**: 2 trompetas armonizadas, trombón, guitarra limpia (charchazo),
  bajo en tumbao, órgano, percusión afrolatina con cencerro en los 4 tiempos
- **Estructura**: intro / verso / pre-coro / coro ×2 / verso / pre-coro / coro /
  outro ×2 con fade

## Para retomarla

La pista ya tiene estructura completa de canción (versos, pre-coros, coros,
outro), así que se le puede escribir letra encima directamente. El riff de
metales de 4 compases funciona como gancho y vuelve en cada coro.

Si se quiere modificar, el generador está parametrizado: tempo, tonalidad,
progresión por sección, estructura en compases y balance de mezcla están todos
como constantes arriba del archivo.

```bash
python3 generate_cumbia_sonora.py
```

---
**Guardada**: 2026-09-22
**Origen**: descarte de "Medio Limón" v4
**Estado**: base instrumental terminada, sin letra
