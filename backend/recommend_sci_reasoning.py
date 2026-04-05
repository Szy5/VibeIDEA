"""
从 Sci-Reasoning 或本地会议数据集中推荐与 Zotero 兴趣相关的论文。

默认保留原有 Sci-Reasoning 工作流；额外支持读取本地爬取的 acl / aaai / emnlp
数据文件（json/jsonl/csv/parquet），按 Zotero 已读论文兴趣进行重排序。
"""

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from tempfile import mkstemp
from typing import Any

import numpy as np
from datasets import load_dataset
from gitignore_parser import parse_gitignore
from loguru import logger
from pyzotero import zotero
from sentence_transformers import SentenceTransformer


VENUE_ALIASES = {
    "acl": {"acl", "annual meeting of the association for computational linguistics"},
    "aaai": {"aaai", "aaai conference on artificial intelligence"},
    "emnlp": {
        "emnlp",
        "conference on empirical methods in natural language processing",
    },
}
TEXT_KEYS = (
    "title",
    "paper_title",
    "name",
)
ABSTRACT_KEYS = (
    "abstract",
    "summary",
    "description",
    "paper_abstract",
)
AUTHOR_KEYS = (
    "authors",
    "author",
    "author_names",
)
VENUE_KEYS = (
    "venue",
    "conference",
    "booktitle",
    "source",
)
YEAR_KEYS = (
    "year",
    "publication_year",
)
LINK_KEYS = (
    "url",
    "link",
    "pdf_url",
    "paper_url",
)


def get_zotero_corpus(id: str, key: str) -> list[dict]:
    """从 Zotero 拉取文献库（与 main.py 一致）。"""
    zot = zotero.Zotero(id, "user", key)
    collections = zot.everything(zot.collections())
    collections = {c["key"]: c for c in collections}
    corpus = zot.everything(zot.items(itemType="conferencePaper || journalArticle || preprint"))
    corpus = [c for c in corpus if c["data"]["abstractNote"] != ""]

    def get_collection_path(col_key: str) -> str:
        if p := collections[col_key]["data"]["parentCollection"]:
            return get_collection_path(p) + "/" + collections[col_key]["data"]["name"]
        return collections[col_key]["data"]["name"]

    for c in corpus:
        c["paths"] = [get_collection_path(col) for col in c["data"]["collections"]]
    return corpus


def filter_corpus(corpus: list[dict], pattern: str) -> list[dict]:
    """按 gitignore 风格排除指定 collection（与 main.py 一致）。"""
    _, filename = mkstemp()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(pattern)
    matcher = parse_gitignore(filename, base_dir="./")
    new_corpus = [c for c in corpus if not any(matcher(p) for p in c["paths"])]
    os.remove(filename)
    return new_corpus


@dataclass
class DatasetPaper:
    title: str
    summary: str
    score: float | None = None
    abstract: str | None = None
    authors: str | None = None
    venue: str | None = None
    year: int | None = None
    source: str | None = None
    url: str | None = None


def _pick_first(row: dict[str, Any], candidates: tuple[str, ...]) -> Any:
    for key in candidates:
        value = row.get(key)
        if value not in (None, ""):
            return value
    return None


def _normalize_authors(value: Any) -> str | None:
    if value in (None, ""):
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        names = []
        for item in value:
            if isinstance(item, str):
                names.append(item)
            elif isinstance(item, dict):
                name = item.get("name") or item.get("full_name")
                if name:
                    names.append(name)
        return ", ".join(names) if names else None
    return str(value)


def _normalize_year(value: Any) -> int | None:
    if value in (None, ""):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = str(value)
    for token in text.replace("/", "-").split("-"):
        if len(token) == 4 and token.isdigit():
            return int(token)
    if text.isdigit() and len(text) == 4:
        return int(text)
    return None


def _normalize_text(value: Any) -> str | None:
    if value in (None, ""):
        return None
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalize_venue_name(value: str | None) -> str:
    return (value or "").strip().lower()


