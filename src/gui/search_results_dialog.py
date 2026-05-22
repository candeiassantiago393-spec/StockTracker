"""Dialog to pick one component when Excel search returns multiple matches."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from . import styles

COLUMNS = (
    "Mouser Reference",
    "Manufacturer",
    "Manufacturer Reference",
    "Description",
    "Stock",
)


class SearchResultsDialog(QDialog):
    def __init__(self, matches: list, row_to_dict, parent=None):
        super().__init__(parent)
        self._matches = matches
        self._row_to_dict = row_to_dict
        self._selected_row = None

        self.setWindowTitle("Search results")
        self.resize(900, 360)
        self.setStyleSheet(styles.MAIN_WINDOW_STYLE)

        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(len(COLUMNS))
        self.table.setHorizontalHeaderLabels(list(COLUMNS))
        self.table.setStyleSheet(styles.TABLE_STYLE)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.verticalHeader().setVisible(False)
        self.table.doubleClicked.connect(self._accept_selection)

        self.table.setRowCount(len(matches))
        for r, row in enumerate(matches):
            data = row_to_dict(row)
            values = (
                data["mouser"],
                data["manufacturer"],
                data["manufacturer_ref"],
                data["description"],
                data["stock"],
            )
            for c, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(r, c, item)

        if matches:
            self.table.selectRow(0)

        layout.addWidget(self.table)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._accept_selection)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _accept_selection(self) -> None:
        row_idx = self.table.currentRow()
        if row_idx < 0 or row_idx >= len(self._matches):
            return
        self._selected_row = self._matches[row_idx]
        self.accept()

    def selected_row(self):
        return self._selected_row
