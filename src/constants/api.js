/**
 * 前端接口与静态资源 URL 常量
 * 开发/生产均从 Vite 的 public 目录提供，如需代理可在此扩展
 */
export const RECOMMENDATIONS_URL = "/recommendations/latest.json";

/** 科学发现知识图谱全局图数据（public/graph/papers_kg.json） */
const BASE = (import.meta.env.BASE_URL || "/").replace(/\/$/, "");
export const GRAPH_JSON_URL = `${BASE}/graph/papers_kg.json`;
