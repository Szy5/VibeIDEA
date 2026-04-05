#!/usr/bin/env python3
"""
Enrich prior-work analysis JSON files with better paper titles and arXiv IDs.

Strategy:
- Target paper layer:
  - Match against the recommendation JSONL by normalized title
  - Prefer OpenAlex/Crossref/arXiv metadata to correct title and arXiv ID
- Prior-work layer:
  - If arxiv_id exists, canonicalize title from arXiv
  - Otherwise search OpenAlex first, then Crossref, rank by title/year/author match
  - Only auto-apply matches above confidence threshold

实体消歧
python -u backend/enrich_prior_work_analysis.py \
  --input_dir results/recommended_acl_aaai_top300_min7.65_prior_work \
  --recommendation_jsonl raw_paper/recommended_acl_aaai_top300_min7.65.jsonl \
  --write_inplace \
  2>&1 | tee results/recommended_acl_aaai_top300_min7.65_prior_work_enrich_inplace.run.log
"""

import argparse
import json
import re
import time
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import requests


USER_AGENT = "VibeIDEA/1.0 (metadata enrichment)"
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


@dataclass
class MatchResult:
    source: str
    title: str | None
    year: int | None
    authors: list[str]
    doi: str | None
    arxiv_id: str | None
    url: str | None
    score: float
    raw: dict[str, Any] | None = None


def normalize_title(title: str | None) -> str:
    text = (title or "").lower()
    text = re.sub(r"[\s\-_:,.;'\"`()\[\]{}]+", " ", text)
    text = re.sub(r"[^a-z0-9 ]+", "", text)
    return " ".join(text.split())


def sequence_score(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_title(a), normalize_title(b)).ratio()


def parse_year(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    text = str(value)
    m = re.search(r"(19|20)\d{2}", text)
    return int(m.group(0)) if m else None


def first_author_surname(authors: str | list[str] | None) -> str | None:
    if not authors:
        return None
    if isinstance(authors, str):
        first = authors.split(",")[0].strip()
    else:
        first = str(authors[0]).strip()
    if not first:
        return None
    tokens = [t for t in re.split(r"\s+", first) if t and t.lower() != "et" and t.lower() != "al."]
    return tokens[-1].lower() if tokens else None


def arxiv_id_from_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    m = re.search(r"10\.48550/arxiv\.(.+)$", doi, re.IGNORECASE)
    return m.group(1) if m else None


def arxiv_id_from_url(url: str | None) -> str | None:
    if not url:
        return None
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([^/?#]+)", url, re.IGNORECASE)
    if not m:
        return None
    return m.group(1).replace(".pdf", "")


def load_recommendation_index(path: str) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            index[normalize_title(obj.get("title"))] = obj
    return index


def request_json(url: str, timeout: int = 30) -> dict[str, Any]:
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    r.raise_for_status()
    return r.json()


def fetch_arxiv_metadata(arxiv_id: str) -> MatchResult | None:
    arxiv_id = arxiv_id.replace("https://arxiv.org/abs/", "").replace("https://www.arxiv.org/abs/", "").rstrip("/")
    url = f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(arxiv_id)}"
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    entry = root.find("atom:entry", ARXIV_NS)
    if entry is None:
        return None
    title = (entry.findtext("atom:title", default="", namespaces=ARXIV_NS) or "").replace("\n", " ").strip()
    published = entry.findtext("atom:published", default="", namespaces=ARXIV_NS)
    year = parse_year(published)
    authors = [a.findtext("atom:name", default="", namespaces=ARXIV_NS).strip() for a in entry.findall("atom:author", ARXIV_NS)]
    return MatchResult(
        source="arxiv",
        title=title,
        year=year,
        authors=authors,
        doi=f"10.48550/arXiv.{arxiv_id}",
        arxiv_id=arxiv_id,
        url=f"https://arxiv.org/abs/{arxiv_id}",
        score=1.0,
        raw=None,
    )


def search_arxiv_by_title(title: str, max_results: int = 5) -> list[MatchResult]:
    query = f'ti:"{title}"'
    url = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results={max_results}"
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    results: list[MatchResult] = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        entry_id = entry.findtext("atom:id", default="", namespaces=ARXIV_NS).split("/abs/")[-1]
        title_text = (entry.findtext("atom:title", default="", namespaces=ARXIV_NS) or "").replace("\n", " ").strip()
        published = entry.findtext("atom:published", default="", namespaces=ARXIV_NS)
        year = parse_year(published)
        authors = [a.findtext("atom:name", default="", namespaces=ARXIV_NS).strip() for a in entry.findall("atom:author", ARXIV_NS)]
        results.append(
            MatchResult(
                source="arxiv_search",
                title=title_text,
                year=year,
                authors=authors,
                doi=f"10.48550/arXiv.{entry_id}",
                arxiv_id=entry_id,
                url=f"https://arxiv.org/abs/{entry_id}",
                score=0.0,
            )
        )
    return results


def search_openalex(title: str, per_page: int = 5) -> list[MatchResult]:
    url = f"https://api.openalex.org/works?search={urllib.parse.quote(title)}&per-page={per_page}"
    data = request_json(url)
    results: list[MatchResult] = []
    for item in data.get("results", []):
        doi = item.get("doi")
        ids = item.get("ids") or {}
        results.append(
            MatchResult(
                source="openalex",
                title=item.get("display_name"),
                year=parse_year(item.get("publication_year")),
                authors=[a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])],
                doi=doi,
                arxiv_id=arxiv_id_from_doi(doi) or arxiv_id_from_url(ids.get("doi")),
                url=item.get("primary_location", {}).get("landing_page_url") or item.get("id"),
                score=0.0,
                raw=item,
            )
        )
    return results


