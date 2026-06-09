"""Pick one material row from Excel search results."""
from PySide6.QtWidgets import QDialog, QTableWidget

from .designer.popups.gui_popup_search import Ui_PopupSearch
from .siemens_template.popup_shell import fill_readonly_table

COLUMNS = (
    "Supplier Reference",
    "Serial Number",
    "Description",
    "Calibration Date",
    "Calibration Expiration",
)


class MaterialSearchDialog(QDialog):
    def __init__(self, matches: list, row_to_dict, parent=None):
        super().__init__(parent)
        self._matches = matches
        self._selected_row = None

        self.ui = Ui_PopupSearch()
        self.ui.setupUi(self)
        self.ui.table_search.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.ui.table_search.doubleClicked.connect(self._accept_selection)

        table_rows = [row_to_dict(row) for row in matches]

        def values(data):
            return (
                data["supplier_reference"],
                data["serial_number"],
                data["description"],
                data["calibration_date"],
                data["calibration_expiration"],
            )

        fill_readonly_table(
            self.ui.table_search,
            COLUMNS,
            table_rows,
            row_values=values,
        )

        if matches:
            self.ui.table_search.selectRow(0)

        self.ui.btn_ok.clicked.connect(self._accept_selection)
        self.ui.btn_cancel.clicked.connect(self.reject)

    def _accept_selection(self) -> None:
        row_idx = self.ui.table_search.currentRow()
        if row_idx < 0 or row_idx >= len(self._matches):
            return
        self._selected_row = self._matches[row_idx]
        self.accept()

    def selected_row(self):
        return self._selected_row
