"""Per-equipment folders under data/equipments/{id}/ for datasheets and images."""
from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .stock import DATA_DIR

EQUIPMENTS_DIR = DATA_DIR / "equipments"
_README_NAME = "README.txt"
_IMAGE_BASENAME = "image"
_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}


def is_image_file(path: Path | str) -> bool:
    return Path(path).suffix.lower() in _IMAGE_SUFFIXES


@dataclass(frozen=True)
class SupportDocument:
    path: Path
    name: str
    size_bytes: int
    modified: datetime
    equipment_id: str = ""


class EquipmentStorage:
    """One folder per equipment: datasheet + image live together."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root) if root else EQUIPMENTS_DIR

    def ensure_root(self) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        readme = self.root / _README_NAME
        if not readme.exists():
            readme.write_text(
                "Equipment folders\n"
                "=================\n\n"
                "Each subfolder is one equipment (folder name = Excel ID).\n"
                "Store the datasheet and image there; the app links by filename.\n\n"
                "Typical layout:\n"
                "  3/\n"
                "    DS_Fluke_87V.pdf\n"
                "    image.jpg\n",
                encoding="utf-8",
            )
        return self.root

    @staticmethod
    def _equipment_id_str(equipment_id: str | int) -> str:
        text = str(equipment_id or "").strip()
        return text or "unknown"

    def equipment_dir(self, equipment_id: str | int) -> Path:
        return self.ensure_root() / self._equipment_id_str(equipment_id)

    def ensure_equipment_dir(self, equipment_id: str | int) -> Path:
        folder = self.equipment_dir(equipment_id)
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    @staticmethod
    def _is_reserved_name(name: str) -> bool:
        lowered = name.lower()
        return lowered == _README_NAME.lower() or lowered.startswith(
            f"{_IMAGE_BASENAME}."
        )

    def resolve_datasheet(
        self, equipment_id: str | int, filename: str
    ) -> Path | None:
        name = str(filename).strip()
        if not name:
            return None
        per_eq = self.equipment_dir(equipment_id) / name
        if per_eq.is_file():
            return per_eq
        return None

    def resolve_image(self, equipment_id: str | int, filename: str) -> Path | None:
        name = str(filename).strip()
        if not name:
            return None
        per_eq = self.equipment_dir(equipment_id) / name
        if per_eq.is_file():
            return per_eq
        return None

    def document_for_datasheet(
        self, equipment_id: str | int, filename: str
    ) -> SupportDocument | None:
        path = self.resolve_datasheet(equipment_id, filename)
        if path is None:
            return None
        stat = path.stat()
        return SupportDocument(
            path=path,
            name=path.name,
            size_bytes=stat.st_size,
            modified=datetime.fromtimestamp(stat.st_mtime),
            equipment_id=self._equipment_id_str(equipment_id),
        )

    def install_datasheet(
        self, source: Path, equipment_id: str | int
    ) -> tuple[bool, str]:
        source = Path(source)
        if not source.is_file():
            return False, "Selected path is not a file."

        folder = self.ensure_equipment_dir(equipment_id)
        target = folder / source.name
        if target.exists():
            stem = source.stem
            suffix = source.suffix
            index = 1
            while target.exists():
                target = folder / f"{stem}_{index}{suffix}"
                index += 1

        try:
            shutil.copy2(source, target)
        except OSError as exc:
            return False, f"Could not copy datasheet: {exc}"

        return True, target.name

    def add_image(
        self, source: Path, equipment_id: str | int
    ) -> tuple[bool, str]:
        source = Path(source)
        if not source.is_file():
            return False, "Selected path is not a file."
        if not is_image_file(source):
            return False, "File is not a supported image (PNG, JPG, WEBP, BMP, GIF)."

        folder = self.ensure_equipment_dir(equipment_id)
        for existing in folder.iterdir():
            if existing.is_file() and existing.stem.lower() == _IMAGE_BASENAME:
                try:
                    existing.unlink()
                except OSError:
                    pass

        target = folder / f"{_IMAGE_BASENAME}{source.suffix.lower()}"
        try:
            shutil.copy2(source, target)
        except OSError as exc:
            return False, f"Could not copy image: {exc}"

        return True, target.name

    def remove_image_file(
        self, equipment_id: str | int, filename: str
    ) -> tuple[bool, str]:
        name = str(filename).strip()
        if not name:
            return True, ""
        path = self.resolve_image(equipment_id, name)
        if path is None:
            return True, ""
        try:
            path.unlink()
        except OSError as exc:
            return False, f"Could not remove image file: {exc}"
        return True, name

    def list_documents(self, query: str = "") -> list[SupportDocument]:
        """All support files across equipment folders."""
        needle = query.strip().lower()
        documents: list[SupportDocument] = []
        seen: set[str] = set()

        def add_path(path: Path, equipment_id: str = "") -> None:
            key = str(path.resolve()).lower()
            if key in seen:
                return
            if not path.is_file() or path.name == _README_NAME:
                return
            if self._is_reserved_name(path.name):
                return
            if needle and needle not in path.name.lower():
                return
            seen.add(key)
            stat = path.stat()
            documents.append(
                SupportDocument(
                    path=path,
                    name=path.name,
                    size_bytes=stat.st_size,
                    modified=datetime.fromtimestamp(stat.st_mtime),
                    equipment_id=equipment_id,
                )
            )

        self.ensure_root()
        for child in sorted(self.root.iterdir(), key=lambda p: p.name.lower()):
            if not child.is_dir():
                continue
            eq_id = child.name
            for path in sorted(child.iterdir(), key=lambda p: p.name.lower()):
                add_path(path, eq_id)

        documents.sort(key=lambda doc: doc.name.lower())
        return documents

    def open_equipment_folder(
        self, equipment_id: str | int | None = None
    ) -> tuple[bool, str]:
        if equipment_id is not None and str(equipment_id).strip():
            folder = self.ensure_equipment_dir(equipment_id)
        else:
            folder = self.ensure_root()
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
