"""Add or edit a material (supplier ref, serial number, description, dates)."""
from PySide6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget

from . import styles
from .message_dialog import SiemensMessage


class MaterialDialog(QDialog):
    def __init__(self, parent=None, *, initial: dict | None = None, title: str = "Material"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet(styles.POPUP_WINDOW_STYLE)
        self.setMinimumWidth(480)

        initial = initial or {}
        root = QVBoxLayout(self)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(styles.POPUP_TITLE_STYLE)
        root.addWidget(title_lbl)

        form_host = QWidget()
        form = QFormLayout(form_host)
        form.setSpacing(12)

        field_style = styles.MATERIAL_VALUE_FIELD_STYLE.replace("QLabel", "QLineEdit")
        self.supplier_reference = QLineEdit(str(initial.get("supplier_reference", "")))
        self.supplier_reference.setStyleSheet(field_style)
        self.serial_number = QLineEdit(str(initial.get("serial_number", "")))
        self.serial_number.setStyleSheet(field_style)
        self.description = QLineEdit(str(initial.get("description", "")))
        self.description.setStyleSheet(field_style)
        self.calibration_date = QLineEdit(str(initial.get("calibration_date", "")))
        self.calibration_date.setPlaceholderText("YYYY-MM-DD")
        self.calibration_date.setStyleSheet(field_style)
        self.calibration_expiration = QLineEdit(
            str(initial.get("calibration_expiration", ""))
        )
        self.calibration_expiration.setPlaceholderText("YYYY-MM-DD")
        self.calibration_expiration.setStyleSheet(field_style)

        for label, widget in (
            ("Supplier Reference", self.supplier_reference),
            ("Serial Number", self.serial_number),
            ("Description", self.description),
            ("Calibration Date", self.calibration_date),
            ("Calibration Expiration", self.calibration_expiration),
        ):
            lbl = QLabel(label)
            lbl.setStyleSheet(styles.FIELD_LABEL_STYLE)
            form.addRow(lbl, widget)

        root.addWidget(form_host)

        actions = QHBoxLayout()
        actions.addStretch()
        btn_ok = self._make_button("OK")
        btn_cancel = self._make_button("Cancel")
        btn_ok.clicked.connect(self._validate_and_accept)
        btn_cancel.clicked.connect(self.reject)
        actions.addWidget(btn_ok)
        actions.addWidget(btn_cancel)
        root.addLayout(actions)

    @staticmethod
    def _make_button(text: str):
        from PySide6.QtWidgets import QPushButton

        btn = QPushButton(text)
        btn.setStyleSheet(styles.POPUP_BTN_STYLE)
        btn.setMinimumWidth(100)
        return btn

    def _validate_and_accept(self) -> None:
        if (
            not self.supplier_reference.text().strip()
            and not self.serial_number.text().strip()
            and not self.description.text().strip()
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
            "supplier_reference": self.supplier_reference.text().strip(),
            "serial_number": self.serial_number.text().strip(),
            "description": self.description.text().strip(),
            "calibration_date": self.calibration_date.text().strip(),
            "calibration_expiration": self.calibration_expiration.text().strip(),
        }
