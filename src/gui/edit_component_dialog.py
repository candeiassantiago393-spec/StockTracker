"""Edit component — Qt Designer gui_popup_edit.ui + location field."""
from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit

from .designer.popups.components.gui_popup_edit import Ui_PopupEdit
from .location_combo import LocationMultiEditor
from .manual_component_dialog import _widen_text_field
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

        for field in (
            self.ui.supplier_reference,
            self.ui.manufacturer,
            self.ui.manufacturer_reference,
            self.ui.description_field,
        ):
            _widen_text_field(field)

        form = self.ui.body_form.findChild(QFormLayout, "form_edit")
        if form is None:
            form = self.ui.body_form.layout()
        tracker = getattr(parent, "tracker", None)
        self._tracker = tracker
        self.location_field = LocationMultiEditor(
            tracker,
            current=str(component_data.get("location", "")),
            parent=self,
        )
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
                "Enter a Supplier Reference (any text) OR both Manufacturer and "
                "Manufacturer Reference.",
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
            "location": location,
        }
