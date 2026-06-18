###############################################################################
# 1. Module Level Documentation
###############################################################################
"""
Common types for distributor search results.

Each supplier module maps its API response to `PartInfo` via `normalize_part`.
"""

###############################################################################
# 2. Imports
###############################################################################
from typing import Literal, TypedDict

###############################################################################
# 3. Constants and Global Variables
###############################################################################
SupplierId = Literal["mouser", "digikey", "tme", "robert_mauser", "rs"]

###############################################################################
# 4. Type definitions
###############################################################################


class PartInfo(TypedDict, total=False):
    """
    Class:
        Normalized part record returned by any supplier adapter.
    """

    supplier: str
    supplier_part_number: str
    manufacturer: str
    manufacturer_part_number: str
    description: str
    image_url: str
    product_url: str
    datasheet_url: str
    # Campos legado (compatibilidade com resposta Mouser / Excel)
    MouserPartNumber: str
    Manufacturer: str
    ManufacturerPartNumber: str
    Description: str


###############################################################################
# 5. Public functions
###############################################################################


def normalize_part(raw: dict, supplier: SupplierId) -> PartInfo:
    """
    Public Function:
        Map a raw API dict to the unified `PartInfo` structure.
    Args:
        raw (dict): Supplier-specific response fields.
        supplier (SupplierId): Internal supplier identifier.
    Returns:
        PartInfo: Normalized part dictionary.
    """
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
    image_url = str(
        raw.get("image_url")
        or raw.get("ImagePath")
        or raw.get("PhotoUrl")
        or ""
    ).strip()
    product_url = str(
        raw.get("product_url")
        or raw.get("ProductDetailUrl")
        or raw.get("ProductUrl")
        or raw.get("DetailUrl")
        or ""
    ).strip()
    datasheet_url = str(
        raw.get("datasheet_url")
        or raw.get("DataSheetUrl")
        or raw.get("DatasheetUrl")
        or raw.get("PrimaryDatasheet")
        or ""
    ).strip()
    if isinstance(raw.get("PrimaryDatasheet"), dict):
        datasheet_url = datasheet_url or str(
            raw["PrimaryDatasheet"].get("Url")
            or raw["PrimaryDatasheet"].get("url")
            or ""
        ).strip()
    return PartInfo(
        supplier=supplier,
        supplier_part_number=str(spn),
        manufacturer=str(mfr),
        manufacturer_part_number=str(mpn),
        description=str(desc),
        image_url=image_url,
        product_url=product_url,
        datasheet_url=datasheet_url,
        MouserPartNumber=str(spn),
        Manufacturer=str(mfr),
        ManufacturerPartNumber=str(mpn),
        Description=str(desc),
    )