def _matches_requested_venues(row: dict[str, Any], path: str, venues: set[str] | None) -> bool:
    if not venues:
        return True
    row_venue = _normalize_venue_name(_normalize_text(_pick_first(row, VENUE_KEYS)))
    basename = os.path.basename(path).lower()
    dirname = os.path.dirname(path).lower()
    haystacks = [row_venue, basename, dirname]
    for venue in venues:
        aliases = VENUE_ALIASES.get(venue, {venue})
        for alias in aliases:
            if any(alias in haystack for haystack in haystacks):
                return True
    return False


def _row_to_paper(row: dict[str, Any], source: str) -> DatasetPaper | None:
    title = _normalize_text(_pick_first(row, TEXT_KEYS))
    abstract = _normalize_text(_pick_first(row, ABSTRACT_KEYS))
    summary = abstract or title
    if not summary:
        return None
    venue = _normalize_text(_pick_first(row, VENUE_KEYS))
    return DatasetPaper(
        title=title or "",
        summary=summary,
        abstract=abstract,
        authors=_normalize_authors(_pick_first(row, AUTHOR_KEYS)),
        venue=venue,
        year=_normalize_year(_pick_first(row, YEAR_KEYS)),
        source=source,
        url=_normalize_text(_pick_first(row, LINK_KEYS)),
    )


def _iter_local_rows(path: str) -> tuple[list[dict[str, Any]], str]:
    extension = os.path.splitext(path)[1].lower()
    if extension == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data, "json"
        if isinstance(data, dict):
            for key in ("papers", "data", "items", "results"):
                value = data.get(key)
                if isinstance(value, list):
                    return value, f"json:{key}"
        raise ValueError(f"{path} 不是可识别的论文列表 JSON")

    if extension in {".jsonl", ".ndjson"}:
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows, "jsonl"

    if extension in {".csv", ".parquet"}:
        ds = load_dataset(extension.removeprefix("."), data_files=path, split="train")
        return [dict(row) for row in ds], extension.removeprefix(".")

    raise ValueError(f"暂不支持的数据格式: {path}")


def load_sci_reasoning_papers(
    include_2025: bool = True,
    include_2023_2024: bool = True,
    venues: set[str] | None = None,
) -> list[DatasetPaper]:
    """加载 Sci-Reasoning 数据集，返回带 title/summary 的论文列表。"""
    papers: list[DatasetPaper] = []
    files_to_load: list[tuple[str, str]] = []
    if include_2025:
        files_to_load.append(("2025/all_papers_2025.csv", "Sci-Reasoning:2025"))
    if include_2023_2024:
        files_to_load.append(("2023-2024/all_papers.csv", "Sci-Reasoning:2023-2024"))

    for data_file, source in files_to_load:
        ds = load_dataset("AmberLJC/Sci-Reasoning", data_files=data_file, split="train")
        logger.info(f"{source} 论文数量: {len(ds)}")
        for row in ds:
            row = dict(row)
            if not _matches_requested_venues(row, data_file, venues):
                continue
            paper = _row_to_paper(row, source=source)
            if paper is not None:
                papers.append(paper)
    return papers


def load_local_conference_papers(
    dataset_paths: list[str],
    venues: set[str] | None = None,
) -> list[DatasetPaper]:
    papers: list[DatasetPaper] = []
    for path in dataset_paths:
        rows, fmt = _iter_local_rows(path)
        logger.info(f"加载本地数据 {path} ({fmt})，共 {len(rows)} 条")
        accepted = 0
        for row in rows:
            if not isinstance(row, dict):
                continue
            if not _matches_requested_venues(row, path, venues):
                continue
            paper = _row_to_paper(row, source=path)
            if paper is None:
                continue
            papers.append(paper)
            accepted += 1
        logger.info(f"{path} 过滤后保留 {accepted} 篇")
    return papers


def deduplicate_papers(papers: list[DatasetPaper]) -> list[DatasetPaper]:
    seen: set[str] = set()
    unique_papers: list[DatasetPaper] = []
    for paper in papers:
        key = " ".join((paper.title or paper.summary).lower().split())
        if key in seen:
            continue
        seen.add(key)
        unique_papers.append(paper)
    return unique_papers


