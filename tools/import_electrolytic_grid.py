"""Import SMD electrolytic capacitor grid counts into Generic sheet."""
from __future__ import annotations

import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.stock import StockTracker  # noqa: E402

LOCATION = "ELECTROLYTIC CAPACITORES"
PACKAGE = "SMD"
USER = "GRID-IMPORT"

# Grid positions 1–25 + position 30 (150uF 10V) as user #26.
# #14 (6.8uF 50V) omitted by user → quantity 0.
_GRID_SPECS: dict[int, tuple[str, str]] = {
    1: ("1uF", "10V"),
    2: ("1uF", "16V"),
    3: ("1uF", "25V"),
    4: ("1uF", "35V"),
    5: ("1uF", "50V"),
    6: ("1uF", "50V"),
    7: ("2.2uF", "10V"),
    8: ("2.2uF", "16V"),
    9: ("4.7uF", "10V"),
    10: ("4.7uF", "16V"),
    11: ("4.7uF", "25V"),
    12: ("4.7uF", "35V"),
    13: ("4.7uF", "50V"),
    14: ("6.8uF", "50V"),
    15: ("10uF", "6.3V"),
    16: ("10uF", "10V"),
    17: ("10uF", "16V"),
    18: ("10uF", "25V"),
    19: ("10uF", "35V"),
    20: ("10uF", "35V"),
    21: ("10uF", "50V"),
    22: ("18uF", "50V"),
    23: ("22uF", "10V"),
    24: ("22uF", "16V"),
    25: ("22uF", "25V"),
    26: ("150uF", "10V"),
}

_QUANTITIES: dict[int, int] = {
    1: 0,
    2: 4,
    3: 4,
    4: 20,
    5: 82,
    6: 0,
    7: 22,
    8: 2,
    9: 0,
    10: 1,
    11: 12,
    12: 2,
    13: 10,
    15: 100,
    16: 5,
    17: 80,
    18: 13,
    19: 0,
    20: 0,
    21: 3,
    22: 1,
    23: 1,
    24: 2,
    25: 40,
    26: 8,
}


def _norm_cap(text: str) -> str:
    return (
        str(text or "")
        .strip()
        .upper()
        .replace("µ", "U")
        .replace(" ", "")
    )


def _norm_volt(text: str) -> str:
    v = _norm_cap(text)
    if not v:
        return ""
    if not v.endswith("V"):
        v = f"{v}V"
    return v


def _excel_value(cap: str, voltage: str) -> str:
    return f"{cap} {voltage}"


def _parse_value_voltage(value: str, voltage_col: str) -> tuple[str, str] | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    m = re.match(r"^([\d.]+(?:[Uu][Ff]|UF))\s*(.*)$", raw, re.IGNORECASE)
    if not m:
        return None
    cap = m.group(1)
    tail = m.group(2).strip()
    volt = _norm_volt(voltage_col or tail)
    if not volt and tail:
        volt = _norm_volt(tail)
    return cap, volt


def _matches_spec(data: dict, cap: str, voltage: str) -> bool:
    parsed = _parse_value_voltage(data["value"], data.get("voltage", ""))
    if parsed is None:
        return False
    p_cap, p_volt = parsed
    return _norm_cap(p_cap) == _norm_cap(cap) and _norm_volt(p_volt) == _norm_volt(voltage)


def _find_row(tracker: StockTracker, sheet, cap: str, voltage: str):
    """Match only rows in the electrolytic location (avoid ceramic 0603 duplicates)."""
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        if tracker.row_is_empty(row) or tracker._massive_row_is_header(row):
            continue
        data = tracker.massive_row_to_dict(row)
        if data["part_type"] != "C":
            continue
        loc = str(data.get("location") or "").strip().upper()
        if LOCATION.upper() not in loc:
            continue
        if _matches_spec(data, cap, voltage):
            return row
    return None


def _merged_targets() -> dict[tuple[str, str], int]:
    totals: dict[tuple[str, str], int] = defaultdict(int)
    for slot, (cap, volt) in _GRID_SPECS.items():
        qty = _QUANTITIES.get(slot, 0)
        totals[(cap, volt)] += qty
    return dict(totals)


def import_grid(*, dry_run: bool = False) -> None:
    targets = _merged_targets()
    tracker = StockTracker()
    tracker.ensure_workbook_sheets()
    workbook = tracker.get_workbook()
    sheet = tracker.get_massive_sheet(workbook)

    added = 0
    updated = 0
    skipped = 0

    for (cap, volt), target_qty in sorted(
        targets.items(), key=lambda item: (_norm_cap(item[0][0]), _norm_volt(item[0][1]))
    ):
        excel_value = _excel_value(cap, volt)
        row = _find_row(tracker, sheet, cap, volt)

        if row is None:
            if target_qty <= 0:
                skipped += 1
                print(f"SKIP (new, qty 0): {excel_value}")
                continue
            if dry_run:
                print(f"ADD: {excel_value} stock={target_qty}")
                added += 1
                continue
            ok, msg = tracker.add_massive_item(
                USER,
                "C",
                excel_value,
                "",
                PACKAGE,
                initial_stock=target_qty,
                voltage=volt,
                location=LOCATION,
            )
            if ok:
                added += 1
                print(f"ADDED: {excel_value} stock={target_qty}")
            else:
                print(f"FAIL ADD {excel_value}: {msg}")
            workbook = tracker.get_workbook()
            sheet = tracker.get_massive_sheet(workbook)
            continue

        data = tracker.massive_row_to_dict(row)
        current = int(data["stock"])
        if target_qty == current:
            skipped += 1
            print(f"UNCHANGED: {excel_value} stock={current}")
            continue

        if dry_run:
            print(f"SET: {excel_value} {current} -> {target_qty}")
            updated += 1
            continue

        if not data.get("location"):
            tracker.set_massive_location(row, LOCATION)

        if target_qty > current:
            ok, msg = tracker.update_massive_stock(
                USER, row, target_qty - current, "IN"
            )
        else:
            ok, msg = tracker.update_massive_stock(
                USER, row, current - target_qty, "OUT"
            )
        if ok:
            updated += 1
            print(f"UPDATED: {excel_value} {current} -> {target_qty}")
        else:
            print(f"FAIL UPDATE {excel_value}: {msg}")
        workbook = tracker.get_workbook()
        sheet = tracker.get_massive_sheet(workbook)

    print(f"\nDone: added={added}, updated={updated}, skipped={skipped}")


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    xlsx = ROOT / "data" / "stock.xlsx"
    if not dry_run and xlsx.exists():
        backup = xlsx.with_suffix(".xlsx.bak")
        shutil.copy2(xlsx, backup)
        print(f"Backup: {backup}")
    import_grid(dry_run=dry_run)


if __name__ == "__main__":
    main()
