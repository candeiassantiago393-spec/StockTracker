"""Read-only table of Massive inventory rows."""
from PySide6.QtWidgets import QDialog

from .designer.popups.components.gui_popup_history import Ui_PopupHistory
from .siemens_template.popup_shell import fill_readonly_table

COLUMNS = (
    "ID",
    "Type",
    "Value",
    "Tolerance",
    "Package",
    "Name",
    "Stock",
)


class MassiveTableDialog(QDialog):
    def __init__(self, rows, parent=None, *, title: str = "Passive"):
        super().__init__(parent)
        self.ui = Ui_PopupHistory()
        self.ui.setupUi(self)
        if hasattr(self.ui, "tittle"):
            self.ui.tittle.setText(title)
        fill_readonly_table(self.ui.table_history, COLUMNS, rows)
        self.ui.btn_ok.clicked.connect(self.accept)
