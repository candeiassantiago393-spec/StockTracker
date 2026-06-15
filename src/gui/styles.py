"""
Siemens template styles — values from gui_template.ui (Platform Test Bench).
"""

# Template form metrics (gui_template.ui)
TEMPLATE_LABEL_MIN_WIDTH = 74
TEMPLATE_FIELD_WIDTH = 100
TEMPLATE_COMBO_MIN_SIZE = (172, 30)
TEMPLATE_ROW_SPACING = 6
TEMPLATE_ROW_MARGINS = (0, 9, 9, 9)  # left, top, right, bottom
# Main body grids — match footer bar (left/right 16px).
TEMPLATE_PAGE_MARGINS = (16, 0, 16, 0)


def apply_two_column_page_grid(grid) -> None:
    """Symmetric 50/50 columns with no gutter (gui_stocktracker.ui / gui_template.ui)."""
    grid.setContentsMargins(*TEMPLATE_PAGE_MARGINS)
    grid.setHorizontalSpacing(0)
    grid.setVerticalSpacing(0)
    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 1)

MAIN_WINDOW_STYLE = """
* {
    border: none;
    background: #000028;
    padding: 0;
    margin: 0;
    color: #FFFFFF;
    font-family: "SiemensSansPro_A_Bd";
    font-size: 14px;
}
"""

HEADER_STYLE = """
* {
    background: #333353;
}
"""

PRODUCT_NAME_STYLE = """
* {
    font-size: 18px;
}
"""

PAGE_TITLE_STYLE = """
QLabel {
    font-size: 40px;
}
"""

SECTION_TITLE_STYLE = """
QLabel {
    font-size: 20px;
    font-weight: bold;
}
"""

SUBSECTION_TITLE_STYLE = """
QLabel {
    font-size: 16px;
    font-weight: bold;
    padding-top: 4px;
}
"""

FIELD_LABEL_STYLE = ""

LINE_EDIT_STYLE = """
QLineEdit {
    min-width: 100px;
    max-width: 100px;
    max-height: 18px;
    padding: 5px;
    padding-bottom: 7px;
    margin-top: 0px;
    border-radius: 2px;
    border: 1px solid #B3B3BE;
    background-color: #00183B;
    color: #FFFFFF;
}
QLineEdit:hover {
    background-color: #001F39;
    border: 1px solid #00FFB9;
}
"""

COMBOBOX_STYLE = """
QComboBox {
    padding: 5px;
    padding-left: 20px;
    padding-right: 20px;
    min-width: 130;
    min-height: 18px;
    max-width: 130px;
    max-height: 18px;
    border-radius: 2px;
    border: 1px solid #B3B3BE;
    background-color: #00183B;
}
QComboBox:hover {
    background-color: #001F39;
    border: 1px solid #00FFB9;
}
QComboBox QAbstractItemView {
    background-color: #2D2D45;
    padding: 0px;
}
QComboBox QAbstractItemView::item:hover {
    padding: 0px;
    padding-left: 10px;
}
"""

VALUE_FIELD_STYLE = """
QLabel {
    min-width: 100px;
    max-width: 100px;
    max-height: 18px;
    padding: 5px;
    padding-bottom: 7px;
    margin-top: 0px;
    border-radius: 2px;
    border: 1px solid #B3B3BE;
    background-color: #00183B;
    color: #FFFFFF;
}
QLabel:hover {
    background-color: #001F39;
    border: 1px solid #00FFB9;
}
"""

STOCK_VALUE_STYLE = VALUE_FIELD_STYLE

# Wider read-only fields (equipments description, etc.)
EQUIPMENT_VALUE_FIELD_STYLE = """
QLabel {
    min-width: 280px;
    max-width: 480px;
    min-height: 18px;
    padding: 5px;
    padding-bottom: 7px;
    margin-top: 0px;
    border-radius: 2px;
    border: 1px solid #B3B3BE;
    background-color: #00183B;
    color: #FFFFFF;
}
QLabel:hover {
    background-color: #001F39;
    border: 1px solid #00FFB9;
}
"""

BTN_TEMPLATE_STYLE = """
QPushButton {
    min-width: 100px;
    max-width: 100px;
    padding: 6px 12px 6px 12px;
    border-radius: 2px;
    opacity: 1;
    text-align: center;
    background-color: #00CCCC;
    color: #000028;
}
QPushButton:hover {
    background-color: #00FFB9;
}
QPushButton:pressed {
    background-color: #00E5AA;
}
"""

