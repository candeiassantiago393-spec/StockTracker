"""Fix ceramic rows wrongly updated by import_electrolytic_grid.py."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.stock import StockTracker  # noqa: E402

RESTORE = {
    512: 50,  # 1uF 0603 ceramic 25V
    509: 50,  # 2.2uF 0603 ceramic 16V
    513: 50,  # 2.2uF 0603 ceramic 10V
}


def main() -> None:
    tracker = StockTracker()
    workbook = tracker.get_workbook()
    sheet = tracker.get_massive_sheet(workbook)
    history = tracker.get_history_sheet(workbook)

    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        if tracker.row_is_empty(row):
            continue
        row_id = row[0].value
        if row_id not in RESTORE:
            continue
        old = int(row[6].value or 0)
        new = RESTORE[row_id]
        row[6].value = new
        data = tracker.massive_row_to_dict(row)
        label = data["name"] or data["value"]
        movement = "IN" if new > old else "OUT"
        tracker.add_history(history, "GRID-FIX", label, movement, abs(new - old), new)
        print(f"Restored ID {row_id} {data['value']}: {old} -> {new}")

    ok, msg = tracker.add_massive_item(
        "GRID-IMPORT",
        "C",
        "1uF 25V",
        "",
        "SMD",
        initial_stock=4,
        voltage="25V",
        location="ELECTROLYTIC CAPACITORES",
    )
    print(f"Add 1uF 25V electrolytic: {ok} — {msg}")

    if tracker.save_workbook(workbook):
        print("Saved.")
    else:
        print("Save failed — close stock.xlsx in Excel.")


if __name__ == "__main__":
    main()
