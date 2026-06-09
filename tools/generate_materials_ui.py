"""
Generate gui_materials.ui — Materials page (mirrors Components layout).

Run: python tools/generate_materials_ui.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gui import styles  # noqa: E402
from tools.gui_ui_builder import (  # noqa: E402
    PANEL_FRAME_CLOSE,
    input_btn_row_xml,
    input_row_xml,
    output_row_xml,
    page_grid_margins_xml,
    panel_frame_open,
    prop_string,
    section_title_xml,
    vertical_spacer_xml,
)

OUT = ROOT / "src" / "gui" / "designer" / "gui_materials.ui"


def build_ui() -> str:
    left = []
    r = 0
    left.append(section_title_xml("label_operations", "Operations", r, colspan=2))
    r += 1
    left.append(
        input_btn_row_xml("search_entry", "Search Material", "btn_search", "SEARCH", r)
    )
    r += 1
    left.append(
        input_row_xml(
            "supplier_ref_entry",
            "Scan Barcode / Supplier Ref.",
            r,
            with_copy=True,
            copy_btn_name="btn_copy_supplier_ref",
        )
    )
    r += 1
    left.append(vertical_spacer_xml("verticalSpacer_materials_left", r))

    right = []
    rr = 0
    right.append(section_title_xml("label_details", "Material Details", rr))
    rr += 1
    for name, label in (
        ("val_supplier_reference", "Supplier Reference"),
        ("val_serial_number", "Serial Number"),
        ("val_description", "Description"),
        ("val_calibration", "Calibration Date"),
        ("val_expiration", "Calibration Expiration"),
    ):
        right.append(output_row_xml(name, label, rr))
        rr += 1
    right.append(vertical_spacer_xml("verticalSpacer_materials_right", rr))

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MaterialsPage</class>
 <widget class="QWidget" name="MaterialsPage">
  <property name="geometry">
   <rect><x>0</x><y>0</y><width>1284</width><height>520</height></rect>
  </property>
  <property name="styleSheet">
{prop_string(styles.MAIN_WINDOW_STYLE)}  </property>
  <layout class="QGridLayout" name="gridLayout_materials">
{page_grid_margins_xml()}
   <item row="0" column="0">
{panel_frame_open("container_materials_left")}
{chr(10).join(left)}
{PANEL_FRAME_CLOSE}
   </item>
   <item row="0" column="1">
{panel_frame_open("container_materials_right")}
{chr(10).join(right)}
{PANEL_FRAME_CLOSE}
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_ui(), encoding="utf-8")
    print(f"Generated: {OUT}")


if __name__ == "__main__":
    main()
