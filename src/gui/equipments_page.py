"""Equipments inventory page — layout from designer/gui_equipments.ui."""

from pathlib import Path

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QFontMetrics, QGuiApplication
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidgetItem,
    QWidget,
)

from src.core.equipment_images import EquipmentImages, is_image_file
from src.core.equipment_storage import EquipmentStorage, SupportDocument
from src.core.stock import StockTracker

from . import styles

from .confirm_dialog import SiemensConfirmDialog
from .designer.gui_equipments import Ui_EquipmentsPage
from .equipment_loan_dialog import EquipmentLoanDialog
from .equipment_dialog import EquipmentDialog
from .equipment_image_gallery import EquipmentImageGallery
from .equipment_search_dialog import EquipmentSearchDialog
from .message_dialog import SiemensMessage


_IMAGE_FILE_FILTER = (
    "Images (*.png *.jpg *.jpeg *.webp *.bmp *.gif);;All files (*.*)"
)


_IMAGE_PLACEHOLDER = "Drop image here"

# value widget | Excel field key | dialog title | dialog label | date field
_DETAIL_EDIT_FIELDS: tuple[tuple[str, str, str, str, bool], ...] = (
    ("val_supplier_reference", "supplier_reference", "Supplier reference", "Supplier reference:", False),
    ("val_serial_number", "serial_number", "Serial number", "Serial number:", False),
    ("val_name", "name", "Equipment name", "Name:", False),
    ("val_description", "description", "Description", "Description:", False),
    ("val_calibration", "calibration_date", "Calibration date", "Calibration date (YYYY-MM-DD):", True),
    ("val_expiration", "calibration_expiration", "Calibration expiration", "Expiration date (YYYY-MM-DD):", True),
    ("val_datasheet", "datasheet", "Datasheet", "Datasheet filename:", False),
)


