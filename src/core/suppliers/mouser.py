"""API Mouser Electronics — implementado."""
from typing import Optional

import requests

from .base import PartInfo, normalize_part
from .credentials import get_secret


def search(part_number: str, secrets: dict) -> Optional[PartInfo]:
    api_key = get_secret(secrets, "MOUSER_API_KEY")
    if not api_key:
        print("AVISO: MOUSER_API_KEY nao definida (config/secrets.py).")
        return None
    try:
        url = (
            "https://api.mouser.com/api/v1/search/partnumber"
            f"?apiKey={api_key}"
        )
        payload = {
            "SearchByPartRequest": {
                "mouserPartNumber": part_number,
                "partSearchOptions": "None",
            }
        }
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        parts = data.get("SearchResults", {}).get("Parts", [])
        if not parts:
            return None
        part = normalize_part(parts[0], "mouser")
        if not str(part.get("datasheet_url", "")).strip():
            from ..component_datasheet_urls import resolve_datasheet_url

            datasheet_url = resolve_datasheet_url(part)
            if datasheet_url:
                part["datasheet_url"] = datasheet_url
                part["DataSheetUrl"] = datasheet_url
        return part
    except Exception as exc:
        print(f"ERRO Mouser: {exc}")
        return None
