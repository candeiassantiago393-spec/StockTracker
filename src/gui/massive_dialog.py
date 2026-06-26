"""Add / edit Massive inventory item (resistor or capacitor)."""
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from . import styles
from .location_combo import build_location_combo
from .message_dialog import SiemensMessage

_GENERIC_PACKAGES = (
    "0201",
    "0402",
    "0603",
    "0805",
    "1206",
    "1210",
    "1812",
    "2010",
    "2512",
)


class MassiveDialog(QDialog):
    def __init__(
        self,
        parent=None,
        *,
        initial: dict | None = None,
        title: str = "Add Passive Item",
        allow_stock: bool = True,
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self._allow_stock = allow_stock
        data = dict(initial or {})

        root = QVBoxLayout(self)
        heading = QLabel(title.upper())
        heading.setStyleSheet("font-size: 18px; font-weight: 600; color: #00CCCC;")
        root.addWidget(heading)

        form = QFormLayout()
        form.setSpacing(8)

        self.part_type = QComboBox()
        self.part_type.addItems(["R — Resistor", "C — Capacitor"])
        part_type = str(data.get("part_type", "R")).strip().upper()
        self.part_type.setCurrentIndex(1 if part_type == "C" else 0)

        self.value = QLineEdit(str(data.get("value", "")))
        self.value.setPlaceholderText("10k / 100nF / 4.7uF")

        self.tolerance = QLineEdit(str(data.get("tolerance", "")))
        self.tolerance.setPlaceholderText("Optional — 1%, 5%, J…")

        self.package = QComboBox()
        self.package.setEditable(True)
        self.package.setStyleSheet(styles.LINE_EDIT_STYLE)
        self.package.addItems(_GENERIC_PACKAGES)
        package_line = self.package.lineEdit()
        if package_line is not None:
            package_line.setPlaceholderText("0603 / 0805 / 1206")
        package = str(data.get("package", "")).strip()
        if package:
            if self.package.findText(package) < 0:
                self.package.addItem(package)
            self.package.setCurrentText(package)
        elif package_line is not None:
            package_line.clear()

        self.name = QLineEdit(str(data.get("name", "")))
        self.name.setPlaceholderText("Optional — auto-generated if empty")

        self.supplier_reference = QLineEdit(str(data.get("supplier_reference", "")))
        self.dielectric = QLineEdit(str(data.get("dielectric", "")))
        self.dielectric.setPlaceholderText("Optional — X7R, C0G…")
        self.voltage = QLineEdit(str(data.get("voltage", "")))
        self.voltage.setPlaceholderText("Optional — 50V, 16V…")
        self.notes = QLineEdit(str(data.get("notes", "")))

        self.initial_stock = QSpinBox()
        self.initial_stock.setRange(0, 1_000_000)
        self.initial_stock.setValue(int(data.get("stock", 0) or 0))

        form.addRow("Type *", self.part_type)
        form.addRow("Value *", self.value)
        form.addRow("Tolerance", self.tolerance)
        form.addRow("Package *", self.package)
        form.addRow("Name", self.name)
        if allow_stock:
            form.addRow("Stock", self.initial_stock)
        form.addRow("Supplier Ref", self.supplier_reference)
        form.addRow("Dielectric", self.dielectric)
        form.addRow("Voltage", self.voltage)
        form.addRow("Notes", self.notes)
        tracker = getattr(parent, "tracker", None) if parent is not None else None
        self.location = build_location_combo(
            tracker,
            current=str(data.get("location", "")),
            parent=self,
        )
        form.addRow("Location", self.location)
        root.addLayout(form)

        buttons = QHBoxLayout()
        buttons.addStretch()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancel")
        for btn in (btn_ok, btn_cancel):
            btn.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
            btn.setMinimumWidth(100)
        btn_ok.clicked.connect(self._validate_and_accept)
        btn_cancel.clicked.connect(self.reject)
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        root.addLayout(buttons)

        self.value.textChanged.connect(self._on_value_changed)
        if self._value_implies_capacitor(self.value.text()):
            self.part_type.setCurrentIndex(1)

    @staticmethod
    def _value_implies_capacitor(text: str) -> bool:
        lowered = str(text or "").lower()
        return "u" in lowered or "µ" in str(text or "")

    def _on_value_changed(self, text: str) -> None:
        if self._value_implies_capacitor(text):
            self.part_type.setCurrentIndex(1)

    def _validate_and_accept(self) -> None:
        if not self.value.text().strip():
            SiemensMessage.warning(self, "Passive", "Value is required.")
            return
        if not self.package.currentText().strip():
            SiemensMessage.warning(self, "Passive", "Package is required.")
            return
        self.accept()

    def payload(self) -> dict:
        part_type = "C" if self.part_type.currentIndex() == 1 else "R"
        payload = {
            "part_type": part_type,
            "value": self.value.text().strip(),
            "tolerance": self.tolerance.text().strip(),
            "package": self.package.currentText().strip(),
            "name": self.name.text().strip(),
            "supplier_reference": self.supplier_reference.text().strip(),
            "dielectric": self.dielectric.text().strip(),
            "voltage": self.voltage.text().strip(),
            "notes": self.notes.text().strip(),
            "location": self.location.currentText().strip(),
        }
        if self._allow_stock:
            payload["initial_stock"] = int(self.initial_stock.value())
        return payload
