import React, { useMemo } from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface Word {
  text: string;
  start: number;
  end: number;
}

interface AnimatedWordsProps {
  words: Word[];
  fps?: number;
}

export const AnimatedWords: React.FC<AnimatedWordsProps> = ({
  words,
  fps = 24,
}) => {
  const frame = useCurrentFrame();
  const timeInSeconds = frame / fps;

  const activeWords = useMemo(
    () =>
      words.map((word, index) => {
        const isActive = timeInSeconds >= word.start && timeInSeconds <= word.end;
        const progress = isActive
          ? (timeInSeconds - word.start) / (word.end - word.start)
          : timeInSeconds < word.start
            ? -1
            : 1;

        // Position variations for dynamic layout
        const baseY = 300 + (index % 5) * 120;
        const baseX = 200 + (index % 8) * 200;

        return {
          ...word,
          isActive,
          progress,
          x: baseX + Math.sin(index) * 100,
          y: baseY + Math.cos(index) * 80,
        };
      }),
    [words, timeInSeconds, fps]
  );

  return (
    <svg width="1920" height="1080" style={{ position: "absolute" }}>
      {activeWords.map((word, idx) => {
        const opacity = word.isActive
          ? Math.sin(word.progress * Math.PI) // fade in-out
          : 0;
        const scale = 1 + word.progress * 0.3; // slight grow
        const rotation = word.progress * 10; // subtle rotation

        return (
          <g
            key={idx}
            transform={`translate(${word.x}, ${word.y}) scale(${scale}) rotate(${rotation})`}
            opacity={opacity}
          >
            <text
              fontSize="48"
              fill="#ffffff"
              fontFamily="Arial, sans-serif"
              fontWeight="bold"
              textAnchor="middle"
              style={{ pointerEvents: "none" }}
            >
              {word.text}
            </text>
          </g>
        );
      })}
    </svg>
  );
};
