"""
Generate Stock Tracker popup .ui files for Qt Designer (full layout, not shell-only).

Run: python tools/generate_popup_uis.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gui import styles  # noqa: E402

TEMPLATE = ROOT / "src" / "gui" / "siemens_template" / "gui_popup.ui"
OUT_DIR = ROOT / "src" / "gui" / "designer" / "popups"
INSERT_MARKER = '      <item>\n       <widget class="QWidget" name="container_button"'


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def prop_string(value: str) -> str:
    return f'   <string notr="true">{esc(value)}</string>\n'


def line_edit_xml(name: str) -> str:
    return f"""          <widget class="QLineEdit" name="{name}">
           <property name="styleSheet">
{prop_string(styles.LINE_EDIT_STYLE)}           </property>
          </widget>
"""


def form_row_xml(row: int, label: str, field_xml: str) -> str:
    return f"""         <item row="{row}" column="0">
          <widget class="QLabel" name="label_{label}">
           <property name="text"><string>{esc(label)}</string></property>
          </widget>
         </item>
         <item row="{row}" column="1">
{field_xml}
         </item>
"""


def form_edit_body() -> str:
    stock_label = f"""          <widget class="QLabel" name="label_current_stock">
           <property name="styleSheet">
{prop_string(styles.VALUE_FIELD_STYLE)}           </property>
           <property name="text"><string>0</string></property>
          </widget>
"""
    rows = [
        (0, "Supplier Reference", line_edit_xml("supplier_reference")),
        (1, "Manufacturer", line_edit_xml("manufacturer")),
        (2, "Manufacturer Reference", line_edit_xml("manufacturer_reference")),
        (3, "Description", line_edit_xml("description_field")),
        (4, "Current Stock", stock_label),
    ]
    items = "\n".join(form_row_xml(r, lbl, fld) for r, lbl, fld in rows)
    return f"""      <item>
       <widget class="QWidget" name="body_form" native="true">
        <layout class="QFormLayout" name="form_edit">
         <property name="spacing"><number>{styles.TEMPLATE_ROW_SPACING}</number></property>
{items}
        </layout>
       </widget>
      </item>
"""


def form_manual_body() -> str:
    rows = [
        (0, "Supplier Reference", line_edit_xml("supplier_reference")),
        (1, "Manufacturer", line_edit_xml("manufacturer")),
        (2, "Manufacturer Reference", line_edit_xml("manufacturer_reference")),
        (3, "Description", line_edit_xml("description_field")),
        (
            4,
            "Initial Stock",
            f"""          <widget class="QSpinBox" name="initial_stock">
           <property name="minimum"><number>0</number></property>
           <property name="maximum"><number>999999</number></property>
           <property name="styleSheet">
{prop_string(styles.LINE_EDIT_STYLE)}           </property>
          </widget>
""",
        ),
    ]
    items = "\n".join(form_row_xml(r, lbl, fld) for r, lbl, fld in rows)
    return f"""      <item>
       <widget class="QWidget" name="body_form" native="true">
        <layout class="QFormLayout" name="form_manual">
         <property name="spacing"><number>{styles.TEMPLATE_ROW_SPACING}</number></property>
{items}
        </layout>
       </widget>
      </item>
"""


def table_body(name: str, columns: tuple[str, ...]) -> str:
    cols = "\n".join(
        f"""         <column>
          <property name="text"><string>{esc(c)}</string></property>
         </column>"""
        for c in columns
    )
    return f"""      <item>
       <widget class="QTableWidget" name="{name}">
        <property name="minimumSize">
         <size>
          <width>0</width>
          <height>280</height>
         </size>
        </property>
        <property name="styleSheet">
{prop_string(styles.TABLE_STYLE)}        </property>
{cols}
       </widget>
      </item>
"""


COMPONENT_HISTORY_COLUMNS = (
    "Date",
    "User",
    "Supplier Reference",
    "Movement",
    "Quantity",
    "Stock After",
)
COMPONENT_SEARCH_COLUMNS = (
    "Supplier Reference",
    "Manufacturer",
    "Manufacturer Reference",
    "Description",
    "Stock",
)
MATERIAL_HISTORY_COLUMNS = (
    "ID",
    "Supplier Reference",
    "Serial Number",
    "Description",
    "Calibration Date",
    "Calibration Expiration",
)
MATERIAL_SEARCH_COLUMNS = (
    "Supplier Reference",
    "Serial Number",
    "Description",
    "Calibration Date",
    "Calibration Expiration",
)

COMPONENTS_DIR = OUT_DIR / "components"
MATERIALS_DIR = OUT_DIR / "materials"
SHARED_DIR = OUT_DIR / "shared"


def form_material_body() -> str:
    rows = [
        (0, "Supplier Reference", line_edit_xml("supplier_reference")),
        (1, "Serial Number", line_edit_xml("serial_number")),
        (2, "Description", line_edit_xml("description_field")),
        (3, "Calibration Date", line_edit_xml("calibration_date")),
        (4, "Calibration Expiration", line_edit_xml("calibration_expiration")),
    ]
    items = "\n".join(form_row_xml(r, lbl, fld) for r, lbl, fld in rows)
    return f"""      <item>
       <widget class="QWidget" name="body_form" native="true">
        <layout class="QFormLayout" name="form_material">
         <property name="spacing"><number>{styles.TEMPLATE_ROW_SPACING}</number></property>
{items}
        </layout>
       </widget>
      </item>
