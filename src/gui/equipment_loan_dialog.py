"""Record equipment loan details."""
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from . import styles
from .message_dialog import SiemensMessage

_LOAN_PLACES = (
    "Factory",
    "Lab",
    "Office",
    "Other",
)


class EquipmentLoanDialog(QDialog):
    def __init__(
        self,
        parent=None,
        *,
        initial: dict | None = None,
        title: str = "Loan equipment",
    ):
        super().__init__(parent)
        initial = initial or {}
        self.setWindowTitle(title)

        root = QVBoxLayout(self)
        heading = QLabel(title, self)
        heading.setStyleSheet(styles.POPUP_TITLE_STYLE)
        root.addWidget(heading)

        form_host = QWidget(self)
        form = QFormLayout(form_host)
        form.setSpacing(styles.TEMPLATE_ROW_SPACING)

        self.loaned_to = QLineEdit(form_host)
        self.loaned_to.setStyleSheet(styles.LINE_EDIT_STYLE)
        self.loaned_to.setPlaceholderText("Person or department")
        self.loaned_to.setText(str(initial.get("loaned_to", "")))

        self.place_combo = QComboBox(form_host)
        self.place_combo.setStyleSheet(styles.LINE_EDIT_STYLE)
        self.place_combo.addItems(_LOAN_PLACES)
        place = str(initial.get("loan_place", "")).strip()
        if place and self.place_combo.findText(place) < 0:
            self.place_combo.addItem(place)
        if place:
            self.place_combo.setCurrentText(place)

        self.place_custom = QLineEdit(form_host)
        self.place_custom.setStyleSheet(styles.LINE_EDIT_STYLE)
        self.place_custom.setPlaceholderText("Custom place (if Other)")
        self.place_custom.setText(
            place if place and place not in _LOAN_PLACES else ""
        )

        self.home_location = QLineEdit(form_host)
        self.home_location.setStyleSheet(styles.LINE_EDIT_STYLE)
        self.home_location.setPlaceholderText("Where it normally stays when not loaned")
        self.home_location.setText(str(initial.get("location", "")))

        self.notes = QLineEdit(form_host)
        self.notes.setStyleSheet(styles.LINE_EDIT_STYLE)
        self.notes.setPlaceholderText("Optional notes")

        form.addRow("Loaned to", self.loaned_to)
        form.addRow("Place", self.place_combo)
        form.addRow("Other place", self.place_custom)
        form.addRow("Home location", self.home_location)
        form.addRow("Notes", self.notes)
        root.addWidget(form_host)

        buttons = QHBoxLayout()
        btn_ok = QPushButton("OK", self)
        btn_ok.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        btn_cancel = QPushButton("Cancel", self)
        btn_cancel.setStyleSheet(styles.BTN_COPY_STYLE)
        btn_ok.clicked.connect(self._validate_and_accept)
        btn_cancel.clicked.connect(self.reject)
        buttons.addStretch()
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        root.addLayout(buttons)

    def _resolved_place(self) -> str:
        place = self.place_combo.currentText().strip()
        if place == "Other":
            return self.place_custom.text().strip()
        return place

    def _validate_and_accept(self) -> None:
        if not self.loaned_to.text().strip():
            SiemensMessage.warning(self, "Missing field", "Provide who received the equipment.")
            return
        if not self._resolved_place():
            SiemensMessage.warning(
                self,
                "Missing field",
                "Provide where the equipment is (Lab, Factory, Workshop, etc.).",
            )
            return
        self.accept()

    def payload(self) -> dict:
        return {
            "loaned_to": self.loaned_to.text().strip(),
            "loan_place": self._resolved_place(),
            "location": self.home_location.text().strip(),
            "notes": self.notes.text().strip(),
        }
