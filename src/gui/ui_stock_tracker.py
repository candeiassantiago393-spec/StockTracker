"""
Stock Tracker UI — layout and styles aligned with gui_template.ui.
"""
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from src.gui.siemens_template.resources import resources_rc  # noqa: F401

from . import styles


class Ui_StockTracker:
    """Builds Stock Tracker on QMainWindow using Siemens template structure."""

    def setupUi(self, window: QMainWindow) -> None:
        window.setObjectName("StockTracker")
        window.resize(1284, 720)
        window.setWindowTitle("Stock Tracker")
        icon = QIcon()
        icon.addFile(
            ":/siemens_logo/logos/sie-favicon_internet.ico",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        window.setWindowIcon(icon)
        window.setStyleSheet(styles.MAIN_WINDOW_STYLE)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        root = QVBoxLayout(self.centralwidget)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # Header — template: logo + title, no stretch
        self.header = QWidget()
        self.header.setObjectName("header")
        self.header.setStyleSheet(styles.HEADER_STYLE)
        self.header.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        header_row = QHBoxLayout(self.header)
        header_row.setSpacing(16)

        self.brand_label = QLabel()
        self.brand_label.setObjectName("brand_identifier")
        self.brand_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        pix = QPixmap(":/siemens_logo/logos/Siemens Logo.png")
        if not pix.isNull():
            self.brand_label.setPixmap(pix)

        self.product_name = QLabel("Stock Tracker")
        self.product_name.setObjectName("product_name")
        self.product_name.setStyleSheet(styles.PRODUCT_NAME_STYLE)
        self.product_name.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

        header_row.addWidget(self.brand_label)
        header_row.addWidget(self.product_name)
        root.addWidget(self.header)

        self.container_main_body = QWidget()
        self.container_main_body.setObjectName("container_main_body")
        body_grid = QGridLayout(self.container_main_body)
        body_grid.setContentsMargins(16, -1, -1, -1)

        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.StyledPanel)
        title_frame.setFrameShadow(QFrame.Shadow.Raised)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        self.tab1_title = QLabel("Inventory")
        self.tab1_title.setObjectName("tab1_title")
        self.tab1_title.setStyleSheet(styles.PAGE_TITLE_STYLE)
        title_layout.addWidget(self.tab1_title)
        body_grid.addWidget(title_frame, 0, 0, 1, 2)

        # Left panel — template gridLayout_7
        self.container_tab1_left = QFrame()
        self.container_tab1_left.setObjectName("container_tab1_left")
        self.container_tab1_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_tab1_left.setFrameShadow(QFrame.Shadow.Raised)
        left_grid = QGridLayout(self.container_tab1_left)
        left_grid.setContentsMargins(-1, 15, -1, -1)
        left_grid.setVerticalSpacing(0)

        row = 0
        section = QLabel("Operations")
        section.setStyleSheet(styles.SECTION_TITLE_STYLE)
        left_grid.addWidget(section, row, 0)
        row += 1

        self.user_entry = self._add_field_row(left_grid, row, "User Name")
        row += 1

        self.search_entry = QLineEdit()
        self.search_entry.setObjectName("search_entry")
        self.search_entry.setStyleSheet(styles.LINE_EDIT_STYLE)
        self.search_entry.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_search = QPushButton("SEARCH")
        self.btn_search.setObjectName("btn_search")
        self.btn_search.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_search.setMinimumSize(124, 0)
        self._add_field_row(left_grid, row, "Search Component", self.search_entry, self.btn_search)
        row += 1

        self.supplier_combo = QComboBox()
        self.supplier_combo.setObjectName("supplier_combo")
        self.supplier_combo.setStyleSheet(styles.COMBOBOX_STYLE)
        self.supplier_combo.setMinimumSize(*styles.TEMPLATE_COMBO_MIN_SIZE)
        self._add_combo_row(left_grid, row, "Distributor", self.supplier_combo)
        row += 1

        self.barcode_entry = self._add_field_row(
            left_grid, row, "Scan Barcode / Supplier Ref."
        )
        row += 1

        self.quantity_entry = QLineEdit()
        self.quantity_entry.setObjectName("quantity_entry")
        self.quantity_entry.setStyleSheet(styles.LINE_EDIT_STYLE)
        self.quantity_entry.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_scan = QPushButton("SCAN")
        self.btn_scan.setObjectName("btn_scan")
        self.btn_scan.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_scan.setMinimumSize(124, 0)
        self._add_field_row(left_grid, row, "Quantity", self.quantity_entry, self.btn_scan)
        row += 1

        self.btn_add_stock = QPushButton("ADD STOCK")
        self.btn_add_stock.setObjectName("btn_add_stock")
        self.btn_add_stock.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_add_stock.setMinimumSize(124, 0)
        self.btn_remove_stock = QPushButton("REMOVE STOCK")
        self.btn_remove_stock.setObjectName("btn_remove_stock")
        self.btn_remove_stock.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_remove_stock.setMinimumSize(124, 0)
        self._add_button_row(
            left_grid, row, "Button", self.btn_add_stock, self.btn_remove_stock
        )
        row += 1

        left_grid.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding),
            row,
            1,
        )

        body_grid.addWidget(self.container_tab1_left, 1, 0)

        # Right panel — template field rows (Data output style)
        self.container_tab1_right = QFrame()
        self.container_tab1_right.setObjectName("container_tab1_right")
        self.container_tab1_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_tab1_right.setFrameShadow(QFrame.Shadow.Raised)
        right_grid = QGridLayout(self.container_tab1_right)
        right_grid.setContentsMargins(-1, 15, -1, -1)
        right_grid.setVerticalSpacing(0)

        r = 0
        details = QLabel("Component Details")
        details.setStyleSheet(styles.SECTION_TITLE_STYLE)
        right_grid.addWidget(details, r, 0)
        r += 1

        self.val_mouser = self._add_output_row(right_grid, r, "Supplier Reference")
        r += 1
        self.val_manufacturer = self._add_output_row(right_grid, r, "Manufacturer")
        r += 1
        self.val_manufacturer_ref = self._add_output_row(
            right_grid, r, "Manufacturer Reference"
        )
        r += 1
        self.val_description = self._add_output_row(right_grid, r, "Description")
        r += 1
        self.val_stock = self._add_output_row(right_grid, r, "Current Stock")
        r += 1

        right_grid.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding),
            r,
            1,
        )

        body_grid.addWidget(self.container_tab1_right, 1, 1)
        root.addWidget(self.container_main_body)

        # Footer actions — template button row style
        actions_widget = QWidget()
        actions_widget.setObjectName("widget_actions")
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(16, 9, 16, 9)
        actions_layout.setSpacing(6)

        self.btn_history_all = QPushButton("Last 20")
        self.btn_history_all.setObjectName("btn_history_all")
        self.btn_history_all.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_history_all.setMinimumSize(124, 0)

        self.btn_history_component = QPushButton("Comp. hist.")
        self.btn_history_component.setObjectName("btn_history_component")
        self.btn_history_component.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_history_component.setMinimumSize(124, 0)

        self.btn_add_manual = QPushButton("ADD MANUAL COMPONENT")
        self.btn_add_manual.setObjectName("btn_add_manual")
        self.btn_add_manual.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_add_manual.setMinimumSize(124, 0)

        self.btn_clear = QPushButton("CLEAR")
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_clear.setMinimumSize(124, 0)

        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_exit.setMinimumSize(124, 0)

        actions_layout.addWidget(self.btn_history_all)
        actions_layout.addWidget(self.btn_history_component)
        actions_layout.addWidget(self.btn_add_manual)
        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_clear)
        actions_layout.addWidget(self.btn_exit)
        root.addWidget(actions_widget)

        self.status_label = QLabel("")
        self.status_label.setObjectName("status_label")
        self.status_label.setStyleSheet(styles.STATUS_STYLE)
        self.status_label.setWordWrap(True)
        root.addWidget(self.status_label)

        window.setCentralWidget(self.centralwidget)

    def _make_template_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(styles.FIELD_LABEL_STYLE)
        label.setMinimumWidth(styles.TEMPLATE_LABEL_MIN_WIDTH)
        label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        return label

    def _template_row_layout(self) -> tuple[QWidget, QHBoxLayout]:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setSpacing(styles.TEMPLATE_ROW_SPACING)
        layout.setContentsMargins(*styles.TEMPLATE_ROW_MARGINS)
        return row, layout

    def _add_field_row(
        self,
        grid: QGridLayout,
        row: int,
        label_text: str,
        field: QLineEdit | None = None,
        *extra: QPushButton,
    ) -> QLineEdit:
        row_w, layout = self._template_row_layout()
        layout.addWidget(self._make_template_label(label_text))
        if field is None:
            field = QLineEdit()
            field.setStyleSheet(styles.LINE_EDIT_STYLE)
            field.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(field)
        for widget in extra:
            layout.addWidget(widget)
        grid.addWidget(row_w, row, 0, 1, 2)
        return field

    def _add_combo_row(
        self, grid: QGridLayout, row: int, label_text: str, combo: QComboBox
    ) -> None:
        row_w = QWidget()
        inner = QGridLayout(row_w)
        inner.setContentsMargins(0, 9, 9, 9)
        label = self._make_template_label(label_text)
        inner.addWidget(label, 0, 0)
        inner.addWidget(combo, 0, 1)
        grid.addWidget(row_w, row, 0, 1, 2)

    def _add_output_row(self, grid: QGridLayout, row: int, title: str) -> QLabel:
        row_w, layout = self._template_row_layout()
        layout.addWidget(self._make_template_label(title))
        value = QLabel("")
        value.setStyleSheet(styles.VALUE_FIELD_STYLE)
        layout.addWidget(value)
        grid.addWidget(row_w, row, 0, 1, 2)
        return value

    def _add_button_row(
        self, grid: QGridLayout, row: int, label_text: str, *buttons: QPushButton
    ) -> None:
        row_w, layout = self._template_row_layout()
        layout.addWidget(self._make_template_label(label_text))
        for btn in buttons:
            layout.addWidget(btn)
        grid.addWidget(row_w, row, 0, 1, 2)
