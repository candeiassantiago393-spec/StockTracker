"""Side-by-side equipment image thumbnails with horizontal scroll."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from . import styles

_SELECTED_BORDER = "2px solid #00FFB9"
_DEFAULT_BORDER = "1px dashed #B3B3BE"
_LAYOUT_PAD = 12
_THUMB_GAP = 8
_MIN_THUMB_WIDTH = 110
_MIN_THUMB_HEIGHT = 150


class EquipmentImageGallery(QWidget):
    """Horizontal strip of equipment images; click to select for delete."""

    selection_changed = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._selected = ""
        self._placeholders: list[str] = []
        self._image_items: list[tuple[str, Path]] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self._scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self._host = QWidget()
        self._layout = QHBoxLayout(self._host)
        self._layout.setContentsMargins(_LAYOUT_PAD, _LAYOUT_PAD, _LAYOUT_PAD, _LAYOUT_PAD)
        self._layout.setSpacing(_THUMB_GAP)
        self._layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self._placeholder = QLabel("Drop image here")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setMinimumHeight(styles.EQUIPMENT_IMAGE_PREVIEW_MIN_HEIGHT)
        self._placeholder.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self._layout.addWidget(self._placeholder)

        self._scroll.setWidget(self._host)
        root.addWidget(self._scroll)
        self._apply_panel_style(drag=False)

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        super().resizeEvent(event)
        if self._image_items:
            self._render_images()

    def _viewport_size(self) -> tuple[int, int]:
        width = self._scroll.viewport().width()
        height = self.height()
        if width < 80:
            width = max(self.width(), styles.EQUIPMENT_IMAGE_PREVIEW_MIN_WIDTH)
        if height < 80:
            height = styles.EQUIPMENT_IMAGE_PREVIEW_HEIGHT
        return width, height

    def _thumb_bounds(self, count: int) -> tuple[int, int]:
        """Pick a balanced thumb size for the current image count and panel size."""
        view_w, view_h = self._viewport_size()
        usable_w = max(view_w - _LAYOUT_PAD * 2, _MIN_THUMB_WIDTH)
        usable_h = max(view_h - _LAYOUT_PAD * 2, _MIN_THUMB_HEIGHT)
        gaps = _THUMB_GAP * max(0, count - 1)

        if count <= 1:
            return usable_w, usable_h

        per_width = (usable_w - gaps) // count
        if count == 2:
            thumb_w = max(_MIN_THUMB_WIDTH, min(usable_w // 2 - _THUMB_GAP // 2, per_width))
            return thumb_w, usable_h

        thumb_w = max(_MIN_THUMB_WIDTH, min(usable_w // 2, per_width))
        if count >= 4:
            thumb_w = max(_MIN_THUMB_WIDTH, min(thumb_w, 180))
        return thumb_w, min(usable_h, 260)

    def _apply_panel_style(self, *, drag: bool) -> None:
        style = (
            styles.EQUIPMENT_IMAGE_PREVIEW_DRAG_STYLE
            if drag
            else styles.EQUIPMENT_IMAGE_PREVIEW_STYLE
        )
        self._placeholder.setStyleSheet(style)
        self.setStyleSheet(style)

    def set_drag_highlight(self, active: bool) -> None:
        self._apply_panel_style(drag=active)
        if active and self._placeholders:
            self._placeholder.setText("Release to add image")

    def selected_filename(self) -> str:
        return self._selected

    def clear_selection(self) -> None:
        self._selected = ""
        self.selection_changed.emit("")

    def _clear_layout_widgets(self) -> None:
        while self._layout.count():
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._placeholders.clear()

    def show_placeholder(self, text: str = "Drop image here") -> None:
        self._image_items = []
        self._clear_layout_widgets()
        self.clear_selection()
        self._placeholder = QLabel(text)
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setMinimumHeight(styles.EQUIPMENT_IMAGE_PREVIEW_MIN_HEIGHT)
        self._placeholder.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self._apply_panel_style(drag=False)
        self._layout.addWidget(self._placeholder)
        self._placeholders = [text]

    def show_images(self, items: list[tuple[str, Path]]) -> None:
        """items: (filename, absolute path) pairs."""
        self._image_items = list(items)
        self._render_images()
        if self._image_items and self._scroll.viewport().width() < 80:
            QTimer.singleShot(0, self._render_images)

    def _render_images(self) -> None:
        items = self._image_items
        selected = self._selected
        self._clear_layout_widgets()
        self._selected = selected

        if not items:
            self.show_placeholder()
            return

        thumb_w, thumb_h = self._thumb_bounds(len(items))

        for filename, path in items:
            pixmap = QPixmap(str(path))
            if pixmap.isNull():
                continue

            label = QLabel()
            label.setProperty("image_filename", filename)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.setToolTip(filename)

            border = (
                _SELECTED_BORDER
                if filename == self._selected
                else _DEFAULT_BORDER
            )
            label.setStyleSheet(
                f"QLabel {{ border: {border}; border-radius: 2px; "
                f"background-color: #00183B; padding: 4px; }}"
            )

            scaled = pixmap.scaled(
                thumb_w,
                thumb_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            label.setPixmap(scaled)
            label.setFixedSize(scaled.width() + 8, scaled.height() + 8)
            label.mousePressEvent = (  # type: ignore[method-assign, assignment]
                lambda event, name=filename, widget=label: self._on_thumb_click(
                    name, widget
                )
            )
            self._layout.addWidget(label)

        if len(items) <= 2:
            self._layout.addStretch()

    def _on_thumb_click(self, filename: str, widget: QLabel) -> None:
        self._selected = filename
        for index in range(self._layout.count()):
            item = self._layout.itemAt(index)
            if item is None:
                continue
            child = item.widget()
            if not isinstance(child, QLabel):
                continue
            name = child.property("image_filename")
            if not name:
                continue
            border = _SELECTED_BORDER if str(name) == filename else _DEFAULT_BORDER
            child.setStyleSheet(
                f"QLabel {{ border: {border}; border-radius: 2px; "
                f"background-color: #00183B; padding: 4px; }}"
            )
        self.selection_changed.emit(filename)
