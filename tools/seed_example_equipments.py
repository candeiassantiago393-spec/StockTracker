# tools/seed_example_equipments.py
"""Seed example calibrated equipments and sample datasheets for demos."""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.equipment_storage import EquipmentStorage  # noqa: E402
from src.core.stock import StockTracker  # noqa: E402

EXAMPLE_DATASHEETS: dict[str, str] = {
    "DS_Rohde_RTM3004_Oscilloscope.pdf": (
        "Stock Tracker — sample datasheet\n"
        "Rohde & Schwarz RTM3004 Digital Oscilloscope\n"
        "Bandwidth: 4 GHz | Channels: 4\n"
    ),
    "DS_Keysight_34465A_Multimeter.pdf": (
        "Stock Tracker — sample datasheet\n"
        "Keysight 34465A 6.5 Digit Bench Multimeter\n"
        "Resolution: 6.5 digits | Interfaces: USB, LAN\n"
    ),
    "DS_Fluke_87V_Multimeter.pdf": (
        "Stock Tracker — sample datasheet\n"
        "Fluke 87V Industrial True-RMS Multimeter\n"
        "CAT IV 600 V | Temperature measurement\n"
    ),
    "DS_HIOKI_PW6001_Power_Analyzer.pdf": (
        "Stock Tracker — sample datasheet\n"
        "Hioki PW6001 Power Analyzer\n"
        "High accuracy power measurements for motor drives\n"
    ),
    "DS_Tektronix_AFG31000_Generator.pdf": (
        "Stock Tracker — sample datasheet\n"
        "Tektronix AFG31000 Arbitrary Function Generator\n"
        "250 MS/s sample rate | 14-bit vertical resolution\n"
    ),
}

EXAMPLE_EQUIPMENTS = [
    {
        "supplier_reference": "R&S-RTM3004-001",
        "serial_number": "SN-OSC-2024-001",
        "name": "Oscilloscope RTM3004",
        "description": "Oscilloscope Rohde & Schwarz RTM3004",
        "datasheet": "DS_Rohde_RTM3004_Oscilloscope.pdf",
        "calibration_months_ago": 3,
        "valid_months": 12,
    },
    {
        "supplier_reference": "KEYS-34465A-01",
        "serial_number": "SN-DMM-2023-014",
        "name": "Multimeter 34465A",
        "description": "Multimeter Keysight 34465A",
        "datasheet": "DS_Keysight_34465A_Multimeter.pdf",
        "calibration_months_ago": 6,
        "valid_months": 24,
    },
    {
        "supplier_reference": "FLUKE-87V-LAB",
        "serial_number": "SN-FLK-87V-8821",
        "name": "Multimeter 87V",
        "description": "Multimeter Fluke 87V",
        "datasheet": "DS_Fluke_87V_Multimeter.pdf",
        "calibration_months_ago": 2,
        "valid_months": 12,
    },
    {
        "supplier_reference": "HIOKI-PW6001",
        "serial_number": "SN-PWR-2024-003",
        "name": "Power analyzer PW6001",
        "description": "Power analyzer Hioki PW6001",
        "datasheet": "DS_HIOKI_PW6001_Power_Analyzer.pdf",
        "calibration_months_ago": 4,
        "valid_months": 12,
    },
    {
        "supplier_reference": "TEK-AFG31000",
        "serial_number": "SN-AFG-2022-109",
        "name": "Generator AFG31000",
        "description": "Function generator Tektronix AFG31000",
        "datasheet": "DS_Tektronix_AFG31000_Generator.pdf",
        "calibration_months_ago": 8,
        "valid_months": 24,
    },
]


def _dates(months_ago: int, valid_months: int) -> tuple[str, str]:
    today = date.today()
    calib = today - timedelta(days=months_ago * 30)
    expiry = calib + timedelta(days=valid_months * 30)
    return calib.isoformat(), expiry.isoformat()


def _write_equipment_datasheet(
    storage: EquipmentStorage, equipment_id: str | int, name: str, body: str
) -> None:
    path = storage.ensure_equipment_dir(equipment_id) / name
    if not path.exists():
        path.write_text(body, encoding="utf-8")


def seed_equipments(*, skip_existing: bool = True) -> int:
    tracker = StockTracker()
    tracker.ensure_workbook_sheets()
    storage = EquipmentStorage()

    added = 0
    workbook = tracker.get_workbook()
    sheet = tracker.get_equipments_sheet(workbook)

    for item in EXAMPLE_EQUIPMENTS:
        ref = item["supplier_reference"]
        if skip_existing and tracker.find_equipment_by_supplier_ref(sheet, ref):
            continue
        calib, expiry = _dates(item["calibration_months_ago"], item["valid_months"])
        ok, message = tracker.add_equipment(
            supplier_reference=ref,
            serial_number=item["serial_number"],
            name=item.get("name", ""),
            description=item["description"],
            calibration_date=calib,
            calibration_expiration=expiry,
            datasheet=item["datasheet"],
        )
        if ok:
            added += 1
            print(f"  + {item['description']}")
            workbook = tracker.get_workbook()
            sheet = tracker.get_equipments_sheet(workbook)
            row = tracker.find_equipment_by_supplier_ref(sheet, ref)
            if row is not None:
                eq_id = tracker.equipment_row_to_dict(row)["id"]
                ds_name = item["datasheet"]
                _write_equipment_datasheet(
                    storage, eq_id, ds_name, EXAMPLE_DATASHEETS[ds_name]
                )
        else:
            print(f"  ! {ref}: {message}")
        workbook = tracker.get_workbook()
        sheet = tracker.get_equipments_sheet(workbook)

    return added


def main() -> None:
    print("Stock Tracker — example equipments")
    print(f"Equipment folders: {EquipmentStorage().ensure_root()}")
    count = seed_equipments()
    print(f"Done. Added {count} equipment(s).")


if __name__ == "__main__":
    main()
