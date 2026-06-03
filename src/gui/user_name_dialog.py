"""Pedir nome de utilizador no popup Siemens (sem voltar ao ecra principal)."""
from PySide6.QtWidgets import QDialog, QLineEdit

from .designer.popups.gui_popup_confirm import Ui_PopupConfirm

_LINE_EDIT_STYLE = """
background-color: #333353;
border-radius: 2px;
padding: 8px;
color: #f3f3f0;
border: 1px solid #009999;
font-size: 14px;
"""


class UserNameDialog(QDialog):
    def __init__(self, parent=None, initial: str = ""):
        super().__init__(parent)
        self.ui = Ui_PopupConfirm()
        self.ui.setupUi(self)
        self.ui.tittle.setText("User Name")
        self.ui.description.setText("Enter your name to continue with this operation.")
        self.ui.description.setMinimumHeight(72)
        self.ui.btn_ok.setText("OK")
        self.ui.btn_cancel.setVisible(False)

        self._entry = QLineEdit(self)
        self._entry.setStyleSheet(_LINE_EDIT_STYLE)
        self._entry.setMinimumHeight(40)
        self._entry.setPlaceholderText("User name")
        if initial:
            self._entry.setText(initial)
        self.ui.verticalLayout.insertWidget(2, self._entry)

        self.ui.btn_ok.clicked.connect(self._accept_if_valid)
        self._entry.returnPressed.connect(self._accept_if_valid)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._entry.setFocus()

    def _accept_if_valid(self) -> None:
        if self._entry.text().strip():
            self.accept()

    def name(self) -> str:
        return self._entry.text().strip()

    @staticmethod
    def ask(parent=None, initial: str = "") -> str | None:
        dialog = UserNameDialog(parent, initial=initial)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.name()
        return None