def search_crossref(title: str, rows: int = 5) -> list[MatchResult]:
    url = f"https://api.crossref.org/works?query.title={urllib.parse.quote(title)}&rows={rows}"
    data = request_json(url)
    results: list[MatchResult] = []
    for item in data.get("message", {}).get("items", []):
        authors = []
        for a in item.get("author", []):
            name = " ".join([a.get("given", ""), a.get("family", "")]).strip()
            if name:
                authors.append(name)
        title_list = item.get("title") or []
        doi = item.get("DOI")
        year = None
        for key in ("published-print", "published-online", "issued", "created"):
            year = parse_year(item.get(key, {}).get("date-parts", [[None]])[0][0] if item.get(key) else None)
            if year:
                break
        results.append(
            MatchResult(
                source="crossref",
                title=title_list[0] if title_list else None,
                year=year,
                authors=authors,
                doi=doi,
                arxiv_id=arxiv_id_from_doi(doi),
                url=f"https://doi.org/{doi}" if doi else None,
                score=0.0,
                raw=item,
            )
        )
    return results


def fetch_openalex_by_doi(doi: str) -> MatchResult | None:
    clean_doi = doi.strip()
    if clean_doi.lower().startswith("https://doi.org/"):
        clean_doi = clean_doi.split("doi.org/", 1)[1]
    if clean_doi.lower().startswith("http://doi.org/"):
        clean_doi = clean_doi.split("doi.org/", 1)[1]
    url = f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(clean_doi, safe='')}"
    item = request_json(url)
    ids = item.get("ids") or {}
    item_doi = item.get("doi")
    return MatchResult(
        source="openalex_doi",
        title=item.get("display_name"),
        year=parse_year(item.get("publication_year")),
        authors=[a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])],
        doi=item_doi,
        arxiv_id=arxiv_id_from_doi(item_doi) or arxiv_id_from_url(ids.get("doi")),
        url=item.get("primary_location", {}).get("landing_page_url") or item.get("id"),
        score=1.0,
        raw=item,
    )


def fetch_crossref_by_doi(doi: str) -> MatchResult | None:
    clean_doi = doi.strip()
    if clean_doi.lower().startswith("https://doi.org/"):
        clean_doi = clean_doi.split("doi.org/", 1)[1]
    if clean_doi.lower().startswith("http://doi.org/"):
        clean_doi = clean_doi.split("doi.org/", 1)[1]
    url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi, safe='')}"
    item = request_json(url).get("message", {})
    authors = []
    for a in item.get("author", []):
        name = " ".join([a.get("given", ""), a.get("family", "")]).strip()
        if name:
            authors.append(name)
    title_list = item.get("title") or []
    year = None
    for key in ("published-print", "published-online", "issued", "created"):
        year = parse_year(item.get(key, {}).get("date-parts", [[None]])[0][0] if item.get(key) else None)
        if year:
            break
    item_doi = item.get("DOI")
    return MatchResult(
        source="crossref_doi",
        title=title_list[0] if title_list else None,
        year=year,
        authors=authors,
        doi=item_doi,
        arxiv_id=arxiv_id_from_doi(item_doi),
        url=f"https://doi.org/{item_doi}" if item_doi else None,
        score=1.0,
        raw=item,
    )


