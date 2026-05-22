"""TME API — https://developers.tme.eu (token + app secret, HMAC signed POST)."""
import base64
import collections
import hashlib
import hmac
import urllib.parse
from typing import Any, Optional

import requests

from .base import PartInfo, normalize_part
from .credentials import get_secret

# Not secret — fixed TME API host
TME_API_HOST = "https://api.tme.eu"
TME_DEFAULT_COUNTRY = "PT"
TME_DEFAULT_LANGUAGE = "EN"


def _signature(url: str, params: dict, api_secret: str) -> str:
    ordered = collections.OrderedDict(sorted(params.items()))
    encoded = urllib.parse.urlencode(ordered, quote_via=urllib.parse.quote)
    base = ("POST&" + urllib.parse.quote(url, "") + "&" + urllib.parse.quote(encoded, "")).encode()
    digest = hmac.new(api_secret.encode(), base, hashlib.sha1).digest()
    return base64.encodebytes(digest).decode().strip()


def _post(endpoint: str, params: dict, token: str, secret: str) -> Optional[dict]:
    url = f"{TME_API_HOST}{endpoint}.json"
    body = dict(params)
    body["Token"] = token
    body["ApiSignature"] = _signature(url, body, secret)
    try:
        response = requests.post(
            url,
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("Status") != "OK":
            print(f"TME: API status {data.get('Status')!r} — {data.get('ErrorMessage', data)}")
            return None
        return data.get("Data") or {}
    except Exception as exc:
        print(f"ERRO TME: {exc}")
        return None


def _product_from_item(item: dict) -> PartInfo:
    symbol = item.get("Symbol") or item.get("SymbolTME") or ""
    producer = item.get("Producer") or item.get("Manufacturer") or ""
    if isinstance(producer, dict):
        producer = producer.get("Name", "")
    return normalize_part(
        {
            "supplier_part_number": symbol,
            "manufacturer": str(producer),
            "manufacturer_part_number": item.get("OriginalSymbol")
            or item.get("ManufacturerSymbol")
            or "",
            "description": item.get("Description") or item.get("Name") or "",
        },
        "tme",
    )


def _get_products(part_number: str, token: str, secret: str) -> Optional[PartInfo]:
    data = _post(
        "/Products/GetProducts",
        {
            "SymbolList[0]": part_number,
            "Country": TME_DEFAULT_COUNTRY,
            "Language": TME_DEFAULT_LANGUAGE,
        },
        token,
        secret,
    )
    if not data:
        return None
    products = data.get("ProductList") or []
    if not products:
        return None
    return _product_from_item(products[0])


def _search_products(part_number: str, token: str, secret: str) -> Optional[PartInfo]:
    """Keyword search when exact TME symbol is unknown."""
    data = _post(
        "/Products/Search",
        {
            "SearchPlain": part_number,
            "Country": TME_DEFAULT_COUNTRY,
            "Language": TME_DEFAULT_LANGUAGE,
        },
        token,
        secret,
    )
    if not data:
        return None
    products = data.get("ProductList") or data.get("Products") or []
    if not products:
        return None
    return _product_from_item(products[0])


def search(part_number: str, secrets: dict) -> Optional[PartInfo]:
    token = get_secret(secrets, "TME_API_TOKEN")
    secret = get_secret(secrets, "TME_APP_SECRET")
    if not token or not secret:
        print(
            "TME: set TME_API_TOKEN and TME_APP_SECRET in config/secrets.py "
            "(developers.tme.eu - application - private key)."
        )
        return None

    part_number = part_number.strip()
    if not part_number:
        return None

    part = _get_products(part_number, token, secret)
    if part:
        return part
    return _search_products(part_number, token, secret)
