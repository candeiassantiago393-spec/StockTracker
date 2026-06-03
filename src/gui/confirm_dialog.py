"""Siemens confirmation popup — delegates to message_dialog."""
from .message_dialog import SiemensMessageDialog


class SiemensConfirmDialog:
    @staticmethod
    def ask(title: str, message: str, parent=None) -> bool:
        return SiemensMessageDialog.ask(parent, title, message)
