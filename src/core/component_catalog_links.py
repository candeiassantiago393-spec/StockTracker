"""Cache distributor product/datasheet URLs for Components (on-demand)."""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Any

from .stock import DATA_DIR

CACHE_DIR = DATA_DIR / "catalog_links"
INDEX_FILE = "_links.json"
_README_NAME = "README.txt"
LINK_TTL_SECONDS = 30 * 24 * 60 * 60
MAX_LINK_ENTRIES = 2000

_lock = threading.Lock()


def _now() -> float:
    return time.time()


def ensure_folder() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    readme = CACHE_DIR / _README_NAME
    if not readme.exists():
        readme.write_text(
            "Catalog link cache\n"
            "==================\n\n"
            "Product and datasheet URLs from distributor APIs.\n"
            "Filled only when you view a component — not from the full Excel scan.\n",
            encoding="utf-8",
        )
    return CACHE_DIR


def _load_index() -> dict[str, dict[str, Any]]:
    path = ensure_folder() / INDEX_FILE
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _save_index(index: dict[str, dict[str, Any]]) -> None:
    try:
        (ensure_folder() / INDEX_FILE).write_text(
            json.dumps(index, indent=2),
            encoding="utf-8",
        )
    except OSError:
        pass


def _prune_index(index: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    now = _now()
    kept: dict[str, dict[str, Any]] = {}
    for key, entry in index.items():
        age = now - float(entry.get("cached_at", 0))
        if age <= LINK_TTL_SECONDS and (
            str(entry.get("product_url", "")).strip()
            or str(entry.get("datasheet_url", "")).strip()
            or str(entry.get("image_url", "")).strip()
        ):
            kept[key] = entry
    if len(kept) <= MAX_LINK_ENTRIES:
        return kept
    ordered = sorted(
        kept.items(),
        key=lambda item: float(item[1].get("last_access", item[1].get("cached_at", 0))),
    )
    return dict(ordered[-MAX_LINK_ENTRIES:])


def get_cached_links(cache_key: str) -> dict[str, str] | None:
    key = str(cache_key or "").strip().upper()
    if not key:
        return None
    with _lock:
        index = _load_index()
        entry = index.get(key)
        if not entry:
            return None
        age = _now() - float(entry.get("cached_at", 0))
        if age > LINK_TTL_SECONDS:
            index.pop(key, None)
            _save_index(index)
            return None
        entry["last_access"] = _now()
        index[key] = entry
        _save_index(_prune_index(index))
        return {
            "product_url": str(entry.get("product_url", "")).strip(),
            "datasheet_url": str(entry.get("datasheet_url", "")).strip(),
            "image_url": str(entry.get("image_url", "")).strip(),
            "manufacturer": str(entry.get("manufacturer", "")).strip(),
            "manufacturer_part_number": str(
                entry.get("manufacturer_part_number", "")
            ).strip(),
        }


def store_links(cache_key: str, part: dict[str, Any]) -> dict[str, str]:
    from .component_datasheet_urls import resolve_datasheet_url, validated_datasheet_url

    key = str(cache_key or "").strip().upper()
    product_url = str(
        part.get("product_url")
        or part.get("ProductDetailUrl")
        or ""
    ).strip()
    datasheet_url = str(
        part.get("datasheet_url")
        or part.get("DataSheetUrl")
        or ""
    ).strip()
    if not datasheet_url:
        datasheet_url = resolve_datasheet_url(part)
    else:
        datasheet_url = validated_datasheet_url(datasheet_url) or resolve_datasheet_url(
            part
        )
    if not key:
        return {
            "product_url": product_url,
            "datasheet_url": datasheet_url,
            "image_url": str(part.get("image_url", "")).strip(),
        }

    image_url = str(part.get("image_url", "")).strip()
    manufacturer = str(
        part.get("manufacturer") or part.get("Manufacturer") or ""
    ).strip()
    manufacturer_part_number = str(
        part.get("manufacturer_part_number")
        or part.get("ManufacturerPartNumber")
        or ""
    ).strip()
    now = _now()
    with _lock:
        index = _load_index()
        index[key] = {
            "product_url": product_url,
            "datasheet_url": datasheet_url,
            "image_url": image_url,
            "manufacturer": manufacturer,
            "manufacturer_part_number": manufacturer_part_number,
            "cached_at": now,
            "last_access": now,
        }
        _save_index(_prune_index(index))
    return {
        "product_url": product_url,
        "datasheet_url": datasheet_url,
        "image_url": image_url,
    }
