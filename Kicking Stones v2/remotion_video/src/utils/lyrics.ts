// Parse lyrics_timing.json
export interface LyricLine {
  text: string;
  start: number;
  end: number;
}

export interface Section {
  section: string;
  lines: LyricLine[];
}

export const loadLyrics = async (): Promise<Section[]> => {
  const response = await fetch("../lyrics_timing.json");
  return response.json();
};

// Get words with precise timing
export const getWordsWithTiming = (lines: LyricLine[]) => {
  return lines.flatMap((line) => {
    const words = line.text.split(" ");
    const wordDuration = (line.end - line.start) / words.length;
    return words.map((word, i) => ({
      text: word,
      start: line.start + i * wordDuration,
      end: line.start + (i + 1) * wordDuration,
    }));
  });
};
