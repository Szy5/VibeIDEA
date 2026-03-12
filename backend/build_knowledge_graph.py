import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT_DIR / "results"
GRAPH_DIR = ROOT_DIR / "public" / "graph"
GLOBAL_GRAPH_PATH = GRAPH_DIR / "papers_kg.json"
INDEX_PATH = GRAPH_DIR / "papers_kg_index.json"
FAISS_INDEX_PATH = GRAPH_DIR / "papers_kg_faiss.index"
FAISS_IDS_PATH = GRAPH_DIR / "papers_kg_faiss_ids.json"

# 代理：程序入口尽早加载 .env，使 HTTP_PROXY/HTTPS_PROXY 在下载模型前生效（与 main.py 一致）
def _apply_proxy_from_env() -> None:
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT_DIR / ".env", override=True)
    except Exception:
        pass


# --------- 数据模型 ---------

@dataclass
class Node:
    id: str
    title: str
    year: Optional[int] = None
    authors: Optional[List[str]] = None
    arxiv_id: Optional[str] = None
    source: str = "prior_work"  # "main" or "prior_work"
    patterns: List[str] = field(default_factory=list)
    narratives: List[str] = field(default_factory=list)
    degree_in: int = 0
    degree_out: int = 0


@dataclass
class Edge:
    source: str
    target: str
    role: str
    relation_type: str
    description: str
    weight: Optional[float] = None
    year_diff: Optional[int] = None


ROLE_TO_RELATION: Dict[str, str] = {
    "Baseline": "IMPROVES_OVER",
    "Foundation": "BUILDS_ON",
    "Gap Identification": "IDENTIFIES_GAP_OF",
    "Inspiration": "INSPIRED_BY",
}


def normalize_arxiv_id(raw: Optional[str]) -> Optional[str]:
    """统一为 XXXX.XXXXX 形式，去掉版本后缀（如 v1、v2）。"""
    if not raw or not str(raw).strip():
        return None
    s = str(raw).strip()
    # 去掉末尾 v数字
    s = re.sub(r"v\d+$", "", s, flags=re.IGNORECASE).strip()
    # 只保留符合 数字.数字 的部分（如 2512.17912）
    m = re.match(r"^(\d{4}\.\d{4,5})", s)
    if m:
        return m.group(1)
    if re.match(r"^\d+\.\d+$", s):
        return s
    return s or None


def normalize_title_for_match(title: str) -> str:
    """用于匹配的标题：去首尾空白、中间空白规整为单空格、转小写（匹配时不区分大小写）。"""
    if not title:
        return ""
    return " ".join(str(title).strip().split()).lower()


def canonical_paper_id(title: str, year: Optional[int], arxiv_id: Optional[str]) -> str:
    """根据规范化后的 arxiv_id 或 (title, year) 生成稳定 ID；调用方应传入已 normalize 的 arxiv_id。"""
    aid = normalize_arxiv_id(arxiv_id)
    if aid:
        return aid
    base = f"{normalize_title_for_match(title)}-{year or ''}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]


def normalize_authors(authors: Optional[str]) -> Optional[List[str]]:
    if not authors:
        return None
    # 简单按逗号拆分
    parts = [a.strip() for a in str(authors).split(",") if a.strip()]
    return parts or None


def role_to_relation_type(role: str) -> str:
    return ROLE_TO_RELATION.get(role, "OTHER")


def estimate_weight(role: str) -> float:
    """根据 role 简单估一个权重, 后续需要可以再精细化。"""
    if role == "Baseline":
        return 1.0
    if role == "Foundation":
        return 0.8
    if role == "Gap Identification":
        return 0.9
    if role == "Inspiration":
        return 0.6
    return 0.5


# --------- FAISS 标题相似度（可选）---------

