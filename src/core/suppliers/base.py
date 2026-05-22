"""Modelo comum para resultados de pesquisa em distribuidores."""
from typing import Literal, TypedDict

SupplierId = Literal["mouser", "digikey", "tme", "robert_mauser", "rs"]


class PartInfo(TypedDict, total=False):
    """Formato normalizado devolvido por cada fornecedor."""

    supplier: str
    supplier_part_number: str
    manufacturer: str
    manufacturer_part_number: str
    description: str
    # Campos legado (compatibilidade com resposta Mouser / Excel)
    MouserPartNumber: str
    Manufacturer: str
    ManufacturerPartNumber: str
    Description: str


def normalize_part(raw: dict, supplier: SupplierId) -> PartInfo:
    """Converte resposta de API para formato unico."""
    spn = (
        raw.get("supplier_part_number")
        or raw.get("MouserPartNumber")
        or raw.get("Symbol")
        or ""
    )
    mfr = raw.get("manufacturer") or raw.get("Manufacturer") or ""
    mpn = (
        raw.get("manufacturer_part_number")
        or raw.get("ManufacturerPartNumber")
        or ""
    )
    desc = raw.get("description") or raw.get("Description") or ""
    return PartInfo(
        supplier=supplier,
        supplier_part_number=str(spn),
        manufacturer=str(mfr),
        manufacturer_part_number=str(mpn),
        description=str(desc),
        MouserPartNumber=str(spn),
        Manufacturer=str(mfr),
        ManufacturerPartNumber=str(mpn),
        Description=str(desc),
    )
