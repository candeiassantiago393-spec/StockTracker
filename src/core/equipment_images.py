"""Equipment image helpers — files live under data/equipments/{id}/."""
from __future__ import annotations

from pathlib import Path

from .equipment_storage import EQUIPMENTS_DIR, EquipmentStorage, is_image_file

EQUIPMENT_IMAGES_DIR = EQUIPMENTS_DIR


class EquipmentImages:
    """Thin wrapper around per-equipment storage."""

    def __init__(self, folder: Path | None = None) -> None:
        self._storage = EquipmentStorage(folder)

    def ensure_folder(self) -> Path:
        return self._storage.ensure_root()

    def resolve_path(
        self, filename: str, equipment_id: str | int | None = None
    ) -> Path | None:
        if equipment_id is None:
            return None
        return self._storage.resolve_image(equipment_id, filename)

    def add_image(self, source: Path, equipment_id: str | int) -> tuple[bool, str]:
        return self._storage.add_image(source, equipment_id)

    def remove_image(
        self, filename: str, equipment_id: str | int | None = None
    ) -> tuple[bool, str]:
        if equipment_id is None:
            return True, ""
        return self._storage.remove_image_file(equipment_id, filename)
