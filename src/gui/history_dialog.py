"""History table — Qt Designer gui_popup_history.ui."""
from PySide6.QtWidgets import QDialog

from .designer.popups.components.gui_popup_history import Ui_PopupHistory
from .siemens_template.popup_shell import fill_readonly_table

COLUMNS = (
    "Date",
    "User",
    "Supplier Reference",
    "Movement",
    "Quantity",
    "Stock After",
)


class HistoryDialog(QDialog):
    def __init__(self, rows, parent=None):
        super().__init__(parent)
        self.ui = Ui_PopupHistory()
        self.ui.setupUi(self)
        fill_readonly_table(self.ui.table_history, COLUMNS, rows)
        self.ui.btn_ok.clicked.connect(self.accept)