"""


def _cleanup_legacy_popups() -> None:
    """Remove flat popups/*.ui from before components/materials/shared split."""
    for pattern in ("gui_popup_*.ui", "gui_popup_*.py"):
        for path in OUT_DIR.glob(pattern):
            path.unlink()
            print(f"Removed legacy {path.name}")


def patch_popup(
    base: str,
    *,
    class_name: str,
    title: str,
    subtitle: str | None,
    width: int,
    height: int,
    body_xml: str,
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    show_cancel: bool = True,
) -> str:
    xml = base
    xml = xml.replace("<class>Popup</class>", f"<class>{class_name}</class>")
    xml = xml.replace('name="Popup"', f'name="{class_name}"', 1)
    xml = xml.replace("<string>Popup Title</string>", f"<string>{esc(title)}</string>")
    xml = xml.replace(
        "<width>641</width>",
        f"<width>{width}</width>",
        1,
    )
    xml = xml.replace(
        "<height>283</height>",
        f"<height>{height}</height>",
        1,
    )
    if subtitle:
        xml = xml.replace(
            "<string>Popup description</string>",
            f"<string>{esc(subtitle)}</string>",
        )
    else:
        xml = xml.replace(
            '      <item>\n       <widget class="QWidget" name="widget" native="true">',
            '      <item>\n       <widget class="QWidget" name="widget" native="true">\n'
            '        <property name="maximumSize">\n'
            '         <size>\n'
            '          <width>0</width>\n'
            '          <height>0</height>\n'
            '         </size>\n'
            '        </property>',
            1,
        )
    xml = xml.replace("<string>Ok</string>", f"<string>{esc(ok_text)}</string>", 1)
    xml = xml.replace(
        "<string>Cancel</string>",
        f"<string>{esc(cancel_text)}</string>",
        1,
    )
    if not show_cancel:
        xml = xml.replace(
            '          <widget class="QPushButton" name="btn_cancel">',
            '          <widget class="QPushButton" name="btn_cancel">\n'
            '           <property name="visible"><bool>false</bool></property>',
            1,
        )
    if INSERT_MARKER not in xml:
        raise RuntimeError("Popup template structure changed; update INSERT_MARKER")
    xml = xml.replace(INSERT_MARKER, body_xml + INSERT_MARKER, 1)
    return xml


def main() -> None:
    base = TEMPLATE.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    COMPONENTS_DIR.mkdir(parents=True, exist_ok=True)
    MATERIALS_DIR.mkdir(parents=True, exist_ok=True)
    SHARED_DIR.mkdir(parents=True, exist_ok=True)
    _cleanup_legacy_popups()

    component_variants = [
        (
            COMPONENTS_DIR / "gui_popup_manual.ui",
            patch_popup(
                base,
                class_name="PopupManual",
                title="Add Manual Component",
                subtitle=(
                    "Supplier Reference is optional when both Manufacturer and "
                    "Manufacturer Reference are provided."
                ),
                width=641,
                height=520,
                body_xml=form_manual_body(),
                ok_text="Save",
                cancel_text="Cancel",
            ),
        ),
        (
            COMPONENTS_DIR / "gui_popup_history.ui",
            patch_popup(
                base,
                class_name="PopupHistory",
                title="Component History",
                subtitle=None,
                width=850,
                height=480,
                body_xml=table_body("table_history", COMPONENT_HISTORY_COLUMNS),
                ok_text="Close",
                show_cancel=False,
            ),
        ),
        (
            COMPONENTS_DIR / "gui_popup_search.ui",
            patch_popup(
                base,
                class_name="PopupSearch",
                title="Component search results",
                subtitle="Select a row and press Ok, or double-click a row.",
                width=900,
                height=480,
                body_xml=table_body("table_search", COMPONENT_SEARCH_COLUMNS),
            ),
        ),
        (
            COMPONENTS_DIR / "gui_popup_edit.ui",
            patch_popup(
                base,
                class_name="PopupEdit",
                title="Edit Component",
                subtitle="Update component data. Use ADD/REMOVE STOCK to change quantity.",
                width=641,
                height=480,
                body_xml=form_edit_body(),
                ok_text="Save",
                cancel_text="Cancel",
            ),
        ),
    ]

    material_variants = [
        (
            MATERIALS_DIR / "gui_popup_material.ui",
            patch_popup(
                base,
                class_name="PopupMaterial",
                title="Material",
                subtitle=(
                    "Provide Supplier Reference, Serial Number or Description."
                ),
                width=641,
                height=520,
                body_xml=form_material_body(),
                ok_text="Save",
                cancel_text="Cancel",
            ),
        ),
        (
            MATERIALS_DIR / "gui_popup_history.ui",
            patch_popup(
                base,
                class_name="PopupMaterialHistory",
                title="Materials",
                subtitle=None,
                width=950,
                height=480,
                body_xml=table_body("table_history", MATERIAL_HISTORY_COLUMNS),
                ok_text="Close",
                show_cancel=False,
            ),
        ),
        (
            MATERIALS_DIR / "gui_popup_search.ui",
            patch_popup(
                base,
                class_name="PopupMaterialSearch",
                title="Material search results",
                subtitle="Select a row and press Ok, or double-click a row.",
                width=950,
                height=480,
                body_xml=table_body("table_search", MATERIAL_SEARCH_COLUMNS),
            ),
        ),
    ]

    shared_variants = [
        (
            SHARED_DIR / "gui_popup_confirm.ui",
            patch_popup(
                base,
                class_name="PopupConfirm",
                title="Confirm",
                subtitle="Please confirm this action.",
                width=641,
                height=320,
                body_xml="",
                ok_text="Yes",
                cancel_text="No",
            ),
        ),
    ]

    for path, content in (
        *component_variants,
        *material_variants,
        *shared_variants,
    ):
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path}")

    template_copy = SHARED_DIR / "gui_popup_template.ui"
    template_copy.write_text(base, encoding="utf-8")
    print(f"Wrote {template_copy}")
    print("Popups: popups/components/, popups/materials/, popups/shared/")


if __name__ == "__main__":
    main()
