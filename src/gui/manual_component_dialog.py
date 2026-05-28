"""Add manual component — Siemens gui_popup.ui shell."""
from PySide6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QWidget,
)

from . import styles
from .siemens_template.popup_shell import SiemensPopupDialog


class ManualComponentDialog(SiemensPopupDialog):
    def __init__(self, parent=None):
        super().__init__(
            "Add Manual Component",
            parent,
            connect_default_buttons=False,
        )
        self.resize(641, 420)
        self.set_subtitle(
            "Supplier Reference is optional when both Manufacturer and "
            "Manufacturer Reference are provided."
        )

        form_host = QWidget()
        form = QFormLayout(form_host)
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(styles.TEMPLATE_ROW_SPACING)

        self.supplier_reference = QLineEdit()
        self.supplier_reference.setPlaceholderText("Optional")
        self.supplier_reference.setStyleSheet(styles.LINE_EDIT_STYLE)
        form.addRow("Supplier Reference", self.supplier_reference)

        self.manufacturer = QLineEdit()
        self.manufacturer.setStyleSheet(styles.LINE_EDIT_STYLE)
        form.addRow("Manufacturer", self.manufacturer)

        self.manufacturer_reference = QLineEdit()
        self.manufacturer_reference.setStyleSheet(styles.LINE_EDIT_STYLE)
        form.addRow("Manufacturer Reference", self.manufacturer_reference)

        self.description_field = QLineEdit()
        self.description_field.setStyleSheet(styles.LINE_EDIT_STYLE)
        form.addRow("Description", self.description_field)

        self.initial_stock = QSpinBox()
        self.initial_stock.setMinimum(0)
        self.initial_stock.setMaximum(999999)
        self.initial_stock.setValue(0)
        self.initial_stock.setStyleSheet(styles.LINE_EDIT_STYLE)
        form.addRow("Initial Stock", self.initial_stock)

        self.set_body_widget(form_host)
        self.configure_buttons(ok_text="Save", cancel_text="Cancel")

        self.ui.btn_ok.clicked.connect(self._validate_and_accept)
        self.ui.btn_cancel.clicked.connect(self.reject)

    def _validate_and_accept(self) -> None:
        supplier_ref = self.supplier_reference.text().strip()
        manufacturer = self.manufacturer.text().strip()
        manufacturer_ref = self.manufacturer_reference.text().strip()

        if not supplier_ref and not (manufacturer and manufacturer_ref):
            QMessageBox.warning(
                self,
                "Missing identity",
                "Provide Supplier Reference OR both Manufacturer and Manufacturer Reference.",
            )
            return
        self.accept()

    def payload(self) -> dict:
        return {
            "supplier_reference": self.supplier_reference.text().strip(),
            "manufacturer": self.manufacturer.text().strip(),
            "manufacturer_reference": self.manufacturer_reference.text().strip(),
            "description": self.description_field.text().strip(),
            "initial_stock": int(self.initial_stock.value()),
        }
