"""Helpers for Siemens popup tables (dialogs use designer/popups/gui_popup_*.py)."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)


def fill_readonly_table(
    table: QTableWidget,
    columns: tuple[str, ...],
    rows: list,
    *,
    row_values=None,
) -> None:
    """Populate a table with non-editable cells (popup content)."""
    from .. import styles

    table.setColumnCount(len(columns))
    table.setHorizontalHeaderLabels(list(columns))
    table.setStyleSheet(styles.TABLE_STYLE)
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.verticalHeader().setVisible(False)

    table.setRowCount(len(rows))
    for r, row in enumerate(rows):
        values = row_values(row) if row_values else row
        for c, value in enumerate(values):
            item = QTableWidgetItem(str(value) if value is not None else "")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(r, c, item)
