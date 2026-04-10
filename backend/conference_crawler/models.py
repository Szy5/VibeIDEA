from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class PaperRecord:
    paper_uid: str
    venue: str
    year: int
    track: str
    title: str
    title_normalized: str
    authors: list[str]
    authors_str: str
    author_count: int
    first_author: str
    abstract: str | None = None
    abstract_source: str = "none"
    doi: str | None = None
    arxiv_id: str | None = None
    official_url: str | None = None
    source_official: str = "unknown"
    source_enrich: str = "none"
    openalex_id: str | None = None
    semantic_scholar_id: str | None = None
    volume_id: str | None = None
    issue_url: str | None = None
    paper_url: str | None = None
    crawl_time: str = field(default_factory=utc_now_iso)
    has_abstract: bool = False
    has_doi: bool = False
    has_arxiv_id: bool = False
    quality_score: int = 0
    raw_hash: str | None = None
    raw_json: str | None = None

    def refresh_derived_fields(self) -> None:
        self.authors = [author for author in self.authors if author]
        self.authors_str = ", ".join(self.authors)
        self.author_count = len(self.authors)
        self.first_author = self.authors[0] if self.authors else ""
        self.has_abstract = bool(self.abstract and self.abstract.strip())
        self.has_doi = bool(self.doi)
        self.has_arxiv_id = bool(self.arxiv_id)
        self.quality_score = (
            int(bool(self.title)) * 2
            + int(bool(self.authors)) * 2
            + int(self.has_doi) * 2
            + int(self.has_abstract) * 3
            + int(self.has_arxiv_id)
        )
        if self.raw_json and not self.raw_hash:
            self.raw_hash = hashlib.sha1(self.raw_json.encode("utf-8")).hexdigest()

    def set_raw_payload(self, payload: dict) -> None:
        self.raw_json = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        self.raw_hash = hashlib.sha1(self.raw_json.encode("utf-8")).hexdigest()

    def to_db_row(self) -> dict:
        self.refresh_derived_fields()
        payload = asdict(self)
        payload["authors_json"] = json.dumps(self.authors, ensure_ascii=False)
        payload.pop("authors")
        return payload

    @classmethod
    def from_db_row(cls, row: dict) -> "PaperRecord":
        authors = json.loads(row.get("authors_json") or "[]")
        init = {k: row[k] for k in row.keys() if k not in {"authors_json"}}
        init["authors"] = authors
        return cls(**init)
