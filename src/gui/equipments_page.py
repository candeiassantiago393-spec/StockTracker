"""Equipments inventory page — layout from designer/gui_equipments.ui."""

from pathlib import Path



from PySide6.QtCore import Qt

from PySide6.QtGui import QGuiApplication

from PySide6.QtWidgets import QDialog, QFileDialog, QLineEdit, QListWidgetItem, QWidget



from src.core.stock import StockTracker

from src.core.support_documentation import SupportDocument, SupportDocumentation



from .designer.gui_equipments import Ui_EquipmentsPage

from .equipment_dialog import EquipmentDialog

from .equipment_search_dialog import EquipmentSearchDialog

from .message_dialog import SiemensMessage





class EquipmentsPage(QWidget):

    """Second stacked page: search and manage calibrated equipments."""



    def __init__(self, tracker: StockTracker, main_window):

        super().__init__()

        self.tracker = tracker

        self.main = main_window

        self._selected_row = None

        self._support_docs = SupportDocumentation()

        self._doc_results: list[SupportDocument] = []

        self.ui = Ui_EquipmentsPage()

        self.ui.setupUi(self)

        self._setup_support_doc_tooltips()

        self._setup_doc_list_scroll()

        self._connect_signals()



    def _setup_doc_list_scroll(self) -> None:

        self.ui.doc_results_list.setVerticalScrollBarPolicy(

            Qt.ScrollBarPolicy.ScrollBarAsNeeded

        )

        self.ui.doc_results_list.setHorizontalScrollBarPolicy(

            Qt.ScrollBarPolicy.ScrollBarAsNeeded

        )



    def _setup_support_doc_tooltips(self) -> None:

        self.ui.btn_doc_open.setToolTip("Open the selected document from the list")

        self.ui.btn_open_support_docs.setToolTip("Open support documentation folder")

        self.ui.btn_add_support_doc.setToolTip("Add a document to the support folder")

        self.ui.btn_link_datasheet.setToolTip(

            "Link the selected document to the current equipment"

        )

        self.ui.btn_scan_supplier_ref.setToolTip(

            "Look up equipment by supplier reference / barcode"

        )



    def _format_datasheet_display(self, filename: str) -> str:

        name = str(filename).strip()

        if not name:

            return "(not linked)"

        return name



    def _set_datasheet_display(self, filename: str) -> None:

        display = self._format_datasheet_display(filename)

        self.ui.val_datasheet.setText(display)

        self.ui.val_datasheet.setToolTip(

            f"Datasheet: {display}" if display != "(not linked)" else "No datasheet linked"

        )



    def _reload_selected_row(self) -> None:

        if self._selected_row is None:

            return

        row_idx = self._selected_row[0].row

        workbook = self.tracker.get_workbook()

        sheet = self.tracker.get_equipments_sheet(workbook)

        for row in sheet.iter_rows(min_row=row_idx, max_row=row_idx):

            self._selected_row = row

            break



    def _connect_signals(self) -> None:

        self.ui.btn_search.clicked.connect(self.search_equipment)

        self.ui.supplier_ref_entry.returnPressed.connect(self.lookup_supplier_ref)

        self.ui.btn_scan_supplier_ref.clicked.connect(self.scan_supplier_ref)

        self.ui.btn_doc_search.clicked.connect(self.search_support_document)

        self.ui.doc_search_entry.returnPressed.connect(self.search_support_document)

        self.ui.btn_doc_open.clicked.connect(self.open_selected_support_document)

        self.ui.doc_results_list.itemDoubleClicked.connect(

            self.open_selected_support_document

        )

        self.ui.btn_open_support_docs.clicked.connect(self.open_support_documentation_folder)

        self.ui.btn_add_support_doc.clicked.connect(self.add_support_document)

        self.ui.btn_link_datasheet.clicked.connect(self.link_datasheet_to_equipment)

        self._setup_copy_buttons()



    def _setup_copy_buttons(self) -> None:

        fields = (

            ("btn_copy_supplier_ref", "supplier_ref_entry", "Supplier reference"),

            ("btn_copy_val_supplier_reference", "val_supplier_reference", "Supplier Reference"),

            ("btn_copy_val_serial_number", "val_serial_number", "Serial Number"),

            ("btn_copy_val_description", "val_description", "Description"),

            ("btn_copy_val_calibration", "val_calibration", "Calibration Date"),

            ("btn_copy_val_expiration", "val_expiration", "Calibration Expiration"),

            ("btn_copy_val_datasheet", "val_datasheet", "Datasheet"),

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



    def show_equipment(self, row, *, open_datasheet: bool = True) -> None:

        self._selected_row = row

        data = self.tracker.equipment_row_to_dict(row)

        self.ui.supplier_ref_entry.setText(str(data["supplier_reference"]))

        self.ui.val_supplier_reference.setText(str(data["supplier_reference"]))

        self.ui.val_serial_number.setText(str(data["serial_number"]))

        self.ui.val_description.setText(str(data["description"]))

        self.ui.val_calibration.setText(str(data["calibration_date"]))

        self.ui.val_expiration.setText(str(data["calibration_expiration"]))

        datasheet = str(data.get("datasheet", ""))

        self._set_datasheet_display(datasheet)

        self._load_equipment_datasheet(datasheet, open_datasheet=open_datasheet)

        if datasheet:

            self.set_status(f"Equipment loaded. Datasheet: {datasheet}")

        else:

            self.set_status("Equipment loaded. Datasheet: (not linked)")



    def clear_fields(self) -> None:

        self._selected_row = None

        self.ui.search_entry.clear()

        self.ui.supplier_ref_entry.clear()

        self.ui.val_supplier_reference.clear()

        self.ui.val_serial_number.clear()

        self.ui.val_description.clear()

        self.ui.val_calibration.clear()

        self.ui.val_expiration.clear()

        self._set_datasheet_display("")

        self.ui.doc_results_list.clear()

        self.set_status("")



    def _resolve_search_query(self) -> str:

        return (

            self.ui.search_entry.text().strip()

            or self.ui.supplier_ref_entry.text().strip()

        )



    def search_equipment(self) -> None:

        if not self.main.validate_user():

            return



        query = self._resolve_search_query()

        if not query:

            SiemensMessage.warning(self, "Warning", "Write something to search.")

            return



        self._search_and_show(query)



    def scan_supplier_ref(self) -> None:

        if not self.main.validate_user():

            return

        ref = self.ui.supplier_ref_entry.text().strip()

        if not ref:

            SiemensMessage.warning(

                self,

                "Warning",

                "Please scan or type a supplier reference.",

            )

            return

        self.lookup_supplier_ref()



    def lookup_supplier_ref(self) -> None:

        if not self.main.validate_user():

            return



        ref = self.ui.supplier_ref_entry.text().strip()

        if not ref:

            return



        workbook = self.tracker.get_workbook()

        sheet = self.tracker.get_equipments_sheet(workbook)

        row = self.tracker.find_equipment_by_supplier_ref(sheet, ref)

        if row is None:

            matches = self.tracker.search_equipments_all(sheet, ref)

            if len(matches) == 1:

                row = matches[0]

            elif len(matches) > 1:

                self._pick_from_matches(matches)

                return

            else:

                SiemensMessage.information(self, "Not found", "No equipment found.")

                return



        self.show_equipment(row)

        self.set_status("Equipment found by supplier reference.")



    def _pick_from_matches(self, matches: list) -> None:

        dialog = EquipmentSearchDialog(

            matches, self.tracker.equipment_row_to_dict, parent=self

        )

        if dialog.exec() != QDialog.DialogCode.Accepted:

            self.set_status("Search cancelled.")

            return

        row = dialog.selected_row()

        if row is not None:

            self.show_equipment(row)



    def _search_and_show(self, query: str) -> None:

        workbook = self.tracker.get_workbook()

        sheet = self.tracker.get_equipments_sheet(workbook)

        matches = self.tracker.search_equipments_all(sheet, query)



        if not matches:

            SiemensMessage.information(self, "Not found", "No equipment found.")

            return



        row = matches[0]

        if len(matches) > 1:

            self._pick_from_matches(matches)

            return



        self.show_equipment(row)

        self.set_status("Equipment found.")



    def add_equipment(self) -> None:

        if not self.main.validate_user():

            return



        dialog = EquipmentDialog(self, title="Add Equipment")

        if dialog.exec() != QDialog.DialogCode.Accepted:

            self.set_status("Add equipment cancelled.")

            return



        payload = dialog.payload()

        ok, message = self.tracker.add_equipment(

            description=payload["description"],

            supplier_reference=payload["supplier_reference"],

            serial_number=payload["serial_number"],

            calibration_date=payload["calibration_date"],

            calibration_expiration=payload["calibration_expiration"],

            datasheet=payload["datasheet"],

        )

        if not ok:

            SiemensMessage.warning(self, "Equipment", message)

            self.set_status(message)

            return



        self._refresh_after_save(payload)

        self.set_status(message)

        SiemensMessage.information(self, "Added", message)



    def edit_equipment(self) -> None:

        if not self.main.validate_user():

            return



        if self._selected_row is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Search or select an equipment first.",

            )

            return



        data = self.tracker.equipment_row_to_dict(self._selected_row)

        dialog = EquipmentDialog(self, initial=data, title="Edit Equipment")

        if dialog.exec() != QDialog.DialogCode.Accepted:

            return



        payload = dialog.payload()

        ok, message = self.tracker.update_equipment(

            self._selected_row,

            description=payload["description"],

            supplier_reference=payload["supplier_reference"],

            serial_number=payload["serial_number"],

            calibration_date=payload["calibration_date"],

            calibration_expiration=payload["calibration_expiration"],

            datasheet=payload["datasheet"],

        )

        if not ok:

            SiemensMessage.critical(self, "Error", message)

            return



        self._refresh_after_save(payload)

        self.set_status(message)

        SiemensMessage.information(self, "Updated", message)



    def _refresh_after_save(self, payload: dict) -> None:

        workbook = self.tracker.get_workbook()

        sheet = self.tracker.get_equipments_sheet(workbook)

        row = None

        if payload.get("supplier_reference"):

            row = self.tracker.find_equipment_by_supplier_ref(

                sheet, payload["supplier_reference"]

            )

        if row is None and payload.get("serial_number"):

            matches = self.tracker.search_equipments_all(sheet, payload["serial_number"])

            if matches:

                row = matches[0]

        if row is None and payload.get("description"):

            matches = self.tracker.search_equipments_all(sheet, payload["description"])

            if matches:

                row = matches[0]

        if row is not None:

            self.show_equipment(row)



    def _populate_doc_results_list(self, documents: list[SupportDocument]) -> None:

        self._doc_results = documents

        self.ui.doc_results_list.clear()

        for index, doc in enumerate(documents):

            item = QListWidgetItem(doc.name)

            item.setData(Qt.ItemDataRole.UserRole, str(doc.path))

            self.ui.doc_results_list.addItem(item)

            if index == 0:

                self.ui.doc_results_list.setCurrentRow(0)



    def _load_equipment_datasheet(self, filename: str, *, open_datasheet: bool) -> None:

        self.ui.doc_results_list.clear()

        self._doc_results = []

        name = str(filename).strip()

        if not name:

            return

        document = self._support_docs.document_for_filename(name)

        if document is None:

            self.set_status(f"Datasheet not found: {name}")

            return

        self._populate_doc_results_list([document])

        if open_datasheet:

            ok, message = self._support_docs.open_document(document)

            if not ok:

                SiemensMessage.critical(self, "Open failed", message)

            else:

                self.set_status(f"Equipment loaded. {message}")



    def link_datasheet_to_equipment(self) -> None:

        if self._selected_row is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Search or select an equipment first.",

            )

            return

        item = self.ui.doc_results_list.currentItem()

        if item is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Select a document from the list to link.",

            )

            return

        filename = Path(item.data(Qt.ItemDataRole.UserRole)).name

        ok, message = self.tracker.link_equipment_datasheet(self._selected_row, filename)

        if not ok:

            SiemensMessage.warning(self, "Link datasheet", message)

            self.set_status(message)

            return

        self._reload_selected_row()

        self._set_datasheet_display(filename)

        self._load_equipment_datasheet(filename, open_datasheet=False)

        self.set_status(f"Datasheet linked: {filename}")

        SiemensMessage.information(self, "Linked", message)



    def search_support_document(self) -> None:

        query = self.ui.doc_search_entry.text().strip()

        documents = self._support_docs.list_documents(query)



        if not documents:

            self._doc_results = []

            self.ui.doc_results_list.clear()

            SiemensMessage.information(

                self,

                "Not found",

                "No support document found in the documentation folder.",

            )

            self.set_status("No support document found.")

            return



        self._populate_doc_results_list(documents)

        count = len(documents)

        if count == 1:

            self.set_status("1 document found. Select OPEN or double-click to open.")

        else:

            self.set_status(f"{count} documents found. Select one and press OPEN.")



    def open_selected_support_document(self) -> None:

        item = self.ui.doc_results_list.currentItem()

        if item is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Search for documents first, then select one from the list.",

            )

            return



        path = Path(item.data(Qt.ItemDataRole.UserRole))

        ok, message = self._support_docs.open_document(path)

        if not ok:

            SiemensMessage.critical(self, "Open failed", message)

        self.set_status(message)



    def open_support_documentation_folder(self) -> None:

        ok, message = self._support_docs.open_folder()

        if not ok:

            SiemensMessage.critical(self, "Open folder failed", message)

            return

        self.set_status(message)



    def add_support_document(self) -> None:

        file_path, _ = QFileDialog.getOpenFileName(

            self,

            "Add support document",

            "",

            "Documents (*.pdf *.doc *.docx *.xls *.xlsx *.txt *.zip);;All files (*.*)",

        )

        if not file_path:

            self.set_status("Add document cancelled.")

            return



        ok, message = self._support_docs.add_document(Path(file_path))

        if not ok:

            SiemensMessage.warning(self, "Add document", message)

            self.set_status(message)

            return



        self.set_status(message)

        SiemensMessage.information(self, "Added", message)

        if self._selected_row is not None and message.startswith("Added "):

            filename = message[6:].rstrip(".")

            ok_link, link_msg = self.tracker.link_equipment_datasheet(

                self._selected_row, filename

            )

            if ok_link:

                self._reload_selected_row()

                self._set_datasheet_display(filename)

                self.set_status(f"Datasheet linked: {filename}")

        self.search_support_document()