class FaissContext:
    """FAISS + allenai-specter 标题相似度检索与入库；GPU 优先，代理从环境变量读取。"""
    def __init__(self, threshold: float = 0.98, use_gpu: bool = True):
        self.threshold = threshold
        self._encoder = None
        self._index: Any = None
        self._faiss_ids: List[str] = []
        self._use_gpu = use_gpu
        self._dim: Optional[int] = None

    def _get_encoder(self):
        if self._encoder is not None:
            return self._encoder
        _apply_proxy_from_env()
        try:
            from sentence_transformers import SentenceTransformer
            device = "cuda" if self._use_gpu else "cpu"
            try:
                import torch
                if self._use_gpu and not torch.cuda.is_available():
                    device = "cpu"
                    print("[FAISS] CUDA 不可用，使用 CPU 编码")
            except Exception:
                device = "cpu"
            self._encoder = SentenceTransformer("allenai-specter", device=device)
            print(f"[FAISS] 已加载 allenai-specter，device={device}")
        except Exception as e:
            print(f"[WARN] FAISS 编码器加载失败，将跳过标题相似度融合: {e}")
        return self._encoder

    def _get_index(self):
        if self._index is not None:
            return self._index
        try:
            import faiss
            self._dim = 768  # allenai-specter
            self._index = faiss.IndexFlatIP(self._dim)
        except Exception as e:
            print(f"[WARN] FAISS 不可用，将跳过标题相似度融合: {e}")
        return self._index

    def search(self, title: str) -> Optional[Tuple[str, float]]:
        """检索与 title 最相似的已入图节点，返回 (node_id, score) 或 None。score 为余弦相似度。"""
        if not title or not title.strip():
            return None
        enc = self._get_encoder()
        idx = self._get_index()
        if enc is None or idx is None or idx.ntotal == 0:
            return None
        vec = enc.encode([title.strip()], normalize_embeddings=True)
        vec = np.asarray(vec, dtype=np.float32)
        scores, indices = idx.search(vec, 1)
        if indices[0][0] < 0:
            return None
        score = float(scores[0][0])
        if score < self.threshold:
            return None
        node_id = self._faiss_ids[indices[0][0]]
        return (node_id, score)

    def add(self, node_id: str, title: str) -> None:
        """将节点标题向量加入 FAISS。"""
        if not title or not title.strip():
            return
        enc = self._get_encoder()
        idx = self._get_index()
        if enc is None or idx is None:
            return
        vec = enc.encode([title.strip()], normalize_embeddings=True)
        vec = np.asarray(vec, dtype=np.float32)
        idx.add(vec)
        self._faiss_ids.append(node_id)

    def save(self, index_path: Path, ids_path: Path) -> None:
        if self._index is None or self._index.ntotal == 0:
            return
        try:
            import faiss
            GRAPH_DIR.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self._index, str(index_path))
            ids_path.write_text(json.dumps(self._faiss_ids, ensure_ascii=False), encoding="utf-8")
            print(f"[FAISS] 已保存索引 ntotal={self._index.ntotal} -> {index_path.name}")
        except Exception as e:
            print(f"[WARN] FAISS 保存失败: {e}")

    @classmethod
    def load(cls, index_path: Path, ids_path: Path, threshold: float = 0.88, use_gpu: bool = True) -> Optional["FaissContext"]:
        if not index_path.exists() or not ids_path.exists():
            return cls(threshold=threshold, use_gpu=use_gpu)
        try:
            import faiss
            ctx = cls(threshold=threshold, use_gpu=use_gpu)
            ctx._index = faiss.read_index(str(index_path))
            ctx._faiss_ids = json.loads(ids_path.read_text(encoding="utf-8"))
            if len(ctx._faiss_ids) != ctx._index.ntotal:
                print("[WARN] FAISS ids 与 index 条数不一致，将重建 FAISS")
                return cls(threshold=threshold, use_gpu=use_gpu)
            ctx._dim = ctx._index.d
            print(f"[FAISS] 已加载索引 ntotal={ctx._index.ntotal}")
            return ctx
        except Exception as e:
            print(f"[WARN] FAISS 加载失败，将新建: {e}")
            return cls(threshold=threshold, use_gpu=use_gpu)


def load_existing_graph() -> Tuple[Dict[str, Node], List[Edge]]:
    if not GLOBAL_GRAPH_PATH.exists():
        return {}, []
    data = json.loads(GLOBAL_GRAPH_PATH.read_text(encoding="utf-8"))
    nodes: Dict[str, Node] = {}
    for n in data.get("nodes", []):
        nodes[n["id"]] = Node(
            id=n["id"],
            title=n.get("title", ""),
            year=n.get("year"),
            authors=n.get("authors"),
            arxiv_id=n.get("arxiv_id"),
            source=n.get("source", "prior_work"),
            patterns=n.get("patterns", []) or [],
            narratives=n.get("narratives", []) or [],
            degree_in=n.get("degree_in", 0),
            degree_out=n.get("degree_out", 0),
        )
    edges: List[Edge] = []
    for e in data.get("edges", []):
        edges.append(
            Edge(
                source=e["source"],
                target=e["target"],
                role=e.get("role", ""),
                relation_type=e.get("relation_type", "OTHER"),
                description=e.get("description", ""),
                weight=e.get("weight"),
                year_diff=e.get("year_diff"),
            )
        )
    return nodes, edges


