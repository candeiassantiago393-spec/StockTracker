"""Search Components, Passives and Equipments from one dialog."""
from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
)

from src.core.stock import StockTracker

from . import styles
from .siemens_template.popup_shell import fill_readonly_table

COLUMNS = (
    "Source",
    "Reference",
    "Value / Name",
    "Details",
    "Stock",
)


@dataclass(frozen=True)
class GlobalSearchHit:
    kind: str  # component | passive | equipment
    row: object


class GlobalSearchDialog(QDialog):
    def __init__(self, tracker: StockTracker, main_window, parent=None):
        super().__init__(parent)
        self._tracker = tracker
        self._main = main_window
        self._hits: list[GlobalSearchHit] = []
        self._selected: GlobalSearchHit | None = None

        self.setWindowTitle("Global search")
        self.setMinimumSize(820, 480)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        title = QLabel("GLOBAL SEARCH")
        title.setStyleSheet("font-size: 20px; font-weight: 600; color: #00CCCC;")
        root.addWidget(title)

        hint = QLabel(
            "Search across Components, Passive (R/C) and Equipments. "
            "Press Enter or click Search."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #B3B3BE; font-size: 12px;")
        root.addWidget(hint)

        search_row = QHBoxLayout()
        self._entry = QLineEdit(self)
        self._entry.setStyleSheet(styles.EXPANDING_LINE_EDIT_STYLE)
        self._entry.setPlaceholderText("Reference, value, name, serial…")
        self._entry.returnPressed.connect(self._run_search)
        search_row.addWidget(self._entry, 1)

        self._btn_search = QPushButton("SEARCH")
        self._btn_search.setMinimumWidth(100)
        self._btn_search.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self._btn_search.clicked.connect(self._run_search)
        search_row.addWidget(self._btn_search)
        root.addLayout(search_row)

        self._status = QLabel("Type at least 2 characters to search.")
        self._status.setStyleSheet("color: #B3B3BE; font-size: 12px;")
        root.addWidget(self._status)

        self._table = QTableWidget(self)
        self._table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._table.doubleClicked.connect(self._accept_selection)
        root.addWidget(self._table, 1)

        buttons = QHBoxLayout()
        buttons.addStretch()
        self._btn_open = QPushButton("Open")
        self._btn_open.setMinimumWidth(100)
        self._btn_open.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self._btn_open.clicked.connect(self._accept_selection)
        self._btn_cancel = QPushButton("Close")
        self._btn_cancel.setMinimumWidth(100)
        self._btn_cancel.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self._btn_cancel.clicked.connect(self.reject)
        buttons.addWidget(self._btn_open)
        buttons.addWidget(self._btn_cancel)
        root.addLayout(buttons)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._entry.setFocus()

    def _run_search(self) -> None:
        query = self._entry.text().strip()
        if len(query) < 2:
            self._status.setText("Type at least 2 characters to search.")
            return

        self._hits = self._main.collect_global_search_hits(query)
        self._selected = None
        rows = [self._display(hit) for hit in self._hits]

        def values(data):
            return (
                data["source"],
                data["reference"],
                data["name"],
                data["details"],
                data["stock"],
            )

        fill_readonly_table(self._table, COLUMNS, rows, row_values=values)
        if self._hits:
            self._table.selectRow(0)

        count = len(self._hits)
        self._status.setText(
            f"{count} result(s) for “{query}”."
            if count
            else f"No results for “{query}”."
        )

    def _display(self, hit: GlobalSearchHit) -> dict:
        if hit.kind == "passive":
            data = self._tracker.massive_row_to_dict(hit.row)
            part = str(data.get("part_type") or "").upper()
            type_label = (
                "Resistor" if part == "R" else "Capacitor" if part == "C" else part
            )
            return {
                "source": "Passive",
                "reference": data.get("supplier_reference") or data.get("value") or "—",
                "name": data.get("value") or "—",
                "details": f"{type_label} {data.get('package') or ''} — {data.get('name') or ''}".strip(),
                "stock": data.get("stock", 0),
            }
        if hit.kind == "equipment":
            data = self._tracker.equipment_row_to_dict(hit.row)
            return {
                "source": "Equipment",
                "reference": data.get("supplier_reference") or "—",
                "name": data.get("name") or data.get("description") or "—",
                "details": data.get("serial_number") or "—",
                "stock": "—",
            }
        data = self._tracker.row_to_dict(hit.row)
        return {
            "source": "Component",
            "reference": data.get("mouser") or data.get("manufacturer_ref") or "—",
            "name": data.get("description") or "—",
            "details": data.get("manufacturer") or "—",
            "stock": data.get("stock", 0),
        }

    def _accept_selection(self) -> None:
        row_idx = self._table.currentRow()
        if row_idx < 0 or row_idx >= len(self._hits):
            return
        self._selected = self._hits[row_idx]
        self.accept()

    def selected_hit(self) -> GlobalSearchHit | None:
        return self._selected
