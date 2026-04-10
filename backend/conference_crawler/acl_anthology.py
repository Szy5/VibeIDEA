from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin

from lxml import etree
from loguru import logger

from .http import HttpClient
from .models import PaperRecord
from .normalize import build_paper_uid, canonicalize_doi, normalize_title


MODS_NS = {"mods": "http://www.loc.gov/mods/v3"}
VENUE_URLS = {
    "ACL": "https://aclanthology.org/venues/acl/",
    "EMNLP": "https://aclanthology.org/venues/emnlp/",
}


@dataclass(slots=True)
class VolumeTask:
    venue: str
    year: int
    track: str
    volume_url: str
    xml_url: str
    title: str


class ACLAnthologyCrawler:
    def __init__(self, http_client: HttpClient) -> None:
        self.http = http_client

    def discover_volumes(self, venue: str, years: list[int]) -> list[VolumeTask]:
        venue = venue.upper()
        venue_url = VENUE_URLS[venue]
        tree = self.http.get_html_tree(venue_url)
        volume_tasks: list[VolumeTask] = []
        seen: set[str] = set()
        for anchor in tree.xpath("//a[starts-with(@href, '/volumes/')]"):
            href = anchor.get("href")
            text = " ".join(anchor.text_content().split())
            if not href or not text:
                continue
            slug = href.strip("/").split("/")[-1]
            try:
                year = int(slug.split(".")[0])
            except (ValueError, IndexError):
                continue
            if year not in years:
                continue
            if venue.lower() not in slug:
                continue
            if slug in seen:
                continue
            seen.add(slug)
            volume_url = urljoin("https://aclanthology.org", href)
            track = slug.split(".", 1)[1] if "." in slug else slug
            track = track.replace(f"{venue.lower()}-", "", 1)
            xml_url = volume_url.rstrip("/") + ".xml"
            volume_tasks.append(
                VolumeTask(
                    venue=venue,
                    year=year,
                    track=track,
                    volume_url=volume_url,
                    xml_url=xml_url,
                    title=text,
                )
            )
        logger.info("Discovered {} {} volumes for years {}", len(volume_tasks), venue, years)
        return sorted(volume_tasks, key=lambda item: (item.year, item.track))

    def extract_volume(self, task: VolumeTask) -> list[PaperRecord]:
        root = self.http.get_xml_root(task.xml_url)
        records: list[PaperRecord] = []
        for mods in root.xpath("//mods:mods", namespaces=MODS_NS):
            paper_url = self._extract_text(mods.xpath("./mods:location/mods:url/text()", namespaces=MODS_NS))
            doi = canonicalize_doi(self._extract_text(mods.xpath("./mods:identifier[@type='doi']/text()", namespaces=MODS_NS)))
            if not paper_url or "/volumes/" in paper_url:
                continue
            title = self._extract_text(mods.xpath("./mods:titleInfo/mods:title/text()", namespaces=MODS_NS)) or ""
            authors = self._extract_authors(mods)
            if not authors or paper_url.rstrip("/").endswith(".0"):
                continue
            record = PaperRecord(
                paper_uid=build_paper_uid(task.venue, task.year, title, doi, paper_url),
                venue=task.venue,
                year=task.year,
                track=task.track,
                title=title,
                title_normalized=normalize_title(title),
                authors=authors,
                authors_str="",
                author_count=0,
                first_author="",
                doi=doi,
                official_url=paper_url,
                source_official="acl_anthology",
                volume_id=task.volume_url.rstrip("/").split("/")[-1],
                issue_url=task.volume_url,
                paper_url=paper_url,
            )
            record.set_raw_payload(
                {
                    "volume_url": task.volume_url,
                    "xml_url": task.xml_url,
                    "mods_id": mods.get("ID"),
                    "title": title,
                    "authors": authors,
                    "doi": doi,
                    "paper_url": paper_url,
                }
            )
            record.refresh_derived_fields()
            records.append(record)
        logger.info("Extracted {} papers from {}", len(records), task.xml_url)
        return records

    @staticmethod
    def _extract_text(values: list[str]) -> str | None:
        for value in values:
            value = " ".join(value.split())
            if value:
                return value
        return None

    def _extract_authors(self, mods: etree._Element) -> list[str]:
        authors: list[str] = []
        for name_node in mods.xpath(
            "./mods:name[mods:role/mods:roleTerm='author']",
            namespaces=MODS_NS,
        ):
            given = name_node.xpath("./mods:namePart[@type='given']/text()", namespaces=MODS_NS)
            family = name_node.xpath("./mods:namePart[@type='family']/text()", namespaces=MODS_NS)
            if given or family:
                authors.append(" ".join([*given, *family]).strip())
        return authors