def load_index() -> Dict:
    if not INDEX_PATH.exists():
        return {"version": 1, "last_updated": None, "papers": {}}
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def save_graph(nodes: Dict[str, Node], edges: List[Edge]) -> None:
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "nodes": [asdict(n) for n in nodes.values()],
        "edges": [asdict(e) for e in edges],
    }
    GLOBAL_GRAPH_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def save_index(index: Dict) -> None:
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    index["last_updated"] = datetime.now(timezone.utc).isoformat()
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_analysis_file(path: Path) -> Optional[Dict]:
    try:
        text = path.read_text(encoding="utf-8")
        return json.loads(text)
    except Exception as e:
        # 日志使用 print, 避免依赖 loguru
        print(f"[WARN] Failed to parse {path.name}: {e}")
        return None


def _resolve_or_create_node(
    nodes: Dict[str, Node],
    by_title: Dict[str, str],
    by_arxiv: Dict[str, str],
    title: str,
    year: Optional[int],
    arxiv_id: Optional[str],
    *,
    source: str,
    patterns: Optional[List[str]] = None,
    narratives: Optional[List[str]] = None,
    authors: Optional[List[str]] = None,
    faiss_ctx: Optional[FaissContext] = None,
) -> str:
    """按 arxiv_id、标题完全一致、FAISS 相似度 三步做实体融合，返回图中节点 id。"""
    norm_title = normalize_title_for_match(title or "")
    norm_arxiv = normalize_arxiv_id(arxiv_id)

    # 1) 标题完全一致（小写）
    candidate_id: Optional[str] = None
    match_kind: Optional[str] = None
    if norm_title and norm_title in by_title:
        candidate_id = by_title[norm_title]
        match_kind = "title"
    # 2) arxiv 兜底
    if not candidate_id and norm_arxiv and norm_arxiv in by_arxiv:
        candidate_id = by_arxiv[norm_arxiv]
        match_kind = "arxiv"
    # 3) FAISS 标题相似度（仅前两步未命中时）
    match_score: Optional[float] = None
    if not candidate_id and faiss_ctx is not None:
        hit = faiss_ctx.search(title or "")
        if hit is not None:
            candidate_id, match_score = hit
            match_kind = "faiss"

    if candidate_id and candidate_id in nodes:
        node = nodes[candidate_id]
        if source == "main":
            node.source = "main"
        if not node.title and title:
            node.title = title.strip()
        if node.year is None and year is not None:
            node.year = year
        if not node.arxiv_id and norm_arxiv:
            node.arxiv_id = norm_arxiv
        if authors and not node.authors:
            node.authors = authors
        if patterns:
            for p in patterns:
                if p not in node.patterns:
                    node.patterns.append(p)
        if narratives:
            for na in narratives:
                if na not in node.narratives:
                    node.narratives.append(na)
        if norm_title:
            by_title[norm_title] = candidate_id
        if norm_arxiv:
            by_arxiv[norm_arxiv] = candidate_id
        # 融合日志：便于判断融合来源与调参
        if match_kind:
            incoming_short = (title or "").strip()[:80]
            existing_short = (node.title or "").strip()[:80]
            if match_kind == "faiss" and match_score is not None:
                print(f"[FUSION] faiss score={match_score:.4f}: \"{incoming_short}\" -> node_id={candidate_id} (existing: \"{existing_short}\")")
            else:
                print(f"[FUSION] {match_kind}: \"{incoming_short}\" -> node_id={candidate_id} (existing: \"{existing_short}\")")
        return candidate_id

    # 新节点：id 优先用规范化后的 arxiv，否则用 title+year 的 hash
    new_id = norm_arxiv or canonical_paper_id(title or "unknown", year, None)
    # 若与已有 id 冲突（例如同一 arxiv 之前用 hash 建过），则复用该节点并补全 arxiv
    if new_id in nodes:
        node = nodes[new_id]
        if not node.arxiv_id and norm_arxiv:
            node.arxiv_id = norm_arxiv
        if norm_arxiv:
            by_arxiv[norm_arxiv] = new_id
        if norm_title:
            by_title[norm_title] = new_id
        print(f"[FUSION] id_collision: arxiv={norm_arxiv} 与已有节点 id={new_id} 合并 (title: \"{(node.title or '')[:60]}\")")
        return new_id

    node = Node(
        id=new_id,
        title=(title or norm_arxiv or new_id).strip(),
        year=year,
        authors=authors,
        arxiv_id=norm_arxiv,
        source=source,
        patterns=patterns or [],
        narratives=narratives or [],
    )
    nodes[new_id] = node
    if norm_title:
        by_title[norm_title] = new_id
    if norm_arxiv:
        by_arxiv[norm_arxiv] = new_id
    if faiss_ctx is not None:
        faiss_ctx.add(new_id, node.title)
    return new_id


