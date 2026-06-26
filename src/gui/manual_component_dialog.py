"""Add manual component — Qt Designer gui_popup_manual.ui + location."""
from PySide6.QtWidgets import QDialog, QFormLayout

from .designer.popups.components.gui_popup_manual import Ui_PopupManual
from .location_combo import LocationMultiEditor
from .message_dialog import SiemensMessage


class ManualComponentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_PopupManual()
        self.ui.setupUi(self)

        form = self.ui.body_form.findChild(QFormLayout, "form_manual")
        if form is None:
            form = self.ui.body_form.layout()
        tracker = getattr(parent, "tracker", None)
        self._tracker = tracker
        self.location_field = LocationMultiEditor(tracker, parent=self)
        if isinstance(form, QFormLayout):
            form.addRow("Location", self.location_field)

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
        locations = self.location_field.locations()
        if self._tracker is not None:
            location = self._tracker.format_component_locations(locations)
        else:
            location = ";".join(locations)
        return {
            "supplier_reference": self.ui.supplier_reference.text().strip(),
            "manufacturer": self.ui.manufacturer.text().strip(),
            "manufacturer_reference": self.ui.manufacturer_reference.text().strip(),
            "description": self.ui.description_field.text().strip(),
            "initial_stock": int(self.ui.initial_stock.value()),
            "location": location,
        }
