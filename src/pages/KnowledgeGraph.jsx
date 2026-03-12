// KnowledgeGraph.jsx
import { useState, useEffect, useRef, useCallback } from "react";
import * as d3 from "d3";
import { theme } from "../theme";
import { GRAPH_JSON_URL } from "../constants/api";

// ── Sample Data ────────────────────────────────────────────────
const GRAPH_DATA = {
  nodes: [
    { id: "1", label: "机器学习", type: "concept", size: 48 },
    { id: "2", label: "神经网络", type: "concept", size: 40 },
    { id: "3", label: "反向传播", type: "method", size: 32 },
    { id: "4", label: "梯度下降", type: "method", size: 32 },
    { id: "5", label: "卷积神经网络", type: "model", size: 36 },
    { id: "6", label: "Transformer", type: "model", size: 38 },
    { id: "7", label: "注意力机制", type: "method", size: 34 },
    { id: "8", label: "自然语言处理", type: "concept", size: 40 },
    { id: "9", label: "BERT", type: "model", size: 30 },
    { id: "10", label: "GPT", type: "model", size: 30 },
    { id: "11", label: "图像识别", type: "concept", size: 34 },
    { id: "12", label: "ResNet", type: "model", size: 28 },
    { id: "13", label: "损失函数", type: "method", size: 28 },
    { id: "14", label: "过拟合", type: "concept", size: 26 },
    { id: "15", label: "正则化", type: "method", size: 26 },
    { id: "16", label: "数据增强", type: "method", size: 24 },
    { id: "17", label: "迁移学习", type: "concept", size: 30 },
    { id: "18", label: "强化学习", type: "concept", size: 34 },
  ],
  edges: [
    { source: "1", target: "2", label: "包含" },
    { source: "1", target: "18", label: "分支" },
    { source: "2", target: "3", label: "使用" },
    { source: "2", target: "4", label: "使用" },
    { source: "2", target: "13", label: "依赖" },
    { source: "2", target: "5", label: "衍生" },
    { source: "2", target: "6", label: "衍生" },
    { source: "6", target: "7", label: "核心机制" },
    { source: "6", target: "8", label: "应用于" },
    { source: "8", target: "9", label: "模型" },
    { source: "8", target: "10", label: "模型" },
    { source: "9", target: "17", label: "基于" },
    { source: "10", target: "17", label: "基于" },
    { source: "5", target: "11", label: "用于" },
    { source: "5", target: "12", label: "变体" },
    { source: "11", target: "16", label: "技术" },
    { source: "13", target: "3", label: "计算" },
    { source: "4", target: "3", label: "依赖" },
    { source: "14", target: "15", label: "解决方案" },
    { source: "15", target: "14", label: "缓解" },
    { source: "1", target: "14", label: "问题" },
  ],
};

const TYPE_CONFIG = {
  // 动态知识图谱节点类型
  paper_main: { color: "#22D3EE", glow: "#22D3EE80", label: "主论文" },
  paper_prior: { color: "#A78BFA", glow: "#A78BFA80", label: "前人工作" },
  // Demo 数据保留的类型
  concept: { color: "#6ee7f7", glow: "#6ee7f780", label: "概念" },
  method: { color: "#a78bfa", glow: "#a78bfa80", label: "方法" },
  model: { color: "#34d399", glow: "#34d39980", label: "模型" },
};

// 简单标题截断, 避免节点上文字过长
function shortenTitle(title) {
  if (!title) return "";
  const max = 22;
  return title.length > max ? `${title.slice(0, max)}…` : title;
}

