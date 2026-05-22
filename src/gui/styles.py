"""Siemens-style Qt stylesheets (Stock Tracker GUI)."""

MAIN_WINDOW_STYLE = """
* {
    border: none;
    background: #000028;
    padding: 0;
    margin: 0;
    color: #FFFFFF;
    font-family: "Segoe UI", "SiemensSansPro_A_Bd", sans-serif;
    font-size: 14px;
}
"""

HEADER_STYLE = """
QWidget#header {
    background: #333353;
}
"""

TITLE_STYLE = """
QLabel {
    font-size: 40px;
}
"""

SUBTITLE_STYLE = """
QLabel {
    font-size: 12px;
    color: #B3B3BE;
}
"""

SECTION_TITLE_STYLE = """
QLabel {
    font-size: 20px;
    font-weight: bold;
}
"""

FIELD_LABEL_STYLE = """
QLabel {
    color: #00CCCC;
    font-weight: bold;
}
"""

LINE_EDIT_STYLE = """
QLineEdit {
    min-width: 200px;
    max-height: 28px;
    padding: 6px;
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

VALUE_FIELD_STYLE = """
QLabel {
    min-height: 24px;
    padding: 6px;
    border-radius: 2px;
    border: 1px solid #B3B3BE;
    background-color: #00183B;
    color: #FFFFFF;
}
"""

STOCK_VALUE_STYLE = """
QLabel {
    font-size: 28px;
    font-weight: bold;
    color: #00FFB9;
    border: none;
    background: transparent;
}
"""

BTN_PRIMARY_STYLE = """
QPushButton {
    min-width: 110px;
    padding: 8px 14px;
    border-radius: 2px;
    background-color: #00CCCC;
    color: #000028;
    font-weight: bold;
}
QPushButton:hover { background-color: #00FFB9; }
QPushButton:pressed { background-color: #00E5AA; }
"""

BTN_SUCCESS_STYLE = """
QPushButton {
    min-width: 120px;
    padding: 8px 14px;
    border-radius: 2px;
    background-color: #008C5A;
    color: #FFFFFF;
    font-weight: bold;
}
QPushButton:hover { background-color: #00A86B; }
QPushButton:pressed { background-color: #006B45; }
"""

BTN_DANGER_STYLE = """
QPushButton {
    min-width: 130px;
    padding: 8px 14px;
    border-radius: 2px;
    background-color: #B00020;
    color: #FFFFFF;
    font-weight: bold;
}
QPushButton:hover { background-color: #D00028; }
QPushButton:pressed { background-color: #800018; }
"""

BTN_SECONDARY_STYLE = """
QPushButton {
    min-width: 100px;
    padding: 8px 14px;
    border-radius: 2px;
    background-color: #263847;
    color: #FFFFFF;
    font-weight: bold;
}
QPushButton:hover { background-color: #1D2A35; }
"""

BTN_NEUTRAL_STYLE = """
QPushButton {
    min-width: 90px;
    padding: 8px 14px;
    border-radius: 2px;
    background-color: #555555;
    color: #FFFFFF;
    font-weight: bold;
}
QPushButton:hover { background-color: #333333; }
"""

STATUS_STYLE = """
QLabel {
    color: #B3B3BE;
    font-size: 12px;
    padding: 8px;
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
"""
