"""Edit component — Qt Designer gui_popup_edit.ui."""
from PySide6.QtWidgets import QDialog

from .designer.popups.components.gui_popup_edit import Ui_PopupEdit
from .message_dialog import SiemensMessage


class EditComponentDialog(QDialog):
    def __init__(self, component_data: dict, parent=None):
        super().__init__(parent)
        self.ui = Ui_PopupEdit()
        self.ui.setupUi(self)
        self.ui.supplier_reference.setText(str(component_data.get("mouser", "")))
        self.ui.manufacturer.setText(str(component_data.get("manufacturer", "")))
        self.ui.manufacturer_reference.setText(
            str(component_data.get("manufacturer_ref", ""))
        )
        self.ui.description_field.setText(str(component_data.get("description", "")))
        self.ui.label_current_stock.setText(str(component_data.get("stock", 0)))
        self.ui.btn_ok.clicked.connect(self._validate_and_accept)
        self.ui.btn_cancel.clicked.connect(self.reject)

    def _validate_and_accept(self) -> None:
        supplier_ref = self.ui.supplier_reference.text().strip()
        manufacturer = self.ui.manufacturer.text().strip()
        manufacturer_ref = self.ui.manufacturer_reference.text().strip()

        if not supplier_ref and not (manufacturer and manufacturer_ref):
            SiemensMessage.warning(
                self,
                "Missing identity",
                "Provide Supplier Reference OR both Manufacturer and Manufacturer Reference.",
            )
            return
        self.accept()

    def payload(self) -> dict:
        return {
            "supplier_reference": self.ui.supplier_reference.text().strip(),
            "manufacturer": self.ui.manufacturer.text().strip(),
            "manufacturer_reference": self.ui.manufacturer_reference.text().strip(),
            "description": self.ui.description_field.text().strip(),
        }
