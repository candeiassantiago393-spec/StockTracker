"""Keyboard shortcuts for the main Stock Tracker window."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QLineEdit, QWidget


def _append_tooltip(widget: QWidget | None, hint: str) -> None:
    if widget is None or not hint:
        return
    current = (widget.toolTip() or "").strip()
    suffix = f" ({hint})"
    if suffix in current:
        return
    widget.setToolTip(f"{current}{suffix}" if current else hint.strip(" ()"))


def setup_keyboard_shortcuts(window) -> None:
    """Register context-aware shortcuts on the main window."""
    w = window

    def add(key: str, slot, *, context=Qt.ShortcutContext.WindowShortcut) -> QShortcut:
        shortcut = QShortcut(QKeySequence(key), w)
        shortcut.setContext(context)
        shortcut.activated.connect(slot)
        return shortcut

    add("Ctrl+1", w._show_components_page)
    add("Ctrl+2", w._show_equipments_page)
    add("Ctrl+3", w._show_statistics_page)

    def focus_search() -> None:
        if w._current_section == "components":
            entry = w.ui.search_entry
        elif w._current_section == "equipments":
            entry = w._equipments_page.ui.search_entry
        else:
            return
        entry.setFocus()
        entry.selectAll()

    add("Ctrl+F", focus_search)

    def run_global_search() -> None:
        w.open_global_search()

    add("Ctrl+G", run_global_search)

    def focus_scan_field() -> None:
        if w._current_section == "components" and w._inventory_mode == "components":
            entry = w.ui.barcode_entry
        elif w._current_section == "equipments":
            entry = w._equipments_page.ui.supplier_ref_entry
        else:
            return
        entry.setFocus()
        entry.selectAll()

    add("F6", focus_scan_field)

    def focus_quantity() -> None:
        if w._current_section != "components":
            return
        w.ui.quantity_entry.setFocus()
        w.ui.quantity_entry.selectAll()

    add("F2", focus_quantity)

    def focus_user() -> None:
        w.ui.user_entry.setFocus()
        w.ui.user_entry.selectAll()

    add("F4", focus_user)

    def run_search() -> None:
        if w._current_section == "components":
            w._on_search_clicked()
        elif w._current_section == "equipments":
            w._equipments_page.search_equipment()

    add("Ctrl+Return", run_search)
    add("Ctrl+Enter", run_search)

    def run_scan() -> None:
        if w._current_section == "components":
            w.scan_component()
        elif w._current_section == "equipments":
            w._equipments_page.scan_supplier_ref()

    add("F5", run_scan)

    def stock_in() -> None:
        if w._current_section == "components":
            w.update_stock("IN")

    add("Ctrl+I", stock_in)

    def stock_out() -> None:
        if w._current_section == "components":
            w.update_stock("OUT")

    add("Ctrl+U", stock_out)

    def add_manual() -> None:
        if w._current_section in ("components", "equipments"):
            w.add_manual_entry()

    add("Ctrl+N", add_manual)

    def edit_entry() -> None:
        if w._current_section in ("components", "equipments"):
            w.edit_current_entry()

    add("Ctrl+E", edit_entry)

    def history_filtered() -> None:
        if w._current_section in ("components", "equipments"):
            w.open_history_filtered()

    add("Ctrl+H", history_filtered)

    def history_all() -> None:
        if w._current_section in ("components", "equipments"):
            w.open_history_all()

    add("Ctrl+Shift+H", history_all)

    def clear_fields() -> None:
        if w._current_section not in ("components", "equipments"):
            return
        focused = w.focusWidget()
        if isinstance(focused, QLineEdit) and focused.isEnabled():
            return
        w.clear_all_fields()

    add("Escape", clear_fields)

    def open_excel() -> None:
        if w._current_section in ("components", "equipments"):
            w.open_excel_file()

    add("Ctrl+Shift+E", open_excel)

    def toggle_inventory_mode() -> None:
        if w._current_section != "components":
            return
        combo = w._inventory_mode_combo
        combo.setCurrentIndex(1 - combo.currentIndex())

    add("Ctrl+Shift+M", toggle_inventory_mode)

    apply_shortcut_tooltips(w)


def apply_shortcut_tooltips(window) -> None:
    """Append shortcut hints to main action button tooltips."""
    u = window.ui
    _append_tooltip(u.btn_search, "Ctrl+Enter")
    _append_tooltip(u.btn_scan, "F5")
    _append_tooltip(u.btn_add_stock, "Ctrl+I")
    _append_tooltip(u.btn_remove_stock, "Ctrl+U")
    _append_tooltip(u.btn_history_component, "Ctrl+H")
    _append_tooltip(u.btn_history_all, "Ctrl+Shift+H")
    if hasattr(u, "btn_add_manual"):
        _append_tooltip(u.btn_add_manual, "Ctrl+N")
    if hasattr(u, "btn_edit_component"):
        _append_tooltip(u.btn_edit_component, "Ctrl+E")
    _append_tooltip(u.btn_clear, "Esc")
    if hasattr(window, "btn_open_excel"):
        _append_tooltip(window.btn_open_excel, "Ctrl+Shift+E")
    _append_tooltip(window.btn_nav_components, "Ctrl+1")
    _append_tooltip(window.btn_nav_equipments, "Ctrl+2")
    _append_tooltip(window.btn_nav_statistics, "Ctrl+3")
    _append_tooltip(u.search_entry, "Ctrl+F")
    hint = getattr(window, "_global_search_hint", None)
    _append_tooltip(hint, "Ctrl+G")
    if hasattr(window, "_statistics_page"):
        _append_tooltip(window._statistics_page.btn_export_pdf, "Statistics report")
    _append_tooltip(u.barcode_entry, "F6 · Enter scan")
    _append_tooltip(u.quantity_entry, "F2")
    _append_tooltip(u.user_entry, "F4")
    _append_tooltip(window._inventory_mode_combo, "Ctrl+Shift+M")
