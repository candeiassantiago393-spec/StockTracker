"""Equipment image files — local storage under data/equipment_images/."""
from __future__ import annotations

import shutil
from pathlib import Path

from .stock import DATA_DIR

EQUIPMENT_IMAGES_DIR = DATA_DIR / "equipment_images"
_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
_README_NAME = "README.txt"


def is_image_file(path: Path | str) -> bool:
    return Path(path).suffix.lower() in _IMAGE_SUFFIXES


class EquipmentImages:
    """Manage equipment image files stored locally under data/."""

    def __init__(self, folder: Path | None = None) -> None:
        self.folder = Path(folder) if folder else EQUIPMENT_IMAGES_DIR

    def ensure_folder(self) -> Path:
        self.folder.mkdir(parents=True, exist_ok=True)
        readme = self.folder / _README_NAME
        if not readme.exists():
            readme.write_text(
                "Equipment images folder\n"
                "=======================\n\n"
                "Images linked from the Equipments page are stored here.\n",
                encoding="utf-8",
            )
        return self.folder

    def resolve_path(self, filename: str) -> Path | None:
        name = str(filename).strip()
        if not name:
            return None
        self.ensure_folder()
        path = self.folder / name
        if path.is_file():
            return path
        return None

    def add_image(self, source: Path, equipment_id: str | int) -> tuple[bool, str]:
        source = Path(source)
        if not source.is_file():
            return False, "Selected path is not a file."
        if not is_image_file(source):
            return False, "File is not a supported image (PNG, JPG, WEBP, BMP, GIF)."

        self.ensure_folder()
        eq_id = str(equipment_id).strip() or "unknown"
        suffix = source.suffix.lower()
        target = self.folder / f"eq_{eq_id}{suffix}"
        if target.exists():
            stem = f"eq_{eq_id}"
            index = 1
            while target.exists():
                target = self.folder / f"{stem}_{index}{suffix}"
                index += 1

        try:
            shutil.copy2(source, target)
        except OSError as exc:
            return False, f"Could not copy image: {exc}"

        return True, target.name

    def remove_image(self, filename: str) -> tuple[bool, str]:
        name = str(filename).strip()
        if not name:
            return True, ""
        path = self.resolve_path(name)
        if path is None:
            return True, ""
        try:
            path.unlink()
        except OSError as exc:
            return False, f"Could not remove image file: {exc}"
        return True, name
