import React from "react";
import { useCurrentFrame } from "remotion";

interface Props {
  opacity?: number;
  energyLevel?: number;
}

function seed(n: number) {
  const x = Math.sin(n + 1) * 43758.5453;
  return x - Math.floor(x);
}

const BASE_Y = 1060;

// Pre-computed buildings — all static, no per-frame math except drift
const BUILDINGS = [
  { x: -20,  w: 240, h: 820, depth: 0, notch: false },
  { x: 195,  w: 275, h: 920, depth: 1, notch: true,  nx: 320, nd: 45 },
  { x: 445,  w: 200, h: 740, depth: 0, notch: false },
  { x: 615,  w: 355, h: 960, depth: 2, notch: true,  nx: 820, nd: 60 },
  { x: 935,  w: 265, h: 880, depth: 1, notch: false },
  { x: 1165, w: 310, h: 1000, depth: 2, notch: true, nx: 1350, nd: 35 },
  { x: 1445, w: 235, h: 820, depth: 0, notch: false },
  { x: 1645, w: 290, h: 900, depth: 1, notch: true,  nx: 1800, nd: 50 },
];

// Window rows — 4 simple lines per building (very cheap)
function windowLines(b: typeof BUILDINGS[0]) {
  const lines: { y: number }[] = [];
  const step = 55;
  const topY = BASE_Y - b.h + 25;
  for (let y = topY + step; y < BASE_Y - 20; y += step) {
    lines.push({ y });
  }
  return lines;
}

export const AbstractArchitecture: React.FC<Props> = ({ opacity = 1 }) => {
  const frame = useCurrentFrame();
  const t = frame / 24;
  const driftX = Math.sin(t * 0.03) * 8;
  const driftY = Math.cos(t * 0.025) * 4;

  return (
    <svg width="1920" height="1080" viewBox="0 0 1920 1080"
      style={{ position: "absolute", top: 0, left: 0, opacity }}>
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#090d12" />
          <stop offset="100%" stopColor="#10161e" />
        </linearGradient>
        <linearGradient id="fog" x1="0" y1="0" x2="0" y2="1">
          <stop offset="60%" stopColor="#0a0a0a" stopOpacity="0" />
          <stop offset="100%" stopColor="#0a0a0a" stopOpacity="0.88" />
        </linearGradient>
        <linearGradient id="fogTop" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#090d12" stopOpacity="0.7" />
          <stop offset="18%" stopColor="#090d12" stopOpacity="0" />
        </linearGradient>
      </defs>

      {/* Sky */}
      <rect width="1920" height="1080" fill="url(#sky)" />

      {/* Buildings */}
      <g transform={`translate(${driftX},${driftY})`}>
        {BUILDINGS.map((b, bi) => {
          const topY = BASE_Y - b.h;
          const fill = b.depth === 0 ? "#0f0f0f" : b.depth === 1 ? "#151515" : "#1b1b1b";
          const stroke = b.depth === 0 ? "#1e1e1e" : b.depth === 1 ? "#272727" : "#303030";
          const roof = b.notch && b.nx && b.nd
            ? `M${b.x},${BASE_Y} L${b.x},${topY} L${b.nx - 25},${topY} L${b.nx},${topY + b.nd} L${b.nx + 35},${topY + 8} L${b.x + b.w},${topY} L${b.x + b.w},${BASE_Y} Z`
            : `M${b.x},${BASE_Y} L${b.x},${topY} L${b.x + b.w},${topY} L${b.x + b.w},${BASE_Y} Z`;

          return (
            <g key={bi}>
              <path d={roof} fill={fill} stroke={stroke} strokeWidth="1.5" />
              {/* Window rows — horizontal lines across building */}
              <g stroke={stroke} strokeWidth="1" opacity="0.7" clipPath="">
                {windowLines(b).map((wl, wi) => (
                  <line key={wi} x1={b.x + 8} y1={wl.y} x2={b.x + b.w - 8} y2={wl.y} />
                ))}
              </g>
              {/* Vertical window column dividers — 4-5 per building */}
              {Array.from({ length: 5 }).map((_, vi) => (
                <line key={vi}
                  x1={b.x + (b.w / 5) * vi + b.w / 10}
                  y1={topY + 20}
                  x2={b.x + (b.w / 5) * vi + b.w / 10}
                  y2={BASE_Y - 10}
                  stroke={stroke} strokeWidth="0.8" opacity="0.5" />
              ))}
              {/* One structural band */}
              <line x1={b.x} y1={BASE_Y - b.h * 0.45} x2={b.x + b.w} y2={BASE_Y - b.h * 0.45}
                stroke={stroke} strokeWidth="3" />
            </g>
          );
        })}
      </g>

      {/* Ground */}
      <rect x="0" y={BASE_Y} width="1920" height={1080 - BASE_Y} fill="#0b0b0b" />
      <line x1="0" y1={BASE_Y} x2="1920" y2={BASE_Y} stroke="#202020" strokeWidth="1.5" />

      {/* Fog overlays */}
      <rect width="1920" height="1080" fill="url(#fog)" />
      <rect width="1920" height="1080" fill="url(#fogTop)" />

      {/* Scanlines */}
      <g stroke="#ffffff" strokeWidth="1" opacity="0.025">
        {Array.from({ length: 27 }).map((_, i) => (
          <line key={i} x1="0" y1={i * 40} x2="1920" y2={i * 40} />
        ))}
      </g>
    </svg>
  );
};
