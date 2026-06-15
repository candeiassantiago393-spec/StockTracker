"""Helpers for Siemens popup tables (dialogs use designer/popups/gui_popup_*.py)."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractScrollArea,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from ..styles import POPUP_TABLE_MAX_HEIGHT


def configure_popup_table(
    table: QTableWidget,
    *,
    max_height: int = POPUP_TABLE_MAX_HEIGHT,
) -> None:
    """Fixed viewport height with vertical scroll for large result sets."""
    table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
    table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
    table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
    table.setMinimumHeight(max_height)
    table.setMaximumHeight(max_height)


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
    configure_popup_table(table)
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

    if rows:
        table.scrollToTop()
