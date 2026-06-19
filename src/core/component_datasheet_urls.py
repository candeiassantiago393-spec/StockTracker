"""Resolve datasheet URLs when distributor APIs leave DataSheetUrl empty."""
from __future__ import annotations

import re
import threading
from typing import Any, Callable
from urllib.parse import quote, urlparse

_VISHAY_UX_SERIES_PDF = "https://www.vishay.com/docs/28726/uxa0204.pdf"
_VERIFY_CACHE: dict[str, bool] = {}
_VERIFY_LOCK = threading.Lock()
_VERIFY_CACHE_MAX = 500
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
}


def _text(*values: Any) -> str:
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def _normalize_mpn(mpn: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(mpn or "").upper())


def _vishay_datasheet(mpn: str) -> str:
    key = _normalize_mpn(mpn)
    if not key:
        return ""
    if key.startswith(("UXA0204", "UXB0207", "UXE0414")) or re.match(r"^UX[ABE]", key):
        return _VISHAY_UX_SERIES_PDF
    return f"https://www.vishay.com/doc?keyword={quote(mpn)}"


def _meanwell_datasheet(mpn: str) -> str:
    clean = str(mpn or "").strip()
    if not clean:
        return ""
    return f"https://www.meanwell.com/productinfo.aspx?i={quote(clean)}"


def _phoenix_datasheet(mpn: str) -> str:
    digits = re.sub(r"[^0-9]", "", str(mpn or ""))
    if not digits:
        return ""
    return f"https://www.phoenixcontact.com/en-us/products/{digits}"


def _tdk_datasheet(mpn: str) -> str:
    clean = str(mpn or "").strip()
    if not clean:
        return ""
    return f"https://product.tdk.com/en/search/swip?text={quote(clean)}"


def _molex_datasheet(mpn: str) -> str:
    clean = re.sub(r"[^0-9A-Za-z-]", "", str(mpn or ""))
    if not clean:
        return ""
    return f"https://www.molex.com/en-us/products/part/list/{clean}"


def _te_datasheet(mpn: str) -> str:
    clean = str(mpn or "").strip()
    if not clean:
        return ""
    return f"https://www.te.com/en/product-{quote(clean)}.html"


def _mikroe_datasheet(mpn: str) -> str:
    clean = str(mpn or "").strip()
    if not clean:
        return ""
    slug = clean.lower()
    return f"https://download.mikroe.com/documents/datasheets/{slug}-datasheet.pdf"


_TI_PKG_SUFFIXES = (
    "CPRQ1",
    "DCPRQ1",
    "PRQ1",
    "RQ1",
    "RGTR",
    "RGT",
    "RTJR",
    "RTJ",
    "DCP",
    "DCK",
    "DRB",
    "DBV",
    "PW",
    "RGE",
    "RGER",
    "DGS",
    "DRL",
    "NOPB",
    "NSR",
)


def _remember_verify_result(url: str, ok: bool) -> bool:
    with _VERIFY_LOCK:
        if len(_VERIFY_CACHE) >= _VERIFY_CACHE_MAX:
            _VERIFY_CACHE.clear()
        _VERIFY_CACHE[url] = ok
    return ok


def _probe_datasheet_url(url: str, *, timeout: int = 10) -> bool:
    try:
        from curl_cffi import requests as curl_requests

        response = curl_requests.head(
            url,
            impersonate="chrome120",
            timeout=timeout,
            headers=_BROWSER_HEADERS,
            allow_redirects=True,
        )
        if response.status_code < 400:
            return True
        if response.status_code not in (403, 405):
            return False
    except Exception:
        pass

    try:
        import requests

        response = requests.head(
            url,
            timeout=timeout,
            headers=_BROWSER_HEADERS,
            allow_redirects=True,
        )
        if response.status_code < 400:
            return True
        if response.status_code not in (403, 405):
            return False
    except Exception:
        pass

    try:
        import requests

        response = requests.get(
            url,
            timeout=timeout,
            headers={**_BROWSER_HEADERS, "Range": "bytes=0-0"},
            allow_redirects=True,
            stream=True,
        )
        return response.status_code < 400
    except Exception:
        return False


def verify_datasheet_url(url: str, *, timeout: int = 10) -> bool:
    """Return True when the URL responds (avoids opening known 404 links)."""
    target = str(url or "").strip()
    if not target:
        return False
    with _VERIFY_LOCK:
        cached = _VERIFY_CACHE.get(target)
    if cached is not None:
        return cached
    return _remember_verify_result(target, _probe_datasheet_url(target, timeout=timeout))


def _ti_pdf_slug_candidates(mpn: str) -> list[str]:
    clean = _normalize_mpn(mpn)
    if not clean:
        return []
    candidates: list[str] = []

    if re.match(r"^TPS\d+.*Q1", clean):
        match = re.match(r"^(TPS\d+)", clean)
        if match:
            candidates.append(f"{match.group(1).lower()}-q1")

    trimmed = clean
    for suffix in sorted(_TI_PKG_SUFFIXES, key=len, reverse=True):
        if trimmed.endswith(suffix) and len(trimmed) > len(suffix) + 3:
            trimmed = trimmed[: -len(suffix)]
            candidates.append(trimmed.lower())
            break

    if len(clean) > 4 and clean[-1].isalpha() and clean[-2].isdigit():
        candidates.append(clean[:-1].lower())

    candidates.append(clean.lower())

    if re.match(r"^(LM|SN|TPS|TLV|DRV|INA|ADS|MSP|BQ|CC|ULN|OPA)", clean):
        for end in range(len(clean), 4, -1):
            candidates.append(clean[:end].lower())

    seen: set[str] = set()
    ordered: list[str] = []
    for slug in candidates:
        if slug not in seen:
            seen.add(slug)
            ordered.append(slug)
    return ordered


