"""Pick one Massive item from search results."""
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from . import styles
from .designer.popups.equipments.gui_popup_search import Ui_PopupEquipmentSearch as Ui_PopupSearch
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


class MassiveSearchDialog(QDialog):
    def __init__(self, matches: list, row_to_dict, parent=None):
        super().__init__(parent)
        self._all_matches = matches
        self._row_to_dict = row_to_dict
        self._visible_matches: list = []
        self._selected_row = None

        self.ui = Ui_PopupSearch()
        self.ui.setupUi(self)
        if hasattr(self.ui, "tittle"):
            self.ui.tittle.setText("Passive — search results")
        self.ui.table_search.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.ui.table_search.doubleClicked.connect(self._accept_selection)

        self._build_type_filter()
        self._apply_type_filter()

        self.ui.btn_ok.clicked.connect(self._accept_selection)
        self.ui.btn_cancel.clicked.connect(self.reject)

    def _build_type_filter(self) -> None:
        host = QWidget(self)
        row = QHBoxLayout(host)
        row.setContentsMargins(20, 0, 20, 8)
        row.setSpacing(10)

        label = QLabel("Type")
        label.setMinimumWidth(styles.TEMPLATE_LABEL_MIN_WIDTH)

        self._type_filter = QComboBox()
        self._type_filter.setMinimumWidth(styles.TEMPLATE_COMBO_MIN_SIZE[0])
        self._type_filter.setStyleSheet(styles.LINE_EDIT_STYLE)
        self._type_filter.addItem("All", "")
        self._type_filter.addItem("Resistor (R)", "R")
        self._type_filter.addItem("Capacitor (C)", "C")
        self._type_filter.currentIndexChanged.connect(self._apply_type_filter)

        row.addWidget(label)
        row.addWidget(self._type_filter)
        row.addStretch()

        body_layout = self.ui.table_search.parentWidget().layout()
        if isinstance(body_layout, QVBoxLayout):
            index = body_layout.indexOf(self.ui.table_search)
            body_layout.insertWidget(index, host)

    def _part_type_for_match(self, match) -> str:
        data = self._row_to_dict(match)
        return str(data.get("part_type") or "").strip().upper()

    def _apply_type_filter(self) -> None:
        filter_type = str(self._type_filter.currentData() or "").strip().upper()
        if filter_type:
            self._visible_matches = [
                match
                for match in self._all_matches
                if self._part_type_for_match(match) == filter_type
            ]
        else:
            self._visible_matches = list(self._all_matches)

        self._refill_table()
        self.ui.btn_ok.setEnabled(bool(self._visible_matches))

    def _refill_table(self) -> None:
        table_rows = [self._row_to_dict(row) for row in self._visible_matches]

        def values(data):
            return (
                data["id"],
                data["part_type"],
                data["value"],
                data["tolerance"],
                data["package"],
                data["name"],
                data["stock"],
            )

        fill_readonly_table(
            self.ui.table_search,
            COLUMNS,
            table_rows,
            row_values=values,
        )

        if self._visible_matches:
            self.ui.table_search.selectRow(0)

    def _accept_selection(self) -> None:
        row_idx = self.ui.table_search.currentRow()
        if row_idx < 0 or row_idx >= len(self._visible_matches):
            return
        self._selected_row = self._visible_matches[row_idx]
        self.accept()

    def selected_row(self):
        return self._selected_row
