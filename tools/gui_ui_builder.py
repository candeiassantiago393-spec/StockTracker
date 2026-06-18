"""Shared XML builders for Siemens-aligned Qt Designer .ui files."""
from __future__ import annotations

from src.gui import styles

LW = styles.TEMPLATE_LABEL_MIN_WIDTH
RS = styles.TEMPLATE_ROW_SPACING
RM = styles.TEMPLATE_ROW_MARGINS
PM = styles.TEMPLATE_PAGE_MARGINS


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def prop_string(value: str) -> str:
    return f'   <string notr="true">{esc(value)}</string>\n'


def page_grid_margins_xml(*, top_margin: int = 0) -> str:
    return f"""       <property name="leftMargin"><number>{PM[0]}</number></property>
       <property name="topMargin"><number>{top_margin}</number></property>
       <property name="rightMargin"><number>{PM[2]}</number></property>
       <property name="horizontalSpacing"><number>0</number></property>
       <property name="columnStretch" stdset="0">
        <number>1</number>
        <number>1</number>
       </property>"""


def header_side_margins_xml() -> str:
    return f"""       <property name="leftMargin"><number>{PM[0]}</number></property>
       <property name="rightMargin"><number>{PM[2]}</number></property>"""


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


def row_open(name: str, row: int, *, compact: bool = False) -> str:
    top, bottom = (4, 4) if compact else (RM[1], RM[3])
    return f"""          <item row="{row}" column="0" colspan="2">
           <widget class="QWidget" name="row_{name}" native="true">
            <layout class="QHBoxLayout" name="layout_{name}">
             <property name="spacing"><number>{RS}</number></property>
             <property name="topMargin"><number>{top}</number></property>
             <property name="rightMargin"><number>{RM[2]}</number></property>
             <property name="bottomMargin"><number>{bottom}</number></property>
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


def input_row_xml(
    name: str,
    label: str,
    row: int,
    *,
    with_copy: bool = False,
    copy_btn_name: str | None = None,
) -> str:
    copy_part = ""
    if with_copy:
        copy_part = copy_btn_xml(copy_btn_name or f"btn_copy_{name}")
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


def input_dual_btn_row_xml(
    name: str,
    label: str,
    primary_btn: str,
    primary_text: str,
    secondary_btn: str,
    secondary_text: str,
    row: int,
    *,
    compact: bool = False,
    secondary_width: int = 60,
) -> str:
    if secondary_width >= 124:
        secondary_part = f"""             <item>
              <widget class="QPushButton" name="{secondary_btn}">
               <property name="minimumSize"><size><width>124</width><height>0</height></size></property>
               <property name="styleSheet">
{prop_string(styles.BTN_TEMPLATE_STYLE)}               </property>
               <property name="text"><string>{esc(secondary_text)}</string></property>
              </widget>
             </item>
"""
    else:
        secondary_part = f"""             <item>
              <widget class="QPushButton" name="{secondary_btn}">
               <property name="minimumSize"><size><width>{secondary_width}</width><height>0</height></size></property>
               <property name="maximumSize"><size><width>{secondary_width}</width><height>16777215</height></size></property>
               <property name="styleSheet">
{prop_string(styles.BTN_COPY_STYLE)}               </property>
               <property name="text"><string>{esc(secondary_text)}</string></property>
              </widget>
             </item>
"""
    base = input_btn_row_xml(name, label, primary_btn, primary_text, row, compact=compact)
    return base.replace(ROW_CLOSE, secondary_part + ROW_CLOSE)


def input_btn_row_xml(
    name: str,
    label: str,
    btn_name: str,
    btn_text: str,
    row: int,
    *,
    with_copy: bool = False,
    copy_before_field: bool = False,
    copy_btn_name: str | None = None,
    compact: bool = False,
) -> str:
    copy_part = ""
    if with_copy:
        copy_part = copy_btn_xml(copy_btn_name or f"btn_copy_{name}")
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
        row_open(name, row, compact=compact)
        + f"""             <item>
{template_label_xml(f"label_{name}", label)}
             </item>
{widgets_block}"""
        + ROW_CLOSE
    )


def stock_btn_row_xml(row: int) -> str:
    return (
        row_open("stock_buttons", row)
        + f"""             <item>
{template_label_xml("label_stock_btn", "Stock Actions")}
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


