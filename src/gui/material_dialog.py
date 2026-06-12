"""Add or edit a material — Qt Designer popups/materials/gui_popup_material.ui."""
from PySide6.QtWidgets import QDialog

from .designer.popups.materials.gui_popup_material import Ui_PopupMaterial
from .message_dialog import SiemensMessage


class MaterialDialog(QDialog):
    def __init__(self, parent=None, *, initial: dict | None = None, title: str = "Material"):
        super().__init__(parent)
        self.ui = Ui_PopupMaterial()
        self.ui.setupUi(self)
        self.ui.tittle.setText(title)

        initial = initial or {}
        self.ui.supplier_reference.setText(str(initial.get("supplier_reference", "")))
        self.ui.serial_number.setText(str(initial.get("serial_number", "")))
        self.ui.description_field.setText(str(initial.get("description", "")))
        self.ui.calibration_date.setText(str(initial.get("calibration_date", "")))
        self.ui.calibration_date.setPlaceholderText("YYYY-MM-DD")
        self.ui.calibration_expiration.setText(
            str(initial.get("calibration_expiration", ""))
        )
        self.ui.calibration_expiration.setPlaceholderText("YYYY-MM-DD")

        self.ui.btn_ok.clicked.connect(self._validate_and_accept)
        self.ui.btn_cancel.clicked.connect(self.reject)

    def _validate_and_accept(self) -> None:
        if (
            not self.ui.supplier_reference.text().strip()
            and not self.ui.serial_number.text().strip()
            and not self.ui.description_field.text().strip()
        ):
            SiemensMessage.warning(
                self,
                "Missing field",
                "Provide Supplier Reference, Serial Number or Description.",
            )
            return
        self.accept()

    def payload(self) -> dict:
        return {
            "supplier_reference": self.ui.supplier_reference.text().strip(),
            "serial_number": self.ui.serial_number.text().strip(),
            "description": self.ui.description_field.text().strip(),
            "calibration_date": self.ui.calibration_date.text().strip(),
            "calibration_expiration": self.ui.calibration_expiration.text().strip(),
        }
