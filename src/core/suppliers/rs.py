"""RS Components — API key in secrets; base URL is fixed here (not secret)."""
from typing import Optional

import requests

from .base import PartInfo, normalize_part
from .credentials import get_secret

# Public RS API host (not secret). Override path below if RS docs differ.
RS_API_BASE_URL = "https://api-store.rs-online.com"
RS_PRODUCT_SEARCH_PATH = "/api/products/search"


def _base_url(secrets: dict) -> str:
    """Optional override in secrets only if your account uses a different host."""
    override = get_secret(secrets, "RS_API_BASE_URL")
    return (override or RS_API_BASE_URL).rstrip("/")


def search(part_number: str, secrets: dict) -> Optional[PartInfo]:
    api_key = get_secret(secrets, "RS_API_KEY")
    if not api_key:
        print("RS: set RS_API_KEY in config/secrets.py.")
        return None

    url = f"{_base_url(secrets)}{RS_PRODUCT_SEARCH_PATH}"
    try:
        response = requests.get(
            url,
            params={"partNumber": part_number},
            headers={
                "Accept": "application/json",
                "Ocp-Apim-Subscription-Key": api_key,
            },
            timeout=15,
        )
        if response.status_code in (404, 501):
            print(
                f"RS: HTTP {response.status_code} at {url}. "
                "Check RS API docs or update RS_PRODUCT_SEARCH_PATH in rs.py."
            )
            return None
        if response.status_code == 401:
            print("RS: 401 — check RS_API_KEY.")
            return None
        response.raise_for_status()
        data = response.json()
        items = (
            data
            if isinstance(data, list)
            else data.get("products") or data.get("Products") or []
        )
        if not items:
            return None
        raw = items[0] if isinstance(items[0], dict) else {}
        mapped = {
            "supplier_part_number": raw.get("stockNumber")
            or raw.get("partNumber")
            or part_number,
            "manufacturer": raw.get("brand") or raw.get("manufacturer", ""),
            "manufacturer_part_number": raw.get("manufacturerPartNumber", ""),
            "description": raw.get("description") or raw.get("name", ""),
        }
        return normalize_part(mapped, "rs")
    except Exception as exc:
        print(f"ERRO RS: {exc}")
        return None
