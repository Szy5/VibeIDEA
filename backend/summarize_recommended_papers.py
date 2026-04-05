#!/usr/bin/env python3
"""
Adapt Sci-Reasoning prior-work extraction pipeline to locally recommended papers.

Important:
- Keep the original prior-work prompt and markdown format unchanged.
- Only replace the arXiv metadata/PDF acquisition layer with local JSONL metadata + official PDF URLs.



python -u backend/summarize_recommended_papers.py \
  --input raw_paper/recommended_acl_aaai_top300_min7.65.jsonl \
  --pdf_dir raw_paper/pdfs \
  --output_dir results/recommended_acl_aaai_top300_min7.65_prior_work \
  --mode all \
  --download_workers 8 \
  --gpt_workers 10 \
  > results/recommended_acl_aaai_top300_min7.65_prior_work_batch.log 2>&1

#only 调用大模型进行知识提取
python -u backend/summarize_recommended_papers.py \
  --input raw_paper/recommended_acl_aaai_top300_min7.65.jsonl \
  --pdf_dir raw_paper/pdfs \
  --output_dir results/recommended_acl_aaai_top300_min7.65_prior_work \
  --mode analyze \
  --gpt_workers 10 \
  --model_name gpt-5 \
"""

import argparse
import concurrent.futures
import json
import os
import re
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import fitz
import requests
from dotenv import load_dotenv


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)


VALID_ROLES = [
    "Baseline",
    "Inspiration",
    "Gap Identification",
    "Foundation",
    "Extension",
    "Related Problem",
]


@dataclass
class RecommendedPaper:
    title: str
    summary: str
    score: float | None
    abstract: str | None
    authors: str | None
    venue: str | None
    year: int | None
    source: str | None
    url: str | None
    doi: str | None = None
    arxiv_id: str | None = None


@dataclass
class PriorWork:
    title: str
    authors: str
    year: Optional[int]
    role: str
    relationship_sentence: str
    arxiv_id: Optional[str] = None
    url: Optional[str] = None


@dataclass
class PriorWorkAnalysis:
    paper_title: str
    paper_arxiv_id: str
    paper_abstract: str
    prior_works: list[PriorWork]
    synthesis_narrative: str
    analysis_timestamp: str


def load_recommended_papers(path: str) -> list[RecommendedPaper]:
    papers: list[RecommendedPaper] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            papers.append(
                RecommendedPaper(
                    title=item.get("title", ""),
                    summary=item.get("summary", ""),
                    score=item.get("score"),
                    abstract=item.get("abstract"),
                    authors=item.get("authors"),
                    venue=item.get("venue"),
                    year=item.get("year"),
                    source=item.get("source"),
                    url=item.get("url"),
                    doi=item.get("doi"),
                    arxiv_id=item.get("arxiv_id"),
                )
            )
    return papers


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s.-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[-\s]+", "_", text.strip())
    return text[:120] or "paper"


