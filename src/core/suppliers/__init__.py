"""
Integracao com distribuidores (Mouser, DigiKey, TME, RS, ...).

Cada modulo em suppliers/ trata de um fornecedor.
Credenciais: config/secrets.py (ver secrets.example.py).
"""
from .base import PartInfo, SupplierId
from . import digikey, mouser, robert_mauser, rs, tme
from .credentials import configured_suppliers, is_configured

AVAILABLE: dict[SupplierId, str] = {
    "mouser": "Mouser Electronics",
    "digikey": "DigiKey",
    "tme": "TME",
    "robert_mauser": "Robert Mauser (PT)",
    "rs": "RS Components",
}

IMPLEMENTED: tuple[SupplierId, ...] = ("mouser", "digikey", "tme", "rs")

PLANNED: tuple[SupplierId, ...] = ()


def supplier_label(supplier: SupplierId) -> str:
    return AVAILABLE.get(supplier, supplier)


def search_part(supplier: SupplierId, part_number: str, secrets: dict):
    """Pesquisa unificada por fornecedor."""
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
