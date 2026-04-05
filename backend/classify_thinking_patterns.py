#!/usr/bin/env python3
"""
Classify thinking patterns for prior-work analysis JSON files.

This adapts Sci-Reasoning's thinking_patterns_llm_analysis/code/classify_all.py
to the current repository layout and JSON schema.


python -u backend/classify_thinking_patterns.py \
  --input_dir results/recommended_acl_aaai_top300_min7.65_prior_work \
  --model_name gpt-5 \
  --batch_size 5 \
  --checkpoint_path results/thinking_pattern_classification_checkpoint.json \
  --summary_path results/thinking_pattern_classification_summary.json \
  2>&1 | tee results/thinking_pattern_classification.log

"""

import argparse
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


DEFAULT_TAXONOMY_PATH = (
    "/home/sunzongyuan/projects/Sci-Reasoning/"
    "thinking_patterns_llm_analysis/results/pattern_taxonomy.json"
)


@dataclass
class CostTracker:
    input_cost_per_m: float = 0.25
    output_cost_per_m: float = 2.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    num_calls: int = 0

    def add_usage(self, input_tokens: int, output_tokens: int) -> None:
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.num_calls += 1

    def total_cost(self) -> float:
        return (
            self.total_input_tokens / 1_000_000 * self.input_cost_per_m
            + self.total_output_tokens / 1_000_000 * self.output_cost_per_m
        )

    def summary(self) -> dict[str, Any]:
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_cost_usd": round(self.total_cost(), 4),
            "num_calls": self.num_calls,
        }


def request_chat_completion(
    api_key: str,
    api_base: str,
    model_name: str,
    messages: list[dict[str, str]],
    cost_tracker: CostTracker,
) -> str:
    url = f"{api_base.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_name,
        "messages": messages,
    }

    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=300)
            response.raise_for_status()
            data = response.json()
            usage = data.get("usage", {})
            cost_tracker.add_usage(
                usage.get("prompt_tokens", 0),
                usage.get("completion_tokens", 0),
            )
            return data["choices"][0]["message"]["content"]
        except Exception as exc:
            last_error = exc
            print(f"  [Error] Attempt {attempt + 1}: {exc}", flush=True)
            if attempt < 2:
                time.sleep(2**attempt)
    assert last_error is not None
    raise last_error


