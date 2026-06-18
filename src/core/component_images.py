"""Load component catalog images from distributor URLs."""
from __future__ import annotations

import re

from PySide6.QtGui import QPixmap

_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

_MOUSER_SIZE_PATH = re.compile(r"(/images/[^/]+/)(images|sml)(/)", re.IGNORECASE)


def best_catalog_image_url(url: str) -> list[str]:
    """Return candidate URLs, highest resolution first."""
    image_url = str(url or "").strip()
    if not image_url:
        return []

    candidates: list[str] = []
    seen: set[str] = set()

    def add(candidate: str) -> None:
        key = candidate.strip()
        if key and key not in seen:
            seen.add(key)
            candidates.append(key)

    if "mouser.com" in image_url.lower():
        lrg = _MOUSER_SIZE_PATH.sub(r"\1lrg\3", image_url)
        add(lrg)
        add(image_url)
        if "/lrg/" not in image_url.lower():
            add(image_url.replace("/images/", "/lrg/"))
    else:
        add(image_url)

    return candidates


def _looks_like_image(data: bytes) -> bool:
    if len(data) < 4:
        return False
    if data[:3] == b"\xff\xd8\xff":
        return True
    if data[:4] == b"\x89PNG":
        return True
    if data[:3] == b"GIF":
        return True
    if data[:4] == b"RIFF" and len(data) >= 12 and data[8:12] == b"WEBP":
        return True
    if data[:2] == b"BM":
        return True
    return False


def _download_image_bytes(url: str, *, timeout: int = 15) -> bytes | None:
    """Download image bytes; Mouser CDN needs a real browser TLS fingerprint."""
    image_url = str(url or "").strip()
    if not image_url:
        return None

    try:
        from curl_cffi import requests as curl_requests

        response = curl_requests.get(
            image_url,
            impersonate="chrome120",
            timeout=timeout,
            headers=_BROWSER_HEADERS,
        )
        response.raise_for_status()
        data = response.content
        if _looks_like_image(data):
            return data
    except Exception:
        pass

    try:
        import requests

        response = requests.get(
            image_url,
            timeout=timeout,
            headers=_BROWSER_HEADERS,
        )
        response.raise_for_status()
        data = response.content
        if _looks_like_image(data):
            return data
    except Exception:
        return None
    return None


def fetch_pixmap_from_url(url: str, *, timeout: int = 15) -> QPixmap | None:
    """Download the best available catalog image and return a QPixmap."""
    best: QPixmap | None = None
    best_area = 0

    for candidate in best_catalog_image_url(url):
        data = _download_image_bytes(candidate, timeout=timeout)
        if not data:
            continue
        pixmap = QPixmap()
        if not pixmap.loadFromData(data) or pixmap.isNull():
            continue
        area = pixmap.width() * pixmap.height()
        if area > best_area:
            best = pixmap
            best_area = area

    return best