def infer_arxiv_id(paper: RecommendedPaper) -> str | None:
    if paper.arxiv_id:
        return paper.arxiv_id
    if not paper.url:
        return None
    patterns = [
        r"arxiv\.org/abs/([^/?#]+)",
        r"arxiv\.org/pdf/([^/?#]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, paper.url)
        if match:
            return match.group(1).replace(".pdf", "")
    return None


def paper_identifier(paper: RecommendedPaper) -> str:
    if infer_arxiv_id(paper):
        return infer_arxiv_id(paper).replace("/", "_").replace(".", "_")
    if paper.doi:
        return paper.doi.replace("/", "_").replace(".", "_")
    return slugify(paper.title)


def get_pdf_storage_path(paper: RecommendedPaper, pdf_dir: Path) -> Path:
    venue = (paper.venue or "UNKNOWN").upper()
    year = str(paper.year or "UNKNOWN")
    filename = f"{paper_identifier(paper)}.pdf"
    return pdf_dir / f"venue={venue}" / f"year={year}" / filename


def get_paper_metadata(paper: RecommendedPaper) -> dict[str, Any]:
    authors = []
    if paper.authors:
        authors = [name.strip() for name in paper.authors.split(",") if name.strip()]
    return {
        "arxiv_id": infer_arxiv_id(paper) or "N/A",
        "title": paper.title,
        "abstract": paper.abstract or paper.summary or "",
        "authors": authors,
        "year": paper.year,
        "pdf_url": resolve_pdf_url(paper),
        "url": paper.url,
        "doi": paper.doi,
    }


def resolve_pdf_url(paper: RecommendedPaper) -> str | None:
    arxiv_id = infer_arxiv_id(paper)
    if arxiv_id:
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    if not paper.url:
        return None

    if "aclanthology.org" in paper.url:
        return paper.url.rstrip("/") + ".pdf"

    if "ojs.aaai.org" in paper.url:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})
        response = session.get(paper.url, timeout=30)
        response.raise_for_status()
        html = response.text

        # 1) Most reliable: citation meta tag
        match = re.search(
            r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"',
            html,
            re.IGNORECASE,
        )
        if match:
            return requests.compat.urljoin(paper.url, match.group(1).replace("&amp;", "&"))

        # 2) Direct download link if present
        match = re.search(r'href="([^"]*/article/download/[^"]+)"', html, re.IGNORECASE)
        if match:
            href = match.group(1).replace("&amp;", "&")
            return requests.compat.urljoin(paper.url, href)

        # 3) Galley PDF page like /article/view/<submission>/<galley> -> convert to /article/download/<submission>/<galley>
        match = re.search(
            r'href="([^"]*/article/view/(\d+)/(\d+))"[^>]*>\s*PDF\s*<',
            html,
            re.IGNORECASE,
        )
        if match:
            submission_id = match.group(2)
            galley_id = match.group(3)
            return requests.compat.urljoin(
                paper.url,
                f"/index.php/AAAI/article/download/{submission_id}/{galley_id}",
            )

        # 4) Fallback: infer from current article/view URL
        match = re.search(r"/article/view/(\d+)(?:/(\d+))?", paper.url)
        if match:
            submission_id = match.group(1)
            # if no galley id in URL, try to find any /view/<submission>/<galley> in html first
            if not match.group(2):
                galley_match = re.search(
                    rf"/article/view/{submission_id}/(\d+)",
                    html,
                    re.IGNORECASE,
                )
                if galley_match:
                    return requests.compat.urljoin(
                        paper.url,
                        f"/index.php/AAAI/article/download/{submission_id}/{galley_match.group(1)}",
                    )

    return None


def download_pdf(pdf_url: str, output_path: Path) -> None:
    print(f"[INFO] Downloading PDF from {pdf_url}")
    response = requests.get(pdf_url, headers={"User-Agent": USER_AGENT}, timeout=60)
    if response.status_code != 200:
        raise Exception(f"Failed to download PDF: {response.status_code}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)


def ensure_pdf_downloaded(paper: RecommendedPaper, pdf_dir: Path) -> dict[str, Any]:
    metadata = get_paper_metadata(paper)
    pdf_path = get_pdf_storage_path(paper, pdf_dir)
    result = {
        "title": paper.title,
        "pdf_path": str(pdf_path),
        "pdf_url": metadata["pdf_url"],
        "status": "missing",
        "error": None,
    }
    if pdf_path.exists():
        result["status"] = "exists"
        return result
    if not metadata["pdf_url"]:
        result["status"] = "no_pdf_url"
        return result
    try:
        download_pdf(metadata["pdf_url"], pdf_path)
        result["status"] = "downloaded"
        return result
    except Exception as exc:
        result["status"] = "failed"
        result["error"] = str(exc)
        return result


def extract_pdf_text(pdf_path: Path, max_words: int = 8000, max_pages: int = 15) -> str:
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(min(max_pages, len(doc))):
            page = doc[page_num]
            text += page.get_text() + "\n"
        doc.close()
        print("[INFO] Extracted text using PyMuPDF")
    except Exception as e:
        print(f"[WARN] PyMuPDF failed: {e}")

    if not text.strip():
        try:
            import subprocess

            result = subprocess.run(
                ["pdftotext", "-layout", "-l", str(max_pages), str(pdf_path), "-"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                text = result.stdout
                print("[INFO] Extracted text using pdftotext")
        except Exception as e:
            print(f"[WARN] pdftotext failed: {e}")

    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words])
        print(f"[INFO] Truncated text to {max_words} words (from {len(words)})")
    else:
        print(f"[INFO] Extracted {len(words)} words from PDF")

    return text


def call_gpt5(messages: list[dict[str, str]], api_key: str, api_base: str, model_name: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_name,
        "messages": messages,
    }
    url = f"{api_base.rstrip('/')}/chat/completions"
    print("[INFO] Calling GPT-5 API...")
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=300,
    )
    if response.status_code != 200:
        raise Exception(f"GPT-5 API error: {response.status_code} - {response.text}")
    result = response.json()
    return result["choices"][0]["message"]["content"]


