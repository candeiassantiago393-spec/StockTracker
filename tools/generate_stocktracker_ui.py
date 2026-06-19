"""
Generate gui_stocktracker.ui aligned with gui_template.ui.

Run: python tools/generate_stocktracker_ui.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gui import styles  # noqa: E402
from tools.gui_ui_builder import (  # noqa: E402
    PM,
    RS,
    catalog_links_grid_xml,
    component_details_grid_columns_xml,
    component_image_preview_side_xml,
    esc,
    header_side_margins_xml,
    input_btn_row_xml,
    input_row_xml,
    input_scan_copy_row_xml,
    output_row_label_grid_xml,
    output_row_value_grid_xml,
    page_grid_margins_xml,
    prop_string,
    stock_btn_row_xml,
    vertical_spacer_xml,
)

OUT = ROOT / "src" / "gui" / "designer" / "gui_stocktracker.ui"


def footer_btn_xml(name: str, text: str) -> str:
    return f"""       <item>
        <widget class="QPushButton" name="{name}">
         <property name="minimumSize"><size><width>124</width><height>0</height></size></property>
         <property name="styleSheet">
{prop_string(styles.BTN_TEMPLATE_STYLE)}         </property>
         <property name="text"><string>{esc(text)}</string></property>
        </widget>
       </item>
"""


def build_ui() -> str:
    left = []
    r = 0
    left.append(f"""          <item row="{r}" column="0">
           <widget class="QLabel" name="label_operations">
            <property name="styleSheet">
{prop_string(styles.SECTION_TITLE_STYLE)}            </property>
            <property name="text"><string>Operations</string></property>
           </widget>
          </item>""")
    r += 1
    left.append(input_row_xml("user_entry", "User Name", r))
    r += 1
    left.append(input_btn_row_xml("search_entry", "Search Component", "btn_search", "SEARCH", r))
    r += 1
    left.append(
        input_scan_copy_row_xml(
            "barcode_entry",
            "Scan Barcode / Supplier Ref.",
            "btn_scan",
            r,
            with_copy=False,
        )
    )
    r += 1
    left.append(input_row_xml("quantity_entry", "Quantity", r))
    r += 1
    left.append(stock_btn_row_xml(r))
    r += 1
    left.append(vertical_spacer_xml("verticalSpacer_left", r))

    right = []
    rr = 0
    detail_start = rr + 1
    right.append(f"""          <item row="{rr}" column="0" colspan="5">
           <widget class="QLabel" name="label_details">
            <property name="styleSheet">
{prop_string(styles.SECTION_TITLE_STYLE)}            </property>
            <property name="text"><string>Component Details</string></property>
           </widget>
          </item>""")
    rr += 1
    for name, label in (
        ("val_mouser", "Supplier Reference"),
        ("val_manufacturer", "Manufacturer"),
        ("val_manufacturer_ref", "Manufacturer Reference"),
        ("val_description", "Description"),
        ("val_stock", "Current Stock"),
    ):
        right.append(output_row_label_grid_xml(name, label, rr))
        right.append(output_row_value_grid_xml(name, rr))
        rr += 1
    right.append(catalog_links_grid_xml(rr))
    catalog_row = rr
    rr += 1
    right.append(
        component_image_preview_side_xml(
            detail_start,
            catalog_row - detail_start,
        )
    )
    right.append(vertical_spacer_xml("verticalSpacer_right", rr, col=0, height=12))

    footer = "".join(
        [
            footer_btn_xml("btn_history_all", "Last 20"),
            footer_btn_xml("btn_history_component", "Comp. hist."),
            footer_btn_xml("btn_add_manual", "ADD MANUAL COMPONENT"),
            footer_btn_xml("btn_edit_component", "EDIT COMPONENT"),
            """       <item>
        <spacer name="horizontalSpacer_actions">
         <property name="orientation"><enum>Qt::Orientation::Horizontal</enum></property>
         <property name="sizeHint" stdset="0"><size><width>40</width><height>20</height></size></property>
        </spacer>
       </item>