def score_candidate(
    query_title: str,
    query_year: int | None,
    query_first_author: str | None,
    candidate: MatchResult,
) -> float:
    title_s = sequence_score(query_title, candidate.title or "")
    year_s = 0.0
    if query_year and candidate.year:
        if query_year == candidate.year:
            year_s = 1.0
        elif abs(query_year - candidate.year) == 1:
            year_s = 0.5
    author_s = 0.0
    cand_first = first_author_surname(candidate.authors)
    if query_first_author and cand_first and query_first_author == cand_first:
        author_s = 1.0
    score = title_s * 0.75 + year_s * 0.15 + author_s * 0.10
    return round(score, 4)


def best_external_match(
    title: str,
    year: int | None,
    authors: str | list[str] | None,
    current_arxiv_id: str | None = None,
    doi: str | None = None,
) -> MatchResult | None:
    if current_arxiv_id and current_arxiv_id not in ("N/A", ""):
        try:
            return fetch_arxiv_metadata(current_arxiv_id)
        except Exception:
            pass
    if doi:
        for provider in (fetch_openalex_by_doi, fetch_crossref_by_doi):
            try:
                match = provider(doi)
                if match:
                    return match
            except Exception:
                continue

    query_first_author = first_author_surname(authors)
    candidates: list[MatchResult] = []
    for provider in (search_openalex, search_arxiv_by_title, search_crossref):
        try:
            candidates.extend(provider(title))
        except Exception:
            continue
    if not candidates:
        return None
    for cand in candidates:
        cand.score = score_candidate(title, year, query_first_author, cand)
    candidates.sort(key=lambda x: x.score, reverse=True)
    return candidates[0]


def enrich_target_paper(
    obj: dict[str, Any],
    rec_index: dict[str, dict[str, Any]],
    min_confidence: float,
) -> tuple[dict[str, Any], dict[str, Any]]:
    original_title = obj.get("paper_title")
    original_obj = {
        "paper_title": obj.get("paper_title"),
        "paper_arxiv_id": obj.get("paper_arxiv_id"),
    }
    title_key = normalize_title(original_title)
    rec = rec_index.get(title_key)
    query_title = rec.get("title") if rec else original_title
    query_year = rec.get("year") if rec else None
    query_authors = rec.get("authors") if rec else None
    query_doi = rec.get("doi") if rec else None
    current_arxiv = obj.get("paper_arxiv_id")
    match = best_external_match(
        query_title,
        query_year,
        query_authors,
        None if current_arxiv == "N/A" else current_arxiv,
        doi=query_doi,
    )
    log = {
        "level": "target_paper",
        "before": original_obj,
        "applied": False,
        "match": None,
        "after": {
            "paper_title": obj.get("paper_title"),
            "paper_arxiv_id": obj.get("paper_arxiv_id"),
        },
    }
    if not match or match.score < min_confidence:
        return obj, log
    obj["paper_title"] = match.title or obj["paper_title"]
    obj["paper_arxiv_id"] = match.arxiv_id or "N/A"
    log["applied"] = True
    log["after"] = {
        "paper_title": obj.get("paper_title"),
        "paper_arxiv_id": obj.get("paper_arxiv_id"),
    }
    log["match"] = {
        "source": match.source,
        "title": match.title,
        "year": match.year,
        "doi": match.doi,
        "arxiv_id": match.arxiv_id,
        "score": match.score,
    }
    return obj, log


