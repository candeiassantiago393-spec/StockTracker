"""History table — Qt Designer gui_popup_history.ui."""
from PySide6.QtWidgets import QDialog, QTableWidget

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
    def __init__(self, rows, parent=None, *, title: str | None = None):
        super().__init__(parent)
        self._rows = rows
        self._selected_row = None

        self.ui = Ui_PopupHistory()
        self.ui.setupUi(self)
        if title and hasattr(self.ui, "tittle"):
            self.ui.tittle.setText(title)

        self.ui.table_history.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.ui.table_history.doubleClicked.connect(self._accept_selection)

        fill_readonly_table(self.ui.table_history, COLUMNS, rows)

        if rows:
            self.ui.table_history.selectRow(0)

        self.ui.btn_ok.setText("Open")
        self.ui.btn_ok.clicked.connect(self._accept_selection)
        if hasattr(self.ui, "btn_cancel"):
            self.ui.btn_cancel.setVisible(True)
            self.ui.btn_cancel.setText("Close")
            self.ui.btn_cancel.clicked.connect(self.reject)

    def _accept_selection(self) -> None:
        row_idx = self.ui.table_history.currentRow()
        if row_idx < 0 or row_idx >= len(self._rows):
            return
        self._selected_row = self._rows[row_idx]
        self.accept()

    def selected_row(self):
        return self._selected_row
