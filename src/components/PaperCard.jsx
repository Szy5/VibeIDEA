import { useState } from "react";
import { theme } from "../theme";

export default function PaperCard({ paper }) {
  const [hover, setHover] = useState(false);
  const abstract = paper.tldr || paper.abstract || "";
  return (
    <a
      href={paper.link}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        display: "block",
        padding: theme.spacing.card,
        background: hover ? theme.colors.surfaceRaised : theme.colors.surface,
        border: `1px solid ${hover ? theme.colors.borderStrong : theme.colors.border}`,
        borderRadius: theme.radius.lg,
        cursor: "pointer",
        transition: `border-color ${theme.transition}, background ${theme.transition}, box-shadow ${theme.transition}`,
        boxShadow: hover ? `0 0 20px ${theme.colors.glow}20, 0 4px 12px rgba(0,0,0,0.2)` : "none",
      }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12, marginBottom: 8 }}>
        <span
          style={{
            fontFamily: theme.fonts.heading,
            fontSize: 14,
            fontWeight: 600,
            color: theme.colors.primary,
            lineHeight: 1.4,
            flex: 1,
            letterSpacing: "0.02em",
          }}
        >
          {paper.title}
        </span>
        <span
          style={{
            fontFamily: theme.fonts.mono,
            fontSize: 10,
            color: theme.colors.cta,
            whiteSpace: "nowrap",
            padding: "4px 8px",
            borderRadius: theme.radius.sm,
            background: `${theme.colors.cta}12`,
            border: `1px solid ${theme.colors.cta}40`,
            fontWeight: 500,
            letterSpacing: "0.05em",
          }}
        >
          {paper.category || paper.categories?.[0] || ""}
        </span>
      </div>
      <p
        style={{
          fontFamily: theme.fonts.body,
          fontSize: 13,
          color: theme.colors.textMuted,
          lineHeight: 1.6,
          margin: 0,
          display: "-webkit-box",
          WebkitLineClamp: 3,
          WebkitBoxOrient: "vertical",
          overflow: "hidden",
        }}
      >
        {abstract}
      </p>
      <div style={{ marginTop: 12, display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{ fontFamily: theme.fonts.mono, fontSize: 11, color: theme.colors.textSubtle }}>
          {paper.arxivId || paper.id} · {paper.date || ""}
        </span>
        <span
          style={{
            fontFamily: theme.fonts.mono,
            fontSize: 12,
            color: theme.colors.cta,
            fontWeight: 500,
            display: "inline-flex",
            alignItems: "center",
            gap: 4,
            letterSpacing: "0.03em",
          }}
        >
          阅读全文
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M7 17L17 7M17 7H7M17 7v10" />
          </svg>
        </span>
      </div>
    </a>
  );
}
