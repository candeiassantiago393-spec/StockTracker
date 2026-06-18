"""Interactive catalog image preview with Mouser-style hover zoom."""
from __future__ import annotations

from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPaintEvent, QPixmap, QWheelEvent
from PySide6.QtWidgets import QLabel, QSizePolicy, QWidget

from src.gui import styles


class CatalogImagePreview(QWidget):
    """Product image preview: fit view, hover magnifier, wheel zoom, drag pan."""

    _MIN_ZOOM = 1.0
    _MAX_ZOOM = 4.0
    _LENS_SIZE = 148
    _LENS_ZOOM = 2.6

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(240, 240)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.setMouseTracking(True)
        self.setStyleSheet(styles.EQUIPMENT_IMAGE_PREVIEW_STYLE)
        self.setToolTip(
            "Product image from distributor catalog.\n"
            "Move mouse to magnify · Wheel to zoom · Drag to pan · Double-click to reset"
        )

        self._source: QPixmap | None = None
        self._placeholder = "No image"
        self._image_rect = QRect()
        self._cursor_pos: QPoint | None = None
        self._zoom = 1.0
        self._pan = QPoint(0, 0)
        self._dragging = False
        self._drag_origin = QPoint()
        self._pan_origin = QPoint()

    def set_placeholder(self, text: str) -> None:
        self._placeholder = text or "No image"

    def clear_image(self, placeholder: str = "No image") -> None:
        self._source = None
        self._placeholder = placeholder
        self._reset_view()
        self.update()

    def set_image(self, pixmap: QPixmap | None) -> None:
        if pixmap is None or pixmap.isNull():
            self.clear_image("Image unavailable")
            return
        self._source = pixmap
        self._reset_view()
        self.update()

    def _reset_view(self) -> None:
        self._zoom = 1.0
        self._pan = QPoint(0, 0)
        self._cursor_pos = None
        self._dragging = False
        self.unsetCursor()

    def _fitted_rect(self) -> QRect:
        if self._source is None or self._source.isNull():
            return QRect()
        target = self.rect().adjusted(8, 8, -8, -8)
        if target.width() <= 0 or target.height() <= 0:
            return QRect()
        scaled = self._source.size()
        scaled.scale(target.size(), Qt.AspectRatioMode.KeepAspectRatio)
        x = target.x() + (target.width() - scaled.width()) // 2
        y = target.y() + (target.height() - scaled.height()) // 2
        return QRect(x, y, scaled.width(), scaled.height())

    def _source_point_for_widget(self, pos: QPoint, fitted: QRect) -> QPoint | None:
        if self._source is None or fitted.width() <= 0 or fitted.height() <= 0:
            return None
        if not fitted.contains(pos):
            return None
        rel_x = (pos.x() - fitted.x()) / fitted.width()
        rel_y = (pos.y() - fitted.y()) / fitted.height()
        if self._zoom > 1.0:
            center = QPoint(fitted.center())
            offset = pos - center - self._pan
            rel_x = 0.5 + offset.x() / (fitted.width() * self._zoom)
            rel_y = 0.5 + offset.y() / (fitted.height() * self._zoom)
        sx = int(rel_x * self._source.width())
        sy = int(rel_y * self._source.height())
        sx = max(0, min(self._source.width() - 1, sx))
        sy = max(0, min(self._source.height() - 1, sy))
        return QPoint(sx, sy)

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.fillRect(self.rect(), QColor("#ffffff"))

        if self._source is None or self._source.isNull():
            painter.setPen(QColor("#6b7c8f"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._placeholder)
            return

        fitted = self._fitted_rect()
        self._image_rect = fitted
        if fitted.isEmpty():
            return

        if self._zoom <= 1.0:
            painter.drawPixmap(fitted, self._source)
        else:
            src_w = max(1, int(self._source.width() / self._zoom))
            src_h = max(1, int(self._source.height() / self._zoom))
            center_x = self._source.width() // 2 - int(self._pan.x() * self._source.width() / max(fitted.width(), 1) / self._zoom)
            center_y = self._source.height() // 2 - int(self._pan.y() * self._source.height() / max(fitted.height(), 1) / self._zoom)
            center_x = max(src_w // 2, min(self._source.width() - src_w // 2, center_x))
            center_y = max(src_h // 2, min(self._source.height() - src_h // 2, center_y))
            src = QRect(
                center_x - src_w // 2,
                center_y - src_h // 2,
                src_w,
                src_h,
            )
            painter.drawPixmap(fitted, self._source, src)

        if (
            self._zoom <= 1.0
            and self._cursor_pos is not None
            and fitted.contains(self._cursor_pos)
        ):
            self._paint_magnifier(painter, fitted)

    def _paint_magnifier(self, painter: QPainter, fitted: QRect) -> None:
        if self._source is None or self._cursor_pos is None:
            return

        src_point = self._source_point_for_widget(self._cursor_pos, fitted)
        if src_point is None:
            return

        lens = self._LENS_SIZE
        src_half = max(8, int((lens / self._LENS_ZOOM) * self._source.width() / max(fitted.width(), 1)))
        src_rect = QRect(
            src_point.x() - src_half,
            src_point.y() - src_half,
            src_half * 2,
            src_half * 2,
        )
        src_rect = src_rect.intersected(self._source.rect())
        if src_rect.isEmpty():
            return

        margin = 10
        lens_rect = QRect(
            self.width() - lens - margin,
            margin,
            lens,
            lens,
        )
        if lens_rect.right() > self.width() - margin:
            lens_rect.moveLeft(max(margin, self._cursor_pos.x() - lens // 2))
            lens_rect.moveTop(max(margin, self._cursor_pos.y() - lens - margin))

        painter.save()
        painter.setPen(QColor("#009999"))
        painter.setBrush(QColor("#ffffff"))
        painter.drawRoundedRect(lens_rect.adjusted(-2, -2, 2, 2), 6, 6)
        painter.setClipRect(lens_rect)
        painter.drawPixmap(lens_rect, self._source, src_rect)
        painter.restore()
        painter.setPen(QColor("#009999"))
        painter.drawRoundedRect(lens_rect, 4, 4)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if self._source is None:
            return
        if self._dragging and self._zoom > 1.0:
            delta = event.position().toPoint() - self._drag_origin
            self._pan = self._pan_origin + delta
            self.update()
            return

        self._cursor_pos = event.position().toPoint()
        if self._zoom <= 1.0 and self._image_rect.contains(self._cursor_pos):
            self.setCursor(Qt.CursorShape.CrossCursor)
        elif self._zoom > 1.0:
            self.setCursor(Qt.CursorShape.OpenHandCursor if not self._dragging else Qt.CursorShape.ClosedHandCursor)
        else:
            self.unsetCursor()
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if self._source is None or self._zoom <= 1.0:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_origin = event.position().toPoint()
            self._pan_origin = self._pan
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            if self._zoom > 1.0:
                self.setCursor(Qt.CursorShape.OpenHandCursor)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._cursor_pos = None
        self._dragging = False
        self.unsetCursor()
        self.update()
        super().leaveEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:  # noqa: N802
        if self._source is None:
            return
        delta = event.angleDelta().y()
        if delta == 0:
            return
        step = 0.15 if delta > 0 else -0.15
        self._zoom = max(self._MIN_ZOOM, min(self._MAX_ZOOM, self._zoom + step))
        if self._zoom <= 1.0:
            self._pan = QPoint(0, 0)
            self._dragging = False
        self.update()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._reset_view()
            self.update()


def replace_label_with_catalog_preview(label: QLabel) -> CatalogImagePreview:
    """Swap a designer QLabel for the interactive preview widget."""
    parent = label.parentWidget()
    preview = CatalogImagePreview(parent)
    preview.setMinimumSize(label.minimumSize())
    preview.setSizePolicy(label.sizePolicy())
    layout = parent.layout() if parent is not None else None
    if layout is not None and hasattr(layout, "replaceWidget"):
        layout.replaceWidget(label, preview)
    label.hide()
    label.deleteLater()
    return preview
