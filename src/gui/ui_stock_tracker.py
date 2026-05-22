"""Stock Tracker main window UI (Siemens style)."""
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
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

from . import gui_config, styles


class Ui_StockTracker:
    """Builds widgets on a QMainWindow."""

    def setupUi(self, window: QMainWindow) -> None:
        window.setObjectName("StockTracker")
        window.resize(1284, 720)
        window.setWindowTitle("Stock Tracker")
        window.setStyleSheet(styles.MAIN_WINDOW_STYLE)

        central = QWidget()
        central.setObjectName("centralwidget")
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        header = QWidget()
        header.setObjectName("header")
        header.setStyleSheet(styles.HEADER_STYLE)
        header.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        header_row = QHBoxLayout(header)
        header_row.setSpacing(16)
        header_row.setContentsMargins(16, 10, 16, 10)

        self.brand_label = QLabel()
        for logo_path in (gui_config.LOGO_PNG, gui_config.LOGO_SVG):
            if logo_path.is_file() and logo_path.suffix.lower() == ".png":
                pix = QPixmap(str(logo_path))
                if not pix.isNull():
                    self.brand_label.setPixmap(
                        pix.scaled(
                            120,
                            32,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation,
                        )
                    )
                break

        self.product_name = QLabel("Stock Tracker")
        self.product_name.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.subtitle = QLabel("Electronic Component Inventory System")
        self.subtitle.setStyleSheet(styles.SUBTITLE_STYLE)

        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        title_col.addWidget(self.product_name)
        title_col.addWidget(self.subtitle)

        header_row.addWidget(self.brand_label)
        header_row.addLayout(title_col)
        header_row.addStretch()
        root.addWidget(header)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(16, 16, 16, 8)
        body_layout.setSpacing(12)

        self.page_title = QLabel("Inventory")
        self.page_title.setStyleSheet(styles.TITLE_STYLE)
        body_layout.addWidget(self.page_title)

        panels = QHBoxLayout()
        panels.setSpacing(24)

        left = QFrame()
        left.setFrameShape(QFrame.Shape.StyledPanel)
        left_grid = QGridLayout(left)
        left_grid.setVerticalSpacing(10)
        left_grid.setHorizontalSpacing(8)

        row = 0
        lbl = QLabel("Operations")
        lbl.setStyleSheet(styles.SECTION_TITLE_STYLE)
        left_grid.addWidget(lbl, row, 0, 1, 2)
        row += 1

        self._add_field(left_grid, row, "User Name", styles.FIELD_LABEL_STYLE)
        self.user_entry = QLineEdit()
        self.user_entry.setStyleSheet(styles.LINE_EDIT_STYLE)
        left_grid.addWidget(self.user_entry, row, 1)
        row += 1

        self._add_field(left_grid, row, "Search Component", styles.FIELD_LABEL_STYLE)
        self.search_entry = QLineEdit()
        self.search_entry.setStyleSheet(styles.LINE_EDIT_STYLE)
        left_grid.addWidget(self.search_entry, row, 1)
        row += 1

        self.btn_search = QPushButton("SEARCH")
        self.btn_search.setStyleSheet(styles.BTN_PRIMARY_STYLE)
        left_grid.addWidget(self.btn_search, row, 1, Qt.AlignmentFlag.AlignLeft)
        row += 1

        self._add_field(
            left_grid, row, "Scan Barcode / Mouser Ref.", styles.FIELD_LABEL_STYLE
        )
        self.barcode_entry = QLineEdit()
        self.barcode_entry.setStyleSheet(styles.LINE_EDIT_STYLE)
        left_grid.addWidget(self.barcode_entry, row, 1)
        row += 1

        qty_row = QHBoxLayout()
        self._add_field_qty = QLabel("Quantity")
        self._add_field_qty.setStyleSheet(styles.FIELD_LABEL_STYLE)
        self.quantity_entry = QLineEdit()
        self.quantity_entry.setMaximumWidth(100)
        self.quantity_entry.setStyleSheet(styles.LINE_EDIT_STYLE)
        self.btn_scan = QPushButton("SCAN")
        self.btn_scan.setStyleSheet(styles.BTN_PRIMARY_STYLE)
        qty_row.addWidget(self._add_field_qty)
        qty_row.addWidget(self.quantity_entry)
        qty_row.addWidget(self.btn_scan)
        qty_row.addStretch()
        left_grid.addLayout(qty_row, row, 0, 1, 2)
        row += 1

        stock_btns = QHBoxLayout()
        self.btn_add_stock = QPushButton("ADD STOCK")
        self.btn_add_stock.setStyleSheet(styles.BTN_SUCCESS_STYLE)
        self.btn_remove_stock = QPushButton("REMOVE STOCK")
        self.btn_remove_stock.setStyleSheet(styles.BTN_DANGER_STYLE)
        stock_btns.addWidget(self.btn_add_stock)
        stock_btns.addWidget(self.btn_remove_stock)
        stock_btns.addStretch()
        left_grid.addLayout(stock_btns, row, 0, 1, 2)
        row += 1

        left_grid.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), row, 0
        )

        right = QFrame()
        right.setFrameShape(QFrame.Shape.StyledPanel)
        right_grid = QGridLayout(right)
        right_grid.setVerticalSpacing(10)

        r = 0
        t = QLabel("Component Details")
        t.setStyleSheet(styles.SECTION_TITLE_STYLE)
        right_grid.addWidget(t, r, 0, 1, 2)
        r += 1

        self.val_mouser = self._add_value_row(right_grid, r, "Mouser Reference")
        r += 1
        self.val_manufacturer = self._add_value_row(right_grid, r, "Manufacturer")
        r += 1
        self.val_manufacturer_ref = self._add_value_row(
            right_grid, r, "Manufacturer Reference"
        )
        r += 1
        self.val_description = self._add_value_row(right_grid, r, "Description")
        r += 1

        stock_lbl = QLabel("Current Stock")
        stock_lbl.setStyleSheet(styles.FIELD_LABEL_STYLE)
        right_grid.addWidget(stock_lbl, r, 0)
        self.val_stock = QLabel("")
        self.val_stock.setStyleSheet(styles.STOCK_VALUE_STYLE)
        self.val_stock.setWordWrap(True)
        right_grid.addWidget(self.val_stock, r, 1)
        r += 1

        right_grid.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), r, 0
        )

        panels.addWidget(left, 1)
        panels.addWidget(right, 1)
        body_layout.addLayout(panels)

        actions = QHBoxLayout()
        self.btn_history_all = QPushButton("VIEW LAST 20 HISTORY")
        self.btn_history_all.setStyleSheet(styles.BTN_SECONDARY_STYLE)
        self.btn_history_component = QPushButton("VIEW CURRENT COMPONENT HISTORY")
        self.btn_history_component.setStyleSheet(styles.BTN_SECONDARY_STYLE)
        self.btn_clear = QPushButton("CLEAR")
        self.btn_clear.setStyleSheet(styles.BTN_NEUTRAL_STYLE)
        actions.addWidget(self.btn_history_all)
        actions.addWidget(self.btn_history_component)
        actions.addStretch()
        actions.addWidget(self.btn_clear)
        body_layout.addLayout(actions)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(styles.STATUS_STYLE)
        self.status_label.setWordWrap(True)
        body_layout.addWidget(self.status_label)

        root.addWidget(body)
        window.setCentralWidget(central)

    @staticmethod
    def _add_field(grid: QGridLayout, row: int, text: str, style: str) -> None:
        label = QLabel(text)
        label.setStyleSheet(style)
        grid.addWidget(label, row, 0)

    def _add_value_row(self, grid: QGridLayout, row: int, title: str) -> QLabel:
        label = QLabel(title)
        label.setStyleSheet(styles.FIELD_LABEL_STYLE)
        grid.addWidget(label, row, 0)
        value = QLabel("")
        value.setStyleSheet(styles.VALUE_FIELD_STYLE)
        value.setWordWrap(True)
        value.setMinimumHeight(28)
        grid.addWidget(value, row, 1)
        return value
