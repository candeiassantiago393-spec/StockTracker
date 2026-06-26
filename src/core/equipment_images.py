"""Equipment image helpers — files live under data/equipments/{id}-{name}/."""
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
        self,
        filename: str,
        equipment_id: str | int | None = None,
        *,
        equipment_name: str = "",
    ) -> Path | None:
        if equipment_id is None:
            return None
        return self._storage.resolve_image(
            equipment_id, filename, equipment_name=equipment_name
        )

    def list_images(
        self,
        equipment_id: str | int,
        *,
        equipment_name: str = "",
    ) -> list[str]:
        return self._storage.list_equipment_images(
            equipment_id, equipment_name=equipment_name
        )

    def add_image(
        self,
        source: Path,
        equipment_id: str | int,
        *,
        equipment_name: str = "",
    ) -> tuple[bool, str]:
        return self._storage.add_image(
            source, equipment_id, equipment_name=equipment_name
        )

    def remove_image(
        self,
        filename: str,
        equipment_id: str | int | None = None,
        *,
        equipment_name: str = "",
    ) -> tuple[bool, str]:
        if equipment_id is None:
            return True, ""
        return self._storage.remove_image_file(
            equipment_id, filename, equipment_name=equipment_name
        )