""",
            footer_btn_xml("btn_clear", "CLEAR"),
            footer_btn_xml("btn_exit", "Exit"),
        ]
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>StockTracker</class>
 <widget class="QMainWindow" name="StockTracker">
  <property name="geometry">
   <rect><x>0</x><y>0</y><width>1284</width><height>720</height></rect>
  </property>
  <property name="windowTitle"><string>Stock Tracker</string></property>
  <property name="windowIcon">
   <iconset resource="../siemens_template/resources/resources.qrc">
    <normaloff>:/siemens_logo/logos/sie-favicon_internet.ico</normaloff>:/siemens_logo/logos/sie-favicon_internet.ico</iconset>
  </property>
  <property name="styleSheet">
{prop_string(styles.MAIN_WINDOW_STYLE)}  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <property name="spacing"><number>0</number></property>
    <property name="leftMargin"><number>0</number></property>
    <property name="topMargin"><number>0</number></property>
    <property name="rightMargin"><number>0</number></property>
    <property name="bottomMargin"><number>0</number></property>
    <item>
     <widget class="QWidget" name="header" native="true">
      <property name="sizePolicy">
       <sizepolicy hsizetype="Preferred" vsizetype="Maximum">
        <horstretch>0</horstretch>
        <verstretch>0</verstretch>
       </sizepolicy>
      </property>
      <property name="styleSheet">
{prop_string(styles.HEADER_STYLE)}      </property>
      <layout class="QHBoxLayout" name="horizontalLayout_header">
       <property name="spacing"><number>16</number></property>
{header_side_margins_xml()}
       <item>
        <widget class="QLabel" name="brand_identifier">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Maximum" vsizetype="Preferred">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="pixmap">
          <pixmap resource="../siemens_template/resources/resources.qrc">:/siemens_logo/logos/Siemens Logo.png</pixmap>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QLabel" name="product_name">
         <property name="styleSheet">
{prop_string(styles.PRODUCT_NAME_STYLE)}         </property>
         <property name="text"><string>Stock Tracker</string></property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
    <item>
     <widget class="QWidget" name="container_main_body" native="true">
      <layout class="QGridLayout" name="gridLayout_main">
{page_grid_margins_xml()}
       <item row="0" column="0" colspan="2">
        <widget class="QFrame" name="frame_title">
         <property name="frameShape"><enum>QFrame::Shape::StyledPanel</enum></property>
         <property name="frameShadow"><enum>QFrame::Shadow::Raised</enum></property>
         <layout class="QVBoxLayout" name="verticalLayout_title">
          <property name="spacing"><number>0</number></property>
          <property name="leftMargin"><number>0</number></property>
          <property name="topMargin"><number>0</number></property>
          <property name="rightMargin"><number>0</number></property>
          <property name="bottomMargin"><number>0</number></property>
          <item>
           <widget class="QLabel" name="tab1_title">
            <property name="styleSheet">
{prop_string(styles.PAGE_TITLE_STYLE)}            </property>
            <property name="text"><string>Inventory</string></property>
           </widget>
          </item>
         </layout>
        </widget>
       </item>
       <item row="1" column="0">
        <widget class="QFrame" name="container_tab1_left">
         <property name="frameShape"><enum>QFrame::Shape::StyledPanel</enum></property>
         <property name="frameShadow"><enum>QFrame::Shadow::Raised</enum></property>
         <layout class="QGridLayout" name="gridLayout_left">
          <property name="topMargin"><number>15</number></property>
          <property name="verticalSpacing"><number>0</number></property>
{chr(10).join(left)}
         </layout>
        </widget>
       </item>
       <item row="1" column="1">
        <widget class="QFrame" name="container_tab1_right">
         <property name="frameShape"><enum>QFrame::Shape::StyledPanel</enum></property>
         <property name="frameShadow"><enum>QFrame::Shadow::Raised</enum></property>
         <layout class="QGridLayout" name="gridLayout_right">
          <property name="topMargin"><number>15</number></property>
          <property name="verticalSpacing"><number>0</number></property>
{component_details_grid_columns_xml()}
{chr(10).join(right)}
         </layout>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
    <item>
     <widget class="QWidget" name="widget_actions" native="true">
      <layout class="QHBoxLayout" name="horizontalLayout_actions">
       <property name="spacing"><number>{RS}</number></property>
       <property name="leftMargin"><number>{PM[0]}</number></property>
       <property name="topMargin"><number>9</number></property>
       <property name="rightMargin"><number>{PM[2]}</number></property>
       <property name="bottomMargin"><number>9</number></property>
{footer}
      </layout>
     </widget>
    </item>
    <item>
     <widget class="QLabel" name="status_label">
      <property name="styleSheet">
{prop_string(styles.STATUS_STYLE)}      </property>
      <property name="text"><string></string></property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources>
  <include location="../siemens_template/resources/resources.qrc"/>
 </resources>
 <connections/>
</ui>
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_ui(), encoding="utf-8")
    print(f"Generated: {OUT}")


if __name__ == "__main__":
    main()
