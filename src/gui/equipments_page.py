"""Equipments inventory page — layout from designer/gui_equipments.ui."""

from pathlib import Path

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QFontMetrics, QGuiApplication, QPixmap
from PySide6.QtWidgets import QDialog, QFileDialog, QLabel, QLineEdit, QListWidgetItem, QWidget

from src.core.equipment_images import EquipmentImages, is_image_file
from src.core.stock import StockTracker
from src.core.support_documentation import SupportDocument, SupportDocumentation

from . import styles

from .designer.gui_equipments import Ui_EquipmentsPage
from .equipment_dialog import EquipmentDialog
from .equipment_search_dialog import EquipmentSearchDialog
from .confirm_dialog import SiemensConfirmDialog
from .message_dialog import SiemensMessage


_IMAGE_FILE_FILTER = (
    "Images (*.png *.jpg *.jpeg *.webp *.bmp *.gif);;All files (*.*)"
)


_IMAGE_PLACEHOLDER = "Drop image here"

_MAX_IGNORABLE_SCAN_LEN = 4


class _EquipmentImageDropFilter(QObject):
    """Accept image file drops on the equipment preview label."""

    def __init__(self, page: "EquipmentsPage") -> None:
        super().__init__(page)
        self._page = page

    def _set_drag_highlight(self, active: bool) -> None:
        preview = self._page.ui.equipment_image_preview
        if active:
            preview.setStyleSheet(styles.EQUIPMENT_IMAGE_PREVIEW_DRAG_STYLE)
            preview.setText("Release to add image")
            return
        preview.setStyleSheet(styles.EQUIPMENT_IMAGE_PREVIEW_STYLE)
        self._page._restore_image_placeholder_text()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        preview = self._page.ui.equipment_image_preview
        if obj is not preview:
            return False
        if event.type() == QEvent.Type.DragEnter:
            mime = event.mimeData()
            if mime.hasUrls() and any(
                url.isLocalFile() and is_image_file(url.toLocalFile())
                for url in mime.urls()
            ):
                self._set_drag_highlight(True)
                event.acceptProposedAction()
                return True
            return False
        if event.type() == QEvent.Type.DragLeave:
            self._set_drag_highlight(False)
            return False
        if event.type() == QEvent.Type.Drop:
            self._set_drag_highlight(False)
            mime = event.mimeData()
            if mime.hasUrls():
                for url in mime.urls():
                    if url.isLocalFile():
                        path = Path(url.toLocalFile())
                        if is_image_file(path):
                            self._page._associate_image_file(path)
                            event.acceptProposedAction()
                            return True
            return False
        return False


