from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict

from loguru import logger
from tqdm import tqdm

from .aaai_ojs import AAAIOJSCrawler
from .acl_anthology import ACLAnthologyCrawler
from .config import CrawlerSettings
from .enrich import OpenAlexEnricher, SemanticScholarEnricher
from .exporter import ParquetExporter
from .http import HttpClient
from .state import SQLiteStateStore


class ConferenceCrawlerPipeline:
    def __init__(self, settings: CrawlerSettings) -> None:
        self.settings = settings
        self.settings.ensure_directories()
        self.state = SQLiteStateStore(self.settings.state_db_path)
        self.http = HttpClient(
            user_agent=self.settings.user_agent,
            timeout=self.settings.request_timeout,
            min_interval_by_host={
                "aclanthology.org": self.settings.acl_min_interval,
                "ojs.aaai.org": self.settings.aaai_min_interval,
                "api.openalex.org": self.settings.openalex_min_interval,
                "api.semanticscholar.org": self.settings.semantic_scholar_min_interval,
            },
        )
        self.acl = ACLAnthologyCrawler(self.http)
        self.aaai = AAAIOJSCrawler(self.http)
        self.openalex = OpenAlexEnricher(self.http, self.settings.openalex_api_key)
        self.semantic_scholar = SemanticScholarEnricher(self.http, self.settings.semantic_scholar_api_key)
        self.exporter = ParquetExporter(self.settings.parquet_dir)

    def crawl_official(self, venues: Iterable[str], years: Iterable[int]) -> None:
        years = sorted({int(year) for year in years})
        for venue in [venue.upper() for venue in venues]:
            if venue in {"ACL", "EMNLP"}:
                volume_tasks = self.acl.discover_volumes(venue, years)
                for volume_task in tqdm(volume_tasks, desc=f"{venue} volumes", unit="volume"):
                    task_key = f"official:{venue}:{volume_task.volume_url}"
                    payload = asdict(volume_task)
                    if self.state.get_task_status(task_key) == "success":
                        continue
                    self.state.mark_task(task_key, "official_extract", "running", payload=payload)
                    try:
                        for record in self.acl.extract_volume(volume_task):
                            self.state.upsert_paper(record)
                        self.state.mark_task(task_key, "official_extract", "success", payload=payload)
                    except Exception as exc:
                        self.state.mark_task(task_key, "official_extract", "failed", payload=payload, last_error=str(exc))
                        raise
            elif venue == "AAAI":
                issue_tasks = self.aaai.discover_issues(years)
                for issue_task in tqdm(issue_tasks, desc="AAAI issues", unit="issue"):
                    task_key = f"official:AAAI:{issue_task.issue_url}"
                    payload = asdict(issue_task)
                    try:
                        # Revisit AAAI issue pages on reruns so previously failed article-level tasks
                        # can be retried without clearing the whole issue status.
                        self.state.mark_task(task_key, "official_extract", "running", payload=payload)
                        article_urls = self.aaai.extract_issue_articles(issue_task)
                        for article_url in tqdm(
                            article_urls,
                            desc=f"{issue_task.year} {issue_task.volume_id}",
                            unit="paper",
                            leave=False,
                        ):
                            article_task_key = f"official:AAAI:article:{article_url}"
                            if self.state.get_task_status(article_task_key) == "success":
                                continue
                            self.state.mark_task(
                                article_task_key,
                                "official_article_extract",
                                "running",
                                payload={"issue_url": issue_task.issue_url, "article_url": article_url},
                            )
                            try:
                                record = self.aaai.extract_article(article_url, issue_task)
                                self.state.upsert_paper(record)
                                self.state.mark_task(
                                    article_task_key,
                                    "official_article_extract",
                                    "success",
                                    payload={"issue_url": issue_task.issue_url, "article_url": article_url},
                                )
                            except Exception as article_exc:
                                self.state.mark_task(
                                    article_task_key,
                                    "official_article_extract",
                                    "failed",
                                    payload={"issue_url": issue_task.issue_url, "article_url": article_url},
                                    last_error=str(article_exc),
                                )
                                logger.warning("Failed AAAI article {}: {}", article_url, article_exc)
                        self.state.mark_task(task_key, "official_extract", "success", payload=payload)
                    except Exception as exc:
                        self.state.mark_task(task_key, "official_extract", "failed", payload=payload, last_error=str(exc))
                        raise
            else:
                raise ValueError(f"Unsupported venue: {venue}")

    def enrich(
        self,
        venues: Iterable[str] | None = None,
        years: Iterable[int] | None = None,
        limit: int | None = None,
    ) -> None:
        papers = self.state.iter_papers_needing_enrichment(venues=venues, years=years, limit=limit)
        logger.info("Enriching {} papers with OpenAlex/Semantic Scholar", len(papers))
        for paper in tqdm(papers, desc="Enrich papers", unit="paper"):
            task_key = f"enrich:{paper.paper_uid}"
            if self.state.get_task_status(task_key) == "success":
                continue
            self.state.mark_task(task_key, "enrich", "running", payload={"paper_uid": paper.paper_uid})
            try:
                enriched = self.openalex.enrich(paper)
                enriched = self.semantic_scholar.enrich(enriched)
                self.state.upsert_paper(enriched)
                self.state.mark_task(task_key, "enrich", "success", payload={"paper_uid": paper.paper_uid})
            except Exception as exc:
                self.state.mark_task(task_key, "enrich", "failed", payload={"paper_uid": paper.paper_uid}, last_error=str(exc))
                logger.warning("Failed to enrich {}: {}", paper.paper_uid, exc)

    def export(self, venues: Iterable[str] | None = None, years: Iterable[int] | None = None) -> None:
        papers = self.state.iter_papers(venues=venues, years=years)
        self.exporter.export(papers)
        self.state.write_coverage_report(self.settings.reports_dir / "coverage_report.csv")

    def run_all(self, venues: Iterable[str], years: Iterable[int], enrich_limit: int | None = None) -> None:
        self.crawl_official(venues, years)
        self.enrich(venues=venues, years=years, limit=enrich_limit)
        self.export(venues=venues, years=years)

    def close(self) -> None:
        self.state.close()
