import React from "react";
import { Composition, useCurrentFrame, Audio, staticFile } from "remotion";
import { AbstractArchitecture } from "./components/AbstractArchitecture";
import { RuinsText } from "./components/RuinsText";
import { CracksLayer } from "./components/CracksLayer";
import lyricsData from "./data/lyrics_timing.json";

const VIDEO_FPS = 24;
const VIDEO_WIDTH = 1920;
const VIDEO_HEIGHT = 1080;

// Derive video duration from last lyric line
const lastSection = lyricsData[lyricsData.length - 1];
const lastLine = lastSection.lines[lastSection.lines.length - 1];
const VIDEO_DURATION_S = lastLine ? Math.ceil(lastLine.end) + 3 : 140;
const VIDEO_DURATION_FRAMES = VIDEO_DURATION_S * VIDEO_FPS;

export const KickingStonesVideo: React.FC = () => {
  return (
    <Composition
      id="KickingStones"
      component={KickingStonesComposition}
      durationInFrames={VIDEO_DURATION_FRAMES}
      fps={VIDEO_FPS}
      width={VIDEO_WIDTH}
      height={VIDEO_HEIGHT}
      defaultProps={{}}
    />
  );
};

const KickingStonesComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const time = frame / VIDEO_FPS;

  // Slow breathing energy for background
  const energyLevel = Math.sin(time * 0.8) * 0.4 + 0.6;

  return (
    <div
      style={{
        position: "relative",
        width: VIDEO_WIDTH,
        height: VIDEO_HEIGHT,
        overflow: "hidden",
        backgroundColor: "#0a0a0a",
      }}
    >
      {/* Audio track */}
      <Audio src={staticFile("KickingStonesv5.mp3")} />

      {/* Brutalist concrete background */}
      <AbstractArchitecture energyLevel={energyLevel} opacity={0.45} />

      {/* Decay/cracks overlay */}
      <CracksLayer opacity={0.5} />

      {/* Lyrics — word by word, ruins style */}
      <RuinsText sections={lyricsData as any} fps={VIDEO_FPS} />

      {/* Vignette — cold, dark edges */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          background:
            "radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 40%, rgba(0,0,0,0.75) 100%)",
          pointerEvents: "none",
        }}
      />
    </div>
  );
};
