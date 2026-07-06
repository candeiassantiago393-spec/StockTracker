"""Detail rows for Passive mode — compact two-column layout."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from . import styles


def _build_field_row(
    parent: QWidget,
    title: str,
    *,
    on_copy,
) -> tuple[QLabel, QLabel]:
    title_label = QLabel(title, parent)
    title_label.setMinimumWidth(styles.PASSIVE_DETAIL_LABEL_WIDTH)
    title_label.setMaximumWidth(styles.PASSIVE_DETAIL_LABEL_WIDTH)

    row_wrap = QWidget(parent)
    row_layout = QHBoxLayout(row_wrap)
    row_layout.setContentsMargins(0, 0, 0, 0)
    row_layout.setSpacing(4)

    value_label = QLabel("", row_wrap)
    styles.apply_passive_detail_value_label(value_label)
    value_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    copy_btn = QPushButton("Copy", row_wrap)
    copy_btn.setStyleSheet(styles.BTN_COPY_STYLE)
    copy_btn.setMinimumWidth(56)
    copy_btn.setMaximumWidth(56)
    copy_btn.setToolTip("Copy to clipboard")
    copy_btn.clicked.connect(
        lambda _checked=False, widget=value_label, field=title: on_copy(widget, field)
    )

    row_layout.addWidget(value_label, 1)
    row_layout.addWidget(copy_btn, 0)
    return title_label, row_wrap, value_label


def _build_column(
    parent: QWidget,
    fields: tuple[tuple[str, str], ...],
    *,
    on_copy,
) -> tuple[QWidget, dict[str, QLabel]]:
    column = QWidget(parent)
    grid = QGridLayout(column)
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setHorizontalSpacing(6)
    grid.setVerticalSpacing(2)
    grid.setColumnStretch(1, 1)

    labels: dict[str, QLabel] = {}
    for row_idx, (key, title) in enumerate(fields):
        title_label, row_wrap, value_label = _build_field_row(
            column, title, on_copy=on_copy
        )
        grid.addWidget(title_label, row_idx, 0, Qt.AlignmentFlag.AlignTop)
        grid.addWidget(row_wrap, row_idx, 1)
        labels[key] = value_label
    return column, labels


def build_compact_two_column_detail_panel(
    parent,
    fields: tuple[tuple[str, str], ...],
    *,
    on_copy,
) -> tuple[QWidget, dict[str, QLabel]]:
    """Two columns of label | value+Copy — fills panel width, tight vertical spacing."""
    panel = QWidget(parent)
    panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

    root = QHBoxLayout(panel)
    root.setContentsMargins(0, 0, 8, 0)
    root.setSpacing(16)

    split = (len(fields) + 1) // 2
    left_col, left_labels = _build_column(parent, fields[:split], on_copy=on_copy)
    right_col, right_labels = _build_column(parent, fields[split:], on_copy=on_copy)

    root.addWidget(left_col, 1)
    root.addWidget(right_col, 1)
    return panel, {**left_labels, **right_labels}


def build_detail_panel(
    parent,
    fields: tuple[tuple[str, str], ...],
    *,
    on_copy,
) -> tuple[QWidget, dict[str, QLabel]]:
    """Backward-compatible alias — passive mode uses the compact layout."""
    return build_compact_two_column_detail_panel(
        parent,
        fields,
        on_copy=on_copy,
    )
