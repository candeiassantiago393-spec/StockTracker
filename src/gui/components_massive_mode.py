"""Passive (R/C) inventory mode embedded in the Components page."""
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
)

from src.core.stock import StockTracker

from . import styles
from .confirm_dialog import SiemensConfirmDialog
from .mode_detail_panel import build_detail_panel
from .massive_dialog import MassiveDialog
from .massive_search_dialog import MassiveSearchDialog
from .massive_table_dialog import MassiveTableDialog
from .history_dialog import HistoryDialog
from .message_dialog import SiemensMessage


class ComponentsMassiveMode:
    """Resistors / capacitors on sheet Generic — toggled inside Components."""

    def __init__(self, window) -> None:
        self.window = window
        self.tracker: StockTracker = window.tracker
        self._selected_row = None
        self._detail_labels: dict[str, QLabel] = {}
        self._panel: QWidget | None = None
        self._component_widgets: list[QWidget] = []

    def attach(self) -> None:
        grid = self.window.ui.gridLayout_right
        if not self._component_widgets:
            for index in range(grid.count()):
                item = grid.itemAt(index)
                if item is None:
                    continue
                widget = item.widget()
                if widget is None or widget.objectName() == "label_details":
                    continue
                self._component_widgets.append(widget)

        fields = (
            ("part_type", "Type"),
            ("value", "Value"),
            ("tolerance", "Tolerance"),
            ("package", "Package"),
            ("name", "Name"),
            ("stock", "Stock"),
            ("supplier_reference", "Supplier Ref"),
            ("dielectric", "Dielectric"),
            ("voltage", "Voltage"),
            ("notes", "Notes"),
            ("location", "Location"),
        )
        self._panel, self._detail_labels = build_detail_panel(
            self.window.ui.container_tab1_right,
            fields,
            on_copy=self.window._copy_to_clipboard,
        )

        grid.addWidget(self._panel, 1, 0, 10, 5)
        self._panel.hide()

    def set_active(self, active: bool) -> None:
        if self._panel is None:
            return
        self.window.ui.label_details.setText(
            "Passive Details" if active else "Component Details"
        )
        self._panel.setVisible(active)
        for widget in self._component_widgets:
            widget.setVisible(not active)
        if active:
            self.window.ui.row_barcode_entry.hide()
            self.window.ui.search_entry.setPlaceholderText(
                "Search value, package, name…"
            )
        else:
            if self.window._inventory_mode == "components":
                self.window.ui.row_barcode_entry.show()
                self.window.ui.search_entry.setPlaceholderText("")

    def set_status(self, text: str) -> None:
        self.window.set_status(text)

    def clear_fields(self) -> None:
        self._selected_row = None
        for label in self._detail_labels.values():
            label.clear()
            label.setToolTip("")

    @property
    def has_selection(self) -> bool:
        return self._selected_row is not None

    def show_item(self, row) -> None:
        self._selected_row = row
        data = self.tracker.massive_row_to_dict(row)
        mapping = {
            "part_type": self._format_type(data["part_type"]),
            "value": data["value"],
            "tolerance": data["tolerance"],
            "package": data["package"],
            "name": data["name"],
            "stock": str(data["stock"]),
            "supplier_reference": data["supplier_reference"],
            "dielectric": data["dielectric"],
            "voltage": data["voltage"],
            "notes": data["notes"],
            "location": data["location"],
        }
        for key, text in mapping.items():
            styles.set_mode_detail_text(self._detail_labels[key], text)

    @staticmethod
    def _format_type(part_type: str) -> str:
        if part_type == "R":
            return "Resistor (R)"
        if part_type == "C":
            return "Capacitor (C)"
        return part_type or "—"

    def search(self) -> None:
        if not self.window.validate_user():
            return
        query = self.window.ui.search_entry.text().strip()
        if not query:
            SiemensMessage.warning(self.window, "Passive", "Enter a search term.")
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_massive_sheet(workbook)
        matches = self.tracker.search_massive_all(sheet, query)
        if not matches:
            SiemensMessage.warning(self.window, "Passive", "No matching items found.")
            self.set_status("No Passive items found.")
            return
        if len(matches) == 1:
            self.show_item(matches[0])
            self.set_status("Passive item loaded.")
            return

        dialog = MassiveSearchDialog(
            matches,
            self.tracker.massive_row_to_dict,
            self.window,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.set_status("Search cancelled.")
            return
        row = dialog.selected_row()
        if row is None:
            return
        self.show_item(row)
        self.set_status(f"Selected 1 of {len(matches)} matches.")

    def add_item(self) -> None:
        if not self.window.validate_user():
            return
        dialog = MassiveDialog(self.window, title="Add Passive Item", allow_stock=True)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.set_status("Add Passive item cancelled.")
            return
        payload = dialog.payload()
        user = self.window.ui.user_entry.text().strip()
        ok, message = self.tracker.add_massive_item(
            user,
            payload["part_type"],
            payload["value"],
            payload["tolerance"],
            payload["package"],
            name=payload["name"],
            initial_stock=payload["initial_stock"],
            supplier_reference=payload["supplier_reference"],
            dielectric=payload["dielectric"],
            voltage=payload["voltage"],
            notes=payload["notes"],
            location=payload.get("location", ""),
        )
        if not ok:
            SiemensMessage.warning(self.window, "Passive", message)
            self.set_status(message)
            return

        self._reload_after_save(payload)
        self.set_status(message)
        SiemensMessage.information(self.window, "Added", message)

    def edit_item(self) -> None:
        if not self.window.validate_user():
            return
        if self._selected_row is None:
            SiemensMessage.warning(
                self.window, "Passive", "Search or select an item first."
            )
            return

        data = self.tracker.massive_row_to_dict(self._selected_row)
        dialog = MassiveDialog(
            self.window,
            initial=data,
            title="Edit Passive Item",
            allow_stock=False,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        payload = dialog.payload()
        ok, message = self.tracker.update_massive_item(
            self._selected_row,
            payload["part_type"],
            payload["value"],
            payload["tolerance"],
            payload["package"],
            name=payload["name"],
            supplier_reference=payload["supplier_reference"],
            dielectric=payload["dielectric"],
            voltage=payload["voltage"],
            notes=payload["notes"],
            location=payload.get("location", ""),
        )
        if not ok:
            SiemensMessage.warning(self.window, "Passive", message)
            self.set_status(message)
            return

        self._reload_selected_row()
        self.show_item(self._selected_row)
        self.set_status(message)
        SiemensMessage.information(self.window, "Updated", message)

    def update_stock(self, movement: str) -> None:
        if not self.window.validate_user():
            return
        if self._selected_row is None:
            SiemensMessage.warning(
                self.window, "Passive", "Search or select an item first."
            )
            return

        quantity_text = self.window.ui.quantity_entry.text().strip()
        if not quantity_text:
            SiemensMessage.warning(self.window, "Warning", "Enter quantity.")
            return
        try:
            quantity = int(quantity_text)
        except ValueError:
            SiemensMessage.warning(self.window, "Warning", "Quantity must be a number.")
            return
        if quantity <= 0:
            SiemensMessage.warning(self.window, "Warning", "Quantity must be greater than 0.")
            return

        user = self.window.ui.user_entry.text().strip()
        if movement == "OUT":
            data = self.tracker.massive_row_to_dict(self._selected_row)
            if not SiemensConfirmDialog.ask(
                "Confirm stock removal",
                f"Remove {quantity} from stock?\nCurrent stock: {data['stock']}",
                self.window,
            ):
                self.set_status("Stock removal cancelled.")
                return

        ok, message = self.tracker.update_massive_stock(
            user,
            self._selected_row,
            quantity,
            movement,
        )
        if not ok:
            SiemensMessage.warning(self.window, "Passive", message)
            self.set_status(message)
            return

        self._reload_selected_row()
        self.show_item(self._selected_row)
        self.window.ui.quantity_entry.clear()
        self.set_status(message)
        SiemensMessage.information(self.window, "Success", message)

    def open_history_all(self) -> None:
        if not self.window.validate_user():
            return
        workbook = self.tracker.get_workbook()
        rows = self.tracker.get_massive_rows(workbook)
        MassiveTableDialog(rows, self.window, title="Passive — last 20").exec()

    def open_history_filtered(self) -> None:
        if not self.window.validate_user():
            return
        if self._selected_row is None:
            SiemensMessage.warning(
                self.window, "Passive", "Search or select an item first."
            )
            return
        data = self.tracker.massive_row_to_dict(self._selected_row)
        ref = data["name"] or data["value"]
        workbook = self.tracker.get_workbook()
        rows = self.tracker.get_history_rows(
            workbook,
            component_only=True,
            mouser_ref=ref,
        )
        HistoryDialog(rows, self.window).exec()

    def _reload_selected_row(self) -> None:
        if self._selected_row is None:
            return
        row_idx = self._selected_row[0].row
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_massive_sheet(workbook)
        for row in sheet.iter_rows(min_row=row_idx, max_row=row_idx):
            self._selected_row = row
            break

    def _reload_after_save(self, payload: dict) -> None:
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_massive_sheet(workbook)
        row = self.tracker.find_massive_by_identity(
            sheet,
            payload["part_type"],
            payload["value"],
            payload["tolerance"],
            payload["package"],
            dielectric=payload.get("dielectric", ""),
        )
        if row is not None:
            self.show_item(row)
