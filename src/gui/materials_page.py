"""Materials inventory page — layout from designer/gui_materials.ui."""
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QDialog, QLineEdit, QWidget

from src.core.stock import StockTracker

from .designer.gui_materials import Ui_MaterialsPage
from .material_dialog import MaterialDialog
from .material_search_dialog import MaterialSearchDialog
from .message_dialog import SiemensMessage


class MaterialsPage(QWidget):
    """Second stacked page: search and manage calibrated materials."""

    def __init__(self, tracker: StockTracker, main_window):
        super().__init__()
        self.tracker = tracker
        self.main = main_window
        self._selected_row = None
        self.ui = Ui_MaterialsPage()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.ui.btn_search.clicked.connect(self.search_material)
        self.ui.supplier_ref_entry.returnPressed.connect(self.lookup_supplier_ref)
        self._setup_copy_buttons()

    def _setup_copy_buttons(self) -> None:
        fields = (
            ("btn_copy_supplier_ref", "supplier_ref_entry", "Supplier reference"),
            ("btn_copy_val_supplier_reference", "val_supplier_reference", "Supplier Reference"),
            ("btn_copy_val_serial_number", "val_serial_number", "Serial Number"),
            ("btn_copy_val_description", "val_description", "Description"),
            ("btn_copy_val_calibration", "val_calibration", "Calibration Date"),
            ("btn_copy_val_expiration", "val_expiration", "Calibration Expiration"),
        )
        for btn_name, value_name, label in fields:
            btn = getattr(self.ui, btn_name, None)
            value = getattr(self.ui, value_name, None)
            if btn is None or value is None:
                continue
            btn.clicked.connect(
                lambda _checked=False, widget=value, field=label: self._copy_to_clipboard(
                    widget, field
                )
            )

    def _copy_to_clipboard(self, widget, field_name: str) -> None:
        if isinstance(widget, QLineEdit):
            text = widget.text().strip()
        else:
            text = widget.text().strip()
        if not text:
            self.set_status(f"Nothing to copy ({field_name}).")
            return
        QGuiApplication.clipboard().setText(text)
        self.set_status(f"Copied {field_name} to clipboard.")

    def set_status(self, text: str) -> None:
        self.main.set_status(text)

    @property
    def search_entry(self):
        return self.ui.search_entry

    @property
    def supplier_ref_entry(self):
        return self.ui.supplier_ref_entry

    @property
    def val_supplier_reference(self):
        return self.ui.val_supplier_reference

    @property
    def val_serial_number(self):
        return self.ui.val_serial_number

    @property
    def val_description(self):
        return self.ui.val_description

    @property
    def val_calibration(self):
        return self.ui.val_calibration

    @property
    def val_expiration(self):
        return self.ui.val_expiration

    def show_material(self, row) -> None:
        self._selected_row = row
        data = self.tracker.material_row_to_dict(row)
        self.ui.supplier_ref_entry.setText(str(data["supplier_reference"]))
        self.ui.val_supplier_reference.setText(str(data["supplier_reference"]))
        self.ui.val_serial_number.setText(str(data["serial_number"]))
        self.ui.val_description.setText(str(data["description"]))
        self.ui.val_calibration.setText(str(data["calibration_date"]))
        self.ui.val_expiration.setText(str(data["calibration_expiration"]))

    def clear_fields(self) -> None:
        self._selected_row = None
        self.ui.search_entry.clear()
        self.ui.supplier_ref_entry.clear()
        self.ui.val_supplier_reference.clear()
        self.ui.val_serial_number.clear()
        self.ui.val_description.clear()
        self.ui.val_calibration.clear()
        self.ui.val_expiration.clear()
        self.set_status("")

    def _resolve_search_query(self) -> str:
        return (
            self.ui.search_entry.text().strip()
            or self.ui.supplier_ref_entry.text().strip()
        )

    def search_material(self) -> None:
        if not self.main.validate_user():
            return

        query = self._resolve_search_query()
        if not query:
            SiemensMessage.warning(self, "Warning", "Write something to search.")
            return

        self._search_and_show(query)

    def lookup_supplier_ref(self) -> None:
        if not self.main.validate_user():
            return

        ref = self.ui.supplier_ref_entry.text().strip()
        if not ref:
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_materials_sheet(workbook)
        row = self.tracker.find_material_by_supplier_ref(sheet, ref)
        if row is None:
            matches = self.tracker.search_materials_all(sheet, ref)
            if len(matches) == 1:
                row = matches[0]
            elif len(matches) > 1:
                self._pick_from_matches(matches)
                return
            else:
                SiemensMessage.information(self, "Not found", "No material found.")
                return

        self.show_material(row)
        self.set_status("Material found by supplier reference.")

    def _pick_from_matches(self, matches: list) -> None:
        dialog = MaterialSearchDialog(
            matches, self.tracker.material_row_to_dict, parent=self
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.set_status("Search cancelled.")
            return
        row = dialog.selected_row()
        if row is not None:
            self.show_material(row)

    def _search_and_show(self, query: str) -> None:
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_materials_sheet(workbook)
        matches = self.tracker.search_materials_all(sheet, query)

        if not matches:
            SiemensMessage.information(self, "Not found", "No material found.")
            return

        row = matches[0]
        if len(matches) > 1:
            self._pick_from_matches(matches)
            return

        self.show_material(row)
        self.set_status("Material found.")

    def add_material(self) -> None:
        if not self.main.validate_user():
            return

        dialog = MaterialDialog(self, title="Add Material")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.set_status("Add material cancelled.")
            return

        payload = dialog.payload()
        ok, message = self.tracker.add_material(
            description=payload["description"],
            supplier_reference=payload["supplier_reference"],
            serial_number=payload["serial_number"],
            calibration_date=payload["calibration_date"],
            calibration_expiration=payload["calibration_expiration"],
        )
        if not ok:
            SiemensMessage.warning(self, "Material", message)
            self.set_status(message)
            return

        self._refresh_after_save(payload)
        self.set_status(message)
        SiemensMessage.information(self, "Added", message)

    def edit_material(self) -> None:
        if not self.main.validate_user():
            return

        if self._selected_row is None:
            SiemensMessage.warning(
                self,
                "Warning",
                "Search or select a material first.",
            )
            return

        data = self.tracker.material_row_to_dict(self._selected_row)
        dialog = MaterialDialog(self, initial=data, title="Edit Material")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        payload = dialog.payload()
        ok, message = self.tracker.update_material(
            self._selected_row,
            description=payload["description"],
            supplier_reference=payload["supplier_reference"],
            serial_number=payload["serial_number"],
            calibration_date=payload["calibration_date"],
            calibration_expiration=payload["calibration_expiration"],
        )
        if not ok:
            SiemensMessage.critical(self, "Error", message)
            return

        self._refresh_after_save(payload)
        self.set_status(message)
        SiemensMessage.information(self, "Updated", message)

    def _refresh_after_save(self, payload: dict) -> None:
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_materials_sheet(workbook)
        row = None
        if payload.get("supplier_reference"):
            row = self.tracker.find_material_by_supplier_ref(
                sheet, payload["supplier_reference"]
            )
        if row is None and payload.get("serial_number"):
            matches = self.tracker.search_materials_all(sheet, payload["serial_number"])
            if matches:
                row = matches[0]
        if row is None and payload.get("description"):
            matches = self.tracker.search_materials_all(sheet, payload["description"])
            if matches:
                row = matches[0]
        if row is not None:
            self.show_material(row)
