"""Automatic Excel backups before save (bounded retention)."""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from .stock import DATA_DIR

BACKUP_DIR = DATA_DIR / "backups"
MAX_BACKUP_FILES = 20
_README_NAME = "README.txt"


def _backup_name_for(source: Path) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    stem = source.stem or "stock"
    if stem.lower() == "stock":
        return f"stock_{stamp}.xlsx"
    return f"{stem}_{stamp}.xlsx"


def ensure_backup_folder() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    readme = BACKUP_DIR / _README_NAME
    if not readme.exists():
        readme.write_text(
            "Excel automatic backups\n"
            "=======================\n\n"
            "Before each save, the app copies stock.xlsx here.\n"
            f"Only the last {MAX_BACKUP_FILES} backups are kept.\n"
            "Restore: close Excel, copy a backup over data/stock.xlsx\n",
            encoding="utf-8",
        )
    return BACKUP_DIR


def prune_backups(folder: Path | None = None, *, max_files: int = MAX_BACKUP_FILES) -> int:
    """Delete oldest backups beyond max_files. Returns number removed."""
    target = Path(folder) if folder else BACKUP_DIR
    if not target.is_dir():
        return 0
    files = sorted(
        (p for p in target.glob("*.xlsx") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
    )
    removed = 0
    while len(files) > max_files:
        oldest = files.pop(0)
        try:
            oldest.unlink()
            removed += 1
        except OSError:
            break
    return removed


def backup_excel_file(
    excel_path: Path,
    *,
    max_backups: int = MAX_BACKUP_FILES,
) -> Path | None:
    """
    Copy excel_path into data/backups/ before overwriting.

    Returns backup path on success, None if skipped or failed.
    Failure does not raise — callers should still attempt save.
    """
    source = Path(excel_path)
    if not source.is_file():
        return None
    try:
        if source.stat().st_size <= 0:
            return None
    except OSError:
        return None

    folder = ensure_backup_folder()
    destination = folder / _backup_name_for(source)

    try:
        shutil.copy2(source, destination)
    except OSError:
        return None

    prune_backups(folder, max_files=max_backups)
    return destination
