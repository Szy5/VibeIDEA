/**
 * Design system: Research Daily — 科技风 / Tech & Sci‑fi
 * 深色背景、青色主色、网格与微光
 */
export const theme = {
  colors: {
    primary: "#E2E8F0",
    secondary: "#94A3B8",
    cta: "#22D3EE",
    ctaDim: "#0891B2",
    accent: "#06B6D4",
    success: "#10B981",
    background: "#0A0E17",
    backgroundMuted: "#0F1419",
    surface: "#151B26",
    surfaceRaised: "#1A2234",
    border: "rgba(34, 211, 238, 0.15)",
    borderStrong: "rgba(34, 211, 238, 0.35)",
    glow: "rgba(34, 211, 238, 0.4)",
    text: "#E2E8F0",
    textMuted: "#94A3B8",
    textSubtle: "#64748B",
  },
  fonts: {
    heading: "'Orbitron', 'Noto Sans SC', sans-serif",
    body: "'JetBrains Mono', 'Fira Code', 'Noto Sans SC', monospace",
    sans: "'Noto Sans SC', sans-serif",
    mono: "'JetBrains Mono', 'Fira Code', monospace",
  },
  spacing: {
    section: 48,
    card: 24,
    tight: 12,
  },
  transition: "200ms ease",
  radius: { sm: 6, md: 8, lg: 12 },
};

export const fontImports = `
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Noto+Sans+SC:wght@300;400;500;600&display=swap');
`;
