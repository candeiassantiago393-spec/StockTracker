"""DigiKey API — OAuth 2-legged + keyword search (v4)."""
from typing import Optional

import requests

from .base import PartInfo, normalize_part
from .credentials import get_secret


def _api_host(secrets: dict) -> str:
    env = str(secrets.get("DIGIKEY_ENV", "sandbox")).strip().lower()
    if env == "production":
        return "https://api.digikey.com"
    return "https://sandbox-api.digikey.com"


def _access_token(host: str, client_id: str, client_secret: str) -> Optional[str]:
    try:
        response = requests.post(
            f"{host}/v1/oauth2/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
            timeout=15,
        )
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as exc:
        print(f"ERRO DigiKey (token): {exc}")
        return None


def search(part_number: str, secrets: dict) -> Optional[PartInfo]:
    client_id = get_secret(secrets, "DIGIKEY_CLIENT_ID")
    client_secret = get_secret(secrets, "DIGIKEY_CLIENT_SECRET")
    if not client_id or not client_secret:
        print(
            "DigiKey: set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET "
            "in config/secrets.py (developer.digikey.com)."
        )
        return None

    host = _api_host(secrets)
    token = _access_token(host, client_id, client_secret)
    if not token:
        return None

    try:
        response = requests.post(
            f"{host}/products/v4/search/keyword",
            headers={
                "X-DIGIKEY-Client-Id": client_id,
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={"Keywords": part_number, "RecordCount": 1},
            timeout=15,
        )
        if response.status_code == 403:
            print(
                "DigiKey: 403 Forbidden — check sandbox/production (DIGIKEY_ENV) "
                "and API product subscription on the developer portal."
            )
            return None
        response.raise_for_status()
        data = response.json()
        products = data.get("Products") or data.get("products") or []
        if not products:
            return None
        raw = products[0]
        mapped = {
            "supplier_part_number": raw.get("DigiKeyPartNumber") or raw.get("dkPartNumber"),
            "manufacturer": raw.get("Manufacturer", {}).get("Name")
            if isinstance(raw.get("Manufacturer"), dict)
            else raw.get("Manufacturer"),
            "manufacturer_part_number": raw.get("ManufacturerProductNumber")
            or raw.get("ManufacturerPartNumber"),
            "description": raw.get("ProductDescription") or raw.get("Description"),
        }
        return normalize_part(mapped, "digikey")
    except Exception as exc:
        print(f"ERRO DigiKey (search): {exc}")
        return None
