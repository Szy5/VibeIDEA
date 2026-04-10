from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urljoin

from loguru import logger

from .http import HttpClient
from .models import PaperRecord
from .normalize import build_paper_uid, canonicalize_doi, normalize_title, normalize_whitespace


ARCHIVE_URL = "https://ojs.aaai.org/index.php/AAAI/issue/archive"
TARGET_VOLUMES = {2023: "Vol. 37", 2024: "Vol. 38", 2025: "Vol. 39"}


@dataclass(slots=True)
class IssueTask:
    venue: str
    year: int
    title: str
    issue_url: str
    volume_id: str


class AAAIOJSCrawler:
    def __init__(self, http_client: HttpClient) -> None:
        self.http = http_client

    def discover_issues(self, years: list[int]) -> list[IssueTask]:
        wanted_volumes = {TARGET_VOLUMES[year] for year in years}
        queue = [ARCHIVE_URL]
        visited: set[str] = set()
        discovered: dict[str, IssueTask] = {}

        while queue:
            page_url = queue.pop(0)
            if page_url in visited:
                continue
            visited.add(page_url)
            tree = self.http.get_html_tree(page_url)

            for block in tree.xpath("//div[contains(@class,'obj_issue_summary')]"):
                href = block.xpath(".//a[contains(@class,'title') and contains(@href, '/issue/view/')]/@href")
                title_text = block.xpath(".//a[contains(@class,'title')]/text()")
                series_text = block.xpath(".//div[contains(@class,'series')]/text()")
                href = href[0] if href else None
                title = normalize_whitespace(" ".join([*title_text, *series_text])) or ""
                if not href or not title:
                    continue
                if not any(volume in title for volume in wanted_volumes):
                    continue
                year = next((value for value, volume in TARGET_VOLUMES.items() if volume in title), None)
                if year is None or year not in years:
                    continue
                issue_url = href if href.startswith("http") else urljoin(page_url, href)
                volume_match = re.search(r"Vol\.\s+\d+\s+No\.\s+\d+", title)
                volume_id = volume_match.group(0) if volume_match else title
                discovered[issue_url] = IssueTask(
                    venue="AAAI",
                    year=year,
                    title=title,
                    issue_url=issue_url,
                    volume_id=volume_id,
                )

            for anchor in tree.xpath("//a[contains(@href, '/issue/archive')]"):
                href = anchor.get("href")
                if not href:
                    continue
                next_url = href if href.startswith("http") else urljoin(page_url, href)
                if next_url not in visited and next_url not in queue:
                    queue.append(next_url)

        logger.info("Discovered {} AAAI issues for years {}", len(discovered), years)
        return sorted(discovered.values(), key=lambda item: (item.year, item.issue_url))

    def extract_issue_articles(self, task: IssueTask) -> list[str]:
        tree = self.http.get_html_tree(task.issue_url)
        urls: list[str] = []
        seen: set[str] = set()
        for anchor in tree.xpath("//div[contains(@class,'obj_article_summary')]//h3[contains(@class,'title')]//a"):
            href = anchor.get("href")
            if not href:
                continue
            article_url = href if href.startswith("http") else urljoin(task.issue_url, href)
            if article_url in seen:
                continue
            seen.add(article_url)
            urls.append(article_url)
        logger.info("Discovered {} articles in {}", len(urls), task.issue_url)
        return urls

    def extract_article(self, article_url: str, issue_task: IssueTask) -> PaperRecord:
        tree = self.http.get_html_tree(article_url)
        meta_map = self._collect_meta(tree)
        title = self._first_meta(meta_map, "citation_title") or ""
        authors = meta_map.get("citation_author", [])
        doi = canonicalize_doi(self._first_meta(meta_map, "citation_doi"))
        official_url = self._first_meta(meta_map, "citation_abstract_html_url") or article_url
        track = self._first_meta(meta_map, "DC.Type.articleType") or "unknown"
        abstract = normalize_whitespace(
            " ".join(
                text.strip()
                for text in tree.xpath(
                    "//section[contains(@class,'item') and contains(@class,'abstract')]//text()"
                )
                if text.strip() and text.strip().lower() != "abstract"
            )
        )
        record = PaperRecord(
            paper_uid=build_paper_uid("AAAI", issue_task.year, title, doi, official_url),
            venue="AAAI",
            year=issue_task.year,
            track=track,
            title=title,
            title_normalized=normalize_title(title),
            authors=authors,
            authors_str="",
            author_count=0,
            first_author="",
            abstract=abstract,
            abstract_source="official" if abstract else "none",
            doi=doi,
            official_url=official_url,
            source_official="aaai_ojs",
            volume_id=issue_task.volume_id,
            issue_url=issue_task.issue_url,
            paper_url=official_url,
        )
        record.set_raw_payload(
            {
                "article_url": article_url,
                "issue_url": issue_task.issue_url,
                "title": title,
                "authors": authors,
                "doi": doi,
                "track": track,
                "abstract": abstract,
            }
        )
        record.refresh_derived_fields()
        return record

    @staticmethod
    def _collect_meta(tree) -> dict[str, list[str]]:
        meta_map: dict[str, list[str]] = {}
        for meta in tree.xpath("//meta[@name and @content]"):
            key = meta.get("name")
            content = meta.get("content")
            if not key or content is None:
                continue
            meta_map.setdefault(key, []).append(content)
        return meta_map

    @staticmethod
    def _first_meta(meta_map: dict[str, list[str]], key: str) -> str | None:
        values = meta_map.get(key) or []
        for value in values:
            value = normalize_whitespace(value)
            if value:
                return value
        return None
