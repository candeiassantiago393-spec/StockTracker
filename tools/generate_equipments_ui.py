"""
Generate gui_equipments.ui — Equipments page (mirrors Components layout).

Run: python tools/generate_equipments_ui.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gui import styles  # noqa: E402
from tools.gui_ui_builder import (  # noqa: E402
    PANEL_FRAME_CLOSE,
    equipment_image_panel_xml,
    input_btn_row_xml,
    input_dual_btn_row_xml,
    input_scan_copy_row_xml,
    label_button_row_xml,
    list_widget_row_xml,
    output_row_xml,
    output_row_xml,
    page_grid_margins_xml,
    panel_frame_open,
    prop_string,
    section_title_xml,
    subsection_title_xml,
    vertical_spacer_xml,
)

OUT = ROOT / "src" / "gui" / "designer" / "gui_equipments.ui"


def build_ui() -> str:
    left = []
    r = 0
    left.append(section_title_xml("label_operations", "Operations", r, colspan=2))
    r += 1
    left.append(
        input_btn_row_xml("search_entry", "Search Equipment", "btn_search", "SEARCH", r)
    )
    r += 1
    left.append(
        input_scan_copy_row_xml(
            "supplier_ref_entry",
            "Scan Barcode / Supplier Ref.",
            "btn_scan_supplier_ref",
            r,
            with_copy=False,
        )
    )
    r += 1
    left.append(equipment_image_panel_xml(r))
    r += 1
    left.append(vertical_spacer_xml("verticalSpacer_equipments_left", r, height=12))

    right = []
    rr = 0
    right.append(section_title_xml("label_details", "Equipment Details", rr))
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
    right.append(output_row_xml("val_datasheet", "Datasheet", rr))
    rr += 1
    right.append(
        subsection_title_xml("label_support_docs", "Support Documentation", rr, colspan=2)
    )
    rr += 1
    right.append(
        input_dual_btn_row_xml(
            "doc_search_entry",
            "Search doc",
            "btn_doc_search",
            "SEARCH",
            "btn_doc_open",
            "OPEN",
            rr,
            compact=True,
            secondary_width=124,
        )
    )
    rr += 1
    right.append(list_widget_row_xml("doc_results_list", rr))
    rr += 1
    right.append(
        label_button_row_xml(
            "btn_link_datasheet",
            "Link",
            "LINK",
            rr,
            compact=True,
        )
    )
    rr += 1
    right.append(
        label_button_row_xml(
            "btn_open_support_docs",
            "Folder",
            "OPEN FOLDER",
            rr,
            compact=True,
        )
    )
    rr += 1
    right.append(
        label_button_row_xml(
            "btn_add_support_doc",
            "Add",
            "ADD DOC",
            rr,
            compact=True,
        )
    )
    rr += 1
    right.append(vertical_spacer_xml("verticalSpacer_equipments_right", rr))

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>EquipmentsPage</class>
 <widget class="QWidget" name="EquipmentsPage">
  <property name="geometry">
   <rect><x>0</x><y>0</y><width>1284</width><height>520</height></rect>
  </property>
  <property name="styleSheet">
{prop_string(styles.MAIN_WINDOW_STYLE)}  </property>
  <layout class="QGridLayout" name="gridLayout_equipments">
{page_grid_margins_xml(top_margin=-18)}
   <item row="0" column="0">
{panel_frame_open("container_equipments_left")}
{chr(10).join(left)}
{PANEL_FRAME_CLOSE}
   </item>
   <item row="0" column="1">
{panel_frame_open("container_equipments_right", top_margin=-36)}
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
