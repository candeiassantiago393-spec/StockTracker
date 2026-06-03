###############################################################################
# 1. Module Level Documentation
###############################################################################
"""
Distributor integration layer (Mouser, DigiKey, TME, RS, …).

Each file under `suppliers/` implements one vendor.
Credentials: `config/secrets.py` (see `secrets.example.py`).
"""

###############################################################################
# 2. Imports
###############################################################################
from .base import PartInfo, SupplierId
from . import digikey, mouser, robert_mauser, rs, tme
from .credentials import configured_suppliers, is_configured

###############################################################################
# 3. Constants and Global Variables
###############################################################################
AVAILABLE: dict[SupplierId, str] = {
    "mouser": "Mouser Electronics",
    "digikey": "DigiKey",
    "tme": "TME",
    "robert_mauser": "Robert Mauser (PT)",
    "rs": "RS Components",
}

IMPLEMENTED: tuple[SupplierId, ...] = ("mouser", "digikey", "tme", "rs")

PLANNED: tuple[SupplierId, ...] = ()

###############################################################################
# 4. Public functions
###############################################################################


def supplier_label(supplier: SupplierId) -> str:
    """
    Public Function:
        Human-readable supplier name for UI messages.
    """
    return AVAILABLE.get(supplier, supplier)


def search_part(supplier: SupplierId, part_number: str, secrets: dict):
    """
    Public Function:
        Dispatch search to the correct supplier module.
    Args:
        supplier (SupplierId): Target distributor.
        part_number (str): SKU, MPN, or barcode text.
        secrets (dict): Loaded credentials from `config/secrets.py`.
    Returns:
        PartInfo | None: Normalized part or None if not found / not configured.
    """
    if supplier == "mouser":
        return mouser.search(part_number, secrets)
    if supplier == "digikey":
        return digikey.search(part_number, secrets)
    if supplier == "tme":
        return tme.search(part_number, secrets)
    if supplier == "robert_mauser":
        return robert_mauser.search(part_number, secrets)
    if supplier == "rs":
        return rs.search(part_number, secrets)
    print(f"Unknown supplier: {supplier}")
    return None
