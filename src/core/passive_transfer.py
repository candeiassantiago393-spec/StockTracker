"""Detect resistors/capacitors and map catalog or manual fields to Generic (Passive) rows."""
from __future__ import annotations

import re
from dataclasses import dataclass

_SMD_PACKAGES = (
    "0201",
    "0402",
    "0603",
    "0805",
    "1206",
    "1210",
    "1812",
    "2010",
    "2512",
)

_RESISTOR_MPN_PATTERNS = (
    r"\bCRCW",
    r"\bCRG0",
    r"\bRC0\d{3}",
    r"\bERJ[- ]",
    r"\bERA[- ]",
    r"\bRK73",
    r"\bRT0\d{3}",
    r"\bWSL\d",
    r"\bCRM0",
)

_CAPACITOR_MPN_PATTERNS = (
    r"\bGRM",
    r"\bCL0[1-9]",
    r"\bCC0\d{3}",
    r"\bUMK",
    r"\bCGA",
    r"\bJMK",
    r"\bEMK",
)


def _mpn_indicates_type(text: str) -> str | None:
    upper = text.upper()
    for pattern in _CAPACITOR_MPN_PATTERNS:
        if re.search(pattern, upper):
            return "C"
    for pattern in _RESISTOR_MPN_PATTERNS:
        if re.search(pattern, upper):
            return "R"
    return None

@dataclass(frozen=True)
class PassiveCandidate:
    part_type: str  # R or C
    value: str
    tolerance: str
    package: str
    dielectric: str
    voltage: str
    supplier_reference: str
    notes: str
    auto_ready: bool  # value + package parsed — safe to auto-add


def _blob(*texts: str) -> str:
    return " ".join(str(text or "").strip() for text in texts if str(text or "").strip())


def _flatten_product_attributes(raw: dict) -> str:
    parts: list[str] = []
    for attr in raw.get("ProductAttributes") or raw.get("Attributes") or []:
        if not isinstance(attr, dict):
            continue
        name = str(attr.get("AttributeName") or attr.get("Name") or "").strip()
        value = str(attr.get("AttributeValue") or attr.get("Value") or "").strip()
        if name or value:
            parts.append(f"{name} {value}".strip())
    return " ".join(parts)


def catalog_part_context(part: dict) -> dict[str, str]:
    """Gather every text field from a distributor part record."""
    description = str(
        part.get("description")
        or part.get("Description")
        or ""
    ).strip()
    manufacturer = str(
        part.get("manufacturer")
        or part.get("Manufacturer")
        or ""
    ).strip()
    manufacturer_reference = str(
        part.get("manufacturer_part_number")
        or part.get("ManufacturerPartNumber")
        or ""
    ).strip()
    supplier_reference = str(
        part.get("supplier_part_number")
        or part.get("MouserPartNumber")
        or part.get("Symbol")
        or ""
    ).strip()
    category = str(part.get("category") or part.get("Category") or "").strip()
    extra = str(part.get("product_attributes_text") or "").strip()
    if not extra:
        extra = _flatten_product_attributes(part)
    return {
        "description": description,
        "manufacturer": manufacturer,
        "manufacturer_reference": manufacturer_reference,
        "supplier_reference": supplier_reference,
        "category": category,
        "extra_text": extra,
    }


def detect_passive_type(*texts: str) -> str | None:
    """Return R, C, or None."""
    text = _blob(*texts).lower()
    if not text:
        return None

    if re.search(
        r"\b(?:capacitor|capacitance|tantalum|ceramic\s+cap|mlcc|multilayer\s+ceramic)\b",
        text,
    ):
        return "C"
    if re.search(
        r"\b(?:resistor|resistance|thin\s+film|thick\s+film|chip\s+res|film\s+res)\b",
        text,
    ):
        return "R"

    if re.search(r"\bres\s+(?:smd|chip|thick|thin|mf|cf)\b", text):
        return "R"
    if re.search(r"\bcap\s+(?:smd|cer|ceramic|elec|elect)\b", text):
        return "C"

    if re.search(r"\d+(?:\.\d+)?\s*[punµu]f\b", text, re.IGNORECASE):
        return "C"
    if re.search(
        r"\d+(?:\.\d+)?\s*(?:[kmg])?\s*(?:ohm|ohms|ω|Ω)\b",
        text,
        re.IGNORECASE,
    ):
        return "R"
    if re.search(r"\b\d+(?:\.\d+)?\s*r\b(?![a-z])", text, re.IGNORECASE):
        return "R"
    if re.search(r"\b\d+\s*[kmg]\s*ohms?\b", text, re.IGNORECASE):
        return "R"

    mpn_type = _mpn_indicates_type(text)
    if mpn_type:
        return mpn_type

    if re.search(r"\bres\b", text) and re.search(r"\b0\d{3}\b", text):
        return "R"
    if re.search(r"\bcap\b", text) and re.search(r"\b0\d{3}\b", text):
        return "C"

    if re.search(r"\brc0\d{3}\b", text):
        return "R"
    if re.search(r"\bcl0[1-9]\d\b", text):
        return "C"

    return None


