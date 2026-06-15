"""Read-only table of equipments from Excel."""
from PySide6.QtWidgets import QDialog

from .designer.popups.equipments.gui_popup_history import Ui_PopupEquipmentHistory as Ui_PopupHistory
from .siemens_template.popup_shell import fill_readonly_table

COLUMNS = (
    "ID",
    "Supplier Reference",
    "Serial Number",
    "Description",
    "Calibration Date",
    "Calibration Expiration",
)


class EquipmentsTableDialog(QDialog):
    def __init__(self, rows, parent=None, *, title: str = "Equipments"):
        super().__init__(parent)
        self.ui = Ui_PopupHistory()
        self.ui.setupUi(self)
        if hasattr(self.ui, "tittle"):
            self.ui.tittle.setText(title)
        fill_readonly_table(self.ui.table_history, COLUMNS, rows)
        self.ui.btn_ok.clicked.connect(self.accept)