def input_scan_copy_row_xml(
    name: str,
    label: str,
    scan_btn_name: str,
    row: int,
    *,
    copy_btn_name: str | None = None,
    compact: bool = False,
) -> str:
    copy_name = copy_btn_name or f"btn_copy_{name}"
    return (
        row_open(name, row, compact=compact)
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
             <item>
              <widget class="QPushButton" name="{scan_btn_name}">
               <property name="minimumSize"><size><width>124</width><height>0</height></size></property>
               <property name="styleSheet">
{prop_string(styles.BTN_TEMPLATE_STYLE)}               </property>
               <property name="text"><string>SCAN</string></property>
              </widget>
             </item>
{copy_btn_xml(copy_name)}"""
        + ROW_CLOSE
    )


def output_row_wide_xml(name: str, label: str, row: int) -> str:
    return (
        row_open(name, row)
        + f"""             <item>
{template_label_xml(f"title_{name}", label)}
             </item>
             <item>
              <widget class="QLabel" name="{name}">
               <property name="styleSheet">
{prop_string(styles.EQUIPMENT_VALUE_FIELD_STYLE)}               </property>
               <property name="text"><string></string></property>
              </widget>
             </item>
{copy_btn_xml(f"btn_copy_{name}")}"""
        + ROW_CLOSE
    )


def output_row_xml(name: str, label: str, row: int) -> str:
    return (
        row_open(name, row)
        + f"""             <item>
{template_label_xml(f"title_{name}", label)}
             </item>
             <item>
              <widget class="QLabel" name="{name}">
               <property name="styleSheet">
{prop_string(styles.VALUE_FIELD_STYLE)}               </property>
               <property name="text"><string></string></property>
              </widget>
             </item>
{copy_btn_xml(f"btn_copy_{name}")}"""
        + ROW_CLOSE
    )


def subsection_title_xml(name: str, text: str, row: int, *, colspan: int = 1) -> str:
    span = f' colspan="{colspan}"' if colspan > 1 else ""
    return f"""          <item row="{row}" column="0"{span}>
           <widget class="QLabel" name="{name}">
            <property name="styleSheet">
{prop_string(styles.SUBSECTION_TITLE_STYLE)}            </property>
            <property name="text"><string>{esc(text)}</string></property>
           </widget>
          </item>"""


def section_title_xml(name: str, text: str, row: int, *, col: int = 0, colspan: int = 1) -> str:
    span = f' colspan="{colspan}"' if colspan > 1 else ""
    return f"""          <item row="{row}" column="{col}"{span}>
           <widget class="QLabel" name="{name}">
            <property name="styleSheet">
{prop_string(styles.SECTION_TITLE_STYLE)}            </property>
            <property name="text"><string>{esc(text)}</string></property>
           </widget>
          </item>"""


def wide_button_row_xml(
    btn_name: str,
    btn_text: str,
    row: int,
    *,
    label: str = "Action",
    min_width: int = 280,
) -> str:
    return (
        row_open(btn_name, row)
        + f"""             <item>
{template_label_xml(f"label_{btn_name}", label)}
             </item>
             <item>
              <widget class="QPushButton" name="{btn_name}">
               <property name="minimumSize"><size><width>{min_width}</width><height>0</height></size></property>
               <property name="sizePolicy">
                <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
                 <horstretch>1</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="styleSheet">
{prop_string(styles.BTN_WIDE_ACTION_STYLE)}               </property>
               <property name="text"><string>{esc(btn_text)}</string></property>
              </widget>
             </item>
"""
        + ROW_CLOSE
    )


def label_button_row_xml(
    btn_name: str,
    label: str,
    btn_text: str,
    row: int,
    *,
    compact: bool = False,
) -> str:
    return (
        row_open(btn_name, row, compact=compact)
        + f"""             <item>
{template_label_xml(f"label_{btn_name}", label)}
             </item>
             <item>
              <widget class="QPushButton" name="{btn_name}">
               <property name="minimumSize"><size><width>124</width><height>0</height></size></property>
               <property name="styleSheet">
{prop_string(styles.BTN_TEMPLATE_STYLE)}               </property>
               <property name="text"><string>{esc(btn_text)}</string></property>
              </widget>
             </item>
"""
        + ROW_CLOSE
    )


def full_width_button_row_xml(btn_name: str, btn_text: str, row: int) -> str:
    return f"""          <item row="{row}" column="0" colspan="2">
           <widget class="QPushButton" name="{btn_name}">
            <property name="sizePolicy">
             <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
              <horstretch>1</horstretch>
              <verstretch>0</verstretch>
             </sizepolicy>
            </property>
            <property name="styleSheet">
{prop_string(styles.BTN_WIDE_ACTION_STYLE)}            </property>
            <property name="text"><string>{esc(btn_text)}</string></property>
           </widget>
          </item>"""


def list_widget_row_xml(
    name: str,
    row: int,
    *,
    min_height: int = 52,
    max_height: int = 64,
) -> str:
    return f"""          <item row="{row}" column="0" colspan="2">
           <widget class="QListWidget" name="{name}">
            <property name="minimumSize"><size><width>0</width><height>{min_height}</height></size></property>
            <property name="maximumSize"><size><width>16777215</width><height>{max_height}</height></size></property>
            <property name="styleSheet">
{prop_string(styles.LIST_WIDGET_STYLE)}            </property>
           </widget>
          </item>"""


def component_image_preview_xml(row: int) -> str:
    return f"""          <item row="{row}" column="0" colspan="2">
           <widget class="QLabel" name="component_image_preview">
            <property name="minimumSize"><size><width>240</width><height>240</height></size></property>
            <property name="sizePolicy">
             <sizepolicy hsizetype="Preferred" vsizetype="Expanding">
              <horstretch>0</horstretch>
              <verstretch>1</verstretch>
             </sizepolicy>
            </property>
            <property name="alignment"><set>Qt::AlignmentFlag::AlignCenter</set></property>
            <property name="styleSheet">
{prop_string(styles.EQUIPMENT_IMAGE_PREVIEW_STYLE)}            </property>
            <property name="text"><string>No image</string></property>
           </widget>
          </item>"""


def equipment_image_panel_xml(row: int) -> str:
    return f"""          <item row="{row}" column="0" colspan="2">
           <widget class="QWidget" name="equipment_image_panel" native="true">
            <layout class="QVBoxLayout" name="layout_equipment_image_panel">
             <property name="spacing"><number>6</number></property>
             <property name="topMargin"><number>9</number></property>
             <property name="rightMargin"><number>9</number></property>
             <property name="bottomMargin"><number>9</number></property>
             <item>
              <widget class="QLabel" name="equipment_image_preview">
               <property name="minimumSize"><size><width>300</width><height>260</height></size></property>
               <property name="sizePolicy">
                <sizepolicy hsizetype="Preferred" vsizetype="Expanding">
                 <horstretch>0</horstretch>
                 <verstretch>1</verstretch>
                </sizepolicy>
               </property>
               <property name="toolTip"><string>Drag and drop an image file here</string></property>
               <property name="alignment"><set>Qt::AlignmentFlag::AlignCenter</set></property>
               <property name="styleSheet">
{prop_string(styles.EQUIPMENT_IMAGE_PREVIEW_STYLE)}               </property>
               <property name="text"><string>Drop image here</string></property>
              </widget>
             </item>
             <item>
              <widget class="QWidget" name="row_equipment_image_buttons" native="true">
               <layout class="QHBoxLayout" name="layout_equipment_image_buttons">
                <property name="spacing"><number>6</number></property>
                <property name="topMargin"><number>0</number></property>
                <property name="bottomMargin"><number>0</number></property>
                <item>
                 <widget class="QPushButton" name="btn_set_equipment_image">
                  <property name="minimumSize"><size><width>64</width><height>0</height></size></property>
                  <property name="maximumSize"><size><width>64</width><height>16777215</height></size></property>
                  <property name="toolTip"><string>Add or replace equipment image</string></property>
                  <property name="styleSheet">
{prop_string(styles.BTN_COMPACT_STYLE)}                  </property>
                  <property name="text"><string>Add</string></property>
                 </widget>
                </item>
                <item>
                 <widget class="QPushButton" name="btn_clear_equipment_image">
                  <property name="minimumSize"><size><width>64</width><height>0</height></size></property>
                  <property name="maximumSize"><size><width>64</width><height>16777215</height></size></property>
                  <property name="toolTip"><string>Delete equipment image</string></property>
                  <property name="styleSheet">
{prop_string(styles.BTN_COMPACT_STYLE)}                  </property>
                  <property name="text"><string>Delete</string></property>
                 </widget>
                </item>
                <item>
                 <spacer name="horizontalSpacer_equipment_image">
                  <property name="orientation"><enum>Qt::Orientation::Horizontal</enum></property>
                  <property name="sizeHint" stdset="0"><size><width>40</width><height>20</height></size></property>
                 </spacer>
                </item>
               </layout>
              </widget>
             </item>
            </layout>
           </widget>
          </item>"""


def vertical_spacer_xml(name: str, row: int, *, col: int = 1, height: int = 40) -> str:
    return f"""          <item row="{row}" column="{col}">
           <spacer name="{name}">
            <property name="orientation"><enum>Qt::Orientation::Vertical</enum></property>
            <property name="sizeHint" stdset="0"><size><width>20</width><height>{height}</height></size></property>
           </spacer>
          </item>"""


def panel_frame_open(name: str, *, top_margin: int = 15) -> str:
    return f"""        <widget class="QFrame" name="{name}">
         <property name="frameShape"><enum>QFrame::Shape::StyledPanel</enum></property>
         <property name="frameShadow"><enum>QFrame::Shadow::Raised</enum></property>
         <layout class="QGridLayout" name="gridLayout_{name}">
          <property name="topMargin"><number>{top_margin}</number></property>
          <property name="verticalSpacing"><number>0</number></property>
"""


PANEL_FRAME_CLOSE = """         </layout>
        </widget>
"""