def _parse_package(text: str) -> str:
    embedded = (
        r"RC(0\d{3})",
        r"CRCW(0\d{3})",
        r"CRG(0\d{3})",
        r"RM(0\d{3})",
        r"RT(0\d{3})",
        r"RK73[BH]?(0\d{3})",
        r"CL(0\d{3})",
        r"CC(0\d{3})",
    )
    for pattern in embedded:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            package = match.group(1)
            if package in _SMD_PACKAGES:
                return package

    for package in _SMD_PACKAGES:
        if re.search(rf"\b{package}\b", text, re.IGNORECASE):
            return package
        if re.search(rf"(?<!\d){package}(?!\d)", text, re.IGNORECASE):
            return package

    match = re.search(r"\b(0\d{3})\b", text)
    if match and match.group(1) in _SMD_PACKAGES:
        return match.group(1)
    return ""


def _parse_tolerance(text: str) -> str:
    match = re.search(r"(?:±|\+/-)?\s*(\d+(?:\.\d+)?\s*%)", text, re.IGNORECASE)
    if match:
        return match.group(1).replace(" ", "")
    match = re.search(r"\b([0-9]{1,2}[a-zA-Z])\b", text)
    if match:
        return match.group(1).upper()
    match = re.search(r"\b([0-9]+)\s*percent\b", text, re.IGNORECASE)
    if match:
        return f"{match.group(1)}%"
    return ""


def _parse_dielectric(text: str) -> str:
    match = re.search(
        r"\b(X7R|X5R|C0G|NP0|Y5V|X6S|X7S|Z5U|C0G|U2J)\b",
        text,
        re.IGNORECASE,
    )
    return match.group(1).upper() if match else ""


def _parse_voltage(text: str) -> str:
    match = re.search(r"\b(\d+(?:\.\d+)?\s*(?:v|kv))\b", text, re.IGNORECASE)
    if match:
        return match.group(1).replace(" ", "").upper()
    return ""


def _format_value_suffix(value: str, suffix: str) -> str:
    suffix = (suffix or "").upper()
    if suffix in {"K", "M", "G"}:
        return f"{value}{suffix.lower()}"
    return value


def _parse_resistor_value(text: str) -> str:
    patterns = (
        r"(\d+(?:\.\d+)?)\s*([kmgKM]?)\s*(?:ohm|ohms|ω|Ω)\b",
        r"\bres(?:istor)?\s*(\d+(?:\.\d+)?)\s*([kmKM]?)\b",
        r"\b(\d+(?:\.\d+)?)\s*([kmKM])(?:\b|_|-|/|%)",
        r"\b(\d+(?:\.\d+)?)\s*([kmKM])\b",
        r"\b(\d+)\s*([rkRKM])(\d)\b",
        r"\b(\d+(?:\.\d+)?)\s*r\b(?![a-z])",
        r"\b0+r0*\b",
    )
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue
        if pattern.endswith("0+r0*\\b"):
            return "0"
        if len(match.groups()) >= 3 and match.group(3):
            return f"{match.group(1)}{match.group(2).lower()}{match.group(3)}"
        return _format_value_suffix(
            match.group(1),
            match.group(2) if match.lastindex and match.lastindex >= 2 else "",
        )
    # Embedded in MPN e.g. 0710KL, 1002
    match = re.search(
        r"(?:[-_/])(\d{3,4})(?:[rkRKM]|ohm)",
        text,
        re.IGNORECASE,
    )
    if match:
        digits = match.group(1)
        if len(digits) == 3:
            return f"{digits[0]}{digits[1:].lower()}"
        if len(digits) == 4:
            return f"{digits[:2]}{digits[2:].lower()}"
    return ""


def _parse_capacitor_value(text: str) -> str:
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*([punµuPUN]?)\s*F\b",
        text,
        re.IGNORECASE,
    )
    if match:
        value = match.group(1)
        unit = match.group(2).lower().replace("µ", "u")
        if unit:
            return f"{value}{unit}F"
        return f"{value}F"
    match = re.search(r"\b(\d+(?:\.\d+)?)([punµu])f\b", text, re.IGNORECASE)
    if match:
        unit = match.group(2).lower().replace("µ", "u")
        return f"{match.group(1)}{unit}F"
    return ""


