"""Detail rows for Passive mode — same layout as Components (label | value + Copy)."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QWidget

from . import styles


def build_detail_panel(
    parent,
    fields: tuple[tuple[str, str], ...],
    *,
    on_copy,
) -> tuple[QWidget, dict[str, QLabel]]:
    panel = QWidget(parent)
    grid = QGridLayout(panel)
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setVerticalSpacing(0)
    styles.apply_component_details_grid(grid)

    labels: dict[str, QLabel] = {}
    for row_idx, (key, title) in enumerate(fields, start=1):
        title_label = QLabel(title)
        title_label.setMinimumWidth(styles.COMPONENT_DETAIL_LABEL_WIDTH)
        title_label.setMaximumWidth(styles.COMPONENT_DETAIL_LABEL_WIDTH)

        row_wrap = QWidget(panel)
        row_layout = QHBoxLayout(row_wrap)
        row_layout.setContentsMargins(0, 9, 9, 9)
        row_layout.setSpacing(6)

        value_label = QLabel("")
        styles.apply_mode_detail_value_label(value_label)
        value_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        copy_btn = QPushButton("Copy")
        copy_btn.setStyleSheet(styles.BTN_COPY_STYLE)
        copy_btn.setMinimumWidth(60)
        copy_btn.setMaximumWidth(60)
        copy_btn.setToolTip("Copy to clipboard")
        copy_btn.clicked.connect(
            lambda _checked=False, widget=value_label, field=title: on_copy(
                widget, field
            )
        )

        row_layout.addWidget(value_label)
        row_layout.addWidget(copy_btn)

        grid.addWidget(title_label, row_idx, 0)
        grid.addWidget(row_wrap, row_idx, 2)
        labels[key] = value_label

    return panel, labels
