"""Passive (R/C) inventory mode embedded in the Components page."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QInputDialog,
    QLabel,
    QSizePolicy,
    QWidget,
)

from src.core.stock import StockTracker

from . import styles
from .confirm_dialog import SiemensConfirmDialog
from .location_combo import pick_location
from .mode_detail_panel import build_detail_panel
from .massive_dialog import MassiveDialog
from .massive_search_dialog import MassiveSearchDialog
from .massive_table_dialog import MassiveTableDialog
from .history_dialog import HistoryDialog
from .message_dialog import SiemensMessage

_PASSIVE_FIELD_TITLES = {
    "part_type": "Type",
    "value": "Value",
    "tolerance": "Tolerance",
    "package": "Package",
    "name": "Name",
    "stock": "Stock",
    "supplier_reference": "Supplier Ref",
    "dielectric": "Dielectric",
    "voltage": "Voltage",
    "notes": "Notes",
    "location": "Location",
}


class ComponentsMassiveMode:
    """Resistors / capacitors on sheet Generic — toggled inside Components."""

    def __init__(self, window) -> None:
        self.window = window
        self.tracker: StockTracker = window.tracker
        self._selected_row = None
        self._detail_labels: dict[str, QLabel] = {}
        self._detail_click_targets: list[tuple[QWidget | None, QLabel, str]] = []
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

        grid.addWidget(
            self._panel,
            1,
            0,
            1,
            5,
            Qt.AlignmentFlag.AlignTop,
        )
        self._panel.hide()
        self._saved_entry_styles: dict = {}
        self._right_spacer_in_grid = True
        self._setup_detail_field_clicks()

    def _setup_detail_field_clicks(self) -> None:
        """Click Passive detail fields to quick-edit (or Add Passive when empty)."""
        self._detail_click_targets.clear()
        for key, label in self._detail_labels.items():
            row_wrap = label.parentWidget()
            title = _PASSIVE_FIELD_TITLES.get(key, key)
            if key == "stock":
                label.setToolTip("Use quantity + ADD STOCK / REMOVE STOCK")
            else:
                label.setToolTip(f"Click to edit {title.lower()}")

            click_widgets = [w for w in (row_wrap, label) if w is not None]
            for widget in click_widgets:
                widget.mousePressEvent = (  # type: ignore[method-assign]
                    lambda event, field_key=key: self._on_detail_field_click(
                        field_key, event
                    )
                )
            self._detail_click_targets.append((row_wrap, label, key))
        self._refresh_detail_field_cursors()

    @staticmethod
    def _label_raw_text(label: QLabel) -> str:
        text = str(label.toolTip() or label.text() or "").strip()
        return "" if text == "—" else text

    def _refresh_detail_field_cursors(self) -> None:
        for row_wrap, label, key in self._detail_click_targets:
            if self._selected_row is not None:
                if key == "stock":
                    cursor = Qt.CursorShape.ArrowCursor
                else:
                    cursor = Qt.CursorShape.PointingHandCursor
            else:
                clickable = self._label_raw_text(label) == ""
                cursor = (
                    Qt.CursorShape.PointingHandCursor
                    if clickable
                    else Qt.CursorShape.ArrowCursor
                )
            label.setCursor(cursor)
            if row_wrap is not None:
                row_wrap.setCursor(cursor)

    def _on_detail_field_click(self, key: str, _event) -> None:
        if self._selected_row is not None:
            if key == "stock":
                SiemensMessage.information(
                    self.window,
                    "Stock",
                    "Use the quantity field and ADD STOCK / REMOVE STOCK buttons.",
                )
                return
            self._edit_passive_field(key)
            return

        label = self._detail_labels.get(key)
        if label is not None and self._label_raw_text(label) == "":
            self.add_item()

    def _edit_passive_field(self, key: str) -> None:
        if not self.window.validate_user():
            return
        if self._selected_row is None:
            SiemensMessage.warning(
                self.window, "Passive", "Search or select an item first."
            )
            return

        data = self.tracker.massive_row_to_dict(self._selected_row)
        title = _PASSIVE_FIELD_TITLES.get(key, key)
        current = str(data.get(key, "")).strip()
        if key == "part_type":
            current = data.get("part_type", "R")

        new_value: str | None = None
        if key == "part_type":
            items = ["R — Resistor", "C — Capacitor"]
            current_index = 1 if current == "C" else 0
            choice, accepted = QInputDialog.getItem(
                self.window,
                title,
                "Passive type:",
                items,
                current_index,
                False,
            )
            if not accepted:
                self.set_status(f"{title} edit cancelled.")
                return
            new_value = "C" if str(choice).startswith("C") else "R"
        elif key == "location":
            picked, accepted = pick_location(
                self.window,
                self.tracker,
                title="Location",
                current=current,
            )
            if not accepted:
                self.set_status(f"{title} edit cancelled.")
                return
            new_value = picked
        else:
            edited, accepted = QInputDialog.getText(
                self.window,
                title,
                f"Edit {title}:",
                text=current,
            )
            if not accepted:
                self.set_status(f"{title} edit cancelled.")
                return
            new_value = edited.strip()

        if new_value is None or new_value == current:
            return

        ok, message = self.tracker.update_massive_item(
            self._selected_row,
            new_value if key == "part_type" else data["part_type"],
            new_value if key == "value" else data["value"],
            new_value if key == "tolerance" else data["tolerance"],
            new_value if key == "package" else data["package"],
            name=new_value if key == "name" else data["name"],
            supplier_reference=(
                new_value if key == "supplier_reference" else data["supplier_reference"]
            ),
            dielectric=new_value if key == "dielectric" else data["dielectric"],
            voltage=new_value if key == "voltage" else data["voltage"],
            notes=new_value if key == "notes" else data["notes"],
            location=new_value if key == "location" else data["location"],
        )
        if not ok:
            SiemensMessage.warning(self.window, "Passive", message)
            self.set_status(message)
            return

        self._reload_selected_row()
        self.show_item(self._selected_row)
        self.set_status(message)

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
            self.window.ui.search_entry.setPlaceholderText(
                "Search value (e.g. 10k, 100nF, 4.7uF)…"
            )
        else:
            if self.window._inventory_mode == "components":
                self.window.ui.search_entry.setPlaceholderText("")
        self._apply_passive_layout(active)

    def _apply_passive_layout(self, compact: bool) -> None:
        """Tighter rows and wider inputs when Passive mode is active."""
        u = self.window.ui
        row_layouts = (
            u.layout_search_entry,
            u.layout_barcode_entry,
            u.layout_quantity_entry,
            u.layout_stock_buttons,
        )
        margins = styles.PASSIVE_ROW_MARGINS if compact else styles.TEMPLATE_ROW_MARGINS
        for layout in row_layouts:
            layout.setContentsMargins(*margins)

        for layout in (
            u.layout_search_entry,
            u.layout_barcode_entry,
            u.layout_quantity_entry,
        ):
            layout.setStretch(0, 0)
            layout.setStretch(1, 1)
            if layout.count() > 2:
                layout.setStretch(2, 0)

        entries = (u.search_entry, u.barcode_entry, u.quantity_entry)
        for entry in entries:
            if compact:
                if entry not in self._saved_entry_styles:
                    self._saved_entry_styles[entry] = entry.styleSheet()
                styles.apply_expanding_line_edit(entry)
            else:
                saved = self._saved_entry_styles.get(entry)
                if saved is not None:
                    entry.setStyleSheet(saved)
                entry.setSizePolicy(
                    QSizePolicy.Policy.Fixed,
                    QSizePolicy.Policy.Fixed,
                )

        preview = getattr(u, "component_image_preview", None)
        if preview is not None:
            preview.setVisible(not compact)
        hint = getattr(self.window, "_global_search_hint", None)
        if hint is not None:
            hint.setVisible(True)

        self.window._set_catalog_chrome_visible(not compact)
        if compact:
            self.window._clear_catalog_links()
        else:
            self.window._update_catalog_links_ui()

        right_grid = u.gridLayout_right
        spacer_item = u.verticalSpacer_right
        if compact:
            if self._right_spacer_in_grid:
                right_grid.removeItem(spacer_item)
                self._right_spacer_in_grid = False
            right_grid.setContentsMargins(8, 8, 8, 8)
        else:
            if not self._right_spacer_in_grid:
                right_grid.addItem(spacer_item, 8, 0, 1, 1)
                self._right_spacer_in_grid = True
            right_grid.setContentsMargins(-1, 15, -1, -1)

        left_grid = u.gridLayout_left
        if compact:
            left_grid.setContentsMargins(8, 8, 8, 8)
        else:
            left_grid.setContentsMargins(-1, 15, -1, -1)

    def set_status(self, text: str) -> None:
        self.window.set_status(text)

    def clear_fields(self) -> None:
        self._selected_row = None
        for label in self._detail_labels.values():
            label.clear()
            label.setToolTip("")
        self._refresh_detail_field_cursors()

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
        for key, label in self._detail_labels.items():
            if key == "stock":
                label.setToolTip("Use quantity + ADD STOCK / REMOVE STOCK")
                continue
            raw = self._label_raw_text(label)
            if raw:
                title = _PASSIVE_FIELD_TITLES.get(key, key)
                label.setToolTip(f"{raw}\n(Click to edit {title.lower()})")
        self._refresh_detail_field_cursors()

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
            SiemensMessage.warning(
                self.window,
                "Passive",
                "Enter a resistance or capacitance value (e.g. 10k, 100nF).",
            )
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_massive_sheet(workbook)
        matches = self.tracker.search_massive_by_value(sheet, query)
        if not matches:
            SiemensMessage.warning(
                self.window,
                "Passive",
                f"No passive item with value matching “{query}”.",
            )
            self.set_status("No Passive items found for that value.")
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

    def scan_supplier_ref(self) -> None:
        """Scan barcode / supplier reference — same flow as Components SCAN."""
        if not self.window.validate_user():
            return

        code = self.window.ui.barcode_entry.text().strip()
        if not code:
            SiemensMessage.warning(
                self.window,
                "Warning",
                "Please scan a barcode or supplier reference.",
            )
            return

        if self.window._is_ignorable_scan(code):
            self.window._clear_ignorable_scan()
            return

        part_number = self.tracker.extract_part_number(code)
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_massive_sheet(workbook)
        self.tracker.get_history_sheet(workbook)

        row = self.tracker.find_massive_any(sheet, part_number, code)
        if row:
            self._show_scanned_row(row, code)
            self.set_status("Passive item found in Excel.")
            return

        part, found_supplier = self.window._lookup_distributor_catalogs(part_number)
        if part is None:
            return

        route = self.window._try_route_passive(
            user=self.window.ui.user_entry.text().strip(),
            catalog_part=part,
            initial_stock=0,
            location="",
            prompt_if_incomplete=True,
        )
        if route == "done":
            supplier_reference = self.tracker.part_supplier_reference(
                part, part_number
            )
            if supplier_reference:
                self.window.ui.barcode_entry.setText(supplier_reference)
            return

        if route == "cancelled":
            return

        from src.core.suppliers import supplier_label

        via = supplier_label(found_supplier) if found_supplier else "distributor"
        SiemensMessage.warning(
            self.window,
            "Passive",
            f"Part found via {via} but is not a resistor/capacitor.\n\n"
            "Switch to Components mode to add catalog components.",
        )
        self.set_status("Not a passive item — use Components mode.")

    def _show_scanned_row(self, row, scanned_code: str) -> None:
        self.show_item(row)
        data = self.tracker.massive_row_to_dict(row)
        ref = str(data.get("supplier_reference") or "").strip() or scanned_code
        self.window.ui.barcode_entry.setText(ref)
        value = str(data.get("value") or "").strip()
        if value:
            self.window.ui.search_entry.setText(value)

    def _resolve_selected_row(self):
        if self._selected_row is not None:
            return self._selected_row

        code = self.window.ui.barcode_entry.text().strip()
        if not code or self.window._is_ignorable_scan(code):
            return None

        part_number = self.tracker.extract_part_number(code)
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_massive_sheet(workbook)
        row = self.tracker.find_massive_any(sheet, part_number, code)
        if row is not None:
            self._show_scanned_row(row, code)
        return row

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
        if self._resolve_selected_row() is None:
            SiemensMessage.warning(
                self.window,
                "Passive",
                "Scan or search a passive item first.",
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

        if movement == "IN":
            self.window._maybe_prompt_location_on_stock_in(
                kind="passive",
                row=self._selected_row,
            )

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
        excel_rows = self.tracker.get_massive_recent_rows(workbook, limit=20)
        if not excel_rows:
            SiemensMessage.information(
                self.window,
                "Passive",
                "No passive items in inventory yet.",
            )
            return

        dialog = MassiveTableDialog(
            excel_rows,
            self.tracker.massive_row_to_dict,
            self.window,
            title="Passive — last 20",
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.set_status("List closed.")
            return

        row = dialog.selected_row()
        if row is None:
            return

        self.show_item(row)
        data = self.tracker.massive_row_to_dict(row)
        value = str(data.get("value") or "").strip()
        if value:
            self.window.ui.search_entry.setText(value)
        ref = str(data.get("supplier_reference") or "").strip()
        if ref:
            self.window.ui.barcode_entry.setText(ref)
        self.set_status("Passive item opened from list.")

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
        if not rows:
            SiemensMessage.information(
                self.window,
                "Passive",
                "No history entries for this item.",
            )
            return

        dialog = HistoryDialog(rows, self.window, title="Passive — movement history")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.set_status("History closed.")
            return

        entry = dialog.selected_row()
        if entry is None:
            return

        history_ref = str(entry[2] or "").strip()
        if not history_ref:
            return

        sheet = self.tracker.get_massive_sheet(workbook)
        matches = self.tracker.search_massive_all(sheet, history_ref)
        if not matches and self._selected_row is not None:
            matches = [self._selected_row]
        if not matches:
            SiemensMessage.warning(
                self.window,
                "Passive",
                f"No passive item found for “{history_ref}”.",
            )
            return

        self.show_item(matches[0])
        data = self.tracker.massive_row_to_dict(matches[0])
        value = str(data.get("value") or "").strip()
        if value:
            self.window.ui.search_entry.setText(value)
        supplier_ref = str(data.get("supplier_reference") or "").strip()
        if supplier_ref:
            self.window.ui.barcode_entry.setText(supplier_ref)
        self.set_status("Passive item opened from history.")

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