def analyze_for_passive(
    *,
    description: str = "",
    manufacturer: str = "",
    manufacturer_reference: str = "",
    supplier_reference: str = "",
    category: str = "",
    extra_text: str = "",
) -> PassiveCandidate | None:
    """Build passive fields from component / catalog text."""
    combined = _blob(
        description,
        manufacturer,
        manufacturer_reference,
        supplier_reference,
        category,
        extra_text,
    )
    part_type = detect_passive_type(
        description,
        manufacturer,
        manufacturer_reference,
        supplier_reference,
        category,
        extra_text,
    )
    if not part_type:
        return None

    package = _parse_package(combined)
    if not package:
        package = _parse_package(manufacturer_reference)
    if not package:
        package = _parse_package(supplier_reference)

    tolerance = _parse_tolerance(combined)
    dielectric = _parse_dielectric(combined)
    voltage = _parse_voltage(combined)
    value = (
        _parse_capacitor_value(combined)
        if part_type == "C"
        else _parse_resistor_value(combined)
    )
    if not value:
        value = (
            _parse_capacitor_value(manufacturer_reference)
            if part_type == "C"
            else _parse_resistor_value(manufacturer_reference)
        )

    notes_parts: list[str] = []
    if description:
        notes_parts.append(description)
    if category:
        notes_parts.append(category)
    if manufacturer or manufacturer_reference:
        notes_parts.append(
            " / ".join(
                part
                for part in (manufacturer.strip(), manufacturer_reference.strip())
                if part
            )
        )
    notes = " — ".join(notes_parts)

    return PassiveCandidate(
        part_type=part_type,
        value=value,
        tolerance=tolerance,
        package=package,
        dielectric=dielectric,
        voltage=voltage,
        supplier_reference=str(supplier_reference or "").strip(),
        notes=notes,
        auto_ready=bool(value and package),
    )


def analyze_for_catalog_part(part: dict) -> PassiveCandidate | None:
    """Detect passive from a normalized distributor part dict."""
    return analyze_for_passive(**catalog_part_context(part))


def passive_dialog_initial(
    candidate: PassiveCandidate,
    *,
    initial_stock: int = 0,
    location: str = "",
) -> dict:
    return {
        "part_type": candidate.part_type,
        "value": candidate.value,
        "tolerance": candidate.tolerance,
        "package": candidate.package,
        "dielectric": candidate.dielectric,
        "voltage": candidate.voltage,
        "supplier_reference": candidate.supplier_reference,
        "notes": candidate.notes,
        "stock": initial_stock,
        "location": location,
    }


def _candidate_autofill_fields(candidate: PassiveCandidate) -> dict[str, str]:
    fields: dict[str, str] = {"part_type": candidate.part_type}
    for key in ("value", "tolerance", "package", "dielectric", "voltage", "notes"):
        value = str(getattr(candidate, key, "") or "").strip()
        if value:
            fields[key] = value
    return fields


def _merge_autofill(base: dict[str, str], extra: dict[str, str]) -> dict[str, str]:
    merged = dict(base)
    for key, value in extra.items():
        if value and not merged.get(key):
            merged[key] = value
    return merged


def _catalog_part_has_passive_text(part: dict) -> bool:
    ctx = catalog_part_context(part)
    return bool(
        str(ctx.get("description") or "").strip()
        or str(ctx.get("extra_text") or "").strip()
        or str(ctx.get("category") or "").strip()
    )


def enrich_passive_from_reference(
    supplier_reference: str,
    *,
    notes: str = "",
    tracker=None,
) -> dict[str, str]:
    """
    Suggest passive fields from supplier ref text, Excel, or distributor catalog.
    Used to auto-fill Package (and related fields) in the add/edit dialog.
    """
    ref = str(supplier_reference or "").strip()
    if not ref:
        return {}

    fields: dict[str, str] = {}
    local = analyze_for_passive(
        supplier_reference=ref,
        manufacturer_reference=notes,
        extra_text=notes,
    )
    if local is not None:
        fields = _merge_autofill(fields, _candidate_autofill_fields(local))

    if tracker is not None:
        workbook = tracker.get_workbook()
        massive = tracker.get_massive_sheet(workbook)
        row = tracker.find_massive_by_supplier_ref(massive, ref)
        if row is not None:
            data = tracker.massive_row_to_dict(row)
            fields = _merge_autofill(
                fields,
                {
                    "part_type": data.get("part_type", ""),
                    "value": data.get("value", ""),
                    "tolerance": data.get("tolerance", ""),
                    "package": data.get("package", ""),
                    "dielectric": data.get("dielectric", ""),
                    "voltage": data.get("voltage", ""),
                    "notes": data.get("notes", ""),
                },
            )

        if not fields.get("package"):
            part = tracker.lookup_catalog_part(ref)
            if part is not None and not _catalog_part_has_passive_text(part):
                part = None
            if part is None or not analyze_for_catalog_part(part):
                fresh, _supplier = tracker.search_any_supplier(ref)
                if fresh is not None:
                    part = fresh
            if part is not None:
                catalog = analyze_for_catalog_part(part)
                if catalog is not None:
                    fields = _merge_autofill(fields, _candidate_autofill_fields(catalog))

    return fields
