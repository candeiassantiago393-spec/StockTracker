"""Stock Tracker main window — uses StockTracker from src.core.stock."""
import os
from pathlib import Path

from PySide6.QtCore import Qt, QStringListModel, QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QCompleter,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.component_images import fetch_catalog_pixmap
from src.core.stock import StockTracker
from src.core.suppliers import supplier_label
from src.core.suppliers.base import SupplierId

from .catalog_image_preview import CatalogImagePreview, replace_label_with_catalog_preview

from .confirm_dialog import SiemensConfirmDialog
from .message_dialog import SiemensMessage
from .edit_component_dialog import EditComponentDialog
from .history_dialog import HistoryDialog
from .manual_component_dialog import ManualComponentDialog
from .search_results_dialog import SearchResultsDialog
from .equipments_page import EquipmentsPage
from .equipments_table_dialog import EquipmentsTableDialog
from .user_name_dialog import UserNameDialog

from . import styles

_ACTION_LABELS = {
    "components": {
        "history_all": "Last 20",
        "history_item": "Comp. hist.",
        "manual": "ADD MANUAL",
        "edit": "EDIT",
    },
    "equipments": {
        "history_all": "Last 20",
        "history_item": "Eq. hist.",
        "manual": "ADD MANUAL",
        "edit": "EDIT",
    },
}


def _load_ui_class():
    """Qt Designer export (gui_stocktracker.ui)."""
    from .designer.gui_stocktracker import Ui_StockTracker as DesignerUi

    designer_py = Path(__file__).resolve().parent / "designer" / "gui_stocktracker.py"
    source = designer_py.read_text(encoding="utf-8")
    required = ("barcode_entry", "val_stock", "btn_scan", "user_entry", "btn_open_product")
    if not all(name in source for name in required):
        raise RuntimeError(
            "gui_stocktracker.py incompleto. Corre: "
            "python tools/generate_stocktracker_ui.py && "
            "pyside6-uic src/gui/designer/gui_stocktracker.ui "
            "-o src/gui/designer/gui_stocktracker.py"
        )
    return DesignerUi


class _CatalogImageLoader(QThread):
    """Background load so large inventories do not freeze the UI on image fetch."""

    loaded = Signal(object)

    def __init__(
        self,
        lookup_refs: list[str],
        tracker: StockTracker,
        *,
        fallback_url: str = "",
    ) -> None:
        super().__init__()
        self._lookup_refs = lookup_refs
        self._tracker = tracker
        self._fallback_url = str(fallback_url or "").strip()

    def run(self) -> None:
        refs = self._lookup_refs
        fallback = self._fallback_url

        if refs:
            part = self._tracker.lookup_catalog_part_any(*refs)
            image_url = fallback or (
                str(part.get("image_url", "")).strip() if part else ""
            )
            if not image_url:
                image_url = self._tracker.lookup_catalog_image_url_any(*refs)

            def url_fetcher() -> str:
                return image_url

            pixmap = fetch_catalog_pixmap(refs[0], url_fetcher) if image_url else None
        elif fallback:
            from src.core.component_images import fetch_pixmap_from_url

            pixmap = fetch_pixmap_from_url(fallback)
        else:
            pixmap = None

        if not self.isInterruptionRequested():
            self.loaded.emit(pixmap)


class _CatalogLinksLoader(QThread):
    """Resolve distributor WEB/DS links without blocking the UI."""

    loaded = Signal(str, str)

    def __init__(self, lookup_refs: list[str], tracker: StockTracker) -> None:
        super().__init__()
        self._lookup_refs = lookup_refs
        self._tracker = tracker

    def run(self) -> None:
        product_url, datasheet_url = self._tracker.lookup_catalog_links_any(
            *self._lookup_refs
        )
        if not self.isInterruptionRequested():
            self.loaded.emit(product_url, datasheet_url)


class StockTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tracker = StockTracker()
        Ui_StockTracker = _load_ui_class()
        self.ui = Ui_StockTracker()
        self.ui.setupUi(self)
        self._connect_signals()
        self._setup_page_navigation()
        self._setup_open_excel_button()
        self._setup_copy_buttons()
        self._setup_empty_details_click_targets()
        self._setup_component_image_preview()
        self._setup_catalog_links()
        self._catalog_image_loader: _CatalogImageLoader | None = None
        self._catalog_image_token = 0
        self._catalog_links_loader: _CatalogLinksLoader | None = None
        self._catalog_links_token = 0
        self._catalog_product_url = ""
        self._catalog_datasheet_url = ""
        self._setup_autocompletes()
        self.ui.user_entry.setFocus()

    def _setup_page_navigation(self) -> None:
        """Components vs Equipments — stacked pages + header navigation."""
        body_index = self.ui.verticalLayout.indexOf(self.ui.container_main_body)
        self.ui.verticalLayout.removeWidget(self.ui.container_main_body)

        # Title stays visible on both pages (same position as original row 0).
        self.ui.gridLayout_main.removeWidget(self.ui.frame_title)
        title_wrap = QWidget(self.ui.centralwidget)
        title_layout = QHBoxLayout(title_wrap)
        title_layout.setContentsMargins(*styles.TEMPLATE_PAGE_MARGINS)
        title_layout.setSpacing(0)
        title_layout.addWidget(self.ui.frame_title)
        self.ui.verticalLayout.insertWidget(body_index, title_wrap)
        user_wrap = self._build_shared_user_row()
        styles.apply_two_column_page_grid(self.ui.gridLayout_main)

        self._page_stack = QStackedWidget(self.ui.centralwidget)
        self._page_stack.addWidget(self.ui.container_main_body)
        self._equipments_page = EquipmentsPage(self.tracker, self)
        self._page_stack.addWidget(self._equipments_page)

        # The User Name row overlays the top of the page area instead of taking
        # its own full-width slot. This lets the right-hand column ("Equipment
        # Details" / "Component Details") start level with User Name; the left
        # column is offset down by the same amount so its content stays put.
        body_wrap = QWidget(self.ui.centralwidget)
        body_grid = QGridLayout(body_wrap)
        body_grid.setContentsMargins(0, 0, 0, 0)
        body_grid.setSpacing(0)
        body_grid.addWidget(self._page_stack, 0, 0)
        body_grid.addWidget(user_wrap, 0, 0, Qt.AlignmentFlag.AlignTop)
        self.ui.verticalLayout.insertWidget(body_index + 1, body_wrap)

        band = user_wrap.sizeHint().height()
        self._offset_left_column(self.ui.gridLayout_left, band)
        equipments_left = self._equipments_page.findChild(
            QWidget, "container_equipments_left"
        )
        if equipments_left is not None:
            self._offset_left_column(equipments_left.layout(), band)
        user_wrap.raise_()

        header_layout = self.ui.horizontalLayout_header
        header_layout.addItem(
            QSpacerItem(
                40,
                20,
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum,
            )
        )

        self.btn_nav_components = QPushButton("COMPONENTS", self.ui.header)
        self.btn_nav_equipments = QPushButton("EQUIPMENTS", self.ui.header)
        for btn in (self.btn_nav_components, self.btn_nav_equipments):
            btn.setMinimumSize(124, 0)
            btn.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
            header_layout.addWidget(btn)

        self.btn_nav_components.clicked.connect(self._show_components_page)
        self.btn_nav_equipments.clicked.connect(self._show_equipments_page)
        self._current_section = "components"
        self._show_components_page()

    def _apply_action_bar_labels(self, section: str) -> None:
        labels = _ACTION_LABELS[section]
        u = self.ui
        u.btn_history_all.setText(labels["history_all"])
        u.btn_history_component.setText(labels["history_item"])
        if hasattr(u, "btn_add_manual"):
            u.btn_add_manual.setText(labels["manual"])
            u.btn_add_manual.setToolTip(
                "Add manual component" if section == "components" else "Add manual equipment"
            )
        if hasattr(u, "btn_edit_component"):
            u.btn_edit_component.setText(labels["edit"])
            u.btn_edit_component.setToolTip(
                "Edit component" if section == "components" else "Edit equipment"
            )

    def _build_shared_user_row(self) -> QWidget:
        """User Name — overlay above both pages (same slot as Components .ui)."""
        self.ui.gridLayout_left.removeWidget(self.ui.row_user_entry)

        for widget, new_row in (
            (self.ui.row_search_entry, 1),
            (self.ui.row_barcode_entry, 2),
            (self.ui.row_quantity_entry, 3),
            (self.ui.row_stock_buttons, 4),
        ):
            self.ui.gridLayout_left.removeWidget(widget)
            self.ui.gridLayout_left.addWidget(widget, new_row, 0, 1, 2)

        self.ui.gridLayout_left.removeItem(self.ui.verticalSpacer_left)
        self.ui.gridLayout_left.addItem(self.ui.verticalSpacer_left, 5, 1, 1, 1)

        user_wrap = QWidget(self.ui.centralwidget)
        # Transparent so the overlay only shows the User Name row, never a panel
        # covering the right column behind it.
        user_wrap.setStyleSheet("background: transparent;")
        grid = QGridLayout(user_wrap)
        styles.apply_two_column_page_grid(grid)
        grid.addWidget(self.ui.row_user_entry, 0, 0)
        return user_wrap

    @staticmethod
    def _offset_left_column(layout, extra_top: int) -> None:
        """Push a left-column grid down so its content clears the User Name row."""
        if layout is None:
            return
        m = layout.contentsMargins()
        layout.setContentsMargins(m.left(), m.top() + extra_top, m.right(), m.bottom())

    def _show_components_page(self) -> None:
        self._current_section = "components"
        self._page_stack.setCurrentIndex(0)
        self.ui.tab1_title.setText("Inventory — Components")
        self._apply_action_bar_labels("components")
        self.btn_nav_components.setEnabled(False)
        self.btn_nav_equipments.setEnabled(True)
        self.set_status("")

    def _show_equipments_page(self) -> None:
        self._current_section = "equipments"
        self._page_stack.setCurrentIndex(1)
        self.ui.tab1_title.setText("Inventory — Equipments")
        self._apply_action_bar_labels("equipments")
        self.btn_nav_components.setEnabled(True)
        self.btn_nav_equipments.setEnabled(False)
        self.set_status("")

    def _connect_signals(self):
        u = self.ui
        u.btn_search.clicked.connect(self.search_component_manual)
        u.btn_scan.clicked.connect(self.scan_component)
        u.btn_add_stock.clicked.connect(lambda: self.update_stock("IN"))
        u.btn_remove_stock.clicked.connect(lambda: self.update_stock("OUT"))
        u.btn_history_all.clicked.connect(self.open_history_all)
        u.btn_history_component.clicked.connect(self.open_history_filtered)
        if hasattr(u, "btn_add_manual"):
            u.btn_add_manual.clicked.connect(self.add_manual_entry)
        if hasattr(u, "btn_edit_component"):
            u.btn_edit_component.clicked.connect(self.edit_current_entry)
        u.btn_clear.clicked.connect(self.clear_all_fields)
        if hasattr(u, "btn_exit"):
            u.btn_exit.clicked.connect(self.close)

    def _setup_open_excel_button(self) -> None:
        """Add OPEN EXCEL button near CLEAR/Exit."""
        actions_layout = getattr(self.ui, "horizontalLayout_actions", None)
        clear_btn = getattr(self.ui, "btn_clear", None)
        if actions_layout is None or clear_btn is None:
            return

        self.btn_open_excel = QPushButton("OPEN EXCEL", self.ui.widget_actions)
        self.btn_open_excel.setObjectName("btn_open_excel")
        self.btn_open_excel.setMinimumSize(124, 0)
        self.btn_open_excel.setStyleSheet(clear_btn.styleSheet())
        self.btn_open_excel.clicked.connect(self.open_excel_file)
        actions_layout.insertWidget(actions_layout.indexOf(clear_btn), self.btn_open_excel)

    def _setup_component_image_preview(self) -> None:
        label = getattr(self.ui, "component_image_preview", None)
        if label is None:
            return
        preview = replace_label_with_catalog_preview(label)
        self.ui.component_image_preview = preview
        preview.clear_image()

    def _setup_catalog_links(self) -> None:
        row = getattr(self.ui, "row_catalog_links", None)
        if row is not None:
            row.hide()
        btn_web = getattr(self.ui, "btn_open_product", None)
        btn_ds = getattr(self.ui, "btn_open_datasheet", None)
        if btn_web is not None:
            btn_web.clicked.connect(
                lambda: self._open_catalog_url(self._catalog_product_url, "product")
            )
        if btn_ds is not None:
            btn_ds.clicked.connect(
                lambda: self._open_catalog_url(self._catalog_datasheet_url, "datasheet")
            )
        self._clear_catalog_links()

    def _clear_catalog_links(self) -> None:
        self._catalog_product_url = ""
        self._catalog_datasheet_url = ""
        self._update_catalog_links_ui()

    def _set_catalog_links(self, product_url: str = "", datasheet_url: str = "") -> None:
        self._catalog_product_url = str(product_url or "").strip()
        self._catalog_datasheet_url = str(datasheet_url or "").strip()
        self._update_catalog_links_ui()

    def _update_catalog_links_ui(self) -> None:
        row = getattr(self.ui, "row_catalog_links", None)
        btn_web = getattr(self.ui, "btn_open_product", None)
        btn_ds = getattr(self.ui, "btn_open_datasheet", None)
        has_product = bool(self._catalog_product_url)
        has_datasheet = bool(self._catalog_datasheet_url)
        if row is not None:
            row.setVisible(has_product or has_datasheet)
        if btn_web is not None:
            btn_web.setVisible(has_product)
            btn_web.setEnabled(has_product)
        if btn_ds is not None:
            btn_ds.setVisible(has_datasheet)
            btn_ds.setEnabled(has_datasheet)

    def _open_catalog_url(self, url: str, label: str) -> None:
        target = str(url or "").strip()
        if not target:
            self.set_status(f"No {label} link available.")
            return
        if QDesktopServices.openUrl(QUrl(target)):
            self.set_status(f"Opened {label} link in browser.")
        else:
            SiemensMessage.warning(self, "Open link", f"Could not open {label} link.")

    def _catalog_lookup_refs(self, data: dict | None = None) -> list[str]:
        """References to try for catalog image/links (search text first)."""
        refs: list[str] = []
        for candidate in (
            self.ui.search_entry.text().strip(),
            str((data or {}).get("mouser", "")).strip(),
            str((data or {}).get("manufacturer_ref", "")).strip(),
            self.ui.barcode_entry.text().strip(),
        ):
            if candidate and candidate not in refs:
                refs.append(candidate)
        return refs

    def _refresh_catalog_links(self, lookup_refs: list[str]) -> None:
        if not lookup_refs:
            self._clear_catalog_links()
            return
        if not self.tracker.search_suppliers_order():
            self._clear_catalog_links()
            return

        self._catalog_links_token += 1
        token = self._catalog_links_token
        self._clear_catalog_links()

        if self._catalog_links_loader and self._catalog_links_loader.isRunning():
            self._catalog_links_loader.requestInterruption()
            self._catalog_links_loader.wait(200)

        loader = _CatalogLinksLoader(lookup_refs, self.tracker)

        def on_loaded(product_url: str, datasheet_url: str) -> None:
            if token != self._catalog_links_token:
                return
            self._set_catalog_links(product_url, datasheet_url)

        loader.loaded.connect(on_loaded)
        loader.finished.connect(loader.deleteLater)
        self._catalog_links_loader = loader
        loader.start()

    def _clear_component_image(self, placeholder: str = "No image") -> None:
        preview = getattr(self.ui, "component_image_preview", None)
        if preview is None:
            return
        if isinstance(preview, CatalogImagePreview):
            preview.clear_image(placeholder)
            return
        preview.setStyleSheet(styles.EQUIPMENT_IMAGE_PREVIEW_STYLE)
        preview.clear()
        preview.setText(placeholder)

    def _load_component_catalog_image(
        self,
        lookup_refs: list[str],
        *,
        fallback_url: str = "",
    ) -> None:
        preview = getattr(self.ui, "component_image_preview", None)
        if preview is None:
            return

        refs = [str(ref).strip() for ref in lookup_refs if str(ref).strip()]
        fallback = str(fallback_url or "").strip()
        if not refs and not fallback:
            self._clear_component_image()
            return
        if refs and not fallback and not self.tracker.search_suppliers_order():
            self._clear_component_image()
            return

        self._catalog_image_token += 1
        token = self._catalog_image_token

        if self._catalog_image_loader and self._catalog_image_loader.isRunning():
            self._catalog_image_loader.requestInterruption()
            self._catalog_image_loader.wait(200)

        self._clear_component_image("Loading...")
        self.set_status("Loading catalog image...")

        loader = _CatalogImageLoader(
            refs,
            self.tracker,
            fallback_url=fallback,
        )

        def on_loaded(pixmap) -> None:
            if token != self._catalog_image_token:
                return
            if pixmap is None or (hasattr(pixmap, "isNull") and pixmap.isNull()):
                self._clear_component_image("Image unavailable")
                self.set_status("Catalog image unavailable.")
                return
            if isinstance(preview, CatalogImagePreview):
                preview.set_image(pixmap)
            else:
                preview.setPixmap(pixmap)
                preview.setText("")
            self.set_status("Catalog image loaded.")

        loader.loaded.connect(on_loaded)
        loader.finished.connect(loader.deleteLater)
        self._catalog_image_loader = loader
        loader.start()

    def _show_component_image_url(
        self,
        url: str,
        *,
        lookup_refs: list[str] | None = None,
    ) -> None:
        refs = list(lookup_refs or [])
        if refs:
            self._load_component_catalog_image(refs, fallback_url=url)
            return
        image_url = str(url or "").strip()
        if not image_url:
            self._clear_component_image()
            return
        self._load_component_catalog_image([], fallback_url=image_url)

    def _refresh_component_catalog_image(self, lookup_refs: list[str]) -> None:
        self._load_component_catalog_image(lookup_refs)

    def _display_catalog_part(self, part: dict, lookup_refs: list[str]) -> None:
        """Show API catalog data when the part is not in Excel (or refs differ)."""
        from src.core.component_catalog_links import store_links

        primary = lookup_refs[0] if lookup_refs else ""
        supplier_ref = self.tracker.part_supplier_reference(part, primary)
        manufacturer_ref = self.tracker.part_manufacturer_reference(part)

        refs = list(lookup_refs)
        for extra in (supplier_ref, manufacturer_ref):
            if extra and extra not in refs:
                refs.append(extra)

        if primary:
            store_links(self.tracker.normalize_ref(primary), part)

        u = self.ui
        u.val_mouser.setText(supplier_ref)
        u.val_manufacturer.setText(self.tracker.part_manufacturer(part))
        u.val_manufacturer_ref.setText(manufacturer_ref)
        u.val_description.setText(self.tracker.part_description(part))
        u.val_stock.setText("0")
        u.barcode_entry.setText(supplier_ref or manufacturer_ref or primary)
        self._refresh_empty_detail_cursor()
        self._set_catalog_links(
            str(part.get("product_url", "")),
            str(part.get("datasheet_url", "")),
        )
        self._load_component_catalog_image(
            refs,
            fallback_url=str(part.get("image_url", "")),
        )

    def _setup_empty_details_click_targets(self) -> None:
        """Clicking empty detail rows opens manual component popup."""
        pairs = (
            ("row_val_mouser", "val_mouser"),
            ("row_val_manufacturer", "val_manufacturer"),
            ("row_val_manufacturer_ref", "val_manufacturer_ref"),
            ("row_val_description", "val_description"),
            ("row_val_stock", "val_stock"),
        )
        self._detail_click_targets: list[tuple[QWidget, QWidget]] = []
        for row_name, value_name in pairs:
            row = getattr(self.ui, row_name, None)
            value = getattr(self.ui, value_name, None)
            if row is None or value is None:
                continue
            self._detail_click_targets.append((row, value))
            row.mousePressEvent = (  # type: ignore[method-assign]
                lambda event, widget=value: self._on_empty_detail_click(widget, event)
            )
            value.mousePressEvent = (  # type: ignore[method-assign]
                lambda event, widget=value: self._on_empty_detail_click(widget, event)
            )
        self._refresh_empty_detail_cursor()

    @staticmethod
    def _widget_text(widget: QWidget) -> str:
        if isinstance(widget, (QLabel, QLineEdit)):
            return widget.text().strip()
        return ""

    def _refresh_empty_detail_cursor(self) -> None:
        for row, value in getattr(self, "_detail_click_targets", []):
            clickable = self._widget_text(value) == ""
            cursor = Qt.CursorShape.PointingHandCursor if clickable else Qt.CursorShape.ArrowCursor
            row.setCursor(cursor)
            value.setCursor(cursor)

    def _on_empty_detail_click(self, value_widget: QWidget, _event) -> None:
        if self._widget_text(value_widget):
            return
        self.add_manual_component()

    def open_excel_file(self) -> None:
        """Ensure all inventory sheets exist, then open stock.xlsx in Excel."""
        if not self.tracker.ensure_workbook_sheets():
            SiemensMessage.critical(
                self,
                "Excel file is open",
                "Close stock.xlsx in Excel before updating sheets.",
            )
            return
        try:
            os.startfile(str(self.tracker.excel_file))
            self.set_status(
                "Opened Excel (Components, Equipments, History)."
            )
        except Exception as exc:
            SiemensMessage.critical(
                self,
                "Open Excel failed",
                f"Could not open {self.tracker.excel_file}.\n\n{exc}",
            )

    def _make_completer(
        self, terms: list[str], filter_mode: Qt.MatchFlag
    ) -> QCompleter:
        completer = QCompleter(QStringListModel(terms), self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(filter_mode)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setMaxVisibleItems(12)
        return completer

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

    def _setup_copy_buttons(self) -> None:
        fields = (
            ("btn_copy_barcode_entry", "barcode_entry", "Supplier reference"),
            ("btn_copy_val_mouser", "val_mouser", "Supplier reference"),
            ("btn_copy_val_manufacturer", "val_manufacturer", "Manufacturer"),
            ("btn_copy_val_manufacturer_ref", "val_manufacturer_ref", "Manufacturer reference"),
            ("btn_copy_val_description", "val_description", "Description"),
            ("btn_copy_val_stock", "val_stock", "Current stock"),
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

    def validate_user(self) -> bool:
        if self.ui.user_entry.text().strip():
            return True
        name = UserNameDialog.ask(self, initial=self.ui.user_entry.text())
        if name:
            self.ui.user_entry.setText(name)
            return True
        return False

    def show_component(self, row) -> None:
        data = self.tracker.row_to_dict(row)
        u = self.ui
        u.val_mouser.setText(str(data["mouser"]))
        u.val_manufacturer.setText(str(data["manufacturer"]))
        u.val_manufacturer_ref.setText(str(data["manufacturer_ref"]))
        u.val_description.setText(str(data["description"]))
        u.val_stock.setText(str(data["stock"]))
        self._refresh_empty_detail_cursor()
        refs = self._catalog_lookup_refs(data)
        self._refresh_catalog_links(refs)
        self._refresh_component_catalog_image(refs)

    def clear_inputs_after_action(self) -> None:
        self.ui.search_entry.clear()
        self.ui.barcode_entry.clear()
        self.ui.quantity_entry.clear()

    def open_history_all(self) -> None:
        if self._current_section == "equipments":
            self.open_equipments_table(all_equipments=True)
            return
        self.open_history(False)

    def open_history_filtered(self) -> None:
        if self._current_section == "equipments":
            self.open_equipments_table(all_equipments=False)
            return
        self.open_history(True)

    def open_equipments_table(self, *, all_equipments: bool) -> None:
        if not self.validate_user():
            return

        workbook = self.tracker.get_workbook()
        supplier_reference = ""
        description = ""
        if not all_equipments:
            supplier_reference = (
                self._equipments_page.val_supplier_reference.text().strip()
            )
            description = self._equipments_page.val_description.text().strip()
            if not supplier_reference and not description:
                SiemensMessage.warning(
                    self,
                    "Warning",
                    "Load an equipment first (search).",
                )
                return

        rows = self.tracker.get_equipment_rows(
            workbook,
            equipment_only=not all_equipments,
            supplier_reference=supplier_reference,
            description=description,
        )
        title = "Last 20 equipments" if all_equipments else "Equipment history"
        dialog = EquipmentsTableDialog(rows, self, title=title)
        dialog.exec()

    def add_manual_entry(self) -> None:
        if self._current_section == "equipments":
            self._equipments_page.add_equipment()
            return
        self.add_manual_component()

    def edit_current_entry(self) -> None:
        if self._current_section == "equipments":
            self._equipments_page.edit_equipment()
            return
        self.edit_component()

    def clear_all_fields(self) -> None:
        if self._current_section == "equipments":
            self._equipments_page.clear_fields()
            return

        u = self.ui
        u.search_entry.clear()
        u.barcode_entry.clear()
        u.quantity_entry.clear()
        u.val_mouser.clear()
        u.val_manufacturer.clear()
        u.val_manufacturer_ref.clear()
        u.val_description.clear()
        u.val_stock.clear()
        self._refresh_empty_detail_cursor()
        self._clear_catalog_links()
        self._clear_component_image()
        self.set_status("")

    def scan_component(self) -> None:
        if not self.validate_user():
            return

        code = self.ui.barcode_entry.text().strip()
        if not code:
            SiemensMessage.warning(self, "Warning", "Please scan a barcode.")
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

        part, found_supplier = self._lookup_distributor_catalogs(part_number)
        if part is None:
            return

        supplier_reference = self.tracker.part_supplier_reference(
            part, part_number
        )
        manufacturer_ref = self.tracker.part_manufacturer_reference(part)
        from src.core.component_catalog_links import store_links

        lookup_ref = supplier_reference or manufacturer_ref or part_number
        refs = [r for r in (lookup_ref, part_number) if r]
        store_links(self.tracker.normalize_ref(lookup_ref), part)
        self._set_catalog_links(
            str(part.get("product_url", "")),
            str(part.get("datasheet_url", "")),
        )
        self._show_component_image_url(
            str(part.get("image_url", "")),
            lookup_refs=refs,
        )

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
                SiemensMessage.information(
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
            SiemensMessage.critical(
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
        via = supplier_label(found_supplier) if found_supplier else "distributor"
        self.set_status(
            f"New component added (found via {via}). "
            "Enter quantity and click ADD STOCK."
        )
        SiemensMessage.information(
            self,
            "Added",
            f"New component added with stock 0 (found via {via}).\n"
            "Now enter quantity and click ADD STOCK.",
        )

    def _lookup_distributor_catalogs(
        self, part_number: str
    ) -> tuple[dict | None, SupplierId | None]:
        catalogs = self.tracker.search_suppliers_order()
        if not catalogs:
            SiemensMessage.critical(
                self,
                "API credentials missing",
                "No distributor API is configured.\n\n"
                "Edit config/secrets.py (see secrets.example.py).",
            )
            return None, None

        catalog_names = self.tracker.configured_supplier_labels()
        if not SiemensMessage.question(
            self,
            "Component not found",
            "Component not found in Excel.\n\n"
            f"Search distributor catalogs?\n({catalog_names})",
        ):
            return None, None

        part, found_supplier = self.tracker.search_any_supplier(part_number)
        if part is None:
            SiemensMessage.critical(
                self,
                "Distributor lookup failed",
                f"No result in any configured catalog.\n\n"
                f"Tried: {catalog_names}\n\n"
                "Check internet, API credentials, and the part number.",
            )
        return part, found_supplier

    def search_component_manual(self) -> None:
        if not self.validate_user():
            return

        query = self.ui.search_entry.text().strip()
        if not query:
            SiemensMessage.warning(self, "Warning", "Write something to search.")
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        matches = self.tracker.search_in_excel_all(sheet, query)

        if not matches:
            if len(query) >= 5:
                part, _found_supplier = self._lookup_distributor_catalogs(query)
                if part is not None:
                    self._display_catalog_part(part, [query])
                    self.set_status("Catalog preview — not in Excel.")
                    return
            SiemensMessage.information(self, "Not found", "No component found.")
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
            SiemensMessage.warning(
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
            SiemensMessage.warning(self, "Warning", "Quantity must be a number.")
            return

        if quantity <= 0:
            SiemensMessage.warning(self, "Warning", "Quantity must be greater than 0.")
            return

        part_number = self.tracker.extract_part_number(code)
        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        row = self.tracker.find_component_any(sheet, part_number, code)
        if row is None:
            SiemensMessage.critical(self, "Error", "Component not found.")
            return

        current_stock = int(row[6].value or 0)

        if movement == "OUT":
            if current_stock < quantity:
                SiemensMessage.critical(self, "Error", "Not enough stock.")
                return

            new_stock = current_stock - quantity
            if not SiemensConfirmDialog.ask(
                "Confirm stock removal",
                f"Are you sure you want to remove stock?\n\n"
                f"Component: {row[1].value}\n"
                f"Quantity to remove: {quantity}\n"
                f"Current stock: {current_stock}\n"
                f"Stock after removal: {new_stock}",
                self,
            ):
                self.set_status("Stock removal cancelled.")
                return

        user = self.ui.user_entry.text().strip()
        if not self.tracker.update_stock(user, code, quantity, movement):
            SiemensMessage.critical(
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
        SiemensMessage.information(self, "Success", "Stock updated.")

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
            SiemensMessage.warning(self, "Manual component", message)
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
        SiemensMessage.information(self, "Added", message)

    def edit_component(self) -> None:
        if not self.validate_user():
            return

        code = self.ui.barcode_entry.text().strip()
        mouser_ref = self.ui.val_mouser.text().strip()
        if not code and not mouser_ref:
            SiemensMessage.warning(
                self,
                "Warning",
                "Load a component first (search or scan).",
            )
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        part_number = self.tracker.extract_part_number(code) if code else ""
        row = self.tracker.find_component_any(
            sheet,
            part_number,
            code,
            mouser_ref,
            self.ui.val_manufacturer_ref.text().strip(),
        )
        if row is None:
            SiemensMessage.critical(self, "Error", "Component not found in Excel.")
            return

        dialog = EditComponentDialog(self.tracker.row_to_dict(row), self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        payload = dialog.payload()
        ok, msg = self.tracker.update_component(
            row,
            supplier_reference=payload["supplier_reference"],
            manufacturer=payload["manufacturer"],
            manufacturer_reference=payload["manufacturer_reference"],
            description=payload["description"],
        )
        if not ok:
            SiemensMessage.critical(self, "Error", msg)
            return

        workbook = self.tracker.get_workbook()
        sheet = self.tracker.get_components_sheet(workbook)
        updated = self.tracker.find_component_any(
            sheet,
            payload["supplier_reference"],
            payload["manufacturer_reference"],
            payload["manufacturer"],
        )
        if updated:
            self.show_component(updated)

        self._refresh_autocompletes()
        self.set_status(msg)
        SiemensMessage.information(self, "Updated", msg)