// ── Main Component ─────────────────────────────────────────────
export default function KnowledgeGraph({ embedded = false }) {
  const svgRef = useRef(null);
  const containerRef = useRef(null);
  const simulationRef = useRef(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [dimensions, setDimensions] = useState({ w: 800, h: 600 });
  const [highlightedIds, setHighlightedIds] = useState(null);
  const [graphData, setGraphData] = useState(GRAPH_DATA);
  const [stats, setStats] = useState({
    nodes: GRAPH_DATA.nodes.length,
    edges: GRAPH_DATA.edges.length,
    types: Object.keys(TYPE_CONFIG).length,
  });

  // Load real knowledge graph data (public/graph/papers_kg.json), fallback to demo on failure
  useEffect(() => {
    fetch(GRAPH_JSON_URL)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((raw) => {
        if (!raw || !Array.isArray(raw.nodes) || !Array.isArray(raw.edges)) return;

        // Adapt backend schema {nodes, edges} -> front-end D3 schema
        const nodes = raw.nodes.map((n) => {
          const nodeType = n.source === "main" ? "paper_main" : "paper_prior";
          return {
            id: n.id,
            label: shortenTitle(n.title || n.id),
            type: nodeType,
            size: n.source === "main" ? 44 : 30,
            raw: n,
          };
        });
        const edges = raw.edges.map((e) => ({
          source: e.source,
          target: e.target,
          label: e.relation_type || e.role || "",
          raw: e,
        }));

        const data = { nodes, edges };
        setGraphData(data);
        setStats({
          nodes: data.nodes.length,
          edges: data.edges.length,
          types: Object.keys(TYPE_CONFIG).length,
        });
      })
      .catch((err) => {
        console.warn("[KnowledgeGraph] Failed to load graph JSON, using demo data:", err?.message || err);
      });
  }, []);

  // Search filtering
  useEffect(() => {
    if (!searchQuery.trim()) {
      setHighlightedIds(null);
      return;
    }
    const q = searchQuery.toLowerCase();
    const matched = graphData.nodes
      .filter((n) => n.label.toLowerCase().includes(q))
      .map((n) => n.id);
    const connectedEdges = graphData.edges.filter(
      (e) => matched.includes(e.source) || matched.includes(e.target),
    );
    const connectedNodes = new Set([
      ...matched,
      ...connectedEdges.flatMap((e) => [e.source, e.target]),
    ]);
    setHighlightedIds(connectedNodes);
  }, [searchQuery]);

  // Resize observer
  useEffect(() => {
    if (!containerRef.current) return;
    const ro = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      setDimensions({ w: width, h: height });
    });
    ro.observe(containerRef.current);
    return () => ro.disconnect();
  }, []);

  // D3 simulation
  useEffect(() => {
    const { w, h } = dimensions;
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const nodes = graphData.nodes.map((n) => ({ ...n }));
    const edges = graphData.edges.map((e) => ({ ...e }));

    // Defs: glow filter + arrowhead
    const defs = svg.append("defs");
    Object.entries(TYPE_CONFIG).forEach(([type, cfg]) => {
      const f = defs
        .append("filter")
        .attr("id", `glow-${type}`)
        .attr("x", "-50%")
        .attr("y", "-50%")
        .attr("width", "200%")
        .attr("height", "200%");
      f.append("feGaussianBlur")
        .attr("stdDeviation", "4")
        .attr("result", "blur");
      const merge = f.append("feMerge");
      merge.append("feMergeNode").attr("in", "blur");
      merge.append("feMergeNode").attr("in", "SourceGraphic");
    });

    defs
      .append("marker")
      .attr("id", "arrow")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 18)
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", theme.colors.textSubtle);

    // Layers
    const edgeLayer = svg.append("g").attr("class", "edges");
    const nodeLayer = svg.append("g").attr("class", "nodes");

    // Simulation
    const sim = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(edges)
          .id((d) => d.id)
          .distance(110)
          .strength(0.7),
      )
      .force("charge", d3.forceManyBody().strength(-380).distanceMax(550))
      .force("center", d3.forceCenter(w / 2, h / 2).strength(0.08))
      .force(
        "collide",
        d3
          .forceCollide((d) => d.size + 14)
          .strength(0.85)
          .iterations(3),
      )
      .alphaDecay(0.012);

    simulationRef.current = sim;

    // Edges
    const edgeSel = edgeLayer
      .selectAll("g.edge")
      .data(edges)
      .join("g")
      .attr("class", "edge");
    const edgeColor = "#94a3b8";
    const lines = edgeSel
      .append("line")
      .attr("stroke", edgeColor)
      .attr("stroke-width", 1.5)
      .attr("marker-end", "url(#arrow)")
      .attr("opacity", 0.7);

    const edgeLabels = edgeSel
      .append("text")
      .attr("fill", theme.colors.textMuted)
      .attr("font-size", "10px")
      .attr("font-family", theme.fonts.sans)
      .attr("text-anchor", "middle")
      .attr("dy", -4)
      .text((d) => d.label)
      .attr("opacity", 0);

    // Nodes
    const nodeSel = nodeLayer
      .selectAll("g.node")
      .data(nodes)
      .join("g")
      .attr("class", "node")
      .style("cursor", "pointer")
      .call(
        d3
          .drag()
          .on("start", (event, d) => {
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            d.fx = null;
            d.fy = null;
          }),
      );

    // Outer ring
    nodeSel
      .append("circle")
      .attr("r", (d) => d.size / 2 + 8)
      .attr("fill", "none")
      .attr("stroke", (d) => TYPE_CONFIG[d.type].color)
      .attr("stroke-width", 0.5)
      .attr("opacity", 0.3);

    // Main circle
    nodeSel
      .append("circle")
      .attr("r", (d) => d.size / 2)
      .attr("fill", (d) => `${TYPE_CONFIG[d.type].color}18`)
      .attr("stroke", (d) => TYPE_CONFIG[d.type].color)
      .attr("stroke-width", 1.5)
      .attr("filter", (d) => `url(#glow-${d.type})`);

    // Label
    nodeSel
      .append("text")
      .attr("dy", (d) => d.size / 2 + 16)
      .attr("text-anchor", "middle")
      .attr("fill", theme.colors.textMuted)
      .attr("font-size", (d) => Math.max(10, d.size / 3.5) + "px")
      .attr("font-family", theme.fonts.sans)
      .text((d) => d.label);

    // Node icon / initials
    nodeSel
      .append("text")
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("fill", (d) => TYPE_CONFIG[d.type].color)
      .attr("font-size", (d) => Math.max(9, d.size / 3.8) + "px")
      .attr("font-family", "'Noto Sans SC', sans-serif")
      .attr("font-weight", "600")
      .text((d) => d.label.slice(0, 2));

    // Click handler
    nodeSel.on("click", (event, d) => {
      event.stopPropagation();
      setSelectedNode((prev) => (prev?.id === d.id ? null : d));
    });

    // Hover
    nodeSel
      .on("mouseenter", (event, d) => {
        edgeLabels.attr("opacity", (e) =>
          e.source.id === d.id || e.target.id === d.id ? 0.9 : 0,
        );
        lines
          .attr("stroke", (e) =>
            e.source.id === d.id || e.target.id === d.id
              ? TYPE_CONFIG[d.type].color
              : edgeColor,
          )
          .attr("stroke-width", (e) =>
            e.source.id === d.id || e.target.id === d.id ? 2.5 : 1.5,
          )
          .attr("opacity", (e) =>
            e.source.id === d.id || e.target.id === d.id ? 1 : 0.2,
          );
        nodeSel.attr("opacity", (n) => {
          const connected = edges.some(
            (e) =>
              (e.source.id === d.id && e.target.id === n.id) ||
              (e.target.id === d.id && e.source.id === n.id),
          );
          return n.id === d.id || connected ? 1 : 0.25;
        });
      })
      .on("mouseleave", () => {
        edgeLabels.attr("opacity", 0);
        lines
          .attr("stroke", edgeColor)
          .attr("stroke-width", 1.5)
          .attr("opacity", 0.7);
        nodeSel.attr("opacity", 1);
      });

    svg.on("click", () => setSelectedNode(null));

    // Zoom
    const zoom = d3
      .zoom()
      .scaleExtent([0.3, 3])
      .on("zoom", (e) => {
        edgeLayer.attr("transform", e.transform);
        nodeLayer.attr("transform", e.transform);
      });
    svg.call(zoom);

    // Tick
    sim.on("tick", () => {
      lines
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);
      edgeLabels
        .attr("x", (d) => (d.source.x + d.target.x) / 2)
        .attr("y", (d) => (d.source.y + d.target.y) / 2);
      nodeSel.attr("transform", (d) => `translate(${d.x},${d.y})`);
    });

    return () => sim.stop();
  }, [dimensions]);

  // Apply search highlight to nodes
  useEffect(() => {
    if (!svgRef.current) return;
    d3.select(svgRef.current)
      .selectAll("g.node")
      .attr("opacity", (d) => {
        if (!highlightedIds) return 1;
        return highlightedIds.has(d.id) ? 1 : 0.15;
      });
  }, [highlightedIds]);

  // Get connected info for selected node
  const getNodeConnections = useCallback((node) => {
    if (!node) return [];
    return graphData.edges
      .filter((e) => e.source === node.id || e.target === node.id)
      .map((e) => {
        const otherId = e.source === node.id ? e.target : e.source;
        const other = graphData.nodes.find((n) => n.id === otherId);
        const dir = e.source === node.id ? "→" : "←";
        return { label: e.label, other, dir };
      });
  }, []);

  const graphContent = (
    <>
      <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>
        {/* Canvas */}
        <div ref={containerRef} style={{ flex: 1, position: "relative" }}>
          <svg
            ref={svgRef}
            width="100%"
            height="100%"
            style={{ display: "block" }}
          />

          {/* Legend */}
          <div
            style={{
              position: "absolute",
              bottom: 24,
              left: 24,
              display: "flex",
              flexDirection: "column",
              gap: 8,
              padding: "10px 14px",
              background: theme.colors.surface,
              border: `1px solid ${theme.colors.border}`,
              borderRadius: theme.radius.md,
              boxShadow: `0 0 12px ${theme.colors.glow}15`,
            }}
          >
            {Object.entries(TYPE_CONFIG).map(([type, cfg]) => (
              <div
                key={type}
                style={{ display: "flex", alignItems: "center", gap: 8 }}
              >
                <div
                  style={{
                    width: 10,
                    height: 10,
                    borderRadius: "50%",
                    background: cfg.color + "30",
                    border: `1.5px solid ${cfg.color}`,
                    boxShadow: `0 0 6px ${cfg.color}60`,
                  }}
                />
                <span
                  style={{
                    color: theme.colors.textMuted,
                    fontSize: 11,
                    fontFamily: theme.fonts.mono,
                    letterSpacing: "0.04em",
                  }}
                >
                  {cfg.label}
                </span>
              </div>
            ))}
          </div>

          {/* Hint */}
          <div
            style={{
              position: "absolute",
              bottom: 24,
              right: selectedNode ? 320 : 24,
              color: theme.colors.textSubtle,
              fontSize: 11,
              fontFamily: theme.fonts.mono,
              textAlign: "right",
              letterSpacing: "0.04em",
            }}
          >
            滚轮缩放 · 拖拽平移 · 点击选中
          </div>
        </div>

        {/* Detail Panel */}
        {selectedNode && (
          <div
            style={{
              width: 280,
              background: theme.colors.surface,
              borderLeft: `1px solid ${theme.colors.border}`,
              padding: 20,
              overflowY: "auto",
              flexShrink: 0,
              animation: "fadeIn .2s ease",
              boxShadow: `-8px 0 24px ${theme.colors.glow}10`,
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                marginBottom: 20,
              }}
            >
              <div>
                <div
                  style={{
                    color: theme.colors.primary,
                    fontSize: 14,
                    fontWeight: 600,
                    marginBottom: 4,
                    fontFamily: theme.fonts.heading,
                    letterSpacing: "0.03em",
                    lineHeight: 1.5,
                  }}
                >
                  {selectedNode.raw?.title || selectedNode.label}
                </div>
                <div
                  style={{
                    display: "inline-block",
                    padding: "4px 8px",
                    borderRadius: 4,
                    background: TYPE_CONFIG[selectedNode.type].color + "18",
                    border: `1px solid ${TYPE_CONFIG[selectedNode.type].color}50`,
                    color: TYPE_CONFIG[selectedNode.type].color,
                    fontSize: 10,
                    fontFamily: theme.fonts.mono,
                    letterSpacing: "0.05em",
                  }}
                >
                  {TYPE_CONFIG[selectedNode.type].label}
                </div>
              </div>
              <button
                onClick={() => setSelectedNode(null)}
                style={{
                  background: "none",
                  border: "none",
                  color: theme.colors.textSubtle,
                  cursor: "pointer",
                  fontSize: 20,
                  lineHeight: 1,
                  padding: 0,
                }}
              >
                ×
              </button>
            </div>

            {/* Node visual */}
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                margin: "16px 0",
              }}
            >
              <div
                style={{
                  width: selectedNode.size + 24,
                  height: selectedNode.size + 24,
                  borderRadius: "50%",
                  background: TYPE_CONFIG[selectedNode.type].color + "15",
                  border: `1.5px solid ${TYPE_CONFIG[selectedNode.type].color}`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: `0 0 24px ${TYPE_CONFIG[selectedNode.type].glow}`,
                }}
              >
                <span
                  style={{
                    color: TYPE_CONFIG[selectedNode.type].color,
                    fontWeight: 600,
                    fontSize: 14,
                  }}
                >
                  {selectedNode.label.slice(0, 2)}
                </span>
              </div>
            </div>

            {/* 元信息 + narrative */}
            {selectedNode.raw && (
              <div
                style={{
                  borderTop: `1px solid ${theme.colors.border}`,
                  paddingTop: 12,
                  marginTop: 8,
                  marginBottom: 12,
                }}
              >
                <div
                  style={{
                    color: theme.colors.textSubtle,
                    fontSize: 11,
                    fontFamily: theme.fonts.mono,
                    marginBottom: 6,
                    display: "flex",
                    flexDirection: "column",
                    gap: 4,
                  }}
                >
                  <span>
                    {selectedNode.raw.year ? `年份: ${selectedNode.raw.year}` : "年份: 未知"}
                  </span>
                  {selectedNode.raw.authors && (
                    <span>
                      作者:{" "}
                      <span style={{ fontFamily: theme.fonts.sans }}>
                        {selectedNode.raw.authors.join(", ")}
                      </span>
                    </span>
                  )}
                  {selectedNode.raw.arxiv_id && (
                    <span>
                      arXiv:{" "}
                      <a
                        href={`https://arxiv.org/abs/${selectedNode.raw.arxiv_id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ color: theme.colors.cta }}
                      >
                        {selectedNode.raw.arxiv_id}
                      </a>
                    </span>
                  )}
                  {selectedNode.raw.patterns && selectedNode.raw.patterns.length > 0 && (
                    <span>
                      模式:{" "}
                      {selectedNode.raw.patterns.map((p) => (
                        <span
                          key={p}
                          style={{
                            display: "inline-block",
                            padding: "2px 6px",
                            marginRight: 4,
                            borderRadius: 4,
                            background: `${theme.colors.backgroundMuted}`,
                            border: `1px solid ${theme.colors.border}`,
                            fontSize: 10,
                            fontFamily: theme.fonts.mono,
                          }}
                        >
                          {p}
                        </span>
                      ))}
                    </span>
                  )}
                </div>
                {selectedNode.raw.narratives &&
                  selectedNode.raw.narratives.length > 0 && (
                    <div
                      style={{
                        fontSize: 11,
                        color: theme.colors.textMuted,
                        lineHeight: 1.6,
                        whiteSpace: "pre-wrap",
                      }}
                    >
                      {selectedNode.raw.narratives[0]}
                    </div>
                  )}
              </div>
            )}

            <div style={{ borderTop: `1px solid ${theme.colors.border}`, paddingTop: 16 }}>
              <div
                style={{
                  color: theme.colors.textSubtle,
                  fontSize: 11,
                  letterSpacing: "0.1em",
                  marginBottom: 12,
                  fontFamily: theme.fonts.mono,
                }}
              >
                关联节点
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {getNodeConnections(selectedNode).map((conn, i) => (
                  <div
                    key={i}
                    onClick={() => setSelectedNode(conn.other)}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 8,
                      padding: "8px 10px",
                      borderRadius: 6,
                      background: theme.colors.backgroundMuted,
                      border: `1px solid ${theme.colors.border}`,
                      cursor: "pointer",
                      transition: "border-color .15s",
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor = TYPE_CONFIG[conn.other.type].color + "80";
                      e.currentTarget.style.boxShadow = `0 0 8px ${TYPE_CONFIG[conn.other.type].glow}`;
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor = theme.colors.border;
                      e.currentTarget.style.boxShadow = "none";
                    }}
                  >
                    <div
                      style={{
                        width: 8,
                        height: 8,
                        borderRadius: "50%",
                        background: TYPE_CONFIG[conn.other.type].color,
                        flexShrink: 0,
                        boxShadow: `0 0 6px ${TYPE_CONFIG[conn.other.type].color}80`,
                      }}
                    />
                    <span
                      style={{
                        color: theme.colors.textSubtle,
                        fontSize: 10,
                        fontFamily: theme.fonts.mono,
                        minWidth: 14,
                      }}
                    >
                      {conn.dir}
                    </span>
                    <span style={{ color: theme.colors.textMuted, fontSize: 11, flex: 1 }}>
                      {conn.other.label}
                    </span>
                    <span style={{ color: theme.colors.textSubtle, fontSize: 10 }}>
                      {conn.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div
              style={{
                marginTop: 16,
                borderTop: `1px solid ${theme.colors.border}`,
                paddingTop: 12,
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: theme.colors.textSubtle, fontSize: 11, fontFamily: theme.fonts.mono }}>节点大小</span>
                <span
                  style={{
                    color: theme.colors.cta,
                    fontSize: 11,
                    fontFamily: theme.fonts.mono,
                  }}
                >
                  {selectedNode.size}
                </span>
              </div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: 6,
                }}
              >
                <span style={{ color: theme.colors.textSubtle, fontSize: 11, fontFamily: theme.fonts.mono }}>连接数</span>
                <span
                  style={{
                    color: theme.colors.cta,
                    fontSize: 11,
                    fontFamily: theme.fonts.mono,
                  }}
                >
                  {getNodeConnections(selectedNode).length}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );

  if (embedded) {
    return (
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
          background: "transparent",
          fontFamily: theme.fonts.sans,
        }}
      >
        <style>{`
          @keyframes fadeIn { from{opacity:0;transform:translateY(-8px)} to{opacity:1;transform:translateY(0)} }
        `}</style>
        {/* Embedded toolbar: search + stats */}
        <div
          style={{
            padding: "12px 24px",
            borderBottom: `1px solid ${theme.colors.border}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            background: theme.colors.surface,
            flexShrink: 0,
            boxShadow: `0 0 16px ${theme.colors.glow}08`,
          }}
        >
          <div style={{ position: "relative", width: 240 }}>
            <svg style={{ position: "absolute", left: 10, top: "50%", transform: "translateY(-50%)", pointerEvents: "none" }} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke={theme.colors.textSubtle} strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="搜索节点…"
              style={{
                width: "100%",
                background: theme.colors.backgroundMuted,
                border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.md,
                padding: "7px 12px 7px 32px",
                color: theme.colors.primary,
                fontSize: 13,
                fontFamily: theme.fonts.mono,
                outline: "none",
                transition: "border-color .2s, box-shadow .2s",
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
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery("")}
                style={{
                  position: "absolute",
                  right: 8,
                  top: "50%",
                  transform: "translateY(-50%)",
                  background: "none",
                  border: "none",
                  color: theme.colors.textSubtle,
                  cursor: "pointer",
                  fontSize: 16,
                  lineHeight: 1,
                }}
                aria-label="清除搜索"
              >
                ×
              </button>
            )}
          </div>
          <div style={{ display: "flex", gap: 20 }}>
            {[
              ["节点", stats.nodes, "#22D3EE"],
              ["关系", stats.edges, "#A78BFA"],
              ["类型", stats.types, "#34D399"],
            ].map(([k, v, c]) => (
              <div key={k} style={{ textAlign: "center" }}>
                <div style={{ color: c, fontSize: 18, fontWeight: 600, fontFamily: theme.fonts.mono, textShadow: `0 0 12px ${c}60` }}>{v}</div>
                <div style={{ color: theme.colors.textSubtle, fontSize: 10, letterSpacing: "0.1em", fontFamily: theme.fonts.mono }}>{k}</div>
              </div>
            ))}
          </div>
        </div>
        {graphContent}
      </div>
    );
  }

  return (
    <div
      style={{
        width: "100%",
        height: "100vh",
        background: "#ffffff",
        fontFamily: "'Noto Sans SC', sans-serif",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}
    >
      <style>{`
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        input::placeholder { color: #94a3b8; }
        @keyframes pulse-ring { 0%,100%{opacity:.3;transform:scale(1)} 50%{opacity:.6;transform:scale(1.05)} }
        @keyframes fadeIn { from{opacity:0;transform:translateY(-8px)} to{opacity:1;transform:translateY(0)} }
      `}</style>
      <div
        style={{
          padding: "16px 24px",
          borderBottom: "1px solid #e2e8f0",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: "#ffffff",
          flexShrink: 0,
          zIndex: 10,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 32, height: 32, borderRadius: 8, background: "linear-gradient(135deg,#6ee7f730,#a78bfa30)", border: "1px solid #e2e8f0", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <circle cx="4" cy="4" r="2.5" stroke="#6ee7f7" strokeWidth="1.2" />
              <circle cx="12" cy="4" r="2.5" stroke="#a78bfa" strokeWidth="1.2" />
              <circle cx="8" cy="12" r="2.5" stroke="#34d399" strokeWidth="1.2" />
              <line x1="6" y1="4" x2="10" y2="4" stroke="#475569" strokeWidth="1" />
              <line x1="5" y1="5.5" x2="7" y2="10.5" stroke="#475569" strokeWidth="1" />
              <line x1="11" y1="5.5" x2="9" y2="10.5" stroke="#475569" strokeWidth="1" />
            </svg>
          </div>
          <div>
            <div style={{ color: "#0f172a", fontSize: 14, fontWeight: 600, letterSpacing: "0.02em" }}>知识图谱</div>
            <div style={{ color: "#64748b", fontSize: 11, fontFamily: "'JetBrains Mono', monospace" }}>Knowledge Graph</div>
          </div>
        </div>
        <div style={{ position: "relative", width: 240 }}>
          <svg style={{ position: "absolute", left: 10, top: "50%", transform: "translateY(-50%)" }} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#475569" strokeWidth="2"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" /></svg>
          <input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="搜索节点…"
            style={{ width: "100%", background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 8, padding: "7px 12px 7px 32px", color: "#334155", fontSize: 13, outline: "none", transition: "border-color .2s" }}
            onFocus={(e) => (e.target.style.borderColor = "#6ee7f7")}
            onBlur={(e) => (e.target.style.borderColor = "#e2e8f0")}
          />
          {searchQuery && (
            <button type="button" onClick={() => setSearchQuery("")} style={{ position: "absolute", right: 8, top: "50%", transform: "translateY(-50%)", background: "none", border: "none", color: "#64748b", cursor: "pointer", fontSize: 16, lineHeight: 1 }} aria-label="清除搜索">×</button>
          )}
        </div>
        <div style={{ display: "flex", gap: 20 }}>
          {[["节点", stats.nodes, "#6ee7f7"], ["关系", stats.edges, "#a78bfa"], ["类型", stats.types, "#34d399"]].map(([k, v, c]) => (
            <div key={k} style={{ textAlign: "center" }}>
              <div style={{ color: c, fontSize: 18, fontWeight: 600, fontFamily: "'JetBrains Mono', monospace" }}>{v}</div>
              <div style={{ color: "#64748b", fontSize: 10, letterSpacing: "0.1em" }}>{k}</div>
            </div>
          ))}
        </div>
      </div>
      {graphContent}
    </div>
  );
}