def build_from_files(
    files: List[Path],
    existing_nodes: Optional[Dict[str, Node]] = None,
    existing_edges: Optional[List[Edge]] = None,
    index: Optional[Dict] = None,
    full_rebuild: bool = False,
    use_faiss: bool = True,
    faiss_threshold: float = 0.88,
    use_gpu: bool = True,
) -> Tuple[Dict[str, Node], List[Edge], Dict]:
    nodes: Dict[str, Node] = dict(existing_nodes) if existing_nodes else {}
    edges: List[Edge] = list(existing_edges) if existing_edges else []

    # 实体融合索引：标题 / 规范化 arxiv_id -> 节点 id
    by_title: Dict[str, str] = {}
    by_arxiv: Dict[str, str] = {}
    for n in nodes.values():
        t = normalize_title_for_match(n.title or "")
        if t:
            by_title[t] = n.id
        if n.arxiv_id:
            aid = normalize_arxiv_id(n.arxiv_id)
            if aid:
                by_arxiv[aid] = n.id

    # FAISS：全量重建时新建，增量时加载已有（若存在）
    faiss_ctx: Optional[FaissContext] = None
    if use_faiss:
        if full_rebuild:
            faiss_ctx = FaissContext(threshold=faiss_threshold, use_gpu=use_gpu)
        else:
            faiss_ctx = FaissContext.load(
                FAISS_INDEX_PATH, FAISS_IDS_PATH,
                threshold=faiss_threshold, use_gpu=use_gpu,
            )

    edge_keys = {(e.source, e.target, e.role) for e in edges}

    if index is None:
        index = {"version": 1, "last_updated": None, "papers": {}}

    for path in files:
        data = parse_analysis_file(path)
        if not data:
            continue

        main_title = data.get("paper_title") or ""
        main_arxiv_id_raw = data.get("paper_arxiv_id") or ""
        main_abstract = data.get("paper_abstract") or ""
        prior_works = data.get("prior_works") or []
        synthesis_narrative = data.get("synthesis_narrative") or ""
        innovation = data.get("innovation_classification") or {}
        analysis_ts = data.get("analysis_timestamp")

        patterns: List[str] = []
        primary_name = innovation.get("primary_pattern_name")
        if primary_name:
            patterns.append(primary_name)
        for sec in innovation.get("secondary_pattern_names") or []:
            if sec and sec not in patterns:
                patterns.append(sec)

        # 主论文节点（融合：同标题 / 同 arxiv / FAISS 相似度）
        main_id = _resolve_or_create_node(
            nodes,
            by_title,
            by_arxiv,
            title=main_title or path.stem,
            year=None,
            arxiv_id=main_arxiv_id_raw,
            source="main",
            patterns=patterns,
            narratives=[synthesis_narrative] if synthesis_narrative else None,
            faiss_ctx=faiss_ctx,
        )

        # 若是增量重跑某篇主论文，清理其旧出边
        if not full_rebuild:
            edges = [e for e in edges if e.source != main_id]
            edge_keys = {(e.source, e.target, e.role) for e in edges}

        index.setdefault("papers", {})
        index["papers"][main_id] = {
            "file": path.name,
            "analysis_timestamp": analysis_ts,
            "title": main_title,
        }

        main_node = nodes[main_id]
        if synthesis_narrative and synthesis_narrative not in main_node.narratives:
            main_node.narratives.append(synthesis_narrative)

        # 前人工作节点与边
        for pw in prior_works:
            pw_title = pw.get("title") or ""
            pw_year = pw.get("year")
            pw_role = pw.get("role") or ""
            pw_sentence = pw.get("relationship_sentence") or ""
            pw_arxiv_raw = pw.get("arxiv_id") or None
            pw_authors_raw = pw.get("authors")

            prior_id = _resolve_or_create_node(
                nodes,
                by_title,
                by_arxiv,
                title=pw_title or "unknown",
                year=pw_year,
                arxiv_id=pw_arxiv_raw,
                source="prior_work",
                authors=normalize_authors(pw_authors_raw),
                faiss_ctx=faiss_ctx,
            )

            prior_node = nodes[prior_id]
            key = (main_id, prior_id, pw_role)
            if key in edge_keys:
                continue

            relation = role_to_relation_type(pw_role)
            year_diff: Optional[int] = None
            if main_node.year is not None and prior_node.year is not None:
                year_diff = main_node.year - prior_node.year

            edge = Edge(
                source=main_id,
                target=prior_id,
                role=pw_role,
                relation_type=relation,
                description=pw_sentence,
                weight=estimate_weight(pw_role),
                year_diff=year_diff,
            )
            edges.append(edge)
            edge_keys.add(key)

    # 重新计算度数
    for n in nodes.values():
        n.degree_in = 0
        n.degree_out = 0
    for e in edges:
        if e.source in nodes:
            nodes[e.source].degree_out += 1
        if e.target in nodes:
            nodes[e.target].degree_in += 1

    # 保存 FAISS 索引（由 main 里统一写文件，这里只保证 faiss_ctx 已更新）
    if faiss_ctx is not None:
        faiss_ctx.save(FAISS_INDEX_PATH, FAISS_IDS_PATH)

    return nodes, edges, index


