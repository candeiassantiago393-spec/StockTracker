"""Optional location prompt when adding stock to items without a location."""
from PySide6.QtWidgets import QDialog

from src.core.stock import StockTracker

from .designer.popups.shared.gui_popup_confirm import Ui_PopupConfirm
from .location_combo import build_location_combo


class OptionalLocationDialog(QDialog):
    def __init__(
        self,
        parent=None,
        tracker: StockTracker | None = None,
        *,
        current: str = "",
    ):
        super().__init__(parent)
        self.ui = Ui_PopupConfirm()
        self.ui.setupUi(self)
        self.ui.tittle.setText("Location")
        self.ui.description.setText(
            "This item has no storage location.\n\n"
            "Choose a shelf or drawer now, or click Skip to add stock without "
            "setting a location."
        )
        self.ui.description.setMinimumHeight(88)
        self.ui.btn_ok.setText("Save")
        self.ui.btn_cancel.setVisible(True)
        self.ui.btn_cancel.setText("Skip")

        self._combo = build_location_combo(tracker, current=current, parent=self)
        self._combo.setMinimumHeight(36)
        self.ui.verticalLayout.insertWidget(2, self._combo)

        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)
        line = self._combo.lineEdit()
        if line is not None:
            line.returnPressed.connect(self.accept)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        line = self._combo.lineEdit()
        if line is not None:
            line.setFocus()
            line.selectAll()

    def location(self) -> str:
        return self._combo.currentText().strip()

    @staticmethod
    def ask(
        parent=None,
        tracker: StockTracker | None = None,
        *,
        current: str = "",
    ) -> str | None:
        """
        Returns location text if the user saved a non-empty value.
        Returns None if the user skipped or left the field empty.
        """
        dialog = OptionalLocationDialog(parent, tracker, current=current)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        value = dialog.location()
        return value or None
