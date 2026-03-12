import { useState, useEffect } from "react";
import { theme } from "../theme";
import { RECOMMENDATIONS_URL } from "../constants/api";
import PaperCard from "../components/PaperCard";

export default function ArxivDaily() {
  const [search, setSearch] = useState("");
  const [papers, setPapers] = useState([]);
  const [meta, setMeta] = useState({ date: "", count: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetch(RECOMMENDATIONS_URL)
      .then((res) => {
        if (!res.ok) throw new Error(res.status === 404 ? "no_data" : res.statusText);
        return res.json();
      })
      .then((data) => {
        if (!cancelled && data && Array.isArray(data.papers)) {
          setPapers(data.papers);
          setMeta({ date: data.date || "", count: data.count ?? data.papers.length });
        } else if (!cancelled) {
          setPapers([]);
          setMeta({});
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setPapers([]);
          setMeta({});
          setError(err.message === "no_data" ? null : err.message);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  const filtered = papers.filter(
    (p) =>
      !search.trim() ||
      (p.title || "").toLowerCase().includes(search.toLowerCase()) ||
      (p.abstract || "").toLowerCase().includes(search.toLowerCase()) ||
      (p.tldr || "").toLowerCase().includes(search.toLowerCase()) ||
      (p.category || "").toLowerCase().includes(search.toLowerCase()) ||
      (p.categories || []).some((c) => c.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div
      style={{
        flex: 1,
        overflow: "auto",
        padding: theme.spacing.section,
        maxWidth: 900,
        margin: "0 auto",
        width: "100%",
      }}
    >
      <div style={{ marginBottom: theme.spacing.section }}>
        <h1
          style={{
            fontFamily: theme.fonts.heading,
            fontSize: 28,
            fontWeight: 600,
            color: theme.colors.primary,
            margin: "0 0 8px 0",
            letterSpacing: "0.06em",
            textShadow: `0 0 24px ${theme.colors.glow}30`,
          }}
        >
          每日 ArXiv 推荐
        </h1>
        <p style={{ fontFamily: theme.fonts.mono, fontSize: 12, color: theme.colors.textSubtle, margin: 0, letterSpacing: "0.04em" }}>
          {meta.date ? `${meta.date} · 共 ${meta.count} 篇` : "TODAY'S RECOMMENDED PAPERS · CLICK TO OPEN ON ARXIV"}
        </p>
      </div>

      <div style={{ marginBottom: theme.spacing.card, position: "relative" }}>
        <svg
          style={{ position: "absolute", left: 14, top: "50%", transform: "translateY(-50%)", pointerEvents: "none" }}
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke={theme.colors.textMuted}
          strokeWidth="2"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.35-4.35" />
        </svg>
        <input
          type="search"
          placeholder="搜索标题、摘要或分类…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="搜索论文"
          style={{
            width: "100%",
            maxWidth: 400,
            padding: "12px 16px 12px 44px",
            fontFamily: theme.fonts.mono,
            fontSize: 14,
            color: theme.colors.primary,
            background: theme.colors.surface,
            border: `1px solid ${theme.colors.border}`,
            borderRadius: theme.radius.md,
            outline: "none",
            transition: `border-color ${theme.transition}, box-shadow ${theme.transition}`,
          }}
          onFocus={(e) => {
            e.target.style.borderColor = theme.colors.cta;
            e.target.style.boxShadow = `0 0 0 2px ${theme.colors.glow}40`;
          }}
          onBlur={(e) => {
            e.target.style.borderColor = theme.colors.border;
            e.target.style.boxShadow = "none";
          }}
        />
      </div>

      {loading ? (
        <p style={{ fontFamily: theme.fonts.mono, color: theme.colors.textSubtle, fontSize: 13, letterSpacing: "0.03em" }}>
          // 加载推荐数据…
        </p>
      ) : error ? (
        <p style={{ fontFamily: theme.fonts.mono, color: theme.colors.textSubtle, fontSize: 13, letterSpacing: "0.03em" }}>
          // 加载失败：{error}
        </p>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: theme.spacing.card }}>
          {filtered.length === 0 ? (
            <p style={{ fontFamily: theme.fonts.mono, color: theme.colors.textSubtle, fontSize: 13, letterSpacing: "0.03em" }}>
              {papers.length === 0
                ? "// 暂无推荐数据，请先运行 main.py 生成每日推荐并写入 public/recommendations/latest.json"
                : "// 暂无匹配的推荐论文"}
            </p>
          ) : (
            filtered.map((paper) => <PaperCard key={paper.id || paper.arxivId} paper={paper} />)
          )}
        </div>
      )}
    </div>
  );
}
