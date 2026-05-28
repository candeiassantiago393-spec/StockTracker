"""
Generate Stock Tracker popup .ui files from siemens_template/gui_popup.ui.

Run: python tools/generate_popup_uis.py
Then (optional): .\\tools\\export_popup_uis.ps1
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src" / "gui" / "siemens_template" / "gui_popup.ui"
OUT_DIR = ROOT / "src" / "gui" / "designer" / "popups"

VARIANTS = {
    "gui_popup_manual.ui": (
        "Add Manual Component",
        "Supplier Reference is optional when both Manufacturer and Manufacturer Reference are provided.",
        "form_manual",
    ),
    "gui_popup_history.ui": (
        "History",
        None,
        "table_history",
    ),
    "gui_popup_search.ui": (
        "Search results",
        "Select a row and press Ok, or double-click a row.",
        "table_search",
    ),
}


def patch_popup(base: str, title: str, subtitle: str | None, body_name: str) -> str:
    xml = base.replace("<string>Popup Title</string>", f"<string>{title}</string>")
    if subtitle:
        xml = xml.replace(
            "<string>Popup description</string>",
            f"<string>{subtitle}</string>",
        )
    else:
        # Hide description panel for table-only popups
        xml = xml.replace(
            '<widget class="QWidget" name="widget" native="true">',
            f'<widget class="QWidget" name="widget" native="true">\n'
            f'        <property name="visible"><bool>false</bool></property>',
            1,
        )
    xml = xml.replace('name="Popup"', f'name="Popup_{body_name}"', 1)
    xml = xml.replace("<class>Popup</class>", f"<class>Popup_{body_name}</class>")
    return xml


def main() -> None:
    base = TEMPLATE.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, (title, subtitle, body) in VARIANTS.items():
        path = OUT_DIR / filename
        path.write_text(patch_popup(base, title, subtitle, body), encoding="utf-8")
        print(f"Wrote {path}")
    print("Open in Qt Designer: src/gui/designer/popups/")


if __name__ == "__main__":
    main()
