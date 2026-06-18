"""On-demand disk cache for component catalog images (bounded for large inventories)."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Callable

from .stock import DATA_DIR

CACHE_DIR = DATA_DIR / "component_image_cache"
INDEX_FILE = "_index.json"
_README_NAME = "README.txt"

# Large inventories: only cache images actually viewed; cap disk and entry count.
MAX_CACHE_ENTRIES = 800
MAX_CACHE_BYTES = 150 * 1024 * 1024  # 150 MB
CACHE_TTL_SECONDS = 90 * 24 * 60 * 60  # 90 days
URL_TTL_SECONDS = 30 * 24 * 60 * 60  # re-check distributor URL monthly

_SAFE_REF = re.compile(r"[^\w\-.]+", re.ASCII)


def _now() -> float:
    return time.time()


def cache_key_for_ref(lookup_ref: str) -> str:
    """Filesystem-safe key from supplier or manufacturer reference."""
    norm = str(lookup_ref or "").strip().upper()
    if not norm:
        return ""
    safe = _SAFE_REF.sub("_", norm).strip("._")
    return safe[:120] if safe else ""


class ComponentImageCache:
    """Bounded LRU cache: on-demand only, never preloads the whole Excel inventory."""

    def __init__(self, folder: Path | None = None) -> None:
        self.folder = Path(folder) if folder else CACHE_DIR
        self._index: dict[str, dict] = {}

    def ensure_folder(self) -> Path:
        self.folder.mkdir(parents=True, exist_ok=True)
        readme = self.folder / _README_NAME
        if not readme.exists():
            readme.write_text(
                "Component catalog image cache\n"
                "=============================\n\n"
                "Images are saved here only when you open a component in the app.\n"
                "The Excel inventory is never scanned to fill this folder.\n\n"
                f"Limits: up to {MAX_CACHE_ENTRIES} images, "
                f"{MAX_CACHE_BYTES // (1024 * 1024)} MB total, "
                f"{CACHE_TTL_SECONDS // (24 * 3600)} days per file.\n"
                "Oldest entries are removed automatically when limits are exceeded.\n",
                encoding="utf-8",
            )
        self._load_index()
        return self.folder

    def _index_path(self) -> Path:
        return self.folder / INDEX_FILE

    def _load_index(self) -> None:
        path = self._index_path()
        if not path.is_file():
            self._index = {}
            return
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            self._index = raw if isinstance(raw, dict) else {}
        except (OSError, json.JSONDecodeError):
            self._index = {}

    def _save_index(self) -> None:
        try:
            self._index_path().write_text(
                json.dumps(self._index, indent=2),
                encoding="utf-8",
            )
        except OSError:
            pass

    def _entry_valid(self, entry: dict) -> bool:
        if not entry:
            return False
        age = _now() - float(entry.get("cached_at", 0))
        if age > CACHE_TTL_SECONDS:
            return False
        filename = str(entry.get("file", "")).strip()
        if not filename:
            return False
        path = self.folder / filename
        return path.is_file() and path.stat().st_size > 0

    def _url_still_fresh(self, entry: dict) -> bool:
        age = _now() - float(entry.get("url_at", entry.get("cached_at", 0)))
        return bool(entry.get("url")) and age <= URL_TTL_SECONDS

    def _touch(self, key: str) -> None:
        entry = self._index.get(key)
        if not entry:
            return
        entry["last_access"] = _now()
        path = self.folder / str(entry.get("file", ""))
        if path.is_file():
            try:
                path.touch()
            except OSError:
                pass
        self._save_index()

    def read_bytes(self, lookup_ref: str) -> bytes | None:
        """Return cached image bytes if present and valid."""
        key = cache_key_for_ref(lookup_ref)
        if not key:
            return None
        self.ensure_folder()
        entry = self._index.get(key)
        if not entry or not self._entry_valid(entry):
            self._remove_entry(key)
            return None
        path = self.folder / str(entry["file"])
        try:
            data = path.read_bytes()
        except OSError:
            self._remove_entry(key)
            return None
        if not data:
            self._remove_entry(key)
            return None
        self._touch(key)
        return data

    def cached_image_url(self, lookup_ref: str) -> str:
        """Return a still-fresh distributor URL from cache (skips API lookup)."""
        key = cache_key_for_ref(lookup_ref)
        if not key:
            return ""
        self.ensure_folder()
        entry = self._index.get(key)
        if entry and self._url_still_fresh(entry):
            return str(entry.get("url", "")).strip()
        return ""

    def write_bytes(
        self,
        lookup_ref: str,
        data: bytes,
        *,
        image_url: str = "",
        extension: str = ".bin",
    ) -> bool:
        key = cache_key_for_ref(lookup_ref)
        if not key or not data:
            return False
        self.ensure_folder()
        ext = extension if extension.startswith(".") else f".{extension}"
        if ext == ".bin":
            ext = _extension_for_bytes(data)
        filename = f"{key}{ext}"
        path = self.folder / filename
        old_file = ""
        entry = self._index.get(key)
        if entry:
            old_file = str(entry.get("file", "")).strip()

        try:
            path.write_bytes(data)
        except OSError:
            return False

        if old_file and old_file != filename:
            old_path = self.folder / old_file
            if old_path.is_file():
                try:
                    old_path.unlink()
                except OSError:
                    pass

        now = _now()
        self._index[key] = {
            "file": filename,
            "url": str(image_url or "").strip(),
            "cached_at": now,
            "url_at": now if image_url else float(entry.get("url_at", 0) if entry else 0),
            "last_access": now,
            "size": len(data),
        }
        self._save_index()
        self._enforce_limits()
        return True

    def _remove_entry(self, key: str) -> None:
        entry = self._index.pop(key, None)
        if not entry:
            return
        path = self.folder / str(entry.get("file", ""))
        if path.is_file():
            try:
                path.unlink()
            except OSError:
                pass
        self._save_index()

    def _enforce_limits(self) -> None:
        self._purge_expired()
        entries: list[tuple[str, dict]] = [
            (key, entry) for key, entry in self._index.items() if entry.get("file")
        ]
        if not entries:
            return

        def sort_key(item: tuple[str, dict]) -> float:
            return float(item[1].get("last_access", item[1].get("cached_at", 0)))

        total_bytes = 0
        file_sizes: dict[str, int] = {}
        for key, entry in entries:
            path = self.folder / str(entry.get("file", ""))
            if not path.is_file():
                self._index.pop(key, None)
                continue
            size = path.stat().st_size
            file_sizes[key] = size
            total_bytes += size

        entries.sort(key=sort_key)

        while entries and (
            len(entries) > MAX_CACHE_ENTRIES or total_bytes > MAX_CACHE_BYTES
        ):
            key, _entry = entries.pop(0)
            total_bytes -= file_sizes.get(key, 0)
            self._remove_entry(key)

    def _purge_expired(self) -> None:
        expired = [
            key
            for key, entry in list(self._index.items())
            if not self._entry_valid(entry)
        ]
        for key in expired:
            self._remove_entry(key)

    def clear_all(self) -> int:
        """Remove all cached images (for maintenance). Returns files removed."""
        self.ensure_folder()
        count = 0
        for key in list(self._index.keys()):
            self._remove_entry(key)
            count += 1
        for path in self.folder.glob("*"):
            if path.name in {_README_NAME, INDEX_FILE}:
                continue
            if path.is_file():
                try:
                    path.unlink()
                    count += 1
                except OSError:
                    pass
        self._index = {}
        self._save_index()
        return count

    def stats(self) -> dict[str, int]:
        self.ensure_folder()
        self._purge_expired()
        total_bytes = 0
        for entry in self._index.values():
            path = self.folder / str(entry.get("file", ""))
            if path.is_file():
                total_bytes += path.stat().st_size
        return {
            "entries": len(self._index),
            "bytes": total_bytes,
            "max_entries": MAX_CACHE_ENTRIES,
            "max_bytes": MAX_CACHE_BYTES,
        }


def _extension_for_bytes(data: bytes) -> str:
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if data[:4] == b"\x89PNG":
        return ".png"
    if data[:3] == b"GIF":
        return ".gif"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    if data[:2] == b"BM":
        return ".bmp"
    return ".img"


def resolve_catalog_image(
    lookup_ref: str,
    fetch_image_url: Callable[[], str],
    download_bytes: Callable[[str], bytes | None],
) -> tuple[bytes | None, str]:
    """
    Resolve image bytes with cache-first strategy.

    Returns (image_bytes, source_url_used).
    Never scans Excel — only uses lookup_ref for the current selection.
    """
    cache = ComponentImageCache()
    cache.ensure_folder()

    cached = cache.read_bytes(lookup_ref)
    if cached:
        entry = cache._index.get(cache_key_for_ref(lookup_ref), {})
        return cached, str(entry.get("url", ""))

    image_url = cache.cached_image_url(lookup_ref) or fetch_image_url().strip()
    if not image_url:
        return None, ""

    data = download_bytes(image_url)
    if not data:
        return None, image_url

    cache.write_bytes(lookup_ref, data, image_url=image_url)
    return data, image_url