def _get_device(device_spec: str | None) -> str:
    """
    解析设备：优先使用用户指定，否则自动选择。
    device_spec: "auto" | "cpu" | "cuda" | "cuda:0" | "cuda:1" ...
    """
    if device_spec and device_spec != "auto":
        if device_spec.startswith("cuda"):
            try:
                import torch

                if not torch.cuda.is_available():
                    logger.warning("指定了 GPU 但 CUDA 不可用，回退到 CPU")
                    return "cpu"
                if ":" in device_spec:
                    idx = int(device_spec.split(":")[1])
                    if idx < torch.cuda.device_count():
                        return device_spec
                    logger.warning(
                        f"GPU {idx} 不存在（共 {torch.cuda.device_count()} 张），使用 cuda:0"
                    )
                    return "cuda:0"
                return device_spec
            except Exception as e:
                logger.warning(f"解析设备 {device_spec} 失败: {e}，回退到自动选择")
        elif device_spec == "cpu":
            return "cpu"
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


def rerank_by_zotero_corpus(
    candidate: list[DatasetPaper],
    corpus: list[dict],
    model: str = "avsolatorio/GIST-small-Embedding-v0",
    device_spec: str | None = None,
) -> list[DatasetPaper]:
    """用 Zotero corpus 对候选论文打分并降序排序（逻辑与 recommender.rerank_paper 一致）。"""
    device = _get_device(device_spec)
    logger.info(f"编码设备: {device}（{'GPU' if device.startswith('cuda') else 'CPU'}）")
    encoder = SentenceTransformer(model, device=device)
    corpus = sorted(
        corpus,
        key=lambda x: datetime.strptime(x["data"]["dateAdded"], "%Y-%m-%dT%H:%M:%SZ"),
        reverse=True,
    )
    time_decay_weight = 1 / (1 + np.log10(np.arange(len(corpus)) + 1))
    time_decay_weight = time_decay_weight / time_decay_weight.sum()

    corpus_texts = [p["data"]["abstractNote"] for p in corpus]
    logger.info(f"编码 Zotero corpus（{len(corpus_texts)} 篇）...")
    corpus_feature = encoder.encode(corpus_texts, show_progress_bar=True, batch_size=32)

    candidate_texts = [p.summary for p in candidate]
    logger.info(f"编码候选论文（{len(candidate_texts)} 篇）...")
    candidate_feature = encoder.encode(
        candidate_texts,
        show_progress_bar=True,
        batch_size=32,
    )

    logger.info("计算相似度并排序...")
    sim = encoder.similarity(candidate_feature, corpus_feature)
    scores = (sim * time_decay_weight).sum(axis=1) * 10
    for p, s in zip(candidate, scores):
        p.score = float(s.item())
    return sorted(candidate, key=lambda x: x.score or 0.0, reverse=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从 Sci-Reasoning 或本地会议数据集中推荐与 Zotero 兴趣相关的论文"
    )
    parser.add_argument("--zotero_id", type=str, default=os.environ.get("ZOTERO_ID"))
    parser.add_argument("--zotero_key", type=str, default=os.environ.get("ZOTERO_KEY"))
    parser.add_argument(
        "--zotero_ignore",
        type=str,
        default=None,
        help="Zotero collection to ignore (gitignore-style pattern)",
    )
    parser.add_argument(
        "--dataset_source",
        type=str,
        choices=["sci-reasoning", "local"],
        default="local",
        help="候选论文来源：Sci-Reasoning 或本地爬取数据",
    )
    parser.add_argument(
        "--dataset_paths",
        type=str,
        nargs="*",
        default=[],
        help="本地数据文件路径，支持 json/jsonl/csv/parquet",
    )
    parser.add_argument(
        "--venues",
        type=str,
        nargs="*",
        default=["acl", "aaai", "emnlp"],
        help="只保留指定会议；默认筛选 acl/aaai/emnlp",
    )
    parser.add_argument(
        "--max_paper_num",
        type=int,
        default=50,
        help="输出的最大论文数，-1 表示不截断",
    )
    parser.add_argument(
        "--min_score",
        type=float,
        default=0.6,
        help="只输出 score >= 此阈值的论文",
    )
    parser.add_argument(
        "--embedding_model",
        type=str,
        default="avsolatorio/GIST-small-Embedding-v0",
        help="SentenceTransformer model for embeddings",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=os.environ.get("RECOMMEND_DEVICE", "auto"),
        help="编码设备: auto / cpu / cuda / cuda:0 ...",
    )
    parser.add_argument(
        "--year",
        type=str,
        choices=["2025", "2023-2024", "both"],
        default="both",
        help="dataset_source=sci-reasoning 时生效",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.json",
        help="输出文件路径（JSON）",
    )
    return parser.parse_args()


