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

OUT = ROOT / "src" / "gui" / "designer" / "gui_stocktracker.ui"
LW = styles.TEMPLATE_LABEL_MIN_WIDTH
RS = styles.TEMPLATE_ROW_SPACING
RM = styles.TEMPLATE_ROW_MARGINS


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def prop_string(value: str) -> str:
    return f'   <string notr="true">{esc(value)}</string>\n'


def template_label_xml(name: str, text: str) -> str:
    return f"""              <widget class="QLabel" name="{name}">
               <property name="minimumSize"><size><width>{LW}</width><height>0</height></size></property>
               <property name="sizePolicy">
                <sizepolicy hsizetype="Minimum" vsizetype="Preferred">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="text"><string>{esc(text)}</string></property>
              </widget>
"""


def row_open(name: str, row: int) -> str:
    return f"""          <item row="{row}" column="0" colspan="2">
           <widget class="QWidget" name="row_{name}" native="true">
            <layout class="QHBoxLayout" name="layout_{name}">
             <property name="spacing"><number>{RS}</number></property>
             <property name="topMargin"><number>{RM[1]}</number></property>
             <property name="rightMargin"><number>{RM[2]}</number></property>
             <property name="bottomMargin"><number>{RM[3]}</number></property>
"""


ROW_CLOSE = """            </layout>
           </widget>
          </item>
"""


def copy_btn_xml(copy_btn_name: str, *, width: int = 60) -> str:
    return f"""             <item>
              <widget class="QPushButton" name="{copy_btn_name}">
               <property name="minimumSize"><size><width>{width}</width><height>0</height></size></property>
               <property name="maximumSize"><size><width>{width}</width><height>16777215</height></size></property>
               <property name="toolTip"><string>Copy to clipboard</string></property>
               <property name="styleSheet">
{prop_string(styles.BTN_COPY_STYLE)}               </property>
               <property name="text"><string>Copy</string></property>
              </widget>
             </item>
"""


def input_row_xml(name: str, label: str, row: int, *, with_copy: bool = False) -> str:
    copy_part = copy_btn_xml(f"btn_copy_{name}") if with_copy else ""
    return (
        row_open(name, row)
        + f"""             <item>
{template_label_xml(f"label_{name}", label)}
             </item>
             <item>
              <widget class="QLineEdit" name="{name}">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="styleSheet">
{prop_string(styles.LINE_EDIT_STYLE)}               </property>
              </widget>
             </item>
{copy_part}"""
        + ROW_CLOSE
    )


def input_btn_row_xml(
    name: str,
    label: str,
    btn_name: str,
    btn_text: str,
    row: int,
    *,
    with_copy: bool = False,
    copy_before_field: bool = False,
) -> str:
    copy_part = copy_btn_xml(f"btn_copy_{name}") if with_copy else ""
    field_part = f"""             <item>
              <widget class="QLineEdit" name="{name}">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="styleSheet">
{prop_string(styles.LINE_EDIT_STYLE)}               </property>
              </widget>
             </item>
"""
    action_part = f"""             <item>
              <widget class="QPushButton" name="{btn_name}">
               <property name="minimumSize"><size><width>124</width><height>0</height></size></property>
               <property name="styleSheet">
{prop_string(styles.BTN_TEMPLATE_STYLE)}               </property>
               <property name="text"><string>{esc(btn_text)}</string></property>
              </widget>
             </item>
"""
    if with_copy and copy_before_field:
        widgets_block = copy_part + field_part + action_part
    elif with_copy:
        widgets_block = field_part + copy_part + action_part
    else:
        widgets_block = field_part + action_part
    return (
        row_open(name, row)
        + f"""             <item>
{template_label_xml(f"label_{name}", label)}
             </item>
{widgets_block}"""
        + ROW_CLOSE
    )


def combo_row_xml(row: int) -> str:
    return f"""          <item row="{row}" column="0" colspan="2">
           <widget class="QWidget" name="row_supplier_combo" native="true">
            <layout class="QGridLayout" name="grid_supplier">
             <property name="topMargin"><number>{RM[1]}</number></property>
             <property name="rightMargin"><number>{RM[2]}</number></property>
             <property name="bottomMargin"><number>{RM[3]}</number></property>
             <item row="0" column="0">
{template_label_xml("label_supplier", "Distributor")}
             </item>
             <item row="0" column="1">
              <widget class="QComboBox" name="supplier_combo">
               <property name="minimumSize"><size><width>172</width><height>30</height></size></property>
               <property name="styleSheet">
{prop_string(styles.COMBOBOX_STYLE)}               </property>
              </widget>
             </item>
            </layout>
           </widget>
          </item>
"""


def stock_btn_row_xml(row: int) -> str:
    return (
        row_open("stock_buttons", row)
        + f"""             <item>
{template_label_xml("label_stock_btn", "Button")}
             </item>
             <item>
              <widget class="QPushButton" name="btn_add_stock">
               <property name="minimumSize"><size><width>124</width><height>0</height></size></property>
               <property name="styleSheet">
{prop_string(styles.BTN_TEMPLATE_STYLE)}               </property>
               <property name="text"><string>ADD STOCK</string></property>
              </widget>
             </item>
             <item>
              <widget class="QPushButton" name="btn_remove_stock">
               <property name="minimumSize"><size><width>124</width><height>0</height></size></property>
               <property name="styleSheet">
{prop_string(styles.BTN_TEMPLATE_STYLE)}               </property>
               <property name="text"><string>REMOVE STOCK</string></property>
              </widget>
             </item>
"""
        + ROW_CLOSE
    )


def output_row_xml(name: str, label: str, row: int) -> str:
    ss = styles.VALUE_FIELD_STYLE
    return (
        row_open(name, row)
        + f"""             <item>
{template_label_xml(f"title_{name}", label)}
             </item>
             <item>
              <widget class="QLabel" name="{name}">
               <property name="styleSheet">
{prop_string(ss)}               </property>
               <property name="text"><string></string></property>
              </widget>
             </item>
{copy_btn_xml(f"btn_copy_{name}")}"""
        + ROW_CLOSE
    )


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
        input_row_xml("barcode_entry", "Scan Barcode / Supplier Ref.", r, with_copy=True)
    )
    r += 1
    left.append(input_btn_row_xml("quantity_entry", "Quantity", "btn_scan", "SCAN", r))
    r += 1
    left.append(stock_btn_row_xml(r))
    r += 1
    left.append(f"""          <item row="{r}" column="1">
           <spacer name="verticalSpacer_left">
            <property name="orientation"><enum>Qt::Orientation::Vertical</enum></property>
            <property name="sizeHint" stdset="0"><size><width>20</width><height>40</height></size></property>
           </spacer>
          </item>""")

    right = []
    rr = 0
    right.append(f"""          <item row="{rr}" column="0">
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
        right.append(output_row_xml(name, label, rr))
        rr += 1
    right.append(f"""          <item row="{rr}" column="1">
           <spacer name="verticalSpacer_right">
            <property name="orientation"><enum>Qt::Orientation::Vertical</enum></property>
            <property name="sizeHint" stdset="0"><size><width>20</width><height>40</height></size></property>
           </spacer>
          </item>""")

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
       <property name="leftMargin"><number>16</number></property>
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
       <property name="leftMargin"><number>16</number></property>
       <property name="topMargin"><number>9</number></property>
       <property name="rightMargin"><number>16</number></property>
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