def _ti_datasheet(mpn: str) -> str:
    for slug in _ti_pdf_slug_candidates(mpn):
        url = f"https://www.ti.com/lit/ds/symlink/{slug}.pdf"
        if verify_datasheet_url(url):
            return url
    return ""


def _st_datasheet(mpn: str) -> str:
    clean = str(mpn or "").strip()
    if not clean:
        return ""
    return f"https://www.st.com/en/products/{quote(clean)}.html"


def _wurth_datasheet(mpn: str) -> str:
    clean = str(mpn or "").strip()
    if not clean:
        return ""
    return f"https://www.we-online.com/en/search?q={quote(clean)}"


def _onsemi_datasheet(mpn: str) -> str:
    clean = str(mpn or "").strip()
    if not clean:
        return ""
    return f"https://www.onsemi.com/products/{quote(clean)}"


def _manufacturer_doc_url(manufacturer: str, mpn: str) -> str:
    name = manufacturer.lower()
    rules: list[tuple[tuple[str, ...], Callable[[str], str]]] = [
        (("vishay",), _vishay_datasheet),
        (("mean well", "meanwell"), _meanwell_datasheet),
        (("phoenix",), _phoenix_datasheet),
        (("tdk", "epcos"), _tdk_datasheet),
        (("molex",), _molex_datasheet),
        (("te connectivity", "neohm", "measurement specialties"), _te_datasheet),
        (("mikroe",), _mikroe_datasheet),
        (("texas instruments",), _ti_datasheet),
        (("stmicroelectronics", "st micro"), _st_datasheet),
        (("wurth", "würth"), _wurth_datasheet),
        (("onsemi", "on semi"), _onsemi_datasheet),
        (("ams osram", "osram"), lambda m: f"https://ams.com/search?q={quote(m)}"),
        (("infineon",), lambda m: f"https://www.infineon.com/cms/en/search.html#!view=products&term={quote(m)}"),
        (("analog devices", "analog devices inc"), lambda m: f"https://www.analog.com/en/search.html?q={quote(m)}"),
        (("microchip",), lambda m: f"https://www.microchip.com/en-us/product/{quote(m)}"),
        (("nexperia",), lambda m: f"https://www.nexperia.com/search.html?q={quote(m)}"),
        (("yageo",), lambda m: f"https://www.yageo.com/en/Product/Index/{quote(m)}"),
    ]
    for keys, builder in rules:
        if any(key in name for key in keys):
            return builder(mpn)
    return ""


_BLOCKED_DATASHEET_URL_MARKERS = (
    "kyocera-avx.com/products/search",
    "product.tdk.com/en/search",
    "we-online.com/en/search",
    "ams.com/search",
    "infineon.com/cms/en/search",
    "nexperia.com/search",
    "analog.com/en/search",
)


def is_trusted_datasheet_url(url: str) -> bool:
    """True for direct PDFs, distributor datasheets, and known-good doc hosts."""
    raw = str(url or "").strip()
    if not raw:
        return False
    lowered = raw.lower()
    if any(marker in lowered for marker in _BLOCKED_DATASHEET_URL_MARKERS):
        return False
    if "mouser.com/datasheet/" in lowered:
        return True
    if "digikey.com" in lowered and (
        "/datasheets/" in lowered or lowered.endswith(".pdf")
    ):
        return True
    if "ti.com/lit/" in lowered:
        return True
    path = urlparse(lowered).path
    if path.endswith(".pdf"):
        return True
    if "vishay.com/docs/" in lowered and ".pdf" in lowered:
        return True
    return False


def _mouser_product_url(part: dict[str, Any]) -> str:
    return _text(part.get("product_url"), part.get("ProductDetailUrl"))


def _accept_datasheet_url(url: str, *, verify: bool) -> str:
    candidate = str(url or "").strip()
    if not candidate or not is_trusted_datasheet_url(candidate):
        return ""
    lowered = candidate.lower()
    if not verify or "mouser.com/datasheet/" in lowered:
        return candidate
    if "digikey.com" in lowered and "/datasheets/" in lowered:
        return candidate
    if not verify_datasheet_url(candidate):
        return ""
    return candidate


def validated_datasheet_url(url: str) -> str:
    """Return the URL only when it is trusted and reachable."""
    return _accept_datasheet_url(url, verify=True)


def resolve_datasheet_url(part: dict[str, Any], *, verify: bool = True) -> str:
    """Return a datasheet URL for a catalog part, or empty if none is known."""
    existing = _text(part.get("datasheet_url"), part.get("DataSheetUrl"))
    accepted = _accept_datasheet_url(existing, verify=verify)
    if accepted:
        return accepted

    product_url = _mouser_product_url(part)
    if product_url and "mouser.com" in product_url.lower():
        from .suppliers.mouser_datasheet import fetch_mouser_datasheet_url

        scraped = fetch_mouser_datasheet_url(product_url)
        accepted = _accept_datasheet_url(scraped, verify=verify)
        if accepted:
            return accepted

    manufacturer = _text(part.get("manufacturer"), part.get("Manufacturer"))
    mpn = _text(
        part.get("manufacturer_part_number"),
        part.get("ManufacturerPartNumber"),
    )
    if not mpn:
        return ""

    fallback = _manufacturer_doc_url(manufacturer, mpn)
    return _accept_datasheet_url(fallback, verify=verify)