BTN_COPY_STYLE = """
QPushButton {
    min-width: 60px;
    max-width: 60px;
    padding: 4px 6px;
    border-radius: 2px;
    text-align: center;
    background-color: #00CCCC;
    color: #000028;
    font-size: 12px;
}
QPushButton:hover {
    background-color: #00FFB9;
}
QPushButton:pressed {
    background-color: #00E5AA;
}
"""

BTN_PRIMARY_STYLE = BTN_TEMPLATE_STYLE
BTN_SUCCESS_STYLE = BTN_TEMPLATE_STYLE
BTN_DANGER_STYLE = BTN_TEMPLATE_STYLE
BTN_SECONDARY_STYLE = BTN_TEMPLATE_STYLE
BTN_NEUTRAL_STYLE = BTN_TEMPLATE_STYLE
BTN_WIDE_STYLE = BTN_TEMPLATE_STYLE

STATUS_STYLE = """
QLabel {
    color: #B3B3BE;
    font-size: 12px;
}
"""

TABLE_STYLE = """
QTableWidget {
    background-color: #00183B;
    gridline-color: #333353;
    border: 1px solid #B3B3BE;
}
QHeaderView::section {
    background-color: #333353;
    color: #FFFFFF;
    padding: 6px;
    border: 1px solid #B3B3BE;
    font-weight: bold;
}
QTableWidget QScrollBar:vertical {
    background-color: #00183B;
    width: 12px;
    margin: 0;
}
QTableWidget QScrollBar::handle:vertical {
    background-color: #00CCCC;
    min-height: 24px;
    border-radius: 4px;
}
QTableWidget QScrollBar::add-line:vertical,
QTableWidget QScrollBar::sub-line:vertical {
    height: 0;
}
QTableWidget QScrollBar:horizontal {
    background-color: #00183B;
    height: 12px;
    margin: 0;
}
QTableWidget QScrollBar::handle:horizontal {
    background-color: #00CCCC;
    min-width: 24px;
    border-radius: 4px;
}
QTableWidget QScrollBar::add-line:horizontal,
QTableWidget QScrollBar::sub-line:horizontal {
    width: 0;
}
"""

POPUP_TABLE_MAX_HEIGHT = 280

LIST_WIDGET_STYLE = """
QListWidget {
    background-color: #00183B;
    border: 1px solid #B3B3BE;
    color: #FFFFFF;
    padding: 2px;
    font-size: 12px;
}
QListWidget::item {
    padding: 2px 4px;
    min-height: 18px;
}
QListWidget::item:selected {
    background-color: #333353;
    border: 1px solid #00FFB9;
}
QListWidget::item:hover {
    background-color: #001F39;
}
QListWidget QScrollBar:vertical {
    background-color: #00183B;
    width: 12px;
}
QListWidget QScrollBar::handle:vertical {
    background-color: #00CCCC;
    min-height: 24px;
    border-radius: 4px;
}
"""

BTN_WIDE_ACTION_STYLE = """
QPushButton {
    min-height: 28px;
    padding: 6px 12px;
    border-radius: 2px;
    text-align: center;
    background-color: #00CCCC;
    color: #000028;
}
QPushButton:hover {
    background-color: #00FFB9;
}
QPushButton:pressed {
    background-color: #00E5AA;
}
"""

SUBTITLE_STYLE = STATUS_STYLE

# gui_popup.ui (Siemens popup template)
POPUP_WINDOW_STYLE = """
* {
    border: none;
    background: #000028;
    padding: 0;
    margin: 0;
    color: #f3f3f0;
    font-family: "SiemensSansPro_A_Bd";
    font-size: 14px;
}
"""

POPUP_TITLE_STYLE = """
QLabel {
    color: #009999;
    font-size: 30px;
    font-weight: bold;
}
"""

POPUP_DESCRIPTION_STYLE = """
background-color: #333353;
border-radius: 2px;
padding: 5px;
padding-bottom: 7px;
margin-top: 0px;
color: #f3f3f0;
border: 1px solid #009999;
"""

POPUP_BTN_STYLE = BTN_TEMPLATE_STYLE