def build_candidates(args: argparse.Namespace) -> list[DatasetPaper]:
    venues = {v.lower() for v in args.venues} if args.venues else None
    if args.dataset_source == "sci-reasoning":
        include_2025 = args.year in ("2025", "both")
        include_2023_2024 = args.year in ("2023-2024", "both")
        logger.info("加载 Sci-Reasoning 数据集...")
        candidates = load_sci_reasoning_papers(
            include_2025=include_2025,
            include_2023_2024=include_2023_2024,
            venues=venues,
        )
    else:
        if not args.dataset_paths:
            logger.error("dataset_source=local 时必须提供 --dataset_paths")
            sys.exit(1)
        logger.info("加载本地会议数据集...")
        candidates = load_local_conference_papers(
            dataset_paths=args.dataset_paths,
            venues=venues,
        )

    unique_candidates = deduplicate_papers(candidates)
    logger.info(f"候选论文数: {len(candidates)}，去重后: {len(unique_candidates)}")
    return unique_candidates


def main() -> None:
    args = parse_args()
    if not args.zotero_id or not args.zotero_key:
        logger.error("请设置 --zotero_id / --zotero_key 或环境变量 ZOTERO_ID / ZOTERO_KEY")
        sys.exit(1)

    logger.info("检索 Zotero 文献库...")
    corpus = get_zotero_corpus(args.zotero_id, args.zotero_key)
    logger.info(f"Zotero 论文数: {len(corpus)}")
    if args.zotero_ignore:
        corpus = filter_corpus(corpus, args.zotero_ignore)
        logger.info(f"过滤后 corpus 数: {len(corpus)}")
    if len(corpus) == 0:
        logger.error("Zotero corpus 为空，无法计算相似度")
        sys.exit(1)

    candidates = build_candidates(args)
    if len(candidates) == 0:
        logger.error("候选论文为空，请检查数据路径、字段名或 venue 过滤条件")
        sys.exit(1)

    logger.info("按 Zotero 兴趣相似度重排序...")
    ranked = rerank_by_zotero_corpus(
        candidates,
        corpus,
        model=args.embedding_model,
        device_spec=args.device,
    )

    filtered = [p for p in ranked if p.score is not None and p.score >= args.min_score]
    if args.max_paper_num != -1:
        filtered = filtered[: args.max_paper_num]

    out_list = []
    for paper in filtered:
        item = asdict(paper)
        item["score"] = round(item["score"], 4) if item["score"] is not None else None
        if item["abstract"]:
            item["abstract"] = item["abstract"][:500]
        out_list.append(item)

    logger.info(f"得分 >= {args.min_score} 的论文数: {len(out_list)}")
    for i, item in enumerate(out_list, 1):
        print(f"\n[{i}] score={item['score']} | {item['title']}")
        if item.get("venue") or item.get("year"):
            print(f"    {item.get('venue', '')} {item.get('year', '')}")
        if item.get("source"):
            print(f"    source={item['source']}")
        if item.get("abstract"):
            print(f"    {item['abstract'][:200]}...")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out_list, f, ensure_ascii=False, indent=2)
        logger.success(f"已写入 {args.output}")


if __name__ == "__main__":
    main()
