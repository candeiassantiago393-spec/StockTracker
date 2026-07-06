"""Selectable table of Components inventory rows."""
from PySide6.QtWidgets import QDialog, QTableWidget

from .designer.popups.components.gui_popup_history import Ui_PopupHistory
from .siemens_template.popup_shell import fill_readonly_table

COLUMNS = (
    "ID",
    "Supplier Ref",
    "Manufacturer",
    "Mfr Ref",
    "Description",
    "Stock",
)


class ComponentsTableDialog(QDialog):
    def __init__(
        self,
        excel_rows: list,
        row_to_dict,
        parent=None,
        *,
        title: str = "Components",
    ):
        super().__init__(parent)
        self._rows = excel_rows
        self._row_to_dict = row_to_dict
        self._selected_row = None

        self.ui = Ui_PopupHistory()
        self.ui.setupUi(self)
        if hasattr(self.ui, "tittle"):
            self.ui.tittle.setText(title)

        self.ui.table_history.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.ui.table_history.doubleClicked.connect(self._accept_selection)

        def values(row):
            data = row_to_dict(row)
            return (
                row[0].value or "",
                data["mouser"],
                data["manufacturer"],
                data["manufacturer_ref"],
                data["description"],
                data["stock"],
            )

        fill_readonly_table(
            self.ui.table_history,
            COLUMNS,
            excel_rows,
            row_values=values,
        )

        if excel_rows:
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
