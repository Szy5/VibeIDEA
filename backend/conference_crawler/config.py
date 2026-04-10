from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env", override=False)


@dataclass(slots=True)
class CrawlerSettings:
    root_dir: Path = ROOT_DIR
    data_dir: Path = field(default_factory=lambda: ROOT_DIR / "data" / "conference_metadata")
    state_db_path: Path = field(default_factory=lambda: ROOT_DIR / "data" / "conference_metadata" / "state" / "crawl_state.db")
    parquet_dir: Path = field(default_factory=lambda: ROOT_DIR / "data" / "conference_metadata" / "parquet" / "papers")
    reports_dir: Path = field(default_factory=lambda: ROOT_DIR / "data" / "conference_metadata" / "reports")
    request_timeout: int = field(default_factory=lambda: int(os.getenv("CONF_CRAWLER_TIMEOUT", "30")))
    user_agent: str = field(
        default_factory=lambda: os.getenv(
            "CONF_CRAWLER_USER_AGENT",
            "VibeIDEAConferenceCrawler/0.1 (+https://github.com/)",
        )
    )
    openalex_api_key: str | None = field(default_factory=lambda: os.getenv("OPENALEX_API_KEY") or None)
    semantic_scholar_api_key: str | None = field(default_factory=lambda: os.getenv("SEMANTIC_SCHOLAR_API_KEY") or None)
    enable_semantic_scholar_without_key: bool = field(
        default_factory=lambda: os.getenv("CONF_CRAWLER_ENABLE_S2_WITHOUT_KEY", "0") == "1"
    )
    acl_min_interval: float = field(default_factory=lambda: float(os.getenv("CONF_CRAWLER_ACL_INTERVAL", "0.2")))
    aaai_min_interval: float = field(default_factory=lambda: float(os.getenv("CONF_CRAWLER_AAAI_INTERVAL", "1.2")))
    openalex_min_interval: float = field(default_factory=lambda: float(os.getenv("CONF_CRAWLER_OPENALEX_INTERVAL", "0.3")))
    semantic_scholar_min_interval: float = field(default_factory=lambda: float(os.getenv("CONF_CRAWLER_S2_INTERVAL", "0.8")))

    def ensure_directories(self) -> None:
        for path in [
            self.data_dir,
            self.state_db_path.parent,
            self.parquet_dir,
            self.reports_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)
