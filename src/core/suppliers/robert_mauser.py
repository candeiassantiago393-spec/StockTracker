"""Robert Mauser (distribuidor PT) — sem API publica conhecida."""
from typing import Optional

from .base import PartInfo
from .credentials import get_secret


def search(part_number: str, secrets: dict) -> Optional[PartInfo]:
    """
    Robert Mauser (rm.pt / mauser.pt) has no public REST API like Mouser.
    Future: manual site search, CSV import, or commercial agreement.
    """
    if get_secret(secrets, "ROBERT_MAUSER_API_KEY"):
        print(
            "Robert Mauser: key is set but no public part-search API is wired yet."
        )
        return None
    print(
        "Robert Mauser: no public API. "
        "Use Mouser/TME/RS to import parts or fill Excel manually."
    )
    return None
