"""Export inventory statistics report to PDF."""
from __future__ import annotations

import html
from pathlib import Path

from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QPageLayout, QPageSize, QPdfWriter, QTextDocument

from src.core.inventory_report import build_inventory_report
from src.core.stock import StockTracker

from .location_combo import format_locations_display


def _esc(text) -> str:
    return html.escape(str(text if text is not None else ""))


def _table(headers: tuple[str, ...], rows: list[tuple]) -> str:
    if not rows:
        return "<p><em>No data.</em></p>"
    head = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{_esc(cell)}</td>" for cell in row)
        body_rows.append(f"<tr>{cells}</tr>")
    return (
        '<table border="1" cellspacing="0" cellpadding="4" width="100%">'
        f"<thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody></table>"
    )


def _report_html(data: dict) -> str:
    threshold = data["threshold"]
    sections: list[str] = [
        "<h1>Siemens Stock Tracker — Inventory Report</h1>",
        f"<p>Generated: {_esc(data['generated_at'])}</p>",
        f"<p>Low stock threshold: ≤ {_esc(threshold)} units</p>",
    ]

    dist = data.get("distribution") or []
    if dist:
        sections.append("<h2>Inventory overview</h2>")
        sections.append(
            _table(
                ("Category", "Items", "Stock units"),
                [
                    (item.get("label"), item.get("count"), item.get("stock"))
                    for item in dist
                ],
            )
        )

    missing = data.get("missing_location") or []
    sections.append(f"<h2>Stock without location ({len(missing)})</h2>")
    sections.append(
        _table(
            ("Sheet", "ID", "Reference", "Description", "Stock"),
            [
                (
                    item.get("sheet"),
                    item.get("id"),
                    item.get("reference"),
                    item.get("description"),
                    item.get("stock"),
                )
                for item in missing
            ],
        )
    )

    loc_stats = data.get("location_stats") or []
    sections.append(f"<h2>Storage locations ({len(loc_stats)})</h2>")
    sections.append(
        _table(
            ("Location", "Components", "Passive", "Equipments", "Low stock", "Units"),
            [
                (
                    item.get("location"),
                    item.get("components"),
                    item.get("passive"),
                    item.get("equipments"),
                    item.get("low_stock"),
                    item.get("stock_units"),
                )
                for item in loc_stats
            ],
        )
    )

    low_comp = data.get("low_components") or []
    sections.append(f"<h2>Components — low stock ({len(low_comp)})</h2>")
    sections.append(
        _table(
            ("Component", "Supplier ref", "Location", "Stock"),
            [
                (
                    item.get("label"),
                    item.get("mouser") or item.get("manufacturer_ref"),
                    format_locations_display(
                        StockTracker.parse_component_locations(
                            item.get("location", "")
                        )
                    )
                    or "—",
                    item.get("stock"),
                )
                for item in low_comp
            ],
        )
    )

    low_massive = data.get("low_massive") or []
    sections.append(f"<h2>Passive (R/C) — low stock ({len(low_massive)})</h2>")
    sections.append(
        _table(
            ("Name", "Value", "Package", "Location", "Stock"),
            [
                (
                    item.get("name"),
                    item.get("value"),
                    item.get("package"),
                    item.get("location") or "—",
                    item.get("stock"),
                )
                for item in low_massive
            ],
        )
    )

    equipments = data.get("equipments_expiry") or []
    sections.append(f"<h2>Equipments — calibration ({len(equipments)})</h2>")
    sections.append(
        _table(
            ("Name", "Serial", "Expiration", "Days left"),
            [
                (
                    item.get("name") or item.get("description"),
                    item.get("serial_number"),
                    item.get("calibration_expiration"),
                    item.get("days_left"),
                )
                for item in equipments
            ],
        )
    )

    loaned = data.get("loaned") or []
    sections.append(f"<h2>Equipments on loan ({len(loaned)})</h2>")
    sections.append(
        _table(
            ("Name", "Serial", "Loaned to", "Place", "Since"),
            [
                (
                    item.get("name") or item.get("description"),
                    item.get("serial_number"),
                    item.get("loaned_to"),
                    item.get("loan_place"),
                    item.get("loan_since"),
                )
                for item in loaned
            ],
        )
    )

    movements = data.get("movements") or []
    sections.append("<h2>Stock movements (weekly)</h2>")
    sections.append(
        _table(
            ("Week", "IN", "OUT"),
            [
                (entry.get("label"), entry.get("in"), entry.get("out"))
                for entry in movements
            ],
        )
    )

    style = """
    body { font-family: Arial, sans-serif; font-size: 10pt; color: #111; }
    h1 { font-size: 18pt; color: #006666; }
    h2 { font-size: 13pt; color: #006666; margin-top: 18px; }
    table { border-collapse: collapse; margin-bottom: 12px; }
    th { background: #e8f7f7; text-align: left; }
    td, th { padding: 4px 6px; }
    """
    return (
        f"<html><head><meta charset='utf-8'><style>{style}</style></head>"
        f"<body>{''.join(sections)}</body></html>"
    )


def export_inventory_report_pdf(tracker: StockTracker, output_path: Path) -> Path:
    """Write report PDF; returns absolute path to the created file."""
    target = Path(output_path).expanduser().resolve()
    if target.suffix.lower() != ".pdf":
        target = target.with_suffix(".pdf")
    target.parent.mkdir(parents=True, exist_ok=True)

    data = build_inventory_report(tracker)
    document = QTextDocument()
    document.setHtml(_report_html(data))

    writer = QPdfWriter(str(target))
    writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    writer.setPageMargins(
        QMarginsF(12, 12, 12, 12),
        QPageLayout.Unit.Millimeter,
    )
    document.print_(writer)

    if not target.is_file() or target.stat().st_size == 0:
        raise OSError(f"PDF was not created: {target}")
    return target
