from __future__ import annotations

import re
from urllib.parse import urlparse


def normalize_title(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^a-z0-9 ]+", "", value)
    return value.strip()


def normalize_whitespace(value: str | None) -> str | None:
    if value is None:
        return None
    return re.sub(r"\s+", " ", value).strip()


def canonicalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    doi = doi.strip()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.I)
    return doi.lower()


def extract_arxiv_id(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    patterns = [
        r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)",
        r"^([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)$",
        r"arxiv:([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, value, flags=re.I)
        if match:
            return re.sub(r"v\d+$", "", match.group(1))
    parsed = urlparse(value)
    if parsed.scheme == "" and re.match(r"^[0-9]{4}\.[0-9]{4,5}(?:v\d+)?$", value):
        return re.sub(r"v\d+$", "", value)
    return None


def build_paper_uid(venue: str, year: int, title: str, doi: str | None, official_url: str | None) -> str:
    if doi:
        return f"doi:{canonicalize_doi(doi)}"
    if official_url:
        return f"url:{official_url.strip().lower()}"
    return f"title:{venue.lower()}:{year}:{normalize_title(title)}"