def analyze_prior_works(
    paper_metadata: dict[str, Any],
    paper_text: str,
    api_key: str,
    api_base: str,
    model_name: str,
) -> dict:
    system_prompt = """You are an expert AI research analyst. Your task is to identify the KEY PRIOR WORKS that DIRECTLY led to a research paper's core innovation.

## CRITICAL: Focus on DIRECT Intellectual Lineage

You must identify papers that are **directly responsible** for the current paper's main contributions. Ask yourself:
- "Without this prior work, would the current paper's core idea exist?"
- "Did this prior work directly inspire, enable, or motivate the KEY INNOVATION?"
- "Is this paper cited in the Introduction or Related Work as a PRIMARY influence?"

### ❌ DO NOT INCLUDE:
- Generic infrastructure/tools (e.g., PyTorch, CUDA, standard attention mechanisms)
- Complementary optimizations that are orthogonal to the main contribution
- Papers that share the same domain but don't directly influence the core idea
- Standard baselines that are just compared against without deeper connection
- Well-known foundational works that everyone cites but aren't specific to this innovation

### ✅ DO INCLUDE:
- Papers whose specific IDEAS, METHODS, or FINDINGS directly shaped the current work
- Papers whose LIMITATIONS or GAPS the current paper explicitly addresses
- Papers that introduced the PROBLEM FORMULATION the current paper builds on
- Papers whose TECHNIQUES are directly extended or modified
- Papers that provide the KEY INSIGHT that the current paper leverages

## Role Classifications (assign ONE per paper):

1. **Baseline**: The primary system/method this paper improves upon or compares against as its main competitor
2. **Inspiration**: Paper whose specific idea/approach directly sparked the current paper's key innovation  
3. **Gap Identification**: Paper whose explicit limitations/failures motivated this research direction
4. **Foundation**: Paper that introduced the core problem formulation, dataset, or theoretical framework used
5. **Extension**: Paper whose specific method is directly extended, modified, or generalized
6. **Related Problem**: Paper solving a closely related problem whose solution approach informed this work

## Output Requirements:

For each prior work (identify 5-7 papers, quality over quantity):
1. **Role**: One of the six classifications above
2. **Relationship Sentence**: ONE specific sentence explaining the DIRECT connection to the current paper's innovation. Be concrete about WHAT was borrowed/extended/addressed.

## Synthesis Narrative (200-300 words):
Write a cohesive narrative that flows naturally (NO explicit "Part 1" / "Part 2" labels):

**First ~150 words - Prior Work with Relevant Details:**
Describe each prior work, but FOCUS ONLY on the specific aspects/details that relate to the current paper's innovation. For each prior work, highlight:
- The specific technique, insight, or finding that is relevant (not a general summary)
- How this specific detail connects to what the current paper does
- Do NOT mention the current paper yet - just establish what relevant knowledge existed

**Remaining ~100 words - How They Collectively Inspired Current Work:**
Transition naturally to explain:
- What gap or opportunity emerged from the combination of these prior works
- How the current paper synthesizes or builds upon these specific relevant details
- Why this was a natural next step given the prior work landscape

The narrative should read as one flowing paragraph, not two separate sections.

## Output Format (JSON):
```json
{
  "prior_works": [
    {
      "title": "Exact paper title",
      "authors": "First author et al.",
      "year": 2023,
      "arxiv_id": "if known",
      "role": "One of six roles",
      "relationship_sentence": "Specific sentence about DIRECT connection to core innovation"
    }
  ],
  "synthesis_narrative": "200-300 word flowing narrative: describe prior works focusing on details relevant to current paper, then show how they collectively inspired this work"
}
```

Remember: Every paper you include should pass the test: "This paper DIRECTLY influenced the core innovation, not just the general research area."
"""

    user_prompt = f"""Analyze this research paper and identify the prior works that DIRECTLY led to its core innovation.

## Paper Title:
{paper_metadata['title']}

## Authors:
{', '.join(paper_metadata['authors'])}

## Abstract:
{paper_metadata['abstract']}

## Paper Content (first ~8000 words / 15 pages):
{paper_text if paper_text.strip() else "[PDF extraction unavailable - analyze based on title and abstract]"}

---

TASK: Identify 5-7 prior works that DIRECTLY influenced this paper's KEY CONTRIBUTION. 

Focus on papers that:
1. Introduced ideas/methods this paper directly builds on
2. Had limitations this paper explicitly addresses  
3. Defined the problem formulation used here
4. Are the primary baselines being improved upon

DO NOT include generic tools, orthogonal optimizations, or tangentially related work.

Return your analysis as valid JSON."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response_text = call_gpt5(messages, api_key=api_key, api_base=api_base, model_name=model_name)
    try:
        json_match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", response_text)
        if json_match:
            analysis = json.loads(json_match.group(1))
        else:
            json_match = re.search(r"\{[\s\S]*\}", response_text)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in response")
    except json.JSONDecodeError as e:
        print(f"[WARN] Failed to parse JSON: {e}")
        print(f"[DEBUG] Response preview: {response_text[:1500]}...")
        raise
    return analysis


def generate_markdown_report(analysis: PriorWorkAnalysis) -> str:
    report = f"""# Prior Work Analysis Report

