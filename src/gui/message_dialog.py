"""Siemens-styled alert and question dialogs (gui_popup_confirm.ui)."""
from PySide6.QtWidgets import QDialog

from .designer.popups.shared.gui_popup_confirm import Ui_PopupConfirm


class SiemensMessageDialog(QDialog):
    """Alert (OK) or question (Yes/No) using the Siemens popup template."""

    def __init__(
        self,
        title: str,
        message: str,
        parent=None,
        *,
        ok_text: str = "OK",
        show_cancel: bool = False,
        cancel_text: str = "No",
    ):
        super().__init__(parent)
        self.ui = Ui_PopupConfirm()
        self.ui.setupUi(self)
        self.ui.tittle.setText(title)
        self.ui.description.setText(message)
        self.ui.description.setWordWrap(True)
        self.ui.description.setMinimumHeight(120)
        self.ui.btn_ok.setText(ok_text)
        self.ui.btn_cancel.setText(cancel_text)
        self.ui.btn_cancel.setVisible(show_cancel)
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)

    @staticmethod
    def alert(parent, title: str, message: str) -> None:
        dialog = SiemensMessageDialog(title, message, parent, show_cancel=False)
        dialog.exec()

    @staticmethod
    def ask(parent, title: str, message: str) -> bool:
        dialog = SiemensMessageDialog(
            title,
            message,
            parent,
            ok_text="Yes",
            show_cancel=True,
            cancel_text="No",
        )
        return dialog.exec() == QDialog.DialogCode.Accepted


class SiemensMessage:
    """Drop-in style API similar to QMessageBox (parent, title, text)."""

    @staticmethod
    def warning(parent, title: str, text: str) -> None:
        SiemensMessageDialog.alert(parent, title, text)

    @staticmethod
    def information(parent, title: str, text: str) -> None:
        SiemensMessageDialog.alert(parent, title, text)

    @staticmethod
    def critical(parent, title: str, text: str) -> None:
        SiemensMessageDialog.alert(parent, title, text)

    @staticmethod
    def question(parent, title: str, text: str) -> bool:
        return SiemensMessageDialog.ask(parent, title, text)