class EquipmentsPage(QWidget):

    """Second stacked page: search and manage calibrated equipments."""



    def __init__(self, tracker: StockTracker, main_window):

        super().__init__()

        self.tracker = tracker

        self.main = main_window

        self._selected_row = None

        self._support_docs = SupportDocumentation()

        self._equipment_images = EquipmentImages()

        self._doc_results: list[SupportDocument] = []

        self.ui = Ui_EquipmentsPage()

        self.ui.setupUi(self)

        self._setup_support_doc_tooltips()

        self._setup_doc_list()

        self._setup_equipment_image()

        self._setup_empty_details_click_targets()

        self._connect_signals()



    def _setup_doc_list(self) -> None:

        self.ui.doc_results_list.setVerticalScrollBarPolicy(

            Qt.ScrollBarPolicy.ScrollBarAsNeeded

        )

        self.ui.doc_results_list.setHorizontalScrollBarPolicy(

            Qt.ScrollBarPolicy.ScrollBarAsNeeded

        )

        self._hide_doc_results_list()



    def _hide_doc_results_list(self) -> None:

        self._doc_results = []

        self.ui.doc_results_list.clear()

        self.ui.doc_results_list.setVisible(False)



    def _show_doc_results_list(self, documents: list[SupportDocument]) -> None:

        self._doc_results = documents

        self.ui.doc_results_list.clear()

        for index, doc in enumerate(documents):

            item = QListWidgetItem(doc.name)

            item.setData(Qt.ItemDataRole.UserRole, str(doc.path))

            self.ui.doc_results_list.addItem(item)

            if index == 0:

                self.ui.doc_results_list.setCurrentRow(0)

        self.ui.doc_results_list.setVisible(True)



    def _setup_support_doc_tooltips(self) -> None:

        self.ui.btn_doc_open.setToolTip(

            "Open the selected document from the list, or the linked datasheet"

        )

        self.ui.btn_open_support_docs.setToolTip("Open support documentation folder")

        self.ui.btn_add_support_doc.setToolTip("Add a document to the support folder")

        self.ui.btn_link_datasheet.setToolTip(

            "Link the selected document to the current equipment"

        )

        self.ui.btn_scan_supplier_ref.setToolTip(

            "Look up equipment by supplier reference / barcode"

        )



    def _setup_equipment_image(self) -> None:

        preview = self.ui.equipment_image_preview

        preview.setAcceptDrops(True)

        preview.setToolTip("Drag and drop an image file here")

        self._image_drop_filter = _EquipmentImageDropFilter(self)

        preview.installEventFilter(self._image_drop_filter)

        self.ui.btn_set_equipment_image.setToolTip("Add or replace equipment image")

        self.ui.btn_clear_equipment_image.setToolTip("Delete equipment image")

        self._clear_equipment_image_display()

        self._update_image_buttons()



    def _update_image_buttons(self) -> None:

        has_selection = self._selected_row is not None

        has_image = False

        if has_selection:

            data = self.tracker.equipment_row_to_dict(self._selected_row)

            has_image = bool(str(data.get("image", "")).strip())

        self.ui.btn_set_equipment_image.setVisible(has_selection)

        self.ui.btn_clear_equipment_image.setVisible(has_selection and has_image)



    def _setup_empty_details_click_targets(self) -> None:

        """Clicking empty Equipment Details fields opens Add Equipment dialog."""

        pairs = (

            ("row_val_supplier_reference", "val_supplier_reference"),

            ("row_val_serial_number", "val_serial_number"),

            ("row_val_description", "val_description"),

            ("row_val_calibration", "val_calibration"),

            ("row_val_expiration", "val_expiration"),

            ("row_val_datasheet", "val_datasheet"),

        )

        self._detail_click_targets: list[tuple[QWidget, QWidget]] = []

        for row_name, value_name in pairs:

            row = getattr(self.ui, row_name, None)

            value = getattr(self.ui, value_name, None)

            if row is None or value is None:

                continue

            self._detail_click_targets.append((row, value))

            title = getattr(self.ui, f"title_{value_name}", None)

            click_targets = [w for w in (row, value, title) if w is not None]

            for widget in click_targets:

                widget.mousePressEvent = (  # type: ignore[method-assign]

                    lambda event, w=value: self._on_empty_detail_click(w, event)

                )

        self._refresh_empty_detail_cursor()



    @staticmethod

    def _widget_text(widget: QWidget) -> str:

        if isinstance(widget, (QLabel, QLineEdit)):

            return widget.text().strip()

        return ""



    def _detail_value_empty(self, value_widget: QWidget) -> bool:

        text = self._widget_text(value_widget)

        if value_widget is self.ui.val_datasheet and text == "(not linked)":

            return True

        return text == ""



    def _refresh_empty_detail_cursor(self) -> None:

        for row, value in getattr(self, "_detail_click_targets", []):

            clickable = self._detail_value_empty(value)

            cursor = (

                Qt.CursorShape.PointingHandCursor

                if clickable

                else Qt.CursorShape.ArrowCursor

            )

            row.setCursor(cursor)

            value.setCursor(cursor)

            title = getattr(self.ui, f"title_{value.objectName()}", None)

            if title is not None:

                title.setCursor(cursor)



    def _on_empty_detail_click(self, value_widget: QWidget, _event) -> None:

        if not self._detail_value_empty(value_widget):

            return

        self.add_equipment()



    def _restore_image_placeholder_text(self) -> None:

        label = self.ui.equipment_image_preview

        if label.pixmap() is not None and not label.pixmap().isNull():

            return

        label.setText(_IMAGE_PLACEHOLDER)



    def _clear_equipment_image_display(self, placeholder: str = _IMAGE_PLACEHOLDER) -> None:

        label = self.ui.equipment_image_preview

        label.setStyleSheet(styles.EQUIPMENT_IMAGE_PREVIEW_STYLE)

        label.clear()

        label.setPixmap(QPixmap())

        label.setText(placeholder)



    def _show_equipment_image(self, filename: str) -> None:

        name = str(filename).strip()

        if not name:

            self._clear_equipment_image_display()

            self._update_image_buttons()

            return

        path = self._equipment_images.resolve_path(name)

        if path is None:

            self._clear_equipment_image_display(placeholder="Image not found")

            self._update_image_buttons()

            return

        pixmap = QPixmap(str(path))

        if pixmap.isNull():

            self._clear_equipment_image_display(placeholder="Invalid image")

            self._update_image_buttons()

            return

        label = self.ui.equipment_image_preview

        label.setStyleSheet(styles.EQUIPMENT_IMAGE_PREVIEW_STYLE)

        scaled = pixmap.scaled(

            label.width(),

            label.height(),

            Qt.AspectRatioMode.KeepAspectRatio,

            Qt.TransformationMode.SmoothTransformation,

        )

        label.setPixmap(scaled)

        label.setText("")

        self._update_image_buttons()



    def _associate_image_file(self, source: Path) -> None:

        if self._selected_row is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Search or select an equipment first.",

            )

            return

        data = self.tracker.equipment_row_to_dict(self._selected_row)

        old_image = str(data.get("image", "")).strip()

        ok, result = self._equipment_images.add_image(source, data["id"])

        if not ok:

            SiemensMessage.warning(self, "Image", result)

            self.set_status(result)

            return

        if old_image and old_image != result:

            self._equipment_images.remove_image(old_image)

        ok, message = self.tracker.link_equipment_image(self._selected_row, result)

        if not ok:

            SiemensMessage.warning(self, "Image", message)

            self.set_status(message)

            return

        self._reload_selected_row()

        self._show_equipment_image(result)

        self.set_status(f"Image linked: {result}")

        SiemensMessage.information(self, "Image", message)



    def _set_equipment_image(self) -> None:

        if self._selected_row is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Search or select an equipment first.",

            )

            return

        file_path, _ = QFileDialog.getOpenFileName(

            self,

            "Select equipment image",

            "",

            _IMAGE_FILE_FILTER,

        )

        if not file_path:

            self.set_status("Image selection cancelled.")

            return

        self._associate_image_file(Path(file_path))



    def _clear_equipment_image(self) -> None:

        if self._selected_row is None:

            return

        data = self.tracker.equipment_row_to_dict(self._selected_row)

        old_image = str(data.get("image", "")).strip()

        if not old_image:

            return

        ok, remove_msg = self._equipment_images.remove_image(old_image)

        if not ok:

            SiemensMessage.warning(self, "Image", remove_msg)

            self.set_status(remove_msg)

            return

        ok, message = self.tracker.unlink_equipment_image(self._selected_row)

        if not ok:

            SiemensMessage.warning(self, "Image", message)

            self.set_status(message)

            return

        self._reload_selected_row()

        self._clear_equipment_image_display()

        self._update_image_buttons()

        self.set_status("Equipment image deleted.")

        SiemensMessage.information(self, "Image", message)



    def _format_datasheet_display(self, filename: str) -> str:

        name = str(filename).strip()

        if not name:

            return "(not linked)"

        return name



    def _elide_label_text(self, label, text: str) -> str:

        width = label.width() if label.width() > 0 else 100

        return QFontMetrics(label.font()).elidedText(

            text, Qt.TextElideMode.ElideRight, width

        )



    def _set_datasheet_display(self, filename: str) -> None:

        display = self._format_datasheet_display(filename)

        label = self.ui.val_datasheet

        label.setText(self._elide_label_text(label, display))

        label.setToolTip(

            f"Datasheet: {display}" if display != "(not linked)" else "No datasheet linked"

        )

        self._refresh_empty_detail_cursor()



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

        self.ui.supplier_ref_entry.returnPressed.connect(self._on_supplier_ref_scanned)

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

        self.ui.btn_set_equipment_image.clicked.connect(self._set_equipment_image)

        self.ui.btn_clear_equipment_image.clicked.connect(self._clear_equipment_image)

        self._setup_copy_buttons()



    def _setup_copy_buttons(self) -> None:

        fields = (

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



    def show_equipment(self, row, *, open_datasheet: bool = False) -> None:

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

        self._show_equipment_image(str(data.get("image", "")))

        if datasheet:

            self.set_status(f"Equipment loaded. Datasheet: {datasheet}")

        elif open_datasheet:

            self.set_status("No datasheet found.")

        else:

            self.set_status("Equipment loaded. Datasheet: (not linked)")

        self._refresh_empty_detail_cursor()

        if open_datasheet:

            self._prompt_open_equipment_datasheet(datasheet)



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

        self._hide_doc_results_list()

        self._clear_equipment_image_display()

        self._update_image_buttons()

        self._refresh_empty_detail_cursor()

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



    def _is_ignorable_scan(self, text: str) -> bool:
        code = str(text or "").strip()
        return bool(code) and len(code) <= _MAX_IGNORABLE_SCAN_LEN

    def _clear_ignorable_scan(self) -> None:
        self.ui.supplier_ref_entry.clear()
        self.main.set_status("Short scan ignored — scan the part reference.")
        self.ui.supplier_ref_entry.setFocus()

    def _on_supplier_ref_scanned(self) -> None:
        ref = self.ui.supplier_ref_entry.text().strip()
        if self._is_ignorable_scan(ref):
            self._clear_ignorable_scan()
            return
        self.lookup_supplier_ref()

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

        if self._is_ignorable_scan(ref):
            self._clear_ignorable_scan()
            return

        self.lookup_supplier_ref()



    def lookup_supplier_ref(self) -> None:

        if not self.main.validate_user():

            return



        ref = self.ui.supplier_ref_entry.text().strip()

        if not ref:

            return

        if self._is_ignorable_scan(ref):
            self._clear_ignorable_scan()
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



        self.show_equipment(row, open_datasheet=True)

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

            self.show_equipment(row, open_datasheet=True)



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



        self.show_equipment(row, open_datasheet=True)

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



    def _prompt_open_equipment_datasheet(self, filename: str) -> None:

        name = str(filename).strip()

        if not name:

            return

        if self._support_docs.document_for_filename(name) is None:

            self.set_status(f"Datasheet not found: {name}")

            return

        if SiemensConfirmDialog.ask(

            "Open datasheet",

            "Open the datasheet for this equipment?",

            self,

        ):

            self._open_equipment_datasheet_file(name)



    def _open_equipment_datasheet_file(self, filename: str) -> None:

        name = str(filename).strip()

        if not name:

            return

        document = self._support_docs.document_for_filename(name)

        if document is None:

            self.set_status(f"Datasheet not found: {name}")

            return

        ok, message = self._support_docs.open_document(document)

        if not ok:

            SiemensMessage.critical(self, "Open failed", message)

        else:

            self.set_status(message)



    def link_datasheet_to_equipment(self) -> None:

        if self._selected_row is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Search or select an equipment first.",

            )

            return

        if not self.ui.doc_results_list.isVisible():

            SiemensMessage.warning(

                self,

                "Warning",

                "Search for documents first, then select one from the list.",

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

        self.set_status(f"Datasheet linked: {filename}")

        SiemensMessage.information(self, "Linked", message)



    def search_support_document(self) -> None:

        query = self.ui.doc_search_entry.text().strip()

        documents = self._support_docs.list_documents(query)

        if not documents:

            self._hide_doc_results_list()

            SiemensMessage.information(

                self,

                "Not found",

                "No support document found in the documentation folder.",

            )

            self.set_status("No support document found.")

            return

        self._show_doc_results_list(documents)

        count = len(documents)

        if count == 1:

            self.set_status("1 document found. Select OPEN or double-click to open.")

        else:

            self.set_status(f"{count} documents found. Select one and press OPEN.")



    def open_selected_support_document(self) -> None:

        if self.ui.doc_results_list.isVisible():

            item = self.ui.doc_results_list.currentItem()

            if item is not None:

                path = Path(item.data(Qt.ItemDataRole.UserRole))

                ok, message = self._support_docs.open_document(path)

                if not ok:

                    SiemensMessage.critical(self, "Open failed", message)

                self.set_status(message)

                return

        display = self.ui.val_datasheet.text().strip()

        if display and display != "(not linked)":

            document = self._support_docs.document_for_filename(display)

            if document is not None:

                ok, message = self._support_docs.open_document(document)

                if not ok:

                    SiemensMessage.critical(self, "Open failed", message)

                self.set_status(message)

                return

        SiemensMessage.warning(

            self,

            "Warning",

            "Search for documents first, then select one from the list.",

        )



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


