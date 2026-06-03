"""DigiKey API — OAuth 2-legged + keyword search (v4)."""
from typing import Optional

import requests

from .base import PartInfo, normalize_part
from .credentials import get_secret

_last_error: str = ""


def get_last_error() -> str:
    """Mensagem do ultimo erro (para a GUI)."""
    return _last_error


def _set_error(message: str) -> None:
    global _last_error
    _last_error = message
    print(message)


def _api_host(secrets: dict) -> str:
    env = str(secrets.get("DIGIKEY_ENV", "sandbox")).strip().lower()
    if env == "production":
        return "https://api.digikey.com"
    return "https://sandbox-api.digikey.com"


def _locale_headers(secrets: dict, client_id: str, token: str) -> dict:
    site = get_secret(secrets, "DIGIKEY_LOCALE_SITE") or "PT"
    language = get_secret(secrets, "DIGIKEY_LOCALE_LANGUAGE") or "pt"
    currency = get_secret(secrets, "DIGIKEY_LOCALE_CURRENCY") or "EUR"
    return {
        "X-DIGIKEY-Client-Id": client_id,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-DIGIKEY-Locale-Site": site,
        "X-DIGIKEY-Locale-Language": language,
        "X-DIGIKEY-Locale-Currency": currency,
    }


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
        _set_error(f"ERRO DigiKey (token): {exc}")
        return None


def search(part_number: str, secrets: dict) -> Optional[PartInfo]:
    global _last_error
    _last_error = ""

    client_id = get_secret(secrets, "DIGIKEY_CLIENT_ID")
    client_secret = get_secret(secrets, "DIGIKEY_CLIENT_SECRET")
    if not client_id or not client_secret:
        _set_error(
            "DigiKey: define DIGIKEY_CLIENT_ID e DIGIKEY_CLIENT_SECRET em config/secrets.py."
        )
        return None

    host = _api_host(secrets)
    token = _access_token(host, client_id, client_secret)
    if not token:
        return None

    query = part_number.strip()
    if not query:
        _set_error("DigiKey: referencia vazia.")
        return None

    try:
        response = requests.post(
            f"{host}/products/v4/search/keyword",
            headers=_locale_headers(secrets, client_id, token),
            json={"Keywords": query, "Limit": 10, "Offset": 0},
            timeout=15,
        )
        if response.status_code == 403:
            correlation = ""
            try:
                correlation = response.json().get("correlationId", "")
            except Exception:
                pass
            extra = f"\nCorrelation ID (para suporte DigiKey): {correlation}" if correlation else ""
            _set_error(
                "DigiKey 403: token OK, mas a API de pesquisa recusa o pedido.\n"
                "Se no portal ja tens Approved + Product Information V4 Enabled, "
                "o problema e do lado DigiKey (sandbox mal provisionado), nao das chaves.\n"
                "Testa KeywordSearch no Swagger (Sandbox Mode). Se tambem der 403, "
                "abre ticket em developer.digikey.com com o Correlation ID."
                + extra
            )
            return None
        if response.status_code == 401:
            _set_error(
                "DigiKey 401: token invalido ou DIGIKEY_ENV errado (usa 'sandbox' com Sandbox App)."
            )
            return None
        if not response.ok:
            _set_error(f"DigiKey HTTP {response.status_code}: {response.text[:300]}")
            return None

        data = response.json()
        products = data.get("Products") or data.get("products") or []
        if not products:
            _set_error(
                f"DigiKey: nenhum resultado para '{query}' "
                f"({'sandbox' if 'sandbox' in host else 'production'})."
            )
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
        _set_error(f"ERRO DigiKey (search): {exc}")
        return None
