import React from "react";
import { useCurrentFrame } from "remotion";

function seed(n: number) {
  const x = Math.sin(n + 1) * 43758.5453;
  return x - Math.floor(x);
}

// All crack paths are static (pre-computed, no per-frame math)
const MAIN_CRACKS = [
  "M 310 0 C 295 280 340 540 285 1080",
  "M 750 0 C 780 300 740 560 770 1080",
  "M 1180 0 C 1160 400 1220 640 1175 1080",
  "M 1690 0 C 1715 320 1668 570 1705 1080",
  "M 0 220 C 280 340 550 460 880 610",
  "M 1920 380 C 1610 490 1310 570 960 700",
];

const SMALL_CRACKS = Array.from({ length: 28 }, (_, i) => ({
  x1: seed(i * 11) * 1920,
  y1: seed(i * 17) * 1080,
  x2: seed(i * 11) * 1920 + (seed(i * 23) - 0.5) * 120,
  y2: seed(i * 17) * 1080 + (seed(i * 29) - 0.5) * 120,
  opacity: 0.15 + seed(i * 7) * 0.25,
}));

const DEBRIS = Array.from({ length: 18 }, (_, i) => ({
  x: seed(i * 13) * 1920,
  y: 970 + seed(i * 19) * 90,
  r: 2 + seed(i * 31) * 10,
  opacity: 0.12 + seed(i * 5) * 0.2,
}));

export const CracksLayer: React.FC<{ opacity?: number }> = ({ opacity = 0.4 }) => {
  const frame = useCurrentFrame();
  const t = frame / 24;
  // Only 2 animated values — the rest is static
  const pulse1 = 0.5 + Math.sin(t * 0.15) * 0.15;
  const pulse2 = 0.5 + Math.sin(t * 0.12 + 1.4) * 0.15;

  return (
    <svg width="1920" height="1080" viewBox="0 0 1920 1080"
      style={{ position: "absolute", top: 0, left: 0, pointerEvents: "none" }}>

      {/* Main structural cracks — slow pulse */}
      <g stroke="#353535" fill="none" opacity={opacity * pulse1}>
        {MAIN_CRACKS.map((d, i) => (
          <path key={i} d={d} strokeWidth={i < 4 ? 1.5 : 1} />
        ))}
      </g>

      {/* Secondary hairline cracks — static */}
      <g stroke="#252525" fill="none" opacity={opacity * 0.6}>
        {SMALL_CRACKS.map((c, i) => (
          <line key={i} x1={c.x1} y1={c.y1} x2={c.x2} y2={c.y2}
            strokeWidth="0.8" opacity={c.opacity} />
        ))}
      </g>

      {/* Dark erosion patches — slow pulse, only 8 */}
      <g fill="#070707" opacity={opacity * pulse2 * 0.5}>
        {Array.from({ length: 8 }).map((_, i) => (
          <ellipse key={i}
            cx={seed(i * 37) * 1920}
            cy={seed(i * 41) * 1080}
            rx={25 + seed(i * 29) * 55}
            ry={15 + seed(i * 53) * 35}
          />
        ))}
      </g>

      {/* Debris */}
      <g fill="#1a1a1a">
        {DEBRIS.map((d, i) => (
          <circle key={i} cx={d.x} cy={d.y} r={d.r} opacity={d.opacity} />
        ))}
      </g>

      {/* Border vignette */}
      <rect x="0" y="0" width="1920" height="1080"
        fill="none" stroke="#000000" strokeWidth="110" opacity="0.45" />
    </svg>
  );
};