def collect_all_result_files() -> List[Path]:
    if not RESULTS_DIR.exists():
        return []
    return sorted(RESULTS_DIR.glob("prior_work_analysis_*.json"))


def select_incremental_files(index: Dict) -> List[Path]:
    """根据 index 选择需要增量处理的 JSON 文件。"""
    files: List[Path] = []
    known = index.get("papers", {})
    for path in collect_all_result_files():
        data = parse_analysis_file(path)
        if not data:
            continue
        main_arxiv_id = data.get("paper_arxiv_id") or ""
        main_title = data.get("paper_title") or path.stem
        main_id = canonical_paper_id(
            title=main_title or main_arxiv_id or path.stem,
            year=None,
            arxiv_id=main_arxiv_id or None,
        )
        ts = data.get("analysis_timestamp")
        record = known.get(main_id)
        if record is None:
            files.append(path)
            continue
        old_ts = record.get("analysis_timestamp")
        if ts and old_ts and ts > old_ts:
            files.append(path)
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or update papers knowledge graph from prior_work_analysis JSON.")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full rebuild from all prior_work_analysis_*.json files (ignore existing graph/index).",
    )
    parser.add_argument(
        "--no-faiss",
        action="store_true",
        help="Disable FAISS title-similarity fusion (only arxiv + exact title match).",
    )
    parser.add_argument(
        "--faiss-threshold",
        type=float,
        default=0.88,
        metavar="T",
        help="FAISS cosine similarity threshold for merging (default: 0.88).",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Use CPU for title encoder (default: GPU if available).",
    )
    args = parser.parse_args()

    # 尽早加载 .env 中的代理（HTTP_PROXY/HTTPS_PROXY），避免下载 allenai-specter 时失败
    _apply_proxy_from_env()

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    use_faiss = not args.no_faiss
    use_gpu = not args.cpu

    if args.full or not GLOBAL_GRAPH_PATH.exists():
        # 全量重建
        print("[KG] Running full rebuild...")
        files = collect_all_result_files()
        nodes, edges, index = build_from_files(
            files,
            existing_nodes=None,
            existing_edges=None,
            index=None,
            full_rebuild=True,
            use_faiss=use_faiss,
            faiss_threshold=args.faiss_threshold,
            use_gpu=use_gpu,
        )
        save_graph(nodes, edges)
        save_index(index)
        print(f"[KG] Done. Nodes={len(nodes)}, Edges={len(edges)}")
        return

    # 增量更新
    print("[KG] Running incremental update...")
    existing_nodes, existing_edges = load_existing_graph()
    index = load_index()
    files = select_incremental_files(index)
    if not files:
        print("[KG] No new or updated analysis files. Nothing to do.")
        return

    nodes, edges, index = build_from_files(
        files,
        existing_nodes=existing_nodes,
        existing_edges=existing_edges,
        index=index,
        full_rebuild=False,
        use_faiss=use_faiss,
        faiss_threshold=args.faiss_threshold,
        use_gpu=use_gpu,
    )
    save_graph(nodes, edges)
    save_index(index)
    print(f"[KG] Incremental update done. Nodes={len(nodes)}, Edges={len(edges)}, UpdatedFiles={len(files)}")


if __name__ == "__main__":
    main()

