"""Stock Tracker main window — uses StockTracker from src.core.stock."""
from pathlib import Path

from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtWidgets import QCompleter, QDialog, QMainWindow, QMessageBox

from src.core.stock import StockTracker
from src.core.suppliers import supplier_label
from src.core.suppliers.base import SupplierId
from src.core.suppliers.credentials import is_configured

from .history_dialog import HistoryDialog
from .manual_component_dialog import ManualComponentDialog
from .search_results_dialog import SearchResultsDialog


def _load_ui_class():
    """Prefer Qt Designer export when the generated file is complete."""
    try:
        from .designer.gui_stocktracker import Ui_StockTracker as DesignerUi

        designer_py = Path(__file__).resolve().parent / "designer" / "gui_stocktracker.py"
        source = designer_py.read_text(encoding="utf-8")
        required = ("barcode_entry", "supplier_combo", "val_stock", "btn_scan")
        if all(name in source for name in required):
            return DesignerUi
    except (ImportError, OSError):
        pass
    from .ui_stock_tracker import Ui_StockTracker

    return Ui_StockTracker


class StockTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tracker = StockTracker()
        Ui_StockTracker = _load_ui_class()
        self.ui = Ui_StockTracker()
        self.ui.setupUi(self)
        self._connect_signals()
        self._setup_supplier_combo()
        self._setup_autocompletes()
        self.ui.user_entry.setFocus()

    def _connect_signals(self):
        u = self.ui
        u.btn_search.clicked.connect(self.search_component_manual)
        u.btn_scan.clicked.connect(self.scan_component)
        u.btn_add_stock.clicked.connect(lambda: self.update_stock("IN"))
        u.btn_remove_stock.clicked.connect(lambda: self.update_stock("OUT"))
        u.btn_history_all.clicked.connect(lambda: self.open_history(False))
        u.btn_history_component.clicked.connect(lambda: self.open_history(True))
        if hasattr(u, "btn_add_manual"):
            u.btn_add_manual.clicked.connect(self.add_manual_component)
        u.btn_clear.clicked.connect(self.clear_all_fields)
        if hasattr(u, "btn_exit"):
            u.btn_exit.clicked.connect(self.close)

    def _make_completer(
        self, terms: list[str], filter_mode: Qt.MatchFlag
    ) -> QCompleter:
        completer = QCompleter(QStringListModel(terms), self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(filter_mode)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setMaxVisibleItems(12)
        return completer

    def _setup_supplier_combo(self) -> None:
        combo = self.ui.supplier_combo
        combo.clear()
        configured = self.tracker.configured_suppliers()
        if not configured:
            combo.addItem("No distributor API configured", "")
            combo.setEnabled(False)
            return
        combo.setEnabled(True)
        for supplier_id in configured:
            combo.addItem(supplier_label(supplier_id), supplier_id)
        default = "mouser" if "mouser" in configured else configured[0]
        index = combo.findData(default)
        if index >= 0:
            combo.setCurrentIndex(index)

    def _selected_supplier(self) -> SupplierId | None:
        supplier_id = self.ui.supplier_combo.currentData()
        if not supplier_id:
            return None
        return supplier_id

    def _setup_autocompletes(self) -> None:
        """Excel suggestions for search and barcode/supplier reference fields."""
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)

        self._search_completer = self._make_completer(
            self.tracker.excel_autocomplete_terms(sheet),
            Qt.MatchFlag.MatchContains,
        )
        self.ui.search_entry.setCompleter(self._search_completer)

        self._barcode_completer = self._make_completer(
            self.tracker.excel_autocomplete_supplier_refs(sheet),
            Qt.MatchFlag.MatchStartsWith,
        )
        self.ui.barcode_entry.setCompleter(self._barcode_completer)

    def _refresh_autocompletes(self) -> None:
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        if hasattr(self, "_search_completer"):
            self._search_completer.model().setStringList(
                self.tracker.excel_autocomplete_terms(sheet)
            )
        if hasattr(self, "_barcode_completer"):
            self._barcode_completer.model().setStringList(
                self.tracker.excel_autocomplete_supplier_refs(sheet)
            )

    def set_status(self, text: str) -> None:
        self.ui.status_label.setText(text)

    def validate_user(self) -> bool:
        if not self.ui.user_entry.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter user name.")
            self.ui.user_entry.setFocus()
            return False
        return True

    def show_component(self, row) -> None:
        data = self.tracker.row_to_dict(row)
        u = self.ui
        u.val_mouser.setText(str(data["mouser"]))
        u.val_manufacturer.setText(str(data["manufacturer"]))
        u.val_manufacturer_ref.setText(str(data["manufacturer_ref"]))
        u.val_description.setText(str(data["description"]))
        u.val_stock.setText(str(data["stock"]))

    def clear_inputs_after_action(self) -> None:
        self.ui.search_entry.clear()
        self.ui.barcode_entry.clear()
        self.ui.quantity_entry.clear()

    def clear_all_fields(self) -> None:
        u = self.ui
        u.search_entry.clear()
        u.barcode_entry.clear()
        u.quantity_entry.clear()
        u.val_mouser.clear()
        u.val_manufacturer.clear()
        u.val_manufacturer_ref.clear()
        u.val_description.clear()
        u.val_stock.clear()
        self.set_status("")

    def scan_component(self) -> None:
        if not self.validate_user():
            return

        code = self.ui.barcode_entry.text().strip()
        if not code:
            QMessageBox.warning(self, "Warning", "Please scan a barcode.")
            return

        if len(code) < 5:
            self.ui.barcode_entry.clear()
            self.set_status("Scan ignored: reference too short.")
            self.ui.barcode_entry.setFocus()
            return

        part_number = self.tracker.extract_part_number(code)
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        self.tracker.get_history_sheet(workbook)

        row = self.tracker.find_component_any(sheet, part_number, code)
        if row:
            self.show_component(row)
            self.ui.barcode_entry.setText(str(row[1].value or ""))
            self.set_status("Component found in Excel.")
            return

        supplier = self._selected_supplier()
        distributor_name = (
            supplier_label(supplier) if supplier else "distributor"
        )
        answer = QMessageBox.question(
            self,
            "Component not found",
            f"Component not found in Excel.\n\n"
            f"Search the {distributor_name} catalog?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        if supplier is None or not is_configured(supplier, self.tracker._secrets):
            QMessageBox.critical(
                self,
                "API credentials missing",
                "No distributor API is configured.\n\n"
                "Edit config/secrets.py (see secrets.example.py).",
            )
            return

        part = self.tracker.search_supplier(supplier, part_number)
        if part is None:
            QMessageBox.critical(
                self,
                "Distributor lookup failed",
                f"Could not search {distributor_name} or no result was found.\n\n"
                "Check internet, API credentials, and the part number.",
            )
            return

        supplier_reference = self.tracker.part_supplier_reference(
            part, part_number
        )
        manufacturer_ref = self.tracker.part_manufacturer_reference(part)

        if self.tracker.component_exists(
            sheet, supplier_reference, manufacturer_ref
        ):
            existing = self.tracker.find_component_any(
                sheet,
                supplier_reference,
                manufacturer_ref,
                part_number,
                code,
            )
            if existing:
                self.show_component(existing)
                self.ui.barcode_entry.setText(str(existing[1].value or ""))
                self.set_status("Component already exists in Excel.")
                QMessageBox.information(
                    self,
                    "Already exists",
                    "This component is already in Excel.",
                )
                return

        self.tracker.add_component_row(
            sheet,
            mouser_ref=supplier_reference,
            manufacturer=self.tracker.part_manufacturer(part),
            manufacturer_ref=manufacturer_ref,
            description=self.tracker.part_description(part),
            stock=0,
        )

        if not self.tracker.save_workbook(workbook):
            QMessageBox.critical(
                self,
                "Excel file is open",
                "Close stock.xlsx in Excel before saving.",
            )
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        self.ui.barcode_entry.setText(supplier_reference)
        added_row = self.tracker.find_component_any(
            sheet, supplier_reference, manufacturer_ref, part_number, code
        )
        if added_row:
            self.show_component(added_row)

        self._refresh_autocompletes()
        self.set_status(
            "New component added with stock 0. Enter quantity and click ADD STOCK."
        )
        QMessageBox.information(
            self,
            "Added",
            "New component added with stock 0. "
            "Now enter quantity and click ADD STOCK.",
        )

    def search_component_manual(self) -> None:
        if not self.validate_user():
            return

        query = self.ui.search_entry.text().strip()
        if not query:
            QMessageBox.warning(self, "Warning", "Write something to search.")
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        matches = self.tracker.search_in_excel_all(sheet, query)

        if not matches:
            QMessageBox.information(self, "Not found", "No component found.")
            return

        row = matches[0]
        if len(matches) > 1:
            dialog = SearchResultsDialog(
                matches, self.tracker.row_to_dict, parent=self
            )
            if dialog.exec() != QDialog.DialogCode.Accepted:
                self.set_status("Search cancelled.")
                return
            row = dialog.selected_row()
            if row is None:
                return

        self.ui.barcode_entry.setText(str(row[1].value or ""))
        self.show_component(row)
        count = len(matches)
        if count > 1:
            self.set_status(f"Selected 1 of {count} matches from Excel.")
        else:
            self.set_status("Component found by search.")

    def update_stock(self, movement: str) -> None:
        if not self.validate_user():
            return

        code = self.ui.barcode_entry.text().strip()
        quantity_text = self.ui.quantity_entry.text().strip()

        if not code or not quantity_text:
            QMessageBox.warning(
                self,
                "Warning",
                "Scan/search component and enter quantity.",
            )
            return

        if len(code) < 5:
            self.ui.barcode_entry.clear()
            self.set_status("Reference too short. Scan ignored.")
            return

        try:
            quantity = int(quantity_text)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Quantity must be a number.")
            return

        if quantity <= 0:
            QMessageBox.warning(self, "Warning", "Quantity must be greater than 0.")
            return

        part_number = self.tracker.extract_part_number(code)
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        row = self.tracker.find_component_any(sheet, part_number, code)
        if row is None:
            QMessageBox.critical(self, "Error", "Component not found.")
            return

        current_stock = int(row[6].value or 0)

        if movement == "OUT":
            if current_stock < quantity:
                QMessageBox.critical(self, "Error", "Not enough stock.")
                return

            new_stock = current_stock - quantity
            confirm = QMessageBox.question(
                self,
                "Confirm stock removal",
                f"Are you sure you want to remove stock?\n\n"
                f"Component: {row[1].value}\n"
                f"Quantity to remove: {quantity}\n"
                f"Current stock: {current_stock}\n"
                f"Stock after removal: {new_stock}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if confirm != QMessageBox.StandardButton.Yes:
                self.set_status("Stock removal cancelled.")
                return

        user = self.ui.user_entry.text().strip()
        if not self.tracker.update_stock(user, code, quantity, movement):
            QMessageBox.critical(
                self,
                "Excel file is open",
                "Close stock.xlsx in Excel before saving.",
            )
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        row = self.tracker.find_component_any(sheet, part_number, code)
        if row:
            self.show_component(row)

        self._refresh_autocompletes()
        self.set_status("Stock updated and history saved.")
        self.clear_inputs_after_action()
        QMessageBox.information(self, "Success", "Stock updated.")

    def open_history(self, component_only: bool) -> None:
        if not self.validate_user():
            return

        workbook = self.tracker.get_workbook()
        mouser_ref = self.ui.val_mouser.text().strip()
        rows = self.tracker.get_history_rows(
            workbook,
            component_only=component_only,
            mouser_ref=mouser_ref,
        )
        dialog = HistoryDialog(rows, self)
        dialog.exec()

    def add_manual_component(self) -> None:
        if not self.validate_user():
            return

        dialog = ManualComponentDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.set_status("Manual component creation cancelled.")
            return

        payload = dialog.payload()
        user = self.ui.user_entry.text().strip()
        ok, message = self.tracker.add_manual_component(
            user=user,
            supplier_reference=payload["supplier_reference"],
            manufacturer=payload["manufacturer"],
            manufacturer_reference=payload["manufacturer_reference"],
            description=payload["description"],
            initial_stock=payload["initial_stock"],
        )

        if not ok:
            QMessageBox.warning(self, "Manual component", message)
            self.set_status(message)
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        row = self.tracker.find_component_any(
            sheet,
            payload["supplier_reference"],
            payload["manufacturer_reference"],
            payload["manufacturer"],
        )
        if row:
            self.show_component(row)
            self.ui.barcode_entry.setText(str(row[1].value or ""))

        self._refresh_autocompletes()
        self.set_status(message)
