"""Location picker — single or multiple shelves/drawers for inventory items."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.stock import StockTracker

from . import styles


def format_locations_display(locations: list[str], *, max_shown: int = 2) -> str:
    names = [str(item).strip() for item in locations if str(item).strip()]
    if not names:
        return "—"
    if len(names) <= max_shown:
        return " · ".join(names)
    shown = " · ".join(names[:max_shown])
    return f"{shown} (+{len(names) - max_shown})"


def locations_tooltip(locations: list[str]) -> str:
    names = [str(item).strip() for item in locations if str(item).strip()]
    if not names:
        return "Click to set shelf / drawer"
    if len(names) == 1:
        return names[0]
    return "Locations:\n" + "\n".join(f"• {name}" for name in names)


def build_location_combo(
    tracker: StockTracker | None,
    *,
    current: str = "",
    parent: QWidget | None = None,
) -> QComboBox:
    """Editable combo pre-filled with locations already used in the inventory."""
    combo = QComboBox(parent)
    combo.setEditable(True)
    combo.setStyleSheet(styles.LINE_EDIT_STYLE)
    line = combo.lineEdit()
    if line is not None:
        line.setPlaceholderText("Shelf / drawer / bag")

    known: list[str] = []
    if tracker is not None:
        known = tracker.get_known_locations()

    for loc in known:
        combo.addItem(loc)

    text = str(current or "").strip()
    if text and combo.findText(text) < 0:
        combo.insertItem(0, text)
    if text:
        combo.setCurrentText(text)
    elif combo.count() > 0:
        combo.setCurrentIndex(-1)
        if line is not None:
            line.clear()

    return combo


class LocationMultiEditor(QWidget):
    """Checklist of known locations plus custom entries."""

    def __init__(
        self,
        tracker: StockTracker | None,
        *,
        current: list[str] | str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._tracker = tracker
        if isinstance(current, str):
            current_list = (
                tracker.parse_component_locations(current)
                if tracker is not None
                else ([current] if current.strip() else [])
            )
        else:
            current_list = [str(item).strip() for item in current if str(item).strip()]

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(6)

        hint = QLabel("Tick one or more locations, or add a new one below.")
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #B3B3BE; font-size: 12px;")
        root.addWidget(hint)

        self._list = QListWidget(self)
        self._list.setMinimumHeight(140)
        self._list.setMaximumHeight(180)
        self._list.setStyleSheet(styles.LINE_EDIT_STYLE)
        root.addWidget(self._list)

        add_row = QHBoxLayout()
        self._custom = QLineEdit(self)
        self._custom.setPlaceholderText("New location")
        self._custom.setStyleSheet(styles.LINE_EDIT_STYLE)
        btn_add = QPushButton("Add")
        btn_add.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        btn_add.setMinimumWidth(72)
        btn_add.clicked.connect(self._add_custom_location)
        self._custom.returnPressed.connect(self._add_custom_location)
        add_row.addWidget(self._custom, 1)
        add_row.addWidget(btn_add)
        root.addLayout(add_row)

        self._populate(current_list)

    def _known_locations(self) -> list[str]:
        if self._tracker is None:
            return []
        return self._tracker.get_known_locations()

    def _populate(self, selected: list[str]) -> None:
        self._list.clear()
        selected_set = {name.casefold() for name in selected}
        seen: set[str] = set()

        for loc in selected:
            if loc.casefold() in seen:
                continue
            seen.add(loc.casefold())
            self._add_item(loc, checked=True)

        for loc in self._known_locations():
            if loc.casefold() in seen:
                continue
            seen.add(loc.casefold())
            self._add_item(loc, checked=False)

    def _add_item(self, text: str, *, checked: bool) -> None:
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        )
        self._list.addItem(item)

    def _add_custom_location(self) -> None:
        text = self._custom.text().strip()
        if not text:
            return
        for index in range(self._list.count()):
            item = self._list.item(index)
            if item is not None and item.text().strip().casefold() == text.casefold():
                item.setCheckState(Qt.CheckState.Checked)
                self._custom.clear()
                return
        self._add_item(text, checked=True)
        self._custom.clear()

    def locations(self) -> list[str]:
        names: list[str] = []
        seen: set[str] = set()
        for index in range(self._list.count()):
            item = self._list.item(index)
            if item is None or item.checkState() != Qt.CheckState.Checked:
                continue
            text = item.text().strip()
            key = text.casefold()
            if not text or key in seen:
                continue
            seen.add(key)
            names.append(text)
        return names

    def set_locations(self, locations: list[str]) -> None:
        self._populate(locations)


def pick_location(
    parent: QWidget | None,
    tracker: StockTracker | None,
    *,
    title: str = "Location",
    label: str = "Shelf / drawer / bag:",
    current: str = "",
) -> tuple[str, bool]:
    """Small dialog to pick or type a single location."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)

    root = QVBoxLayout(dialog)
    heading = QLabel(title.upper())
    heading.setStyleSheet("font-size: 16px; font-weight: 600; color: #00CCCC;")
    root.addWidget(heading)

    form = QFormLayout()
    combo = build_location_combo(tracker, current=current, parent=dialog)
    form.addRow(label, combo)
    root.addLayout(form)

    buttons = QHBoxLayout()
    buttons.addStretch()
    btn_ok = QPushButton("OK")
    btn_cancel = QPushButton("Cancel")
    for btn in (btn_ok, btn_cancel):
        btn.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        btn.setMinimumWidth(90)
    btn_ok.clicked.connect(dialog.accept)
    btn_cancel.clicked.connect(dialog.reject)
    buttons.addWidget(btn_ok)
    buttons.addWidget(btn_cancel)
    root.addLayout(buttons)

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return "", False
    return combo.currentText().strip(), True


def pick_locations(
    parent: QWidget | None,
    tracker: StockTracker | None,
    *,
    title: str = "Locations",
    current: list[str] | str = "",
) -> tuple[list[str], bool]:
    """Dialog to pick multiple locations for a component."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    dialog.setMinimumWidth(420)

    root = QVBoxLayout(dialog)
    heading = QLabel(title.upper())
    heading.setStyleSheet("font-size: 16px; font-weight: 600; color: #00CCCC;")
    root.addWidget(heading)

    editor = LocationMultiEditor(tracker, current=current, parent=dialog)
    root.addWidget(editor)

    buttons = QHBoxLayout()
    buttons.addStretch()
    btn_ok = QPushButton("OK")
    btn_cancel = QPushButton("Cancel")
    for btn in (btn_ok, btn_cancel):
        btn.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        btn.setMinimumWidth(90)
    btn_ok.clicked.connect(dialog.accept)
    btn_cancel.clicked.connect(dialog.reject)
    buttons.addWidget(btn_ok)
    buttons.addWidget(btn_cancel)
    root.addLayout(buttons)

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return [], False
    return editor.locations(), True
