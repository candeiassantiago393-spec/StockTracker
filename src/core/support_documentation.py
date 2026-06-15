"""Support documentation folder — datasheets and files for equipments."""
from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .stock import DATA_DIR

SUPPORT_DOCS_DIR = DATA_DIR / "support_documentation"
_README_NAME = "README.txt"


@dataclass(frozen=True)
class SupportDocument:
    path: Path
    name: str
    size_bytes: int
    modified: datetime


class SupportDocumentation:
    """Manage the local support-documentation folder under data/."""

    def __init__(self, folder: Path | None = None) -> None:
        self.folder = Path(folder) if folder else SUPPORT_DOCS_DIR

    def ensure_folder(self) -> Path:
        self.folder.mkdir(parents=True, exist_ok=True)
        readme = self.folder / _README_NAME
        if not readme.exists():
            readme.write_text(
                "Support documentation folder\n"
                "============================\n\n"
                "Place datasheets, manuals and other support files here.\n"
                "Use the Equipments page in Stock Tracker to search, open or add files.\n",
                encoding="utf-8",
            )
        return self.folder

    def list_documents(self, query: str = "") -> list[SupportDocument]:
        self.ensure_folder()
        needle = query.strip().lower()
        documents: list[SupportDocument] = []
        for path in sorted(self.folder.iterdir(), key=lambda p: p.name.lower()):
            if not path.is_file() or path.name == _README_NAME:
                continue
            if needle and needle not in path.name.lower():
                continue
            stat = path.stat()
            documents.append(
                SupportDocument(
                    path=path,
                    name=path.name,
                    size_bytes=stat.st_size,
                    modified=datetime.fromtimestamp(stat.st_mtime),
                )
            )
        return documents

    def resolve_path(self, filename: str) -> Path | None:
        """Return path to a file in the support folder, or None if missing."""
        name = str(filename).strip()
        if not name:
            return None
        self.ensure_folder()
        path = self.folder / name
        if path.is_file():
            return path
        return None

    def document_for_filename(self, filename: str) -> SupportDocument | None:
        path = self.resolve_path(filename)
        if path is None:
            return None
        stat = path.stat()
        return SupportDocument(
            path=path,
            name=path.name,
            size_bytes=stat.st_size,
            modified=datetime.fromtimestamp(stat.st_mtime),
        )

    def add_document(self, source: Path) -> tuple[bool, str]:
        source = Path(source)
        if not source.is_file():
            return False, "Selected path is not a file."

        self.ensure_folder()
        target = self.folder / source.name
        if target.exists():
            stem = source.stem
            suffix = source.suffix
            index = 1
            while target.exists():
                target = self.folder / f"{stem}_{index}{suffix}"
                index += 1

        try:
            shutil.copy2(source, target)
        except OSError as exc:
            return False, f"Could not copy file: {exc}"

        return True, f"Added {target.name}."

    def open_folder(self) -> tuple[bool, str]:
        folder = self.ensure_folder()
        try:
            os.startfile(str(folder))
        except OSError as exc:
            return False, f"Could not open folder: {exc}"
        return True, f"Opened {folder}."

    def open_document(self, document: SupportDocument | Path) -> tuple[bool, str]:
        path = document if isinstance(document, Path) else document.path
        if not path.is_file():
            return False, "File not found."
        try:
            os.startfile(str(path))
        except OSError as exc:
            return False, f"Could not open file: {exc}"
        return True, f"Opened {path.name}."
