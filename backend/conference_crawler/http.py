from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import requests
from lxml import etree, html
from requests.adapters import HTTPAdapter, Retry
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter


TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


class TransientHttpError(RuntimeError):
    """Raised when a request should be retried."""


@dataclass(slots=True)
class HttpClient:
    user_agent: str
    timeout: int
    min_interval_by_host: dict[str, float]
    _session: requests.Session = field(init=False, repr=False)
    _last_request_at: dict[str, float] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._session = requests.Session()
        retry_policy = Retry(
            total=0,
            backoff_factor=0,
            status_forcelist=[],
            allowed_methods=None,
        )
        adapter = HTTPAdapter(max_retries=retry_policy, pool_connections=10, pool_maxsize=10)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)
        self._session.headers.update({"User-Agent": self.user_agent})
        self._last_request_at: dict[str, float] = defaultdict(float)

    def _respect_rate_limit(self, url: str) -> None:
        host = urlparse(url).netloc
        min_interval = self.min_interval_by_host.get(host, 0.0)
        if min_interval <= 0:
            return
        elapsed = time.monotonic() - self._last_request_at[host]
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self._last_request_at[host] = time.monotonic()

    @retry(
        retry=retry_if_exception_type((requests.RequestException, TransientHttpError)),
        wait=wait_exponential_jitter(initial=1, max=60),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        self._respect_rate_limit(url)
        response = self._session.request(method, url, timeout=self.timeout, **kwargs)
        if response.status_code in TRANSIENT_STATUS_CODES:
            raise TransientHttpError(f"{response.status_code} for {url}")
        response.raise_for_status()
        return response

    def get_text(self, url: str, **kwargs: Any) -> str:
        return self.request("GET", url, **kwargs).text

    def get_json(self, url: str, **kwargs: Any) -> dict[str, Any]:
        return self.request("GET", url, **kwargs).json()

    def get_html_tree(self, url: str, **kwargs: Any) -> html.HtmlElement:
        return html.fromstring(self.get_text(url, **kwargs))

    def get_xml_root(self, url: str, **kwargs: Any) -> etree._Element:
        content = self.request("GET", url, **kwargs).content
        return etree.fromstring(content)
