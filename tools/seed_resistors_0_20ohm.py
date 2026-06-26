"""Seed Generic sheet with 0–20 Ω resistors (all SMD packages, stock 0)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.stock import StockTracker  # noqa: E402

# Same packages as Passive add dialog (massive_dialog.py).
RESISTOR_PACKAGES = (
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

# E24-style values from 0 Ω to 20 Ω (lab stock list).
RESISTOR_VALUES_0_TO_20_OHM = (
    "0",
    "0.1",
    "0.22",
    "0.47",
    "1",
    "1.1",
    "1.2",
    "1.3",
    "1.5",
    "1.6",
    "1.8",
    "2",
    "2.2",
    "2.4",
    "2.7",
    "3",
    "3.3",
    "3.6",
    "3.9",
    "4.3",
    "4.7",
    "5.1",
    "5.6",
    "6.2",
    "6.8",
    "7.5",
    "8.2",
    "9.1",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
)


def seed_resistors_0_20ohm(*, skip_existing: bool = True) -> tuple[int, int]:
    """Add resistor rows; returns (added, skipped)."""
    tracker = StockTracker()
    tracker.ensure_workbook_sheets()
    workbook = tracker.get_workbook()
    sheet = tracker.get_massive_sheet(workbook)
    next_id = tracker.next_massive_id(sheet)

    added = 0
    skipped = 0
    for value in RESISTOR_VALUES_0_TO_20_OHM:
        for package in RESISTOR_PACKAGES:
            if skip_existing and tracker.find_massive_by_identity(
                sheet, "R", value, "", package
            ):
                skipped += 1
                continue

            name = tracker.build_massive_name("R", value, "", package)
            sheet.append([
                next_id,
                "R",
                value,
                "",
                package,
                name,
                0,
                "",
                "",
                "",
                "",
                "",
            ])
            next_id += 1
            added += 1

    if added and not tracker.save_workbook(workbook):
        raise RuntimeError("Could not save stock.xlsx — close it in Excel and run again.")

    return added, skipped


def main() -> None:
    print("Stock Tracker — seed resistors 0-20 ohm (all packages, stock 0)")
    total = len(RESISTOR_VALUES_0_TO_20_OHM) * len(RESISTOR_PACKAGES)
    print(f"Combinations: {len(RESISTOR_VALUES_0_TO_20_OHM)} values × "
          f"{len(RESISTOR_PACKAGES)} packages = {total}")
    added, skipped = seed_resistors_0_20ohm()
    print(f"Done. Added {added}, skipped {skipped} (already in sheet).")


if __name__ == "__main__":
    main()
