from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from loguru import logger

from .models import PaperRecord


SCHEMA = pa.schema(
    [
        ("paper_uid", pa.string()),
        ("venue", pa.string()),
        ("year", pa.int16()),
        ("track", pa.string()),
        ("title", pa.string()),
        ("title_normalized", pa.string()),
        ("authors", pa.list_(pa.string())),
        ("authors_str", pa.string()),
        ("author_count", pa.int16()),
        ("first_author", pa.string()),
        ("abstract", pa.string()),
        ("abstract_source", pa.string()),
        ("doi", pa.string()),
        ("arxiv_id", pa.string()),
        ("official_url", pa.string()),
        ("source_official", pa.string()),
        ("source_enrich", pa.string()),
        ("openalex_id", pa.string()),
        ("semantic_scholar_id", pa.string()),
        ("volume_id", pa.string()),
        ("issue_url", pa.string()),
        ("paper_url", pa.string()),
        ("crawl_time", pa.string()),
        ("has_abstract", pa.bool_()),
        ("has_doi", pa.bool_()),
        ("has_arxiv_id", pa.bool_()),
        ("quality_score", pa.int8()),
        ("raw_hash", pa.string()),
        ("raw_json", pa.string()),
    ]
)


class ParquetExporter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = Path(output_dir)

    def export(self, papers: list[PaperRecord]) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        grouped: dict[tuple[str, int], list[dict]] = defaultdict(list)
        for paper in papers:
            paper.refresh_derived_fields()
            grouped[(paper.venue, paper.year)].append(
                {
                    "paper_uid": paper.paper_uid,
                    "venue": paper.venue,
                    "year": paper.year,
                    "track": paper.track,
                    "title": paper.title,
                    "title_normalized": paper.title_normalized,
                    "authors": paper.authors,
                    "authors_str": paper.authors_str,
                    "author_count": paper.author_count,
                    "first_author": paper.first_author,
                    "abstract": paper.abstract,
                    "abstract_source": paper.abstract_source,
                    "doi": paper.doi,
                    "arxiv_id": paper.arxiv_id,
                    "official_url": paper.official_url,
                    "source_official": paper.source_official,
                    "source_enrich": paper.source_enrich,
                    "openalex_id": paper.openalex_id,
                    "semantic_scholar_id": paper.semantic_scholar_id,
                    "volume_id": paper.volume_id,
                    "issue_url": paper.issue_url,
                    "paper_url": paper.paper_url,
                    "crawl_time": paper.crawl_time,
                    "has_abstract": paper.has_abstract,
                    "has_doi": paper.has_doi,
                    "has_arxiv_id": paper.has_arxiv_id,
                    "quality_score": paper.quality_score,
                    "raw_hash": paper.raw_hash,
                    "raw_json": paper.raw_json,
                }
            )

        for (venue, year), rows in grouped.items():
            partition_dir = self.output_dir / f"venue={venue}" / f"year={year}"
            partition_dir.mkdir(parents=True, exist_ok=True)
            output_path = partition_dir / "papers.parquet"
            table = pa.Table.from_pylist(rows, schema=SCHEMA)
            pq.write_table(table, output_path, compression="zstd")
            logger.info("Wrote {} rows to {}", len(rows), output_path)
