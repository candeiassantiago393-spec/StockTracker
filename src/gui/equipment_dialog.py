"""Add or edit an equipment — Qt Designer popups/equipments/gui_popup_equipment.ui."""
from pathlib import Path

from PySide6.QtWidgets import QDialog, QFileDialog, QFormLayout, QHBoxLayout, QPushButton, QWidget

from src.core.support_documentation import SUPPORT_DOCS_DIR

from .designer.popups.equipments.gui_popup_equipment import Ui_PopupEquipment
from . import styles
from .message_dialog import SiemensMessage


class EquipmentDialog(QDialog):
    def __init__(self, parent=None, *, initial: dict | None = None, title: str = "Equipment"):
        super().__init__(parent)
        self.ui = Ui_PopupEquipment()
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
        self.ui.datasheet.setText(str(initial.get("datasheet", "")))
        self.ui.datasheet.setPlaceholderText("Filename in support_documentation/")
        self._add_datasheet_browse_button()

        self.ui.btn_ok.clicked.connect(self._validate_and_accept)
        self.ui.btn_cancel.clicked.connect(self.reject)

    def _add_datasheet_browse_button(self) -> None:
        form = self.ui.form_equipment
        field = self.ui.datasheet
        row = form.indexOf(field)
        if row < 0:
            return
        label_item = form.itemAt(row, QFormLayout.ItemRole.LabelRole)
        label_widget = label_item.widget() if label_item else None
        form.removeRow(row)

        wrapper = QWidget(self.ui.body_form)
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        field.setParent(wrapper)
        layout.addWidget(field)
        browse = QPushButton("Browse", wrapper)
        browse.setStyleSheet(styles.BTN_COPY_STYLE)
        browse.setToolTip("Pick a file from the support documentation folder")
        browse.clicked.connect(self._browse_datasheet)
        layout.addWidget(browse)

        if label_widget:
            form.addRow(label_widget, wrapper)
        else:
            form.addRow("Datasheet", wrapper)

    def _browse_datasheet(self) -> None:
        start_dir = str(SUPPORT_DOCS_DIR) if SUPPORT_DOCS_DIR.exists() else ""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select datasheet",
            start_dir,
            "Documents (*.pdf *.doc *.docx *.xls *.xlsx *.txt *.zip);;All files (*.*)",
        )
        if file_path:
            self.ui.datasheet.setText(Path(file_path).name)

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
            "datasheet": self.ui.datasheet.text().strip(),
        }
