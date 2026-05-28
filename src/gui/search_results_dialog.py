"""Pick one Excel match — Siemens gui_popup.ui shell."""
from PySide6.QtWidgets import QTableWidget, QVBoxLayout, QWidget

from .siemens_template.popup_shell import SiemensPopupDialog, fill_readonly_table

COLUMNS = (
    "Supplier Reference",
    "Manufacturer",
    "Manufacturer Reference",
    "Description",
    "Stock",
)


class SearchResultsDialog(SiemensPopupDialog):
    def __init__(self, matches: list, row_to_dict, parent=None):
        super().__init__(
            "Search results",
            parent,
            connect_default_buttons=False,
        )
        self._matches = matches
        self._row_to_dict = row_to_dict
        self._selected_row = None

        self.resize(900, 480)
        self.set_subtitle("Select a row and press Ok, or double-click a row.")

        host = QWidget()
        layout = QVBoxLayout(host)
        layout.setContentsMargins(0, 12, 0, 0)

        self.table = QTableWidget()
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.doubleClicked.connect(self._accept_selection)

        table_rows = [row_to_dict(row) for row in matches]

        def values(data):
            return (
                data["mouser"],
                data["manufacturer"],
                data["manufacturer_ref"],
                data["description"],
                data["stock"],
            )

        fill_readonly_table(
            self.table,
            COLUMNS,
            table_rows,
            row_values=values,
        )

        if matches:
            self.table.selectRow(0)

        layout.addWidget(self.table)
        self.set_body_widget(host)
        self.configure_buttons(ok_text="Ok", cancel_text="Cancel")

        self.ui.btn_ok.clicked.connect(self._accept_selection)
        self.ui.btn_cancel.clicked.connect(self.reject)

    def _accept_selection(self) -> None:
        row_idx = self.table.currentRow()
        if row_idx < 0 or row_idx >= len(self._matches):
            return
        self._selected_row = self._matches[row_idx]
        self.accept()

    def selected_row(self):
        return self._selected_row