def enrich_prior_work(pw: dict[str, Any], min_confidence: float) -> tuple[dict[str, Any], dict[str, Any]]:
    original_obj = {
        "title": pw.get("title"),
        "arxiv_id": pw.get("arxiv_id"),
        "year": pw.get("year"),
        "authors": pw.get("authors"),
    }
    match = best_external_match(
        pw.get("title", ""),
        parse_year(pw.get("year")),
        pw.get("authors"),
        None if pw.get("arxiv_id") in (None, "", "N/A") else pw.get("arxiv_id"),
    )
    log = {
        "level": "prior_work",
        "before": original_obj,
        "applied": False,
        "match": None,
        "after": {
            "title": pw.get("title"),
            "arxiv_id": pw.get("arxiv_id"),
            "year": pw.get("year"),
            "authors": pw.get("authors"),
        },
    }
    if not match or match.score < min_confidence:
        return pw, log
    pw["title"] = match.title or pw["title"]
    if match.arxiv_id:
        pw["arxiv_id"] = match.arxiv_id
    log["applied"] = True
    log["after"] = {
        "title": pw.get("title"),
        "arxiv_id": pw.get("arxiv_id"),
        "year": pw.get("year"),
        "authors": pw.get("authors"),
    }
    log["match"] = {
        "source": match.source,
        "title": match.title,
        "year": match.year,
        "doi": match.doi,
        "arxiv_id": match.arxiv_id,
        "score": match.score,
    }
    return pw, log


def enrich_file(
    path: Path,
    rec_index: dict[str, dict[str, Any]],
    target_threshold: float,
    prior_threshold: float,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    logs: list[dict[str, Any]] = []
    obj, target_log = enrich_target_paper(obj, rec_index, target_threshold)
    target_log["file"] = str(path)
    logs.append(target_log)

    enriched_prior = []
    for pw in obj.get("prior_works", []):
        pw, log = enrich_prior_work(pw, prior_threshold)
        log["file"] = str(path)
        enriched_prior.append(pw)
        logs.append(log)
        time.sleep(0.05)
    obj["prior_works"] = enriched_prior
    return obj, logs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enrich prior-work analysis JSON files")
    parser.add_argument(
        "--input_dir",
        type=str,
        default="results/recommended_acl_aaai_top300_min7.65_prior_work",
        help="Directory containing prior_work_analysis_*.json",
    )
    parser.add_argument(
        "--recommendation_jsonl",
        type=str,
        default="raw_paper/recommended_acl_aaai_top300_min7.65.jsonl",
        help="Recommendation source JSONL for target-paper metadata",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="results/recommended_acl_aaai_top300_min7.65_prior_work_enriched",
        help="Directory to write enriched JSON files",
    )
    parser.add_argument("--limit", type=int, default=-1, help="Limit number of files")
    parser.add_argument("--target_threshold", type=float, default=0.78)
    parser.add_argument("--prior_threshold", type=float, default=0.82)
    parser.add_argument("--write_inplace", action="store_true", help="Write back into input dir instead of output dir")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = input_dir if args.write_inplace else Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rec_index = load_recommendation_index(args.recommendation_jsonl)

    files = sorted(input_dir.glob("prior_work_analysis_*.json"))
    if args.limit != -1:
        files = files[: args.limit]

    all_logs: list[dict[str, Any]] = []
    for idx, path in enumerate(files, 1):
        print(f"[{idx}/{len(files)}] Enriching {path.name}", flush=True)
        enriched, logs = enrich_file(
            path,
            rec_index=rec_index,
            target_threshold=args.target_threshold,
            prior_threshold=args.prior_threshold,
        )
        out_path = output_dir / path.name
        out_path.write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
        all_logs.extend(logs)
        applied_count = sum(1 for item in logs if item.get("applied"))
        print(
            f"[{idx}/{len(files)}] Done {path.name} | applied_updates={applied_count}/{len(logs)} | output={out_path}",
            flush=True,
        )
        for item in logs:
            before = item.get("before") or {}
            after = item.get("after") or {}
            if item.get("level") == "target_paper":
                before_name = before.get("paper_title")
                after_name = after.get("paper_title")
                before_id = before.get("paper_arxiv_id")
                after_id = after.get("paper_arxiv_id")
            else:
                before_name = before.get("title")
                after_name = after.get("title")
                before_id = before.get("arxiv_id")
                after_id = after.get("arxiv_id")
            status = "updated" if item.get("applied") else "skipped"
            print(
                f"  - {item.get('level')}: {status} | title: {before_name!r} -> {after_name!r} | arxiv: {before_id!r} -> {after_id!r}",
                flush=True,
            )

    log_path = output_dir / "enrichment_log.jsonl"
    with log_path.open("w", encoding="utf-8") as f:
        for item in all_logs:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Wrote enriched files to {output_dir}", flush=True)
    print(f"Wrote log to {log_path}", flush=True)


if __name__ == "__main__":
    main()