class _EquipmentImageDropFilter(QObject):
    """Accept image file drops on the equipment preview label."""

    def __init__(self, page: "EquipmentsPage") -> None:
        super().__init__(page)
        self._page = page

    def _set_drag_highlight(self, active: bool) -> None:
        gallery = self._page._image_gallery
        if active:
            gallery.set_drag_highlight(True)
            return
        gallery.set_drag_highlight(False)
        self._page._restore_image_placeholder_text()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        gallery = self._page._image_gallery
        if obj is not gallery:
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

        self._storage = EquipmentStorage()

        self._equipment_images = EquipmentImages()

        self._doc_results: list[SupportDocument] = []

        self._datasheet_filename = ""

        self._loan_checkbox_blocked = False

        self.ui = Ui_EquipmentsPage()

        self.ui.setupUi(self)

        self._setup_support_doc_tooltips()

        self._setup_doc_list()

        self._setup_equipment_image()

        self._setup_location_panel()

        self._setup_detail_field_clicks()

        self._connect_signals()



    def _equipment_id(self) -> str:

        if self._selected_row is None:

            return ""

        return str(self.tracker.equipment_row_to_dict(self._selected_row).get("id", ""))



    def _equipment_folder_key(self, row=None) -> tuple[str, str]:

        target = row if row is not None else self._selected_row

        if target is None:

            return "", ""

        data = self.tracker.equipment_row_to_dict(target)

        return str(data["id"]), str(data.get("name", "")).strip()



    def _sync_equipment_folder(self, row=None) -> Path:

        target = row if row is not None else self._selected_row

        if target is None:

            return self._storage.ensure_root()

        eq_id, eq_name = self._equipment_folder_key(target)

        return self._storage.ensure_equipment_dir(eq_id, eq_name)



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

        self.ui.btn_open_support_docs.setToolTip(

            "Open this equipment folder (datasheet + image)"

        )

        self.ui.btn_add_support_doc.setToolTip("Add a document to the support folder")

        self.ui.btn_link_datasheet.setToolTip(

            "Link the selected document to the current equipment"

        )

        self.ui.btn_scan_supplier_ref.setToolTip(

            "Look up equipment by supplier reference / barcode"

        )



    def _setup_equipment_image(self) -> None:

        layout = self.ui.layout_equipment_image_panel
        preview = self.ui.equipment_image_preview
        index = layout.indexOf(preview)
        layout.removeWidget(preview)
        preview.hide()

        self._image_gallery = EquipmentImageGallery(self.ui.equipment_image_panel)
        self._image_gallery.setMinimumHeight(styles.EQUIPMENT_IMAGE_PREVIEW_HEIGHT)
        self._image_gallery.setAcceptDrops(True)
        layout.insertWidget(index, self._image_gallery)

        self._image_drop_filter = _EquipmentImageDropFilter(self)
        self._image_gallery.installEventFilter(self._image_drop_filter)

        self.ui.btn_set_equipment_image.setToolTip("Add another equipment image")
        self.ui.btn_clear_equipment_image.setToolTip(
            "Delete selected image (click a thumbnail first), or the last image"
        )

        self._clear_equipment_image_display()
        self._update_image_buttons()



    def _setup_location_panel(self) -> None:

        label = self.ui.val_equipment_location

        label.mousePressEvent = lambda event: self._on_location_click(event)  # type: ignore[method-assign]

        self.ui.chk_equipment_loaned.stateChanged.connect(

            self._on_loan_checkbox_changed

        )

        self._refresh_location_display(empty=True)



    def _current_user(self) -> str:

        return self.main.ui.user_entry.text().strip()



    def _refresh_location_display(self, *, empty: bool = False) -> None:

        chk = self.ui.chk_equipment_loaned

        label = self.ui.val_equipment_location

        self._loan_checkbox_blocked = True

        if empty or self._selected_row is None:

            label.setText("(not set)")

            label.setToolTip("Load an equipment to see location")

            label.setCursor(Qt.CursorShape.ArrowCursor)

            chk.setChecked(False)

            chk.setEnabled(False)

            self._loan_checkbox_blocked = False

            return

        data = self.tracker.equipment_row_to_dict(self._selected_row)

        chk.setEnabled(True)

        if data.get("loaned"):

            loaned_to = str(data.get("loaned_to", "")).strip()

            place = str(data.get("loan_place", "")).strip()

            since = str(data.get("loan_since", "")).strip()

            parts = [f"Loaned to {loaned_to} @ {place}"]

            if since:

                parts.append(f"since {since}")

            home = str(data.get("location", "")).strip()

            if home:

                parts.append(f"(home: {home})")

            label.setText(" — ".join(parts))

            label.setToolTip("Equipment is on loan")

            label.setCursor(Qt.CursorShape.ArrowCursor)

            chk.setChecked(True)

        else:

            home = str(data.get("location", "")).strip() or "(not set)"

            label.setText(home)

            label.setToolTip("Click to set home location")

            label.setCursor(Qt.CursorShape.PointingHandCursor)

            chk.setChecked(False)

        self._loan_checkbox_blocked = False



    def _on_location_click(self, _event) -> None:

        if self._selected_row is None:

            return

        data = self.tracker.equipment_row_to_dict(self._selected_row)

        if data.get("loaned"):

            return

        if not self.main.validate_user():

            return

        current = str(data.get("location", "")).strip()

        new_location, accepted = QInputDialog.getText(

            self,

            "Equipment location",

            "Home location (when not on loan):",

            text=current,

        )

        if not accepted:

            return

        ok, message = self.tracker.set_equipment_location(

            self._selected_row,

            new_location.strip(),

            user=self._current_user(),

        )

        if not ok:

            SiemensMessage.warning(self, "Location", message)

            self.set_status(message)

            return

        self._reload_selected_row()

        self._refresh_location_display()

        self.set_status(message)



    def _on_loan_checkbox_changed(self, state: int) -> None:

        if self._loan_checkbox_blocked:

            return

        if self._selected_row is None:

            self._refresh_location_display(empty=True)

            return

        if not self.main.validate_user():

            self._refresh_location_display()

            return

        checked = state == Qt.CheckState.Checked.value

        data = self.tracker.equipment_row_to_dict(self._selected_row)

        user = self._current_user()

        if checked:

            dialog = EquipmentLoanDialog(

                self,

                initial=data,

                title="Loan equipment",

            )

            if dialog.exec() != QDialog.DialogCode.Accepted:

                self._refresh_location_display()

                return

            payload = dialog.payload()

            ok, message = self.tracker.loan_equipment_out(

                self._selected_row,

                user=user,

                loaned_to=payload["loaned_to"],

                place=payload["loan_place"],

                home_location=payload["location"],

                notes=payload["notes"],

            )

            if not ok:

                SiemensMessage.warning(self, "Loan", message)

                self._refresh_location_display()

                self.set_status(message)

                return

            self._reload_selected_row()

            self._refresh_location_display()

            self.set_status(message)

            SiemensMessage.information(self, "Loaned", message)

            return

        if not data.get("loaned"):

            return

        if not SiemensConfirmDialog.ask(

            "Return equipment",

            "Mark this equipment as returned to its home location?",

            self,

        ):

            self._refresh_location_display()

            return

        ok, message = self.tracker.return_equipment_loan(

            self._selected_row,

            user=user,

        )

        if not ok:

            SiemensMessage.warning(self, "Return", message)

            self._refresh_location_display()

            self.set_status(message)

            return

        self._reload_selected_row()

        self._refresh_location_display()

        self.set_status(message)

        SiemensMessage.information(self, "Returned", message)



    def _update_image_buttons(self) -> None:

        has_selection = self._selected_row is not None

        has_image = bool(self._equipment_image_filenames()) if has_selection else False

        self.ui.btn_set_equipment_image.setVisible(has_selection)

        self.ui.btn_clear_equipment_image.setVisible(has_selection and has_image)

    def _equipment_image_filenames(self, row=None) -> list[str]:
        target = row if row is not None else self._selected_row
        if target is None:
            return []

        data = self.tracker.equipment_row_to_dict(target)
        eq_id, eq_name = self._equipment_folder_key(target)
        from_excel = self.tracker.parse_equipment_images(data.get("image", ""))
        from_folder = self._storage.list_equipment_images(eq_id, equipment_name=eq_name)

        merged: list[str] = []
        seen: set[str] = set()
        for name in from_excel + from_folder:
            if name not in seen:
                seen.add(name)
                merged.append(name)
        return merged



    def _setup_detail_field_clicks(self) -> None:

        """Click Equipment Details fields to quick-edit or open Add Equipment."""

        self._detail_field_specs: dict[QWidget, dict] = {}
        self._detail_field_click_targets: list[tuple[QWidget, QWidget]] = []

        for value_name, data_key, title, label, is_date in _DETAIL_EDIT_FIELDS:
            row = getattr(self.ui, f"row_{value_name}", None)
            value = getattr(self.ui, value_name, None)
            if row is None or value is None:
                continue

            spec = {
                "data_key": data_key,
                "title": title,
                "label": label,
                "is_date": is_date,
            }
            self._detail_field_specs[value] = spec
            self._detail_field_click_targets.append((row, value))
            value.setToolTip(f"Click to set or edit {title.lower()}")

            title_widget = getattr(self.ui, f"title_{value_name}", None)
            click_targets = [w for w in (row, value, title_widget) if w is not None]
            for widget in click_targets:
                widget.mousePressEvent = (  # type: ignore[method-assign]
                    lambda event, w=value: self._on_detail_field_click(w, event)
                )

        self._refresh_detail_field_cursors()

    def _detail_field_current_value(self, value_widget: QWidget, data: dict) -> str:
        spec = self._detail_field_specs.get(value_widget)
        if spec is None:
            return self._widget_text(value_widget)
        return str(data.get(spec["data_key"], "")).strip()

    def _on_detail_field_click(self, value_widget: QWidget, _event) -> None:
        if self._selected_row is not None:
            spec = self._detail_field_specs.get(value_widget)
            if spec is not None:
                self._edit_equipment_field(value_widget, spec)
            return
        if self._detail_value_empty(value_widget):
            self.add_equipment()

    def _find_equipment_row_from_payload(self, payload: dict):
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
        if row is None and payload.get("name"):
            matches = self.tracker.search_equipments_all(sheet, payload["name"])
            if matches:
                row = matches[0]
        if row is None and payload.get("description"):
            matches = self.tracker.search_equipments_all(sheet, payload["description"])
            if matches:
                row = matches[0]
        return row

    def _install_datasheet_for_row(
        self,
        row,
        *,
        source: Path | None = None,
        filename: str = "",
    ) -> str | None:
        """Copy a datasheet file into the equipment folder and link it in Excel."""
        if row is None:
            return None

        eq_id, eq_name = self._equipment_folder_key(row)
        resolved_source = source
        if resolved_source is None and filename:
            candidate = Path(filename)
            if candidate.is_file():
                resolved_source = candidate

        if resolved_source is None or not resolved_source.is_file():
            return str(filename).strip() or None

        folder = self._storage.ensure_equipment_dir(eq_id, eq_name)
        if resolved_source.parent.resolve() == folder.resolve():
            installed_name = resolved_source.name
        else:
            ok, installed_name = self._storage.install_datasheet(
                resolved_source, eq_id, equipment_name=eq_name
            )
            if not ok:
                SiemensMessage.warning(self, "Datasheet", installed_name)
                self.set_status(installed_name)
                return None

        link_ok, link_msg = self.tracker.link_equipment_datasheet(row, installed_name)
        if not link_ok:
            SiemensMessage.warning(self, "Datasheet", link_msg)
            self.set_status(link_msg)
            return None

        return installed_name

    def _equipment_payload_from_row(self, data: dict) -> dict:
        return {
            "description": data["description"],
            "supplier_reference": data["supplier_reference"],
            "serial_number": data["serial_number"],
            "name": data.get("name", ""),
            "calibration_date": data["calibration_date"],
            "calibration_expiration": data["calibration_expiration"],
        }

    def _edit_equipment_field(self, value_widget: QWidget, spec: dict) -> None:
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
        data_key = spec["data_key"]
        current = self._detail_field_current_value(value_widget, data)

        if data_key == "datasheet":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select datasheet",
                "",
                "Documents (*.pdf *.doc *.docx *.xls *.xlsx *.txt *.zip);;All files (*.*)",
            )
            if not file_path:
                self.set_status("Datasheet edit cancelled.")
                return
            installed = self._install_datasheet_for_row(
                self._selected_row, source=Path(file_path)
            )
            if not installed:
                return
            self._reload_selected_row()
            self.show_equipment(self._selected_row)
            self.set_status(f"Datasheet linked: {installed}")
            return

        new_value, accepted = QInputDialog.getText(
            self,
            spec["title"],
            spec["label"],
            text=current,
        )
        if not accepted:
            self.set_status(f"{spec['title']} edit cancelled.")
            return

        new_value = new_value.strip()
        if spec["is_date"]:
            ok, normalized = self.tracker.validate_date(new_value)
            if not ok:
                SiemensMessage.warning(
                    self,
                    "Equipment",
                    "Invalid date (use YYYY-MM-DD or leave empty).",
                )
                return
            new_value = normalized

        if new_value == current:
            return

        payload = self._equipment_payload_from_row(data)
        update_kwargs = dict(payload)
        if data_key == "datasheet":
            ok, message = self.tracker.update_equipment(
                self._selected_row,
                datasheet=new_value,
                **payload,
            )
        else:
            update_kwargs[data_key] = new_value
            ok, message = self.tracker.update_equipment(
                self._selected_row,
                **update_kwargs,
            )

        if not ok:
            SiemensMessage.warning(self, "Equipment", message)
            self.set_status(message)
            return

        self._reload_selected_row()
        self.show_equipment(self._selected_row)
        self.set_status(message)



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



    def _refresh_detail_field_cursors(self) -> None:

        for row, value in getattr(self, "_detail_field_click_targets", []):
            clickable = (
                self._selected_row is not None or self._detail_value_empty(value)
            )
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



    def _restore_image_placeholder_text(self) -> None:
        if self._equipment_image_filenames():
            return
        self._image_gallery.show_placeholder(_IMAGE_PLACEHOLDER)

    def _clear_equipment_image_display(self, placeholder: str = _IMAGE_PLACEHOLDER) -> None:
        self._image_gallery.show_placeholder(placeholder)

    def _show_equipment_images(self, filenames: list[str] | None = None) -> None:
        names = list(filenames or [])
        if not names:
            self._clear_equipment_image_display()
            self._update_image_buttons()
            return

        eq_id, eq_name = self._equipment_folder_key()
        items: list[tuple[str, Path]] = []
        missing: list[str] = []

        for name in names:
            path = (
                self._equipment_images.resolve_path(
                    name, eq_id, equipment_name=eq_name
                )
                if eq_id
                else None
            )
            if path is None:
                missing.append(name)
                continue
            items.append((name, path))

        if not items:
            text = "Image not found" if missing else _IMAGE_PLACEHOLDER
            self._clear_equipment_image_display(placeholder=text)
            self._update_image_buttons()
            return

        self._image_gallery.show_images(items)
        self._update_image_buttons()

    def _show_equipment_image(self, filename: str) -> None:
        names = self._equipment_image_filenames()
        if filename and filename not in names:
            names.append(filename)
        self._show_equipment_images(names)



    def _associate_image_file(self, source: Path) -> None:

        if self._selected_row is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Search or select an equipment first.",

            )

            return

        data = self.tracker.equipment_row_to_dict(self._selected_row)

        eq_name = str(data.get("name", "")).strip()

        ok, result = self._equipment_images.add_image(

            source, data["id"], equipment_name=eq_name

        )

        if not ok:

            SiemensMessage.warning(self, "Image", result)

            self.set_status(result)

            return

        ok, message = self.tracker.append_equipment_image(self._selected_row, result)

        if not ok:

            SiemensMessage.warning(self, "Image", message)

            self.set_status(message)

            return

        self._reload_selected_row()

        self._show_equipment_images(self._equipment_image_filenames())

        self.set_status(f"Image added: {result}")

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

        eq_name = str(data.get("name", "")).strip()

        filenames = self._equipment_image_filenames()

        if not filenames:

            return

        selected = self._image_gallery.selected_filename().strip()

        target = selected if selected in filenames else filenames[-1]

        ok, remove_msg = self._equipment_images.remove_image(

            target, data["id"], equipment_name=eq_name

        )

        if not ok:

            SiemensMessage.warning(self, "Image", remove_msg)

            self.set_status(remove_msg)

            return

        ok, message = self.tracker.remove_equipment_image(self._selected_row, target)

        if not ok:

            SiemensMessage.warning(self, "Image", message)

            self.set_status(message)

            return

        self._reload_selected_row()

        self._show_equipment_images(self._equipment_image_filenames())

        self._update_image_buttons()

        self.set_status(f"Equipment image deleted: {target}")

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

        self._datasheet_filename = str(filename).strip()

        display = self._format_datasheet_display(filename)

        label = self.ui.val_datasheet

        label.setText(self._elide_label_text(label, display))

        label.setToolTip(

            f"Datasheet: {display}" if display != "(not linked)" else "No datasheet linked"

        )

        self._refresh_detail_field_cursors()



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

        self.ui.search_entry.returnPressed.connect(self.search_equipment)

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

        self.ui.btn_set_equipment_image.clicked.connect(self._set_equipment_image)

        self.ui.btn_clear_equipment_image.clicked.connect(self._clear_equipment_image)

        self._setup_copy_buttons()



    def _setup_copy_buttons(self) -> None:

        fields = (

            ("btn_copy_supplier_ref", "supplier_ref_entry", "Supplier reference"),

            ("btn_copy_val_supplier_reference", "val_supplier_reference", "Supplier Reference"),

            ("btn_copy_val_serial_number", "val_serial_number", "Serial Number"),

            ("btn_copy_val_name", "val_name", "Name"),

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

        self._sync_equipment_folder(row)

        data = self.tracker.equipment_row_to_dict(row)

        self.ui.supplier_ref_entry.setText(str(data["supplier_reference"]))

        self.ui.val_supplier_reference.setText(str(data["supplier_reference"]))

        self.ui.val_serial_number.setText(str(data["serial_number"]))

        self.ui.val_name.setText(str(data.get("name", "")))

        self.ui.val_description.setText(str(data["description"]))

        self.ui.val_calibration.setText(str(data["calibration_date"]))

        self.ui.val_expiration.setText(str(data["calibration_expiration"]))

        datasheet = str(data.get("datasheet", ""))

        self._set_datasheet_display(datasheet)

        if open_datasheet and datasheet:

            self._prompt_open_equipment_datasheet(datasheet)

        self._show_equipment_images(self._equipment_image_filenames(row))

        if datasheet:

            self.set_status(f"Equipment loaded. Datasheet: {datasheet}")

        else:

            self.set_status("Equipment loaded. Datasheet: (not linked)")

        self._refresh_detail_field_cursors()

        self._refresh_location_display()



    def clear_fields(self) -> None:

        self._selected_row = None

        self.ui.search_entry.clear()

        self.ui.supplier_ref_entry.clear()

        self.ui.val_supplier_reference.clear()

        self.ui.val_serial_number.clear()

        self.ui.val_name.clear()

        self.ui.val_description.clear()

        self.ui.val_calibration.clear()

        self.ui.val_expiration.clear()

        self._set_datasheet_display("")

        self._hide_doc_results_list()

        self._clear_equipment_image_display()

        self._update_image_buttons()

        self._refresh_detail_field_cursors()

        self._refresh_location_display(empty=True)

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

            name=payload["name"],

            calibration_date=payload["calibration_date"],

            calibration_expiration=payload["calibration_expiration"],

            datasheet=payload["datasheet"],

        )

        if not ok:

            SiemensMessage.warning(self, "Equipment", message)

            self.set_status(message)

            return

        row = self._find_equipment_row_from_payload(payload)
        installed = self._install_datasheet_for_row(
            row,
            source=dialog.datasheet_source(),
            filename=payload.get("datasheet", ""),
        )
        if installed:
            payload["datasheet"] = installed

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

            name=payload["name"],

            calibration_date=payload["calibration_date"],

            calibration_expiration=payload["calibration_expiration"],

            datasheet=payload["datasheet"],

        )

        if not ok:

            SiemensMessage.critical(self, "Error", message)

            return

        installed = self._install_datasheet_for_row(
            self._selected_row,
            source=dialog.datasheet_source(),
            filename=payload.get("datasheet", ""),
        )
        if installed:
            payload["datasheet"] = installed

        self._refresh_after_save(payload)

        self.set_status(message)

        SiemensMessage.information(self, "Updated", message)



    def _refresh_after_save(self, payload: dict) -> None:

        row = self._find_equipment_row_from_payload(payload)

        if row is not None:

            self.show_equipment(row)



    def _prompt_open_equipment_datasheet(self, filename: str) -> None:

        name = str(filename).strip()

        if not name:

            return

        eq_id, eq_name = self._equipment_folder_key()

        document = self._storage.document_for_datasheet(

            eq_id, name, equipment_name=eq_name

        )

        if document is None:

            self.set_status(f"Datasheet not found: {name}")

            return

        if not SiemensConfirmDialog.ask(

            "Open datasheet",

            "Open the datasheet for this equipment?",

            self,

        ):

            return

        ok, message = self._storage.open_document(document)

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

        path = Path(item.data(Qt.ItemDataRole.UserRole))
        installed = self._install_datasheet_for_row(
            self._selected_row, source=path, filename=path.name
        )
        if not installed:
            return

        self._reload_selected_row()

        self._set_datasheet_display(installed)

        self.set_status(f"Datasheet linked: {installed}")

        SiemensMessage.information(self, "Linked", f"Datasheet linked: {installed}")



    def search_support_document(self) -> None:

        query = self.ui.doc_search_entry.text().strip()

        documents = self._storage.list_documents(query)

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



    def _open_linked_datasheet(self) -> bool:
        """Open the equipment's linked datasheet file. Returns True if opened."""
        filename = self._datasheet_filename
        if not filename:
            return False
        eq_id, eq_name = self._equipment_folder_key()
        document = self._storage.document_for_datasheet(
            eq_id, filename, equipment_name=eq_name
        )
        if document is None:
            self.set_status(f"Datasheet not found: {filename}")
            SiemensMessage.warning(
                self,
                "Not found",
                f"Datasheet file not found in equipment folder:\n{filename}",
            )
            return False
        ok, message = self._storage.open_document(document)
        if not ok:
            SiemensMessage.critical(self, "Open failed", message)
        self.set_status(message)
        return ok

    def open_selected_support_document(self) -> None:

        query = self.ui.doc_search_entry.text().strip()

        if query:
            if self.ui.doc_results_list.isVisible():
                item = self.ui.doc_results_list.currentItem()
                if item is not None:
                    path = Path(item.data(Qt.ItemDataRole.UserRole))
                    ok, message = self._storage.open_document(path)
                    if not ok:
                        SiemensMessage.critical(self, "Open failed", message)
                    self.set_status(message)
                    return
            SiemensMessage.warning(
                self,
                "Warning",
                "Select a document from the list, or clear Search doc to open the linked datasheet.",
            )
            return

        if self._open_linked_datasheet():
            return

        SiemensMessage.warning(
            self,
            "Warning",
            "No datasheet linked to this equipment.",
        )



    def open_support_documentation_folder(self) -> None:

        if self._selected_row is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Search or select an equipment first.",

            )

            return

        eq_id, eq_name = self._equipment_folder_key(self._selected_row)

        self._storage.ensure_equipment_dir(eq_id, eq_name)

        ok, message = self._storage.open_equipment_folder(

            eq_id, equipment_name=eq_name

        )

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

        if self._selected_row is None:

            SiemensMessage.warning(

                self,

                "Warning",

                "Search or select an equipment first.",

            )

            return

        data = self.tracker.equipment_row_to_dict(self._selected_row)

        data = self.tracker.equipment_row_to_dict(self._selected_row)

        eq_name = str(data.get("name", "")).strip()

        ok, filename = self._storage.install_datasheet(

            Path(file_path), data["id"], equipment_name=eq_name

        )

        if not ok:

            SiemensMessage.warning(self, "Add document", filename)

            self.set_status(filename)

            return

        self.set_status(f"Added {filename}.")

        SiemensMessage.information(self, "Added", f"Added {filename}.")

        ok_link, link_msg = self.tracker.link_equipment_datasheet(

            self._selected_row, filename

        )

        if ok_link:

            self._reload_selected_row()

            self._set_datasheet_display(filename)

            self.set_status(f"Datasheet linked: {filename}")

        self.search_support_document()


