import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface WordTiming {
  text: string;
  start: number;
  end: number;
}

interface LyricLine {
  text: string;
  start: number;
  end: number;
  words?: WordTiming[];
}

interface Section {
  section: string;
  lines: LyricLine[];
}

interface RuinsTextProps {
  sections: Section[];
  fps?: number;
}

function dsin(frame: number, freq: number, phase = 0) {
  return Math.sin(frame * freq + phase);
}

export const RuinsText: React.FC<RuinsTextProps> = ({ sections, fps = 24 }) => {
  const frame = useCurrentFrame();
  const time = frame / fps;

  const allLines: (LyricLine & { section: string })[] = [];
  sections.forEach((s) =>
    s.lines.forEach((l) => allLines.push({ ...l, section: s.section }))
  );

  const currentLineIdx = allLines.findIndex(
    (l) => time >= l.start && time <= l.end
  );
  const currentLine = allLines[currentLineIdx] ?? null;
  const prevLine = currentLineIdx > 0 ? allLines[currentLineIdx - 1] : null;

  const lineProgress =
    currentLine && currentLine.end > currentLine.start
      ? (time - currentLine.start) / (currentLine.end - currentLine.start)
      : 0;

  const lineOpacity = currentLine
    ? interpolate(lineProgress, [0, 0.04, 0.88, 1], [0, 1, 1, 0.4], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 0;

  const prevOpacity = prevLine && currentLine
    ? interpolate(lineProgress, [0, 0.2, 0.6], [0.25, 0.1, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 0;

  const isBridge = currentLine?.section === "Bridge";
  const isOutro = currentLine?.section === "Outro";

  return (
    <svg width="1920" height="1080" style={{ position: "absolute", top: 0, left: 0 }}>

      {/* Section label — stenciled on wall, top-left */}
      {currentLine && (
        <text
          x={60}
          y={72}
          fontSize="16"
          fontFamily="'Courier New', monospace"
          fill="#404040"
          letterSpacing="6"
          opacity={interpolate(lineProgress, [0, 0.05, 0.3], [0.7, 0.7, 0], { extrapolateRight: "clamp" })}
          
        >
          — {currentLine.section.toUpperCase()} —
        </text>
      )}

      {/* Previous line — fading like old paint on wall */}
      {prevLine && !isBridge && (
        <text
          x={960}
          y={interpolate(lineProgress, [0, 0.6], [472, 450], { extrapolateRight: "clamp" })}
          textAnchor="middle"
          fontSize="34"
          fontFamily="'Courier New', monospace"
          fill="#3a3a3a"
          letterSpacing="3"
          opacity={prevOpacity}
          
        >
          {prevLine.text}
        </text>
      )}

      {/* Horizontal graffiti marks — wall texture context */}
      {currentLine && !isBridge && (
        <>
          <line
            x1={60} y1={520}
            x2={interpolate(lineProgress, [0, 0.15], [60, 400], { extrapolateRight: "clamp" })}
            y2={520}
            stroke="#2a2a2a" strokeWidth="1" opacity={lineOpacity * 0.6}
          />
          <line
            x1={1920 - 60} y1={520}
            x2={interpolate(lineProgress, [0, 0.15], [1920 - 60, 1920 - 400], { extrapolateRight: "clamp" })}
            y2={520}
            stroke="#2a2a2a" strokeWidth="1" opacity={lineOpacity * 0.6}
          />
        </>
      )}

      {/* Current line */}
      {currentLine && isBridge && (
        <BridgeQuote line={currentLine} frame={frame} time={time} lineOpacity={lineOpacity} />
      )}
      {currentLine && isOutro && (
        <OutroWord line={currentLine} frame={frame} time={time} lineOpacity={lineOpacity} />
      )}
      {currentLine && !isBridge && !isOutro && (
        <StandardLine line={currentLine} frame={frame} time={time} lineOpacity={lineOpacity} />
      )}
    </svg>
  );
};

// ─── Standard verses / chorus ────────────────────────────────────────────────

const StandardLine: React.FC<{
  line: LyricLine & { section: string };
  frame: number;
  time: number;
  lineOpacity: number;
}> = ({ line, frame, time, lineOpacity }) => {
  const words = line.words ?? [];
  const glitchPulse = dsin(frame, 0.45) > 0.91;
  const glitchX = glitchPulse ? dsin(frame, 2.1) * 4 : 0;
  const glitchY = glitchPulse ? dsin(frame, 1.7) * 2 : 0;

  const fontSize = 68;
  const charW = fontSize * 0.58;
  const spaceW = charW;

  const totalW = words.reduce((acc, w) => acc + w.text.length * charW + spaceW, 0) - spaceW;
  let xCursor = 960 - totalW / 2;

  const elements: React.ReactNode[] = [];

  words.forEach((word, i) => {
    // A word stays "current" from its start until the NEXT word starts —
    // eliminates gaps in Vosk timing so the highlight tracks the vocal continuously
    const nextStart = i + 1 < words.length ? words[i + 1].start : word.end;
    const isCurrent = time >= word.start && time < nextStart;
    const isPast = time >= nextStart;
    const isVisible = time >= word.start;

    const wx = xCursor + (isCurrent ? glitchX : isPast ? dsin(frame, 0.015, i * 1.4) * 1.2 : 0);
    const wy = 560 + (isCurrent ? glitchY : 0);

    if (isVisible) {
      // Chromatic aberration on current word
      if (isCurrent && glitchPulse) {
        elements.push(
          <text key={`r${i}`} x={wx - 3} y={wy} fontSize={fontSize} fontFamily="'Courier New', monospace" fontWeight="bold" fill="#cc2020" opacity={0.2 * lineOpacity} letterSpacing="2">{word.text}</text>,
          <text key={`c${i}`} x={wx + 3} y={wy} fontSize={fontSize} fontFamily="'Courier New', monospace" fontWeight="bold" fill="#009999" opacity={0.15 * lineOpacity} letterSpacing="2">{word.text}</text>
        );
      }

      // The word itself — spray-painted on wall look
      elements.push(
        <text
          key={`w${i}`}
          x={wx}
          y={wy}
          fontSize={isCurrent ? fontSize + 2 : fontSize}
          fontFamily="'Courier New', monospace"
          fontWeight={isCurrent ? "bold" : "normal"}
          fill={isCurrent ? "#e8e8e8" : isPast ? "#606060" : "#282828"}
          opacity={
            isCurrent ? lineOpacity
            : isPast ? lineOpacity * 0.5
            : lineOpacity * 0.18
          }
          letterSpacing="2"
          
        >
          {word.text}
        </text>
      );
    }

    xCursor += word.text.length * charW + spaceW;
  });

  return <g>{elements}</g>;
};

// ─── Bridge: vertical inscription on wall ────────────────────────────────────

const BridgeQuote: React.FC<{
  line: LyricLine & { section: string };
  frame: number;
  time: number;
  lineOpacity: number;
}> = ({ line, frame, time, lineOpacity }) => {
  const words = line.words ?? [];

  // Layout words across multiple centered rows (wrap), large font
  const fontSize = 64;
  const charW = fontSize * 0.56;
  const spaceW = charW;
  const maxRowW = 1500;

  // Build rows greedily
  const rows: WordTiming[][] = [];
  let row: WordTiming[] = [];
  let rowW = 0;
  words.forEach((w) => {
    const wW = w.text.length * charW + spaceW;
    if (rowW + wW > maxRowW && row.length > 0) {
      rows.push(row);
      row = [];
      rowW = 0;
    }
    row.push(w);
    rowW += wW;
  });
  if (row.length) rows.push(row);

  const lineH = fontSize * 1.4;
  const totalH = rows.length * lineH;
  const startY = 540 - totalH / 2 + fontSize / 2;

  const glitchPulse = dsin(frame, 0.45) > 0.9;
  const glitchX = glitchPulse ? dsin(frame, 2.0) * 4 : 0;

  return (
    <g>
      {/* Quotation marks — large, framing the quote */}
      <text x={130} y={340} fontSize={200} fontFamily="Georgia, serif" fill="#2a2a2a" opacity={lineOpacity * 0.5}>“</text>
      <text x={1660} y={860} fontSize={200} fontFamily="Georgia, serif" fill="#2a2a2a" opacity={lineOpacity * 0.5} textAnchor="end">”</text>

      {rows.map((r, ri) => {
        const totalW = r.reduce((acc, w) => acc + w.text.length * charW + spaceW, 0) - spaceW;
        let x = 960 - totalW / 2;
        const y = startY + ri * lineH;
        return (
          <g key={ri}>
            {r.map((word, wi) => {
              const globalIdx = words.indexOf(word);
              const nextStart = globalIdx + 1 < words.length ? words[globalIdx + 1].start : word.end;
              const isVisible = time >= word.start;
              const isCurrent = time >= word.start && time < nextStart;
              const isPast = time >= nextStart;
              if (!isVisible) {
                x += word.text.length * charW + spaceW;
                return null;
              }
              const wx = x + (isCurrent ? glitchX : 0);
              const fill = isCurrent ? "#e8e8e8" : isPast ? "#6a6a6a" : "#303030";
              const op = isCurrent ? lineOpacity : isPast ? lineOpacity * 0.6 : lineOpacity * 0.2;
              const el = (
                <text
                  key={wi}
                  x={wx}
                  y={y}
                  fontSize={fontSize}
                  fontFamily="'Courier New', monospace"
                  fill={fill}
                  opacity={op}
                  fontWeight={isCurrent ? "bold" : "normal"}
                  letterSpacing="2"
                >
                  {word.text.toUpperCase()}
                </text>
              );
              x += word.text.length * charW + spaceW;
              return el;
            })}
          </g>
        );
      })}
    </g>
  );
};

// ─── Outro: stencil word drops, large, stamped on wall ───────────────────────

const OutroWord: React.FC<{
  line: LyricLine & { section: string };
  frame: number;
  time: number;
  lineOpacity: number;
}> = ({ line, frame, time, lineOpacity }) => {
  const words = line.words ?? [];

  // Show all revealed words stacked / shifting — last one prominent
  const revealedWords = words.filter((w) => time >= w.start);
  if (!revealedWords.length) return null;

  const currentWord = revealedWords[revealedWords.length - 1];
  const wordProgress =
    currentWord.end > currentWord.start
      ? Math.min((time - currentWord.start) / (currentWord.end - currentWord.start), 1)
      : 1;

  const scale = interpolate(wordProgress, [0, 0.07, 1], [1.4, 1, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const opacity = interpolate(wordProgress, [0, 0.05, 0.85, 1], [0, lineOpacity, lineOpacity, lineOpacity * 0.65], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const glitch = dsin(frame, 0.5) > 0.9;
  const gx = glitch ? dsin(frame, 1.8) * 5 : 0;

  return (
    <g>
      {/* Previous words in line — small, above, fading */}
      {revealedWords.slice(0, -1).map((w, i) => (
        <text
          key={i}
          x={960}
          y={420 - (revealedWords.length - 2 - i) * 50}
          fontSize="32"
          fontFamily="'Courier New', monospace"
          fill="#404040"
          textAnchor="middle"
          letterSpacing="4"
          opacity={lineOpacity * 0.3}
          
        >
          {w.text.toUpperCase()}
        </text>
      ))}

      {/* Current word — big stencil stamp */}
      <g transform={`translate(960, 580) scale(${scale})`}>
        {glitch && (
          <>
            <text x={gx - 5} y={0} fontSize={90} fontFamily="'Courier New', monospace" fill="#aa1a1a" opacity={0.22 * opacity} textAnchor="middle" fontWeight="bold" letterSpacing="4">{currentWord.text.toUpperCase()}</text>
            <text x={gx + 5} y={0} fontSize={90} fontFamily="'Courier New', monospace" fill="#007777" opacity={0.18 * opacity} textAnchor="middle" fontWeight="bold" letterSpacing="4">{currentWord.text.toUpperCase()}</text>
          </>
        )}
        <text
          x={gx} y={0}
          fontSize={90}
          fontFamily="'Courier New', monospace"
          fill="#d8d8d8"
          opacity={opacity}
          textAnchor="middle"
          fontWeight="bold"
          letterSpacing="4"
          
        >
          {currentWord.text.toUpperCase()}
        </text>
      </g>
    </g>
  );
};
