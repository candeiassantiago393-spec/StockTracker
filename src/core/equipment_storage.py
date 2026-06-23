"""Per-equipment folders under data/equipments/{id}-{name}/ for datasheets and images."""
from __future__ import annotations

import os
import re
import shutil
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .stock import DATA_DIR

EQUIPMENTS_DIR = DATA_DIR / "equipments"
_README_NAME = "README.txt"
_IMAGE_BASENAME = "image"
_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
_INVALID_FOLDER_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]+')


def is_image_file(path: Path | str) -> bool:
    return Path(path).suffix.lower() in _IMAGE_SUFFIXES


def slugify_equipment_name(name: str) -> str:
    """Filesystem-safe slug (Osciloscópio -> osciloscopio)."""
    text = unicodedata.normalize("NFKD", str(name or ""))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = _INVALID_FOLDER_CHARS.sub("", text.lower().strip())
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def equipment_folder_name(equipment_id: str | int, equipment_name: str = "") -> str:
    """Folder name in Explorer, e.g. 1-osciloscopio."""
    eq_id = str(equipment_id or "").strip() or "unknown"
    slug = slugify_equipment_name(equipment_name)
    if slug:
        return f"{eq_id}-{slug}"
    return eq_id


def equipment_id_from_folder(folder_name: str) -> str:
    text = str(folder_name or "").strip()
    if not text:
        return ""
    if "-" in text:
        return text.split("-", 1)[0]
    return text


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
                "Each subfolder is one equipment (folder name = ID-Name, e.g. 1-osciloscopio).\n"
                "Store the datasheet and image there; the app links by filename.\n\n"
                "Typical layout:\n"
                "  3-multimetro/\n"
                "    DS_Fluke_87V.pdf\n"
                "    image.jpg\n",
                encoding="utf-8",
            )
        return self.root

    @staticmethod
    def _equipment_id_str(equipment_id: str | int) -> str:
        text = str(equipment_id or "").strip()
        return text or "unknown"

    def find_equipment_dir(
        self, equipment_id: str | int, equipment_name: str = ""
    ) -> Path | None:
        eq_id = self._equipment_id_str(equipment_id)
        root = self.ensure_root()

        preferred = root / equipment_folder_name(eq_id, equipment_name)
        if preferred.is_dir():
            return preferred

        legacy = root / eq_id
        if legacy.is_dir():
            return legacy

        prefix = f"{eq_id}-"
        matches = sorted(
            (p for p in root.iterdir() if p.is_dir() and p.name.startswith(prefix)),
            key=lambda p: p.name.lower(),
        )
        if matches:
            return matches[0]
        return None

    def equipment_dir(
        self, equipment_id: str | int, equipment_name: str = ""
    ) -> Path:
        found = self.find_equipment_dir(equipment_id, equipment_name)
        if found is not None:
            return found
        return self.ensure_root() / equipment_folder_name(
            equipment_id, equipment_name
        )

    def _sync_folder_name(
        self, folder: Path, equipment_id: str | int, equipment_name: str
    ) -> Path:
        target = self.ensure_root() / equipment_folder_name(
            equipment_id, equipment_name
        )
        if folder.resolve() == target.resolve():
            return folder
        if target.exists():
            return folder
        try:
            folder.rename(target)
            return target
        except OSError:
            return folder

    def ensure_equipment_dir(
        self, equipment_id: str | int, equipment_name: str = ""
    ) -> Path:
        eq_id = self._equipment_id_str(equipment_id)
        existing = self.find_equipment_dir(eq_id, equipment_name)
        target = self.ensure_root() / equipment_folder_name(eq_id, equipment_name)

        if existing is None:
            target.mkdir(parents=True, exist_ok=True)
            return target

        if equipment_name.strip():
            folder = self._sync_folder_name(existing, eq_id, equipment_name)
        else:
            folder = existing

        folder.mkdir(parents=True, exist_ok=True)
        return folder

    @staticmethod
    def _is_reserved_name(name: str) -> bool:
        lowered = name.lower()
        return lowered == _README_NAME.lower() or lowered.startswith(
            f"{_IMAGE_BASENAME}."
        )

    def resolve_datasheet(
        self,
        equipment_id: str | int,
        filename: str,
        *,
        equipment_name: str = "",
    ) -> Path | None:
        name = str(filename).strip()
        if not name:
            return None
        per_eq = self.equipment_dir(equipment_id, equipment_name) / name
        if per_eq.is_file():
            return per_eq
        return None

    def resolve_image(
        self,
        equipment_id: str | int,
        filename: str,
        *,
        equipment_name: str = "",
    ) -> Path | None:
        name = str(filename).strip()
        if not name:
            return None
        per_eq = self.equipment_dir(equipment_id, equipment_name) / name
        if per_eq.is_file():
            return per_eq
        return None

    def document_for_datasheet(
        self,
        equipment_id: str | int,
        filename: str,
        *,
        equipment_name: str = "",
    ) -> SupportDocument | None:
        path = self.resolve_datasheet(
            equipment_id, filename, equipment_name=equipment_name
        )
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
        self,
        source: Path,
        equipment_id: str | int,
        *,
        equipment_name: str = "",
    ) -> tuple[bool, str]:
        source = Path(source)
        if not source.is_file():
            return False, "Selected path is not a file."

        folder = self.ensure_equipment_dir(equipment_id, equipment_name)
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
        self,
        source: Path,
        equipment_id: str | int,
        *,
        equipment_name: str = "",
    ) -> tuple[bool, str]:
        source = Path(source)
        if not source.is_file():
            return False, "Selected path is not a file."
        if not is_image_file(source):
            return False, "File is not a supported image (PNG, JPG, WEBP, BMP, GIF)."

        folder = self.ensure_equipment_dir(equipment_id, equipment_name)
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
        self,
        equipment_id: str | int,
        filename: str,
        *,
        equipment_name: str = "",
    ) -> tuple[bool, str]:
        name = str(filename).strip()
        if not name:
            return True, ""
        path = self.resolve_image(
            equipment_id, name, equipment_name=equipment_name
        )
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
            eq_id = equipment_id_from_folder(child.name)
            for path in sorted(child.iterdir(), key=lambda p: p.name.lower()):
                add_path(path, eq_id)

        documents.sort(key=lambda doc: doc.name.lower())
        return documents

    def open_equipment_folder(
        self,
        equipment_id: str | int | None = None,
        *,
        equipment_name: str = "",
    ) -> tuple[bool, str]:
        if equipment_id is not None and str(equipment_id).strip():
            folder = self.ensure_equipment_dir(equipment_id, equipment_name)
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
