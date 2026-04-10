from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Iterable

from .models import PaperRecord, utc_now_iso


class SQLiteStateStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.initialize()

    def initialize(self) -> None:
        self.conn.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS papers (
                paper_uid TEXT PRIMARY KEY,
                venue TEXT NOT NULL,
                year INTEGER NOT NULL,
                track TEXT NOT NULL,
                title TEXT NOT NULL,
                title_normalized TEXT NOT NULL,
                authors_json TEXT NOT NULL,
                authors_str TEXT NOT NULL,
                author_count INTEGER NOT NULL,
                first_author TEXT NOT NULL,
                abstract TEXT,
                abstract_source TEXT NOT NULL DEFAULT 'none',
                doi TEXT,
                arxiv_id TEXT,
                official_url TEXT,
                source_official TEXT NOT NULL,
                source_enrich TEXT NOT NULL DEFAULT 'none',
                openalex_id TEXT,
                semantic_scholar_id TEXT,
                volume_id TEXT,
                issue_url TEXT,
                paper_url TEXT,
                crawl_time TEXT NOT NULL,
                has_abstract INTEGER NOT NULL DEFAULT 0,
                has_doi INTEGER NOT NULL DEFAULT 0,
                has_arxiv_id INTEGER NOT NULL DEFAULT 0,
                quality_score INTEGER NOT NULL DEFAULT 0,
                raw_hash TEXT,
                raw_json TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_papers_venue_year ON papers(venue, year);
            CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi);
            CREATE INDEX IF NOT EXISTS idx_papers_official_url ON papers(official_url);
            CREATE TABLE IF NOT EXISTS tasks (
                task_key TEXT PRIMARY KEY,
                task_type TEXT NOT NULL,
                status TEXT NOT NULL,
                payload_json TEXT,
                retry_count INTEGER NOT NULL DEFAULT 0,
                last_error TEXT,
                updated_at TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    def upsert_paper(self, paper: PaperRecord) -> None:
        row = paper.to_db_row()
        columns = [
            "paper_uid",
            "venue",
            "year",
            "track",
            "title",
            "title_normalized",
            "authors_json",
            "authors_str",
            "author_count",
            "first_author",
            "abstract",
            "abstract_source",
            "doi",
            "arxiv_id",
            "official_url",
            "source_official",
            "source_enrich",
            "openalex_id",
            "semantic_scholar_id",
            "volume_id",
            "issue_url",
            "paper_url",
            "crawl_time",
            "has_abstract",
            "has_doi",
            "has_arxiv_id",
            "quality_score",
            "raw_hash",
            "raw_json",
        ]
        assignments = ", ".join([f"{column}=excluded.{column}" for column in columns[1:]])
        self.conn.execute(
            f"""
            INSERT INTO papers ({", ".join(columns)})
            VALUES ({", ".join(["?"] * len(columns))})
            ON CONFLICT(paper_uid) DO UPDATE SET
                {assignments}
            """,
            [row[column] for column in columns],
        )
        self.conn.commit()

    def mark_task(self, task_key: str, task_type: str, status: str, payload: dict | None = None, last_error: str | None = None) -> None:
        payload_json = json.dumps(payload, ensure_ascii=False, sort_keys=True) if payload else None
        self.conn.execute(
            """
            INSERT INTO tasks(task_key, task_type, status, payload_json, retry_count, last_error, updated_at)
            VALUES(?, ?, ?, ?, 0, ?, ?)
            ON CONFLICT(task_key) DO UPDATE SET
                task_type=excluded.task_type,
                status=excluded.status,
                payload_json=excluded.payload_json,
                last_error=excluded.last_error,
                updated_at=excluded.updated_at,
                retry_count=CASE
                    WHEN excluded.status='failed' THEN tasks.retry_count + 1
                    ELSE tasks.retry_count
                END
            """,
            (task_key, task_type, status, payload_json, last_error, utc_now_iso()),
        )
        self.conn.commit()

    def get_task_status(self, task_key: str) -> str | None:
        row = self.conn.execute("SELECT status FROM tasks WHERE task_key = ?", (task_key,)).fetchone()
        return row[0] if row else None

    def iter_papers(self, venues: Iterable[str] | None = None, years: Iterable[int] | None = None) -> list[PaperRecord]:
        clauses: list[str] = []
        params: list[object] = []
        if venues:
            venues = list(venues)
            clauses.append(f"venue IN ({', '.join(['?'] * len(venues))})")
            params.extend(venues)
        if years:
            years = list(years)
            clauses.append(f"year IN ({', '.join(['?'] * len(years))})")
            params.extend(years)
        query = "SELECT * FROM papers"
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY venue, year, title"
        rows = self.conn.execute(query, params).fetchall()
        return [PaperRecord.from_db_row(dict(row)) for row in rows]

    def iter_papers_needing_enrichment(
        self,
        venues: Iterable[str] | None = None,
        years: Iterable[int] | None = None,
        limit: int | None = None,
    ) -> list[PaperRecord]:
        clauses: list[str] = [
            "(papers.abstract IS NULL OR papers.abstract = '' OR papers.arxiv_id IS NULL OR papers.arxiv_id = '')",
            "NOT EXISTS (SELECT 1 FROM tasks WHERE task_key = 'enrich:' || papers.paper_uid AND status = 'success')",
        ]
        params: list[object] = []
        if venues:
            venues = list(venues)
            clauses.append(f"papers.venue IN ({', '.join(['?'] * len(venues))})")
            params.extend(venues)
        if years:
            years = list(years)
            clauses.append(f"papers.year IN ({', '.join(['?'] * len(years))})")
            params.extend(years)
        query = """
            SELECT papers.*
            FROM papers
        """
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY papers.has_abstract ASC, papers.has_arxiv_id ASC, papers.venue, papers.year"
        if limit:
            query += f" LIMIT {int(limit)}"
        rows = self.conn.execute(query, params).fetchall()
        return [PaperRecord.from_db_row(dict(row)) for row in rows]

    def write_coverage_report(self, output_path: Path) -> None:
        rows = self.conn.execute(
            """
            SELECT
                venue,
                year,
                COUNT(*) AS paper_count,
                SUM(CASE WHEN title IS NOT NULL AND title != '' THEN 1 ELSE 0 END) AS has_title_count,
                SUM(CASE WHEN author_count > 0 THEN 1 ELSE 0 END) AS has_authors_count,
                SUM(CASE WHEN has_doi = 1 THEN 1 ELSE 0 END) AS has_doi_count,
                SUM(CASE WHEN has_abstract = 1 THEN 1 ELSE 0 END) AS has_abstract_count,
                SUM(CASE WHEN has_arxiv_id = 1 THEN 1 ELSE 0 END) AS has_arxiv_id_count
            FROM papers
            GROUP BY venue, year
            ORDER BY venue, year
            """
        ).fetchall()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "venue",
                    "year",
                    "paper_count",
                    "has_title_count",
                    "has_authors_count",
                    "has_doi_count",
                    "has_abstract_count",
                    "has_arxiv_id_count",
                ],
            )
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))

    def close(self) -> None:
        self.conn.close()
