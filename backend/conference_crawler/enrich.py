from __future__ import annotations

from typing import Any

from loguru import logger

from .http import HttpClient
from .models import PaperRecord
from .normalize import canonicalize_doi, extract_arxiv_id, normalize_title, normalize_whitespace


class OpenAlexEnricher:
    def __init__(self, http_client: HttpClient, api_key: str | None = None) -> None:
        self.http = http_client
        self.api_key = api_key

    def enrich(self, paper: PaperRecord) -> PaperRecord:
        work = self._find_work(paper)
        if not work:
            return paper

        abstract = self._reconstruct_abstract(work.get("abstract_inverted_index"))
        if abstract and not paper.abstract:
            paper.abstract = normalize_whitespace(abstract)
            paper.abstract_source = "openalex"
        if not paper.openalex_id:
            paper.openalex_id = work.get("id")
        if not paper.arxiv_id:
            ids = work.get("ids") or {}
            paper.arxiv_id = extract_arxiv_id(ids.get("arxiv"))
        if paper.abstract or paper.arxiv_id:
            paper.source_enrich = "openalex"
        paper.refresh_derived_fields()
        return paper

    def _find_work(self, paper: PaperRecord) -> dict[str, Any] | None:
        params_base = {"per-page": 5}
        if self.api_key:
            params_base["api_key"] = self.api_key

        if paper.doi:
            doi = canonicalize_doi(paper.doi)
            for doi_value in [doi, f"https://doi.org/{doi}"]:
                params = dict(params_base)
                params["filter"] = f"doi:{doi_value}"
                payload = self.http.get_json("https://api.openalex.org/works", params=params)
                results = payload.get("results") or []
                if results:
                    return results[0]

        params = dict(params_base)
        params["search"] = paper.title
        payload = self.http.get_json("https://api.openalex.org/works", params=params)
        for candidate in payload.get("results") or []:
            if self._is_candidate_match(candidate, paper):
                return candidate
        return None

    @staticmethod
    def _is_candidate_match(candidate: dict[str, Any], paper: PaperRecord) -> bool:
        candidate_year = candidate.get("publication_year")
        if candidate_year and int(candidate_year) != int(paper.year):
            return False
        candidate_title = normalize_title(candidate.get("title") or "")
        return candidate_title == paper.title_normalized

    @staticmethod
    def _reconstruct_abstract(abstract_index: dict[str, list[int]] | None) -> str | None:
        if not abstract_index:
            return None
        max_position = max((max(positions) for positions in abstract_index.values() if positions), default=-1)
        if max_position < 0:
            return None
        tokens = [""] * (max_position + 1)
        for word, positions in abstract_index.items():
            for position in positions:
                tokens[position] = word
        return " ".join(token for token in tokens if token)


class SemanticScholarEnricher:
    def __init__(self, http_client: HttpClient, api_key: str | None = None) -> None:
        self.http = http_client
        self.api_key = api_key

    def enrich(self, paper: PaperRecord) -> PaperRecord:
        if not self.api_key:
            return paper
        if paper.abstract and paper.arxiv_id:
            return paper
        candidate = self._find_paper(paper)
        if not candidate:
            return paper

        if not paper.abstract and candidate.get("abstract"):
            paper.abstract = normalize_whitespace(candidate.get("abstract"))
            paper.abstract_source = "semantic_scholar"
        external_ids = candidate.get("externalIds") or {}
        if not paper.arxiv_id:
            paper.arxiv_id = extract_arxiv_id(external_ids.get("ArXiv"))
        if not paper.semantic_scholar_id:
            paper.semantic_scholar_id = candidate.get("paperId")
        if paper.abstract or paper.arxiv_id:
            paper.source_enrich = "semantic_scholar"
        paper.refresh_derived_fields()
        return paper

    def _find_paper(self, paper: PaperRecord) -> dict[str, Any] | None:
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        fields = "title,abstract,authors,externalIds,year,url"
        if paper.doi:
            doi = canonicalize_doi(paper.doi)
            url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
            try:
                return self.http.get_json(url, headers=headers, params={"fields": fields})
            except Exception as exc:
                logger.debug("Semantic Scholar DOI lookup failed for {}: {}", paper.paper_uid, exc)
        payload = self.http.get_json(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            headers=headers,
            params={"query": paper.title, "fields": fields, "limit": 5},
        )
        for candidate in payload.get("data") or []:
            if normalize_title(candidate.get("title") or "") == paper.title_normalized and int(candidate.get("year") or 0) == int(paper.year):
                return candidate
        return None
