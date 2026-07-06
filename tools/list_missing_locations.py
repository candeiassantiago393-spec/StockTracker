"""List inventory rows with stock > 0 but no location (Components + Generic)."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.stock import StockTracker


def _stock_int(value) -> int | None:
    if value is None or str(value).strip() == "":
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def main() -> None:
    tracker = StockTracker()
    wb = tracker.get_workbook()
    missing: list[dict] = []

    components = tracker.get_components_sheet(wb)
    for row in components.iter_rows(min_row=2, max_row=components.max_row):
        if tracker.row_is_empty(row):
            continue
        stock = _stock_int(row[6].value)
        if stock is None or stock <= 0:
            continue
        loc = str(row[7].value or "").strip() if len(row) >= 8 else ""
        if loc:
            continue
        data = tracker.row_to_dict(row)
        missing.append(
            {
                "sheet": "Components",
                "id": row[0].value,
                "reference": data["mouser"],
                "description": data["description"],
                "stock": stock,
            }
        )

    generic = tracker.get_massive_sheet(wb)
    for row in generic.iter_rows(min_row=2, max_row=generic.max_row):
        if tracker.row_is_empty(row) or tracker._massive_row_is_header(row):
            continue
        stock = _stock_int(row[6].value)
        if stock is None or stock <= 0:
            continue
        data = tracker.massive_row_to_dict(row)
        if data.get("location", "").strip():
            continue
        missing.append(
            {
                "sheet": "Generic",
                "id": data["id"],
                "reference": data.get("supplier_reference") or data.get("value"),
                "description": (
                    f"{data['part_type']} {data['value']} {data['tolerance']} "
                    f"{data['package']} — {data['name']}"
                ).strip(),
                "stock": stock,
            }
        )

    out_csv = PROJECT_ROOT / "data" / "missing_locations_report.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["sheet", "id", "reference", "description", "stock"],
        )
        writer.writeheader()
        writer.writerows(missing)

    comp_n = sum(1 for x in missing if x["sheet"] == "Components")
    gen_n = sum(1 for x in missing if x["sheet"] == "Generic")
    print(f"Total with stock > 0 and NO location: {len(missing)}")
    print(f"  Components: {comp_n}")
    print(f"  Generic (passives): {gen_n}")
    print(f"Report saved: {out_csv}")
    print()
    for item in missing[:50]:
        desc = str(item["description"])[:70]
        print(
            f"[{item['sheet']}] ID={item['id']} stock={item['stock']} "
            f"ref={item['reference']} — {desc}"
        )
    if len(missing) > 50:
        print(f"... and {len(missing) - 50} more (see CSV)")


if __name__ == "__main__":
    main()
