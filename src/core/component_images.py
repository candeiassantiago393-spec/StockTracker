"""Load component catalog images from distributor URLs."""
from __future__ import annotations

import requests
from PySide6.QtGui import QPixmap


def fetch_pixmap_from_url(url: str, *, timeout: int = 12) -> QPixmap | None:
    """Download an image URL and return a QPixmap, or None on failure."""
    image_url = str(url or "").strip()
    if not image_url:
        return None
    try:
        response = requests.get(image_url, timeout=timeout)
        response.raise_for_status()
        pixmap = QPixmap()
        if pixmap.loadFromData(response.content):
            return pixmap
    except Exception:
        return None
    return None