def load_taxonomy(path: str) -> tuple[list[dict[str, Any]], dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    taxonomy = data.get("taxonomy", [])
    id_to_name = {item["id"]: item["name"] for item in taxonomy if "id" in item and "name" in item}
    return taxonomy, id_to_name


def load_papers(input_dir: Path, overwrite: bool) -> list[dict[str, Any]]:
    papers: list[dict[str, Any]] = []
    for json_file in sorted(input_dir.glob("prior_work_analysis_*.json")):
        try:
            with json_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            print(f"[WARN] Failed to load {json_file}: {exc}", flush=True)
            continue

        narrative = data.get("synthesis_narrative", "")
        if not narrative or len(narrative) < 100:
            continue
        if not overwrite and data.get("innovation_classification"):
            continue

        papers.append(
            {
                "title": data.get("paper_title", json_file.stem),
                "synthesis_narrative": narrative,
                "file_path": str(json_file),
            }
        )
    return papers


def build_messages(batch: list[dict[str, Any]], taxonomy: list[dict[str, Any]]) -> list[dict[str, str]]:
    taxonomy_ref = "\n".join(
        f"- {item['id']}: {item['name']} - {item['description'][:100]}..."
        for item in taxonomy
    )
    papers_text = "\n\n---\n\n".join(
        f'Paper {idx + 1}: "{paper["title"][:60]}..."\n{paper["synthesis_narrative"][:800]}'
        for idx, paper in enumerate(batch)
    )
    system_prompt = "You are an expert at classifying research thinking patterns. Be concise."
    user_prompt = f"""TAXONOMY:
{taxonomy_ref}

PAPERS:
{papers_text}

Classify each paper. Output JSON only:
{{"classifications": [{{"paper_index": 1, "primary_pattern": "P01", "secondary_patterns": ["P03"], "confidence": "high", "reasoning": "brief"}}]}}"""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def parse_classifications(response_text: str, batch: list[dict[str, Any]]) -> list[dict[str, Any]]:
    try:
        if "```json" in response_text:
            json_str = response_text.split("```json", 1)[1].split("```", 1)[0]
        elif "```" in response_text:
            json_str = response_text.split("```", 1)[1].split("```", 1)[0]
        else:
            json_str = response_text
        parsed = json.loads(json_str)
        classifications = parsed.get("classifications", [])
    except Exception:
        classifications = []

    results: list[dict[str, Any]] = []
    for idx, paper in enumerate(batch):
        if idx < len(classifications):
            results.append(classifications[idx])
        else:
            results.append(
                {
                    "paper_index": idx + 1,
                    "primary_pattern": "unknown",
                    "secondary_patterns": [],
                    "confidence": "unknown",
                    "reasoning": "classification_parse_failed_or_missing",
                }
            )
    return results


def apply_names(classification: dict[str, Any], id_to_name: dict[str, str]) -> dict[str, Any]:
    primary = classification.get("primary_pattern")
    secondary = classification.get("secondary_patterns", []) or []
    classification["primary_pattern_name"] = id_to_name.get(primary, "unknown")
    classification["secondary_pattern_names"] = [id_to_name.get(item, "unknown") for item in secondary]
    return classification


def update_json_file(path: Path, classification: dict[str, Any]) -> None:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data["innovation_classification"] = classification
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_checkpoint(
    checkpoint_path: Path,
    processed: list[dict[str, Any]],
    cost_tracker: CostTracker,
) -> None:
    checkpoint_path.write_text(
        json.dumps(
            {
                "classified": processed,
                "input_tokens": cost_tracker.total_input_tokens,
                "output_tokens": cost_tracker.total_output_tokens,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify innovation thinking patterns for prior-work JSON files")
    parser.add_argument(
        "--input_dir",
        type=str,
        default="results/recommended_acl_aaai_top300_min7.65_prior_work",
        help="Directory containing prior_work_analysis_*.json",
    )
    parser.add_argument(
        "--taxonomy_path",
        type=str,
        default=DEFAULT_TAXONOMY_PATH,
        help="Path to Sci-Reasoning pattern_taxonomy.json",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default=os.environ.get("MODEL_NAME", "gpt-5-mini"),
        help="Model name for thinking-pattern classification",
    )
    parser.add_argument("--batch_size", type=int, default=5, help="Classification batch size")
    parser.add_argument("--limit", type=int, default=-1, help="Number of files to process")
    parser.add_argument("--offset", type=int, default=0, help="Start offset")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing innovation_classification")
    parser.add_argument(
        "--checkpoint_path",
        type=str,
        default="results/thinking_pattern_classification_checkpoint.json",
        help="Checkpoint file path",
    )
    parser.add_argument(
        "--summary_path",
        type=str,
        default="results/thinking_pattern_classification_summary.json",
        help="Summary output path",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.15,
        help="Sleep seconds between batches",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv(".env", override=True)
    args = parse_args()
    api_key = os.environ.get("OPENAI_API_KEY")
    api_base = os.environ.get("OPENAI_API_BASE")
    if not api_key or not api_base:
        raise RuntimeError("OPENAI_API_KEY / OPENAI_API_BASE 未配置")

    taxonomy, id_to_name = load_taxonomy(args.taxonomy_path)
    input_dir = Path(args.input_dir)
    papers = load_papers(input_dir, overwrite=args.overwrite)
    papers = papers[args.offset :]
    if args.limit != -1:
        papers = papers[: args.limit]

    checkpoint_path = Path(args.checkpoint_path)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path = Path(args.summary_path)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    cost_tracker = CostTracker()
    processed: list[dict[str, Any]] = []
    start_idx = 0
    if checkpoint_path.exists():
        try:
            checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
            processed = checkpoint.get("classified", [])
            start_idx = len(processed)
            cost_tracker.total_input_tokens = checkpoint.get("input_tokens", 0)
            cost_tracker.total_output_tokens = checkpoint.get("output_tokens", 0)
            cost_tracker.num_calls = max(0, start_idx // max(1, args.batch_size))
            print(f"Resuming from checkpoint: {start_idx} files already classified", flush=True)
        except Exception as exc:
            print(f"[WARN] Failed to load checkpoint: {exc}", flush=True)

    print("=" * 60, flush=True)
    print("THINKING PATTERN CLASSIFICATION", flush=True)
    print("=" * 60, flush=True)
    print(f"Loaded taxonomy with {len(taxonomy)} patterns", flush=True)
    print(f"Loaded {len(papers)} files to classify", flush=True)

    remaining = max(0, len(papers) - start_idx)
    total_batches = (remaining + max(1, args.batch_size) - 1) // max(1, args.batch_size)
    print(f"Classifying {remaining} remaining files in {total_batches} batches", flush=True)

    batch_counter = 0
    for i in range(start_idx, len(papers), max(1, args.batch_size)):
        batch = papers[i : i + max(1, args.batch_size)]
        batch_counter += 1
        print(f"[BATCH {batch_counter}/{total_batches}] Processing {len(batch)} files", flush=True)
        for item in batch:
            print(f"  - {Path(item['file_path']).name}", flush=True)

        messages = build_messages(batch, taxonomy)
        response_text = request_chat_completion(
            api_key=api_key,
            api_base=api_base,
            model_name=args.model_name,
            messages=messages,
            cost_tracker=cost_tracker,
        )
        classifications = parse_classifications(response_text, batch)

        for paper, classification in zip(batch, classifications):
            enriched = apply_names(classification, id_to_name)
            file_path = Path(paper["file_path"])
            update_json_file(file_path, enriched)
            processed.append(
                {
                    "file_path": str(file_path),
                    "title": paper["title"],
                    "innovation_classification": enriched,
                }
            )
            print(
                f"    updated {file_path.name} -> {enriched.get('primary_pattern')} / {enriched.get('secondary_patterns', [])}",
                flush=True,
            )

        pct = len(processed) / len(papers) * 100 if papers else 100.0
        print(
            f"  Progress: {len(processed)}/{len(papers)} ({pct:.1f}%) | Cost: ${cost_tracker.total_cost():.4f}",
            flush=True,
        )
        save_checkpoint(checkpoint_path, processed, cost_tracker)

        if args.sleep > 0:
            time.sleep(args.sleep)

    summary_path.write_text(
        json.dumps(
            {
                "count": len(processed),
                "model_name": args.model_name,
                "input_dir": args.input_dir,
                "taxonomy_path": args.taxonomy_path,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "cost": cost_tracker.summary(),
                "classified": processed,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Classification complete", flush=True)
    print(f"Checkpoint written to {checkpoint_path}", flush=True)
    print(f"Summary written to {summary_path}", flush=True)


if __name__ == "__main__":
    main()
