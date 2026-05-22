#!/usr/bin/env python3
"""Move Siemens template files into src/gui/siemens_template/. Run once from project root."""
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parent.parent
GUI = ROOT / "src" / "gui"
TPL = GUI / "siemens_template"

FILES = [
    "gui_template.ui",
    "gui_template.py",
    "gui_template_setup.py",
    "gui_popup.ui",
    "gui_popup.py",
    "gui_popup_setup.py",
]
FOLDERS = ["widgets", "resources"]


def main():
    TPL.mkdir(parents=True, exist_ok=True)
    (TPL / "__init__.py").write_text(
        '"""Siemens PySide6 templates (examples). Not used by Stock Tracker main window."""\n',
        encoding="utf-8",
    )

    for name in FILES:
        src = GUI / name
        if src.is_file():
            shutil.move(str(src), str(TPL / name))
            print(f"moved file: {name}")

    for folder in FOLDERS:
        src = GUI / folder
        if src.is_dir():
            dest = TPL / folder
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(src), str(dest))
            print(f"moved folder: {folder}")

    # Fix imports in card widgets
    card_entry = TPL / "widgets" / "card" / "card_entry_setup.py"
    if card_entry.is_file():
        text = card_entry.read_text(encoding="utf-8")
        text = text.replace(
            "from src.gui.widgets.card.card_entry",
            "from src.gui.siemens_template.widgets.card.card_entry",
        )
        card_entry.write_text(text, encoding="utf-8")
        print("fixed card_entry_setup.py")

    card_combo = TPL / "widgets" / "card" / "card_combobox_setup.py"
    if card_combo.is_file():
        text = card_combo.read_text(encoding="utf-8")
        text = text.replace(
            "from src.gui.widgets.card.",
            "from src.gui.siemens_template.widgets.card.",
        )
        card_combo.write_text(text, encoding="utf-8")
        print("fixed card_combobox_setup.py")

    progress = TPL / "widgets" / "progress_bar" / "gui_progress_bar.py"
    if progress.is_file():
        text = progress.read_text(encoding="utf-8")
        text = text.replace("from ...resources", "from ..resources")
        progress.write_text(text, encoding="utf-8")
        print("fixed gui_progress_bar.py")

    # gui_config.py
    cfg = GUI / "gui_config.py"
    if cfg.is_file():
        cfg.write_text(
            '''"""Paths for GUI assets (logos, images)."""
from pathlib import Path

GUI_DIR = Path(__file__).resolve().parent
SIEMENS_TEMPLATE_DIR = GUI_DIR / "siemens_template"
RESOURCES_DIR = SIEMENS_TEMPLATE_DIR / "resources"
LOGOS_DIR = RESOURCES_DIR / "logos"

# Optional PNG logo (copy from old project if you have it)
ASSETS_DIR = RESOURCES_DIR / "assets"
LOGO_PNG = ASSETS_DIR / "assetssiemens_digital.png"
LOGO_SVG = LOGOS_DIR / "sie-logo-white-rgb.svg"
''',
            encoding="utf-8",
        )
        print("updated gui_config.py")

    init_py = GUI / "__init__.py"
    init_py.write_text(
        '''"""Stock Tracker GUI package.

Main app (open with main.py / run.bat):
  stock_tracker_window.py, ui_stock_tracker.py, history_dialog.py, styles.py

Siemens examples (do not edit for daily work):
  siemens_template/
"""
''',
        encoding="utf-8",
    )
    print("updated __init__.py")

    print("\nDone. gui root contains:")
    for p in sorted(GUI.iterdir()):
        print(f"  {p.name}")


if __name__ == "__main__":
    main()
