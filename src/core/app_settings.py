"""Persistent app settings (JSON in data/)."""
from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SETTINGS_FILE = DATA_DIR / "app_settings.json"
DEFAULT_LOW_STOCK_THRESHOLD = 10


def _load() -> dict:
    if not SETTINGS_FILE.is_file():
        return {}
    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _save(data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(
        json.dumps(data, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def get_low_stock_threshold() -> int:
    raw = _load().get("low_stock_threshold", DEFAULT_LOW_STOCK_THRESHOLD)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = DEFAULT_LOW_STOCK_THRESHOLD
    return max(0, value)


def set_low_stock_threshold(value: int) -> int:
    limit = max(0, int(value))
    data = _load()
    data["low_stock_threshold"] = limit
    _save(data)
    return limit
