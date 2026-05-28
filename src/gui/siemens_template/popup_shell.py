"""
Siemens popup shell — same layout as gui_popup.ui / GuiPopupSetup.

All Stock Tracker dialogs use Ui_Popup from gui_popup.py (generated from gui_popup.ui).
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from .gui_popup import Ui_Popup


class SiemensPopupDialog(QDialog):
    """Base dialog: title (tittle), optional subtitle, body, Ok/Cancel."""

    def __init__(
        self,
        title: str,
        parent=None,
        *,
        connect_default_buttons: bool = True,
    ):
        super().__init__(parent)
        self.ui = Ui_Popup()
        self.ui.setupUi(self)
        self.ui.tittle.setText(title)
        self._body_index = self.ui.verticalLayout.indexOf(self.ui.widget) + 1

        if connect_default_buttons:
            self.ui.btn_ok.clicked.connect(self.accept)
            self.ui.btn_cancel.clicked.connect(self.reject)

    def set_subtitle(self, text: str | None) -> None:
        """Text in the template description panel (gui_popup.ui «description»)."""
        if text:
            self.ui.description.setText(text)
            self.ui.description.setMinimumHeight(60)
            self.ui.widget.show()
        else:
            self.ui.widget.hide()

    def set_body_widget(self, widget: QWidget) -> None:
        """Main content between subtitle area and Ok/Cancel (form, table, …)."""
        self.ui.verticalLayout.insertWidget(self._body_index, widget)

    def configure_buttons(
        self,
        ok_text: str = "Ok",
        cancel_text: str = "Cancel",
        *,
        show_cancel: bool = True,
    ) -> None:
        self.ui.btn_ok.setText(ok_text)
        self.ui.btn_cancel.setText(cancel_text)
        self.ui.btn_cancel.setVisible(show_cancel)


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
