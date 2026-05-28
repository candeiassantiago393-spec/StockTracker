"""History table — Siemens gui_popup.ui shell."""
from PySide6.QtWidgets import QTableWidget, QVBoxLayout, QWidget

from .siemens_template.popup_shell import SiemensPopupDialog, fill_readonly_table

COLUMNS = (
    "Date",
    "User",
    "Supplier Reference",
    "Movement",
    "Quantity",
    "Stock After",
)


class HistoryDialog(SiemensPopupDialog):
    def __init__(self, rows, parent=None):
        super().__init__("History", parent)
        self.resize(850, 480)
        self.set_subtitle(None)

        host = QWidget()
        layout = QVBoxLayout(host)
        layout.setContentsMargins(0, 20, 0, 0)

        self.table = QTableWidget()
        fill_readonly_table(self.table, COLUMNS, rows)
        layout.addWidget(self.table)

        self.set_body_widget(host)
        self.configure_buttons(ok_text="Close", show_cancel=False)