## Target Paper

**Title:** {analysis.paper_title}

**arXiv ID:** [{analysis.paper_arxiv_id}](https://arxiv.org/abs/{analysis.paper_arxiv_id})

**Abstract:** 
> {analysis.paper_abstract}

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

"""
    roles_order = ["Foundation", "Inspiration", "Gap Identification", "Baseline", "Extension", "Related Problem"]
    by_role: dict[str, list[PriorWork]] = {}
    for pw in analysis.prior_works:
        role = pw.role
        if role not in by_role:
            by_role[role] = []
        by_role[role].append(pw)

    for role in roles_order:
        if role in by_role:
            report += f"### 🏷️ {role}\n\n"
            for pw in by_role[role]:
                year_str = f" ({pw.year})" if pw.year else ""
                arxiv_str = f" [[arXiv](https://arxiv.org/abs/{pw.arxiv_id})]" if pw.arxiv_id else ""
                report += f"""**{pw.title}**{year_str}{arxiv_str}
- *Authors:* {pw.authors}
- *Direct Connection:* {pw.relationship_sentence}

"""

    report += f"""---

## Synthesis: How Prior Work Led to This Paper

{analysis.synthesis_narrative}

---

*Analysis generated on: {analysis.analysis_timestamp}*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
"""
    return report


def process_paper(
    paper: RecommendedPaper,
    output_dir: Path,
    pdf_dir: Path,
    api_key: str,
    api_base: str,
    model_name: str,
    sleep_seconds: float = 0.0,
    skip_existing: bool = True,
) -> tuple[Path, Path]:
    safe_id = paper_identifier(paper)
    output_file = output_dir / f"prior_work_analysis_{safe_id}.json"
    md_file = output_dir / f"prior_work_analysis_{safe_id}.md"
    if skip_existing and output_file.exists() and md_file.exists():
        print(f"[INFO] Skipping existing outputs: {output_file} | {md_file}")
        return output_file, md_file

    print("=" * 70)
    print("PRIOR WORK EXTRACTION PIPELINE (v2 - Direct Lineage Focus)")
    print("=" * 70)
    print("\n[STEP 1] Fetching paper metadata from local recommendations...")
    metadata = get_paper_metadata(paper)
    print(f"  Title: {metadata['title']}")
    print(f"  Authors: {', '.join(metadata['authors'][:3])}{'...' if len(metadata['authors']) > 3 else ''}")
    print(f"  Year: {metadata['year']}")

    print("\n[STEP 2] Downloading and extracting PDF content...")
    paper_text = ""
    pdf_path = get_pdf_storage_path(paper, pdf_dir)
    if pdf_path.exists():
        try:
            print(f"[INFO] Reusing existing PDF: {pdf_path}")
            paper_text = extract_pdf_text(pdf_path)
        except Exception as e:
            print(f"[WARN] PDF extraction failed: {e}")
            print("[INFO] Will analyze based on abstract only")
    elif metadata["pdf_url"]:
        try:
            download_pdf(metadata["pdf_url"], pdf_path)
            paper_text = extract_pdf_text(pdf_path)
        except Exception as e:
            print(f"[WARN] PDF extraction failed: {e}")
            print("[INFO] Will analyze based on abstract only")
    else:
        print("[WARN] No PDF URL found, using abstract only")

    print("\n[STEP 3] Analyzing prior works with GPT-5...")
    analysis = analyze_prior_works(
        metadata,
        paper_text,
        api_key=api_key,
        api_base=api_base,
        model_name=model_name,
    )

    print("\n[STEP 4] Formatting results...")
    prior_works: list[PriorWork] = []
    for pw in analysis.get("prior_works", []):
        prior_works.append(
            PriorWork(
                title=pw.get("title", "Unknown"),
                authors=pw.get("authors", "Unknown"),
                year=pw.get("year"),
                role=pw.get("role", "Foundation"),
                relationship_sentence=pw.get("relationship_sentence", ""),
                arxiv_id=pw.get("arxiv_id"),
                url=pw.get("url"),
            )
        )

    result = PriorWorkAnalysis(
        paper_title=metadata["title"],
        paper_arxiv_id=metadata["arxiv_id"],
        paper_abstract=metadata["abstract"],
        prior_works=prior_works,
        synthesis_narrative=analysis.get("synthesis_narrative", ""),
        analysis_timestamp=datetime.now().isoformat(),
    )

    print("\n[STEP 5] Saving results...")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(asdict(result), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Saved JSON to: {output_file}")

    md_report = generate_markdown_report(result)
    md_file.write_text(md_report, encoding="utf-8")
    print(f"  Saved Markdown to: {md_file}")

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)

    if sleep_seconds > 0:
        time.sleep(sleep_seconds)

    return output_file, md_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prior work extraction for recommended papers")
    parser.add_argument(
        "--input",
        type=str,
        default="raw_paper/recommended_acl_aaai_top300_min7.65.jsonl",
        help="Recommended paper JSONL path",
    )
    parser.add_argument(
        "--pdf_dir",
        type=str,
        default="raw_paper/pdfs",
        help="Directory for storing downloaded raw PDFs",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="results/recommended_acl_aaai_top300_min7.65_prior_work",
        help="Output directory for prior work reports",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default=os.environ.get("MODEL_NAME", "gpt-5"),
        help="Model name used for prior-work extraction",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["all", "download", "analyze"],
        default="all",
        help="download: only fetch PDFs; analyze: only run GPT analysis using local PDFs when available; all: download first then analyze",
    )
    parser.add_argument(
        "--download_workers",
        type=int,
        default=8,
        help="Number of workers for parallel PDF download stage",
    )
    parser.add_argument(
        "--gpt_workers",
        type=int,
        default=1,
        help="Number of workers for parallel GPT analysis stage",
    )
    parser.add_argument("--limit", type=int, default=-1, help="Number of papers to process")
    parser.add_argument("--offset", type=int, default=0, help="Start offset in JSONL")
    parser.add_argument("--sleep", type=float, default=0.0, help="Sleep seconds between API calls")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing JSON/MD outputs")
    return parser.parse_args()


def run_download_stage(
    papers: list[RecommendedPaper],
    pdf_dir: Path,
    workers: int,
) -> dict[str, Any]:
    pdf_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {
            executor.submit(ensure_pdf_downloaded, paper, pdf_dir): paper.title
            for paper in papers
        }
        for idx, future in enumerate(concurrent.futures.as_completed(future_map), 1):
            result = future.result()
            results.append(result)
            print(
                f"[DOWNLOAD {idx}/{len(papers)}] {result['status']}: {result['title']}"
            )
            if result["error"]:
                print(f"  [ERROR] {result['error']}")

    summary = {
        "count": len(results),
        "downloaded": sum(1 for x in results if x["status"] == "downloaded"),
        "exists": sum(1 for x in results if x["status"] == "exists"),
        "no_pdf_url": sum(1 for x in results if x["status"] == "no_pdf_url"),
        "failed": sum(1 for x in results if x["status"] == "failed"),
        "results": results,
        "generated_at": datetime.now().isoformat(),
    }
    return summary


def main() -> None:
    load_dotenv(".env", override=True)
    args = parse_args()
    api_key = os.environ.get("OPENAI_API_KEY")
    api_base = os.environ.get("OPENAI_API_BASE")
    if not api_key or not api_base:
        raise RuntimeError("OPENAI_API_KEY / OPENAI_API_BASE 未配置")

    papers = load_recommended_papers(args.input)
    papers = papers[args.offset :]
    if args.limit != -1:
        papers = papers[: args.limit]

    output_dir = Path(args.output_dir)
    pdf_dir = Path(args.pdf_dir)

    if args.mode in ("all", "download"):
        print("=" * 70)
        print("PDF DOWNLOAD STAGE")
        print("=" * 70)
        download_summary = run_download_stage(
            papers=papers,
            pdf_dir=pdf_dir,
            workers=max(1, args.download_workers),
        )
        download_manifest = output_dir.parent / f"{output_dir.name}_download_manifest.json"
        download_manifest.write_text(
            json.dumps(download_summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Download manifest written to {download_manifest}")
        if args.mode == "download":
            return

    generated_json: list[str] = []
    generated_md: list[str] = []
    if max(1, args.gpt_workers) == 1:
        for idx, paper in enumerate(papers, 1):
            print(f"\n[{idx}/{len(papers)}] Processing: {paper.title}")
            json_path, md_path = process_paper(
                paper,
                output_dir=output_dir,
                pdf_dir=pdf_dir,
                api_key=api_key,
                api_base=api_base,
                model_name=args.model_name,
                sleep_seconds=args.sleep,
                skip_existing=not args.overwrite,
            )
            generated_json.append(str(json_path))
            generated_md.append(str(md_path))
    else:
        print("=" * 70)
        print("GPT ANALYSIS STAGE")
        print("=" * 70)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.gpt_workers)) as executor:
            future_map = {
                executor.submit(
                    process_paper,
                    paper,
                    output_dir,
                    pdf_dir,
                    api_key,
                    api_base,
                    args.model_name,
                    args.sleep,
                    not args.overwrite,
                ): paper
                for paper in papers
            }
            for idx, future in enumerate(concurrent.futures.as_completed(future_map), 1):
                paper = future_map[future]
                try:
                    json_path, md_path = future.result()
                    generated_json.append(str(json_path))
                    generated_md.append(str(md_path))
                    print(f"[ANALYZE {idx}/{len(papers)}] done: {paper.title}")
                except Exception as exc:
                    print(f"[ANALYZE {idx}/{len(papers)}] failed: {paper.title}")
                    print(f"  [ERROR] {exc}")

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "input": args.input,
                "pdf_dir": args.pdf_dir,
                "count": len(generated_md),
                "generated_json": generated_json,
                "generated_md": generated_md,
                "generated_at": datetime.now().isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()
