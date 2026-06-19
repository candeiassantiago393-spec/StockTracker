"""Read datasheet links from Mouser product pages when the API leaves DataSheetUrl empty."""
from __future__ import annotations

import html
import re
from urllib.parse import urljoin, urlparse

_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-PT,pt;q=0.9,en-US,en;q=0.8",
}

_DATASHEET_LABEL = re.compile(
    r"(?:ficha\s*t[eé]cnica|data\s*sheet|datasheet)",
    re.IGNORECASE,
)
_HREF_RE = re.compile(
    r"""<a\b[^>]*\bhref=["']([^"']+)["'][^>]*>""",
    re.IGNORECASE,
)
_JSON_DATASHEET_RE = re.compile(
    r'"(?:DataSheetUrl|datasheetUrl|dataSheetUrl)"\s*:\s*"([^"]+)"',
    re.IGNORECASE,
)


def _fetch_product_html(product_url: str, *, timeout: int = 15) -> str:
    page_url = str(product_url or "").strip()
    if not page_url or "mouser.com" not in page_url.lower():
        return ""

    try:
        from curl_cffi import requests as curl_requests

        response = curl_requests.get(
            page_url,
            impersonate="chrome120",
            timeout=timeout,
            headers=_BROWSER_HEADERS,
        )
        response.raise_for_status()
        text = response.text or ""
    except Exception:
        try:
            import requests

            response = requests.get(
                page_url,
                timeout=timeout,
                headers=_BROWSER_HEADERS,
            )
            response.raise_for_status()
            text = response.text or ""
        except Exception:
            return ""

    lowered = text.lower()
    if "access to this page has been denied" in lowered or "access denied" in lowered:
        return ""
    return text


def _normalize_href(base_url: str, href: str) -> str:
    raw = html.unescape(str(href or "").strip())
    if not raw or raw.startswith(("#", "javascript:", "mailto:")):
        return ""
    return urljoin(base_url, raw)


def _looks_like_datasheet_href(url: str) -> bool:
    lowered = str(url or "").strip().lower()
    if not lowered.startswith(("http://", "https://")):
        return False
    if "mouser.com/productdetail" in lowered:
        return False
    if any(
        token in lowered
        for token in (
            "mouser.com/datasheet/",
            ".pdf",
            "ti.com/lit/",
            "ti.com/general/docs",
            "vishay.com/doc",
            "download.mikroe.com/",
            "catalogs.kyocera-avx.com/",
            "st.com/resource",
            "onsemi.com/",
            "infineon.com/dgdl",
            "analog.com/media",
            "microchip.com/",
        )
    ):
        return True
    path = urlparse(lowered).path
    return path.endswith(".pdf")


def _pick_best_href(candidates: list[str]) -> str:
    ordered = sorted(
        dict.fromkeys(candidate for candidate in candidates if candidate),
        key=lambda url: (
            0 if "mouser.com/datasheet/" in url.lower() else 1,
            0 if url.lower().endswith(".pdf") else 1,
            len(url),
        ),
    )
    for candidate in ordered:
        if _looks_like_datasheet_href(candidate):
            return candidate
    return ""


def parse_mouser_datasheet_url(html_text: str, *, base_url: str = "") -> str:
    """Extract the datasheet href from a Mouser product page."""
    text = str(html_text or "")
    if not text:
        return ""

    for match in _JSON_DATASHEET_RE.finditer(text):
        href = _normalize_href(base_url, match.group(1))
        if href and _looks_like_datasheet_href(href):
            return href

    label_match = _DATASHEET_LABEL.search(text)
    if label_match:
        window = text[label_match.start() : label_match.start() + 2500]
        candidates = [
            _normalize_href(base_url, href)
            for href in _HREF_RE.findall(window)
        ]
        picked = _pick_best_href(candidates)
        if picked:
            return picked

    candidates = [
        _normalize_href(base_url, href)
        for href in _HREF_RE.findall(text)
        if _looks_like_datasheet_href(_normalize_href(base_url, href))
    ]
    return _pick_best_href(candidates)


def fetch_mouser_datasheet_url(product_url: str, *, timeout: int = 15) -> str:
    """Return datasheet URL shown on the Mouser product page, or empty."""
    page_url = str(product_url or "").strip()
    if not page_url:
        return ""
    html_text = _fetch_product_html(page_url, timeout=timeout)
    if not html_text:
        return ""
    return parse_mouser_datasheet_url(html_text, base_url=page_url)
