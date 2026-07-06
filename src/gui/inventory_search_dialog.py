"""Combined Components + Passive search results."""
from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QDialog, QTableWidget

from .designer.popups.components.gui_popup_search import Ui_PopupSearch
from .siemens_template.popup_shell import fill_readonly_table

COLUMNS = (
    "Source",
    "Type / Supplier Ref",
    "Value",
    "Package / Mfr Ref",
    "Name / Description",
    "Stock",
)


@dataclass(frozen=True)
class InventorySearchHit:
    kind: str  # "component" | "passive"
    row: object


class InventorySearchDialog(QDialog):
    def __init__(self, hits: list[InventorySearchHit], tracker, parent=None):
        super().__init__(parent)
        self._hits = hits
        self._tracker = tracker
        self._selected: InventorySearchHit | None = None

        self.ui = Ui_PopupSearch()
        self.ui.setupUi(self)
        if hasattr(self.ui, "tittle"):
            self.ui.tittle.setText("Inventory search results")
        self.ui.table_search.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.ui.table_search.doubleClicked.connect(self._accept_selection)

        table_rows = [self._hit_display(hit) for hit in hits]

        def values(data):
            return (
                data["source"],
                data["col2"],
                data["value"],
                data["col4"],
                data["col5"],
                data["stock"],
            )

        fill_readonly_table(
            self.ui.table_search,
            COLUMNS,
            table_rows,
            row_values=values,
        )

        if hits:
            self.ui.table_search.selectRow(0)

        self.ui.btn_ok.clicked.connect(self._accept_selection)
        self.ui.btn_cancel.clicked.connect(self.reject)

    def _hit_display(self, hit: InventorySearchHit) -> dict:
        if hit.kind == "passive":
            data = self._tracker.massive_row_to_dict(hit.row)
            part_type = str(data.get("part_type") or "").strip().upper()
            type_label = "Resistor" if part_type == "R" else "Capacitor" if part_type == "C" else part_type
            return {
                "source": "Passive",
                "col2": type_label,
                "value": data.get("value") or "—",
                "col4": data.get("package") or "—",
                "col5": data.get("name") or "—",
                "stock": data.get("stock", 0),
            }

        data = self._tracker.row_to_dict(hit.row)
        return {
            "source": "Component",
            "col2": data.get("mouser") or "—",
            "value": "—",
            "col4": data.get("manufacturer_ref") or "—",
            "col5": data.get("description") or "—",
            "stock": data.get("stock", 0),
        }

    def _accept_selection(self) -> None:
        row_idx = self.ui.table_search.currentRow()
        if row_idx < 0 or row_idx >= len(self._hits):
            return
        self._selected = self._hits[row_idx]
        self.accept()

    def selected_hit(self) -> InventorySearchHit | None:
        return self._selected
