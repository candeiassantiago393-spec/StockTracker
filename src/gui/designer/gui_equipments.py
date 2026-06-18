# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_equipments.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_EquipmentsPage(object):
    def setupUi(self, EquipmentsPage):
        if not EquipmentsPage.objectName():
            EquipmentsPage.setObjectName(u"EquipmentsPage")
        EquipmentsPage.resize(1284, 520)
        EquipmentsPage.setStyleSheet(u"\n"
"* {\n"
"    border: none;\n"
"    background: #000028;\n"
"    padding: 0;\n"
"    margin: 0;\n"
"    color: #FFFFFF;\n"
"    font-family: \"SiemensSansPro_A_Bd\";\n"
"    font-size: 14px;\n"
"}\n"
"")
        self.gridLayout_equipments = QGridLayout(EquipmentsPage)
        self.gridLayout_equipments.setObjectName(u"gridLayout_equipments")
        self.gridLayout_equipments.setHorizontalSpacing(0)
        self.gridLayout_equipments.setProperty(u"columnStretch", 1)
        self.gridLayout_equipments.setContentsMargins(16, -18, 16, -1)
        self.container_equipments_left = QFrame(EquipmentsPage)
        self.container_equipments_left.setObjectName(u"container_equipments_left")
        self.container_equipments_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_equipments_left.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_container_equipments_left = QGridLayout(self.container_equipments_left)
        self.gridLayout_container_equipments_left.setObjectName(u"gridLayout_container_equipments_left")
        self.gridLayout_container_equipments_left.setVerticalSpacing(0)
        self.gridLayout_container_equipments_left.setContentsMargins(-1, 15, -1, -1)
        self.label_operations = QLabel(self.container_equipments_left)
        self.label_operations.setObjectName(u"label_operations")
        self.label_operations.setStyleSheet(u"\n"
"QLabel {\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"")

        self.gridLayout_container_equipments_left.addWidget(self.label_operations, 0, 0, 1, 2)

        self.row_search_entry = QWidget(self.container_equipments_left)
        self.row_search_entry.setObjectName(u"row_search_entry")
        self.layout_search_entry = QHBoxLayout(self.row_search_entry)
        self.layout_search_entry.setSpacing(6)
        self.layout_search_entry.setObjectName(u"layout_search_entry")
        self.layout_search_entry.setContentsMargins(-1, 9, 9, 9)
        self.label_search_entry = QLabel(self.row_search_entry)
        self.label_search_entry.setObjectName(u"label_search_entry")
        self.label_search_entry.setMinimumSize(QSize(74, 0))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_search_entry.sizePolicy().hasHeightForWidth())
        self.label_search_entry.setSizePolicy(sizePolicy)

        self.layout_search_entry.addWidget(self.label_search_entry)

        self.search_entry = QLineEdit(self.row_search_entry)
        self.search_entry.setObjectName(u"search_entry")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.search_entry.sizePolicy().hasHeightForWidth())
        self.search_entry.setSizePolicy(sizePolicy1)
        self.search_entry.setStyleSheet(u"\n"
"QLineEdit {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    max-height: 18px;\n"
"    padding: 5px;\n"
"    padding-bottom: 7px;\n"
"    margin-top: 0px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #B3B3BE;\n"
"    background-color: #00183B;\n"
"    color: #FFFFFF;\n"
"}\n"
"QLineEdit:hover {\n"
"    background-color: #001F39;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"")

        self.layout_search_entry.addWidget(self.search_entry)

        self.btn_search = QPushButton(self.row_search_entry)
        self.btn_search.setObjectName(u"btn_search")
        self.btn_search.setMinimumSize(QSize(124, 0))
        self.btn_search.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    padding: 6px 12px 6px 12px;\n"
"    border-radius: 2px;\n"
"    opacity: 1;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_search_entry.addWidget(self.btn_search)


        self.gridLayout_container_equipments_left.addWidget(self.row_search_entry, 1, 0, 1, 2)

        self.row_supplier_ref_entry = QWidget(self.container_equipments_left)
        self.row_supplier_ref_entry.setObjectName(u"row_supplier_ref_entry")
        self.layout_supplier_ref_entry = QHBoxLayout(self.row_supplier_ref_entry)
        self.layout_supplier_ref_entry.setSpacing(6)
        self.layout_supplier_ref_entry.setObjectName(u"layout_supplier_ref_entry")
        self.layout_supplier_ref_entry.setContentsMargins(-1, 9, 9, 9)
        self.label_supplier_ref_entry = QLabel(self.row_supplier_ref_entry)
        self.label_supplier_ref_entry.setObjectName(u"label_supplier_ref_entry")
        self.label_supplier_ref_entry.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.label_supplier_ref_entry.sizePolicy().hasHeightForWidth())
        self.label_supplier_ref_entry.setSizePolicy(sizePolicy)

        self.layout_supplier_ref_entry.addWidget(self.label_supplier_ref_entry)

        self.supplier_ref_entry = QLineEdit(self.row_supplier_ref_entry)
        self.supplier_ref_entry.setObjectName(u"supplier_ref_entry")
        sizePolicy1.setHeightForWidth(self.supplier_ref_entry.sizePolicy().hasHeightForWidth())
        self.supplier_ref_entry.setSizePolicy(sizePolicy1)
        self.supplier_ref_entry.setStyleSheet(u"\n"
"QLineEdit {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    max-height: 18px;\n"
"    padding: 5px;\n"
"    padding-bottom: 7px;\n"
"    margin-top: 0px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #B3B3BE;\n"
"    background-color: #00183B;\n"
"    color: #FFFFFF;\n"
"}\n"
"QLineEdit:hover {\n"
"    background-color: #001F39;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"")

        self.layout_supplier_ref_entry.addWidget(self.supplier_ref_entry)

        self.btn_scan_supplier_ref = QPushButton(self.row_supplier_ref_entry)
        self.btn_scan_supplier_ref.setObjectName(u"btn_scan_supplier_ref")
        self.btn_scan_supplier_ref.setMinimumSize(QSize(124, 0))
        self.btn_scan_supplier_ref.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    padding: 6px 12px 6px 12px;\n"
"    border-radius: 2px;\n"
"    opacity: 1;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_supplier_ref_entry.addWidget(self.btn_scan_supplier_ref)

        self.btn_copy_supplier_ref = QPushButton(self.row_supplier_ref_entry)
        self.btn_copy_supplier_ref.setObjectName(u"btn_copy_supplier_ref")
        self.btn_copy_supplier_ref.setMinimumSize(QSize(60, 0))
        self.btn_copy_supplier_ref.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_supplier_ref.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 60px;\n"
"    max-width: 60px;\n"
"    padding: 4px 6px;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"    font-size: 12px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_supplier_ref_entry.addWidget(self.btn_copy_supplier_ref)


        self.gridLayout_container_equipments_left.addWidget(self.row_supplier_ref_entry, 2, 0, 1, 2)

        self.equipment_image_panel = QWidget(self.container_equipments_left)
        self.equipment_image_panel.setObjectName(u"equipment_image_panel")
        self.layout_equipment_image_panel = QVBoxLayout(self.equipment_image_panel)
        self.layout_equipment_image_panel.setSpacing(6)
        self.layout_equipment_image_panel.setObjectName(u"layout_equipment_image_panel")
        self.layout_equipment_image_panel.setContentsMargins(-1, 9, 9, 9)
        self.equipment_image_preview = QLabel(self.equipment_image_panel)
        self.equipment_image_preview.setObjectName(u"equipment_image_preview")
        self.equipment_image_preview.setMinimumSize(QSize(300, 260))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.equipment_image_preview.sizePolicy().hasHeightForWidth())
        self.equipment_image_preview.setSizePolicy(sizePolicy2)
        self.equipment_image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equipment_image_preview.setStyleSheet(u"\n"
"QLabel {\n"
"    border: 1px dashed #B3B3BE;\n"
"    border-radius: 2px;\n"
"    background-color: #00183B;\n"
"    color: #B3B3BE;\n"
"    font-size: 12px;\n"
"}\n"
"")

        self.layout_equipment_image_panel.addWidget(self.equipment_image_preview)

        self.row_equipment_image_buttons = QWidget(self.equipment_image_panel)
        self.row_equipment_image_buttons.setObjectName(u"row_equipment_image_buttons")
        self.layout_equipment_image_buttons = QHBoxLayout(self.row_equipment_image_buttons)
        self.layout_equipment_image_buttons.setSpacing(6)
        self.layout_equipment_image_buttons.setObjectName(u"layout_equipment_image_buttons")
        self.layout_equipment_image_buttons.setContentsMargins(-1, 0, -1, 0)
        self.btn_set_equipment_image = QPushButton(self.row_equipment_image_buttons)
        self.btn_set_equipment_image.setObjectName(u"btn_set_equipment_image")
        self.btn_set_equipment_image.setMinimumSize(QSize(64, 0))
        self.btn_set_equipment_image.setMaximumSize(QSize(64, 16777215))
        self.btn_set_equipment_image.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 56px;\n"
"    max-width: 64px;\n"
"    padding: 4px 6px;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"    font-size: 11px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_equipment_image_buttons.addWidget(self.btn_set_equipment_image)

        self.btn_clear_equipment_image = QPushButton(self.row_equipment_image_buttons)
        self.btn_clear_equipment_image.setObjectName(u"btn_clear_equipment_image")
        self.btn_clear_equipment_image.setMinimumSize(QSize(64, 0))
        self.btn_clear_equipment_image.setMaximumSize(QSize(64, 16777215))
        self.btn_clear_equipment_image.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 56px;\n"
"    max-width: 64px;\n"
"    padding: 4px 6px;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"    font-size: 11px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_equipment_image_buttons.addWidget(self.btn_clear_equipment_image)

        self.horizontalSpacer_equipment_image = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_equipment_image_buttons.addItem(self.horizontalSpacer_equipment_image)


        self.layout_equipment_image_panel.addWidget(self.row_equipment_image_buttons)


        self.gridLayout_container_equipments_left.addWidget(self.equipment_image_panel, 3, 0, 1, 2)

        self.verticalSpacer_equipments_left = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_container_equipments_left.addItem(self.verticalSpacer_equipments_left, 4, 1, 1, 1)


        self.gridLayout_equipments.addWidget(self.container_equipments_left, 0, 0, 1, 1)

        self.container_equipments_right = QFrame(EquipmentsPage)
        self.container_equipments_right.setObjectName(u"container_equipments_right")
        self.container_equipments_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_equipments_right.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_container_equipments_right = QGridLayout(self.container_equipments_right)
        self.gridLayout_container_equipments_right.setObjectName(u"gridLayout_container_equipments_right")
        self.gridLayout_container_equipments_right.setVerticalSpacing(0)
        self.gridLayout_container_equipments_right.setContentsMargins(-1, -36, -1, -1)
        self.label_details = QLabel(self.container_equipments_right)
        self.label_details.setObjectName(u"label_details")
        self.label_details.setStyleSheet(u"\n"
"QLabel {\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"")

        self.gridLayout_container_equipments_right.addWidget(self.label_details, 0, 0, 1, 1)

        self.row_val_supplier_reference = QWidget(self.container_equipments_right)
        self.row_val_supplier_reference.setObjectName(u"row_val_supplier_reference")
        self.layout_val_supplier_reference = QHBoxLayout(self.row_val_supplier_reference)
        self.layout_val_supplier_reference.setSpacing(6)
        self.layout_val_supplier_reference.setObjectName(u"layout_val_supplier_reference")
        self.layout_val_supplier_reference.setContentsMargins(-1, 9, 9, 9)
        self.title_val_supplier_reference = QLabel(self.row_val_supplier_reference)
        self.title_val_supplier_reference.setObjectName(u"title_val_supplier_reference")
        self.title_val_supplier_reference.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.title_val_supplier_reference.sizePolicy().hasHeightForWidth())
        self.title_val_supplier_reference.setSizePolicy(sizePolicy)

        self.layout_val_supplier_reference.addWidget(self.title_val_supplier_reference)

        self.val_supplier_reference = QLabel(self.row_val_supplier_reference)
        self.val_supplier_reference.setObjectName(u"val_supplier_reference")
        self.val_supplier_reference.setStyleSheet(u"\n"
"QLabel {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    max-height: 18px;\n"
"    padding: 5px;\n"
"    padding-bottom: 7px;\n"
"    margin-top: 0px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #B3B3BE;\n"
"    background-color: #00183B;\n"
"    color: #FFFFFF;\n"
"}\n"
"QLabel:hover {\n"
"    background-color: #001F39;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"")

        self.layout_val_supplier_reference.addWidget(self.val_supplier_reference)

        self.btn_copy_val_supplier_reference = QPushButton(self.row_val_supplier_reference)
        self.btn_copy_val_supplier_reference.setObjectName(u"btn_copy_val_supplier_reference")
        self.btn_copy_val_supplier_reference.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_supplier_reference.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_supplier_reference.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 60px;\n"
"    max-width: 60px;\n"
"    padding: 4px 6px;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"    font-size: 12px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_val_supplier_reference.addWidget(self.btn_copy_val_supplier_reference)


        self.gridLayout_container_equipments_right.addWidget(self.row_val_supplier_reference, 1, 0, 1, 2)

        self.row_val_serial_number = QWidget(self.container_equipments_right)
        self.row_val_serial_number.setObjectName(u"row_val_serial_number")
        self.layout_val_serial_number = QHBoxLayout(self.row_val_serial_number)
        self.layout_val_serial_number.setSpacing(6)
        self.layout_val_serial_number.setObjectName(u"layout_val_serial_number")
        self.layout_val_serial_number.setContentsMargins(-1, 9, 9, 9)
        self.title_val_serial_number = QLabel(self.row_val_serial_number)
        self.title_val_serial_number.setObjectName(u"title_val_serial_number")
        self.title_val_serial_number.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.title_val_serial_number.sizePolicy().hasHeightForWidth())
        self.title_val_serial_number.setSizePolicy(sizePolicy)

        self.layout_val_serial_number.addWidget(self.title_val_serial_number)

        self.val_serial_number = QLabel(self.row_val_serial_number)
        self.val_serial_number.setObjectName(u"val_serial_number")
        self.val_serial_number.setStyleSheet(u"\n"
"QLabel {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    max-height: 18px;\n"
"    padding: 5px;\n"
"    padding-bottom: 7px;\n"
"    margin-top: 0px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #B3B3BE;\n"
"    background-color: #00183B;\n"
"    color: #FFFFFF;\n"
"}\n"
"QLabel:hover {\n"
"    background-color: #001F39;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"")

        self.layout_val_serial_number.addWidget(self.val_serial_number)

        self.btn_copy_val_serial_number = QPushButton(self.row_val_serial_number)
        self.btn_copy_val_serial_number.setObjectName(u"btn_copy_val_serial_number")
        self.btn_copy_val_serial_number.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_serial_number.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_serial_number.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 60px;\n"
"    max-width: 60px;\n"
"    padding: 4px 6px;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"    font-size: 12px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_val_serial_number.addWidget(self.btn_copy_val_serial_number)


        self.gridLayout_container_equipments_right.addWidget(self.row_val_serial_number, 2, 0, 1, 2)

        self.row_val_description = QWidget(self.container_equipments_right)
        self.row_val_description.setObjectName(u"row_val_description")
        self.layout_val_description = QHBoxLayout(self.row_val_description)
        self.layout_val_description.setSpacing(6)
        self.layout_val_description.setObjectName(u"layout_val_description")
        self.layout_val_description.setContentsMargins(-1, 9, 9, 9)
        self.title_val_description = QLabel(self.row_val_description)
        self.title_val_description.setObjectName(u"title_val_description")
        self.title_val_description.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.title_val_description.sizePolicy().hasHeightForWidth())
        self.title_val_description.setSizePolicy(sizePolicy)

        self.layout_val_description.addWidget(self.title_val_description)

        self.val_description = QLabel(self.row_val_description)
        self.val_description.setObjectName(u"val_description")
        self.val_description.setStyleSheet(u"\n"
"QLabel {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    max-height: 18px;\n"
"    padding: 5px;\n"
"    padding-bottom: 7px;\n"
"    margin-top: 0px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #B3B3BE;\n"
"    background-color: #00183B;\n"
"    color: #FFFFFF;\n"
"}\n"
"QLabel:hover {\n"
"    background-color: #001F39;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"")

        self.layout_val_description.addWidget(self.val_description)

        self.btn_copy_val_description = QPushButton(self.row_val_description)
        self.btn_copy_val_description.setObjectName(u"btn_copy_val_description")
        self.btn_copy_val_description.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_description.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_description.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 60px;\n"
"    max-width: 60px;\n"
"    padding: 4px 6px;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"    font-size: 12px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_val_description.addWidget(self.btn_copy_val_description)


        self.gridLayout_container_equipments_right.addWidget(self.row_val_description, 3, 0, 1, 2)

        self.row_val_calibration = QWidget(self.container_equipments_right)
        self.row_val_calibration.setObjectName(u"row_val_calibration")
        self.layout_val_calibration = QHBoxLayout(self.row_val_calibration)
        self.layout_val_calibration.setSpacing(6)
        self.layout_val_calibration.setObjectName(u"layout_val_calibration")
        self.layout_val_calibration.setContentsMargins(-1, 9, 9, 9)
        self.title_val_calibration = QLabel(self.row_val_calibration)
        self.title_val_calibration.setObjectName(u"title_val_calibration")
        self.title_val_calibration.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.title_val_calibration.sizePolicy().hasHeightForWidth())
        self.title_val_calibration.setSizePolicy(sizePolicy)

        self.layout_val_calibration.addWidget(self.title_val_calibration)

        self.val_calibration = QLabel(self.row_val_calibration)
        self.val_calibration.setObjectName(u"val_calibration")
        self.val_calibration.setStyleSheet(u"\n"
"QLabel {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    max-height: 18px;\n"
"    padding: 5px;\n"
"    padding-bottom: 7px;\n"
"    margin-top: 0px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #B3B3BE;\n"
"    background-color: #00183B;\n"
"    color: #FFFFFF;\n"
"}\n"
"QLabel:hover {\n"
"    background-color: #001F39;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"")

        self.layout_val_calibration.addWidget(self.val_calibration)

        self.btn_copy_val_calibration = QPushButton(self.row_val_calibration)
        self.btn_copy_val_calibration.setObjectName(u"btn_copy_val_calibration")
        self.btn_copy_val_calibration.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_calibration.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_calibration.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 60px;\n"
"    max-width: 60px;\n"
"    padding: 4px 6px;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"    font-size: 12px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_val_calibration.addWidget(self.btn_copy_val_calibration)


        self.gridLayout_container_equipments_right.addWidget(self.row_val_calibration, 4, 0, 1, 2)

        self.row_val_expiration = QWidget(self.container_equipments_right)
        self.row_val_expiration.setObjectName(u"row_val_expiration")
        self.layout_val_expiration = QHBoxLayout(self.row_val_expiration)
        self.layout_val_expiration.setSpacing(6)
        self.layout_val_expiration.setObjectName(u"layout_val_expiration")
        self.layout_val_expiration.setContentsMargins(-1, 9, 9, 9)
        self.title_val_expiration = QLabel(self.row_val_expiration)
        self.title_val_expiration.setObjectName(u"title_val_expiration")
        self.title_val_expiration.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.title_val_expiration.sizePolicy().hasHeightForWidth())
        self.title_val_expiration.setSizePolicy(sizePolicy)

        self.layout_val_expiration.addWidget(self.title_val_expiration)

        self.val_expiration = QLabel(self.row_val_expiration)
        self.val_expiration.setObjectName(u"val_expiration")
        self.val_expiration.setStyleSheet(u"\n"
"QLabel {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    max-height: 18px;\n"
"    padding: 5px;\n"
"    padding-bottom: 7px;\n"
"    margin-top: 0px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #B3B3BE;\n"
"    background-color: #00183B;\n"
"    color: #FFFFFF;\n"
"}\n"
"QLabel:hover {\n"
"    background-color: #001F39;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"")

        self.layout_val_expiration.addWidget(self.val_expiration)

        self.btn_copy_val_expiration = QPushButton(self.row_val_expiration)
        self.btn_copy_val_expiration.setObjectName(u"btn_copy_val_expiration")
        self.btn_copy_val_expiration.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_expiration.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_expiration.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 60px;\n"
"    max-width: 60px;\n"
"    padding: 4px 6px;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"    font-size: 12px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_val_expiration.addWidget(self.btn_copy_val_expiration)


        self.gridLayout_container_equipments_right.addWidget(self.row_val_expiration, 5, 0, 1, 2)

        self.row_val_datasheet = QWidget(self.container_equipments_right)
        self.row_val_datasheet.setObjectName(u"row_val_datasheet")
        self.layout_val_datasheet = QHBoxLayout(self.row_val_datasheet)
        self.layout_val_datasheet.setSpacing(6)
        self.layout_val_datasheet.setObjectName(u"layout_val_datasheet")
        self.layout_val_datasheet.setContentsMargins(-1, 9, 9, 9)
        self.title_val_datasheet = QLabel(self.row_val_datasheet)
        self.title_val_datasheet.setObjectName(u"title_val_datasheet")
        self.title_val_datasheet.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.title_val_datasheet.sizePolicy().hasHeightForWidth())
        self.title_val_datasheet.setSizePolicy(sizePolicy)

        self.layout_val_datasheet.addWidget(self.title_val_datasheet)

        self.val_datasheet = QLabel(self.row_val_datasheet)
        self.val_datasheet.setObjectName(u"val_datasheet")
        self.val_datasheet.setStyleSheet(u"\n"
"QLabel {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    max-height: 18px;\n"
"    padding: 5px;\n"
"    padding-bottom: 7px;\n"
"    margin-top: 0px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #B3B3BE;\n"
"    background-color: #00183B;\n"
"    color: #FFFFFF;\n"
"}\n"
"QLabel:hover {\n"
"    background-color: #001F39;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"")

        self.layout_val_datasheet.addWidget(self.val_datasheet)

        self.btn_copy_val_datasheet = QPushButton(self.row_val_datasheet)
        self.btn_copy_val_datasheet.setObjectName(u"btn_copy_val_datasheet")
        self.btn_copy_val_datasheet.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_datasheet.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_datasheet.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 60px;\n"
"    max-width: 60px;\n"
"    padding: 4px 6px;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"    font-size: 12px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_val_datasheet.addWidget(self.btn_copy_val_datasheet)


        self.gridLayout_container_equipments_right.addWidget(self.row_val_datasheet, 6, 0, 1, 2)

        self.label_support_docs = QLabel(self.container_equipments_right)
        self.label_support_docs.setObjectName(u"label_support_docs")
        self.label_support_docs.setStyleSheet(u"\n"
"QLabel {\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    padding-top: 4px;\n"
"}\n"
"")

        self.gridLayout_container_equipments_right.addWidget(self.label_support_docs, 7, 0, 1, 2)

        self.row_doc_search_entry = QWidget(self.container_equipments_right)
        self.row_doc_search_entry.setObjectName(u"row_doc_search_entry")
        self.layout_doc_search_entry = QHBoxLayout(self.row_doc_search_entry)
        self.layout_doc_search_entry.setSpacing(6)
        self.layout_doc_search_entry.setObjectName(u"layout_doc_search_entry")
        self.layout_doc_search_entry.setContentsMargins(-1, 4, 9, 4)
        self.label_doc_search_entry = QLabel(self.row_doc_search_entry)
        self.label_doc_search_entry.setObjectName(u"label_doc_search_entry")
        self.label_doc_search_entry.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.label_doc_search_entry.sizePolicy().hasHeightForWidth())
        self.label_doc_search_entry.setSizePolicy(sizePolicy)

        self.layout_doc_search_entry.addWidget(self.label_doc_search_entry)

        self.doc_search_entry = QLineEdit(self.row_doc_search_entry)
        self.doc_search_entry.setObjectName(u"doc_search_entry")
        sizePolicy1.setHeightForWidth(self.doc_search_entry.sizePolicy().hasHeightForWidth())
        self.doc_search_entry.setSizePolicy(sizePolicy1)
        self.doc_search_entry.setStyleSheet(u"\n"
"QLineEdit {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    max-height: 18px;\n"
"    padding: 5px;\n"
"    padding-bottom: 7px;\n"
"    margin-top: 0px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #B3B3BE;\n"
"    background-color: #00183B;\n"
"    color: #FFFFFF;\n"
"}\n"
"QLineEdit:hover {\n"
"    background-color: #001F39;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"")

        self.layout_doc_search_entry.addWidget(self.doc_search_entry)

        self.btn_doc_search = QPushButton(self.row_doc_search_entry)
        self.btn_doc_search.setObjectName(u"btn_doc_search")
        self.btn_doc_search.setMinimumSize(QSize(124, 0))
        self.btn_doc_search.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    padding: 6px 12px 6px 12px;\n"
"    border-radius: 2px;\n"
"    opacity: 1;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_doc_search_entry.addWidget(self.btn_doc_search)

        self.btn_doc_open = QPushButton(self.row_doc_search_entry)
        self.btn_doc_open.setObjectName(u"btn_doc_open")
        self.btn_doc_open.setMinimumSize(QSize(124, 0))
        self.btn_doc_open.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    padding: 6px 12px 6px 12px;\n"
"    border-radius: 2px;\n"
"    opacity: 1;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_doc_search_entry.addWidget(self.btn_doc_open)


        self.gridLayout_container_equipments_right.addWidget(self.row_doc_search_entry, 8, 0, 1, 2)

        self.doc_results_list = QListWidget(self.container_equipments_right)
        self.doc_results_list.setObjectName(u"doc_results_list")
        self.doc_results_list.setMinimumSize(QSize(0, 52))
        self.doc_results_list.setMaximumSize(QSize(16777215, 64))
        self.doc_results_list.setStyleSheet(u"\n"
"QListWidget {\n"
"    background-color: #00183B;\n"
"    border: 1px solid #B3B3BE;\n"
"    color: #FFFFFF;\n"
"    padding: 2px;\n"
"    font-size: 12px;\n"
"}\n"
"QListWidget::item {\n"
"    padding: 2px 4px;\n"
"    min-height: 18px;\n"
"}\n"
"QListWidget::item:selected {\n"
"    background-color: #333353;\n"
"    border: 1px solid #00FFB9;\n"
"}\n"
"QListWidget::item:hover {\n"
"    background-color: #001F39;\n"
"}\n"
"QListWidget QScrollBar:vertical {\n"
"    background-color: #00183B;\n"
"    width: 12px;\n"
"}\n"
"QListWidget QScrollBar::handle:vertical {\n"
"    background-color: #00CCCC;\n"
"    min-height: 24px;\n"
"    border-radius: 4px;\n"
"}\n"
"")

        self.gridLayout_container_equipments_right.addWidget(self.doc_results_list, 9, 0, 1, 2)

        self.row_btn_link_datasheet = QWidget(self.container_equipments_right)
        self.row_btn_link_datasheet.setObjectName(u"row_btn_link_datasheet")
        self.layout_btn_link_datasheet = QHBoxLayout(self.row_btn_link_datasheet)
        self.layout_btn_link_datasheet.setSpacing(6)
        self.layout_btn_link_datasheet.setObjectName(u"layout_btn_link_datasheet")
        self.layout_btn_link_datasheet.setContentsMargins(-1, 4, 9, 4)
        self.label_btn_link_datasheet = QLabel(self.row_btn_link_datasheet)
        self.label_btn_link_datasheet.setObjectName(u"label_btn_link_datasheet")
        self.label_btn_link_datasheet.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.label_btn_link_datasheet.sizePolicy().hasHeightForWidth())
        self.label_btn_link_datasheet.setSizePolicy(sizePolicy)

        self.layout_btn_link_datasheet.addWidget(self.label_btn_link_datasheet)

        self.btn_link_datasheet = QPushButton(self.row_btn_link_datasheet)
        self.btn_link_datasheet.setObjectName(u"btn_link_datasheet")
        self.btn_link_datasheet.setMinimumSize(QSize(124, 0))
        self.btn_link_datasheet.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    padding: 6px 12px 6px 12px;\n"
"    border-radius: 2px;\n"
"    opacity: 1;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_btn_link_datasheet.addWidget(self.btn_link_datasheet)


        self.gridLayout_container_equipments_right.addWidget(self.row_btn_link_datasheet, 10, 0, 1, 2)

        self.row_btn_open_support_docs = QWidget(self.container_equipments_right)
        self.row_btn_open_support_docs.setObjectName(u"row_btn_open_support_docs")
        self.layout_btn_open_support_docs = QHBoxLayout(self.row_btn_open_support_docs)
        self.layout_btn_open_support_docs.setSpacing(6)
        self.layout_btn_open_support_docs.setObjectName(u"layout_btn_open_support_docs")
        self.layout_btn_open_support_docs.setContentsMargins(-1, 4, 9, 4)
        self.label_btn_open_support_docs = QLabel(self.row_btn_open_support_docs)
        self.label_btn_open_support_docs.setObjectName(u"label_btn_open_support_docs")
        self.label_btn_open_support_docs.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.label_btn_open_support_docs.sizePolicy().hasHeightForWidth())
        self.label_btn_open_support_docs.setSizePolicy(sizePolicy)

        self.layout_btn_open_support_docs.addWidget(self.label_btn_open_support_docs)

        self.btn_open_support_docs = QPushButton(self.row_btn_open_support_docs)
        self.btn_open_support_docs.setObjectName(u"btn_open_support_docs")
        self.btn_open_support_docs.setMinimumSize(QSize(124, 0))
        self.btn_open_support_docs.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    padding: 6px 12px 6px 12px;\n"
"    border-radius: 2px;\n"
"    opacity: 1;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_btn_open_support_docs.addWidget(self.btn_open_support_docs)


        self.gridLayout_container_equipments_right.addWidget(self.row_btn_open_support_docs, 11, 0, 1, 2)

        self.row_btn_add_support_doc = QWidget(self.container_equipments_right)
        self.row_btn_add_support_doc.setObjectName(u"row_btn_add_support_doc")
        self.layout_btn_add_support_doc = QHBoxLayout(self.row_btn_add_support_doc)
        self.layout_btn_add_support_doc.setSpacing(6)
        self.layout_btn_add_support_doc.setObjectName(u"layout_btn_add_support_doc")
        self.layout_btn_add_support_doc.setContentsMargins(-1, 4, 9, 4)
        self.label_btn_add_support_doc = QLabel(self.row_btn_add_support_doc)
        self.label_btn_add_support_doc.setObjectName(u"label_btn_add_support_doc")
        self.label_btn_add_support_doc.setMinimumSize(QSize(74, 0))
        sizePolicy.setHeightForWidth(self.label_btn_add_support_doc.sizePolicy().hasHeightForWidth())
        self.label_btn_add_support_doc.setSizePolicy(sizePolicy)

        self.layout_btn_add_support_doc.addWidget(self.label_btn_add_support_doc)

        self.btn_add_support_doc = QPushButton(self.row_btn_add_support_doc)
        self.btn_add_support_doc.setObjectName(u"btn_add_support_doc")
        self.btn_add_support_doc.setMinimumSize(QSize(124, 0))
        self.btn_add_support_doc.setStyleSheet(u"\n"
"QPushButton {\n"
"    min-width: 100px;\n"
"    max-width: 100px;\n"
"    padding: 6px 12px 6px 12px;\n"
"    border-radius: 2px;\n"
"    opacity: 1;\n"
"    text-align: center;\n"
"    background-color: #00CCCC;\n"
"    color: #000028;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00FFB9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00E5AA;\n"
"}\n"
"")

        self.layout_btn_add_support_doc.addWidget(self.btn_add_support_doc)


        self.gridLayout_container_equipments_right.addWidget(self.row_btn_add_support_doc, 12, 0, 1, 2)

        self.verticalSpacer_equipments_right = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_container_equipments_right.addItem(self.verticalSpacer_equipments_right, 13, 1, 1, 1)


        self.gridLayout_equipments.addWidget(self.container_equipments_right, 0, 1, 1, 1)


        self.retranslateUi(EquipmentsPage)

        QMetaObject.connectSlotsByName(EquipmentsPage)
    # setupUi

    def retranslateUi(self, EquipmentsPage):
        self.label_operations.setText(QCoreApplication.translate("EquipmentsPage", u"Operations", None))
        self.label_search_entry.setText(QCoreApplication.translate("EquipmentsPage", u"Search Equipment", None))
        self.btn_search.setText(QCoreApplication.translate("EquipmentsPage", u"SEARCH", None))
        self.label_supplier_ref_entry.setText(QCoreApplication.translate("EquipmentsPage", u"Scan Barcode / Supplier Ref.", None))
        self.btn_scan_supplier_ref.setText(QCoreApplication.translate("EquipmentsPage", u"SCAN", None))
#if QT_CONFIG(tooltip)
        self.btn_copy_supplier_ref.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_supplier_ref.setText(QCoreApplication.translate("EquipmentsPage", u"Copy", None))
#if QT_CONFIG(tooltip)
        self.equipment_image_preview.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Drag and drop an image file here", None))
#endif // QT_CONFIG(tooltip)
        self.equipment_image_preview.setText(QCoreApplication.translate("EquipmentsPage", u"Drop image here", None))
#if QT_CONFIG(tooltip)
        self.btn_set_equipment_image.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Add or replace equipment image", None))
#endif // QT_CONFIG(tooltip)
        self.btn_set_equipment_image.setText(QCoreApplication.translate("EquipmentsPage", u"Add", None))
#if QT_CONFIG(tooltip)
        self.btn_clear_equipment_image.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Delete equipment image", None))
#endif // QT_CONFIG(tooltip)
        self.btn_clear_equipment_image.setText(QCoreApplication.translate("EquipmentsPage", u"Delete", None))
        self.label_details.setText(QCoreApplication.translate("EquipmentsPage", u"Equipment Details", None))
        self.title_val_supplier_reference.setText(QCoreApplication.translate("EquipmentsPage", u"Supplier Reference", None))
        self.val_supplier_reference.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_supplier_reference.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_supplier_reference.setText(QCoreApplication.translate("EquipmentsPage", u"Copy", None))
        self.title_val_serial_number.setText(QCoreApplication.translate("EquipmentsPage", u"Serial Number", None))
        self.val_serial_number.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_serial_number.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_serial_number.setText(QCoreApplication.translate("EquipmentsPage", u"Copy", None))
        self.title_val_description.setText(QCoreApplication.translate("EquipmentsPage", u"Description", None))
        self.val_description.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_description.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_description.setText(QCoreApplication.translate("EquipmentsPage", u"Copy", None))
        self.title_val_calibration.setText(QCoreApplication.translate("EquipmentsPage", u"Calibration Date", None))
        self.val_calibration.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_calibration.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_calibration.setText(QCoreApplication.translate("EquipmentsPage", u"Copy", None))
        self.title_val_expiration.setText(QCoreApplication.translate("EquipmentsPage", u"Calibration Expiration", None))
        self.val_expiration.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_expiration.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_expiration.setText(QCoreApplication.translate("EquipmentsPage", u"Copy", None))
        self.title_val_datasheet.setText(QCoreApplication.translate("EquipmentsPage", u"Datasheet", None))
        self.val_datasheet.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_datasheet.setToolTip(QCoreApplication.translate("EquipmentsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_datasheet.setText(QCoreApplication.translate("EquipmentsPage", u"Copy", None))
        self.label_support_docs.setText(QCoreApplication.translate("EquipmentsPage", u"Support Documentation", None))
        self.label_doc_search_entry.setText(QCoreApplication.translate("EquipmentsPage", u"Search doc", None))
        self.btn_doc_search.setText(QCoreApplication.translate("EquipmentsPage", u"SEARCH", None))
        self.btn_doc_open.setText(QCoreApplication.translate("EquipmentsPage", u"OPEN", None))
        self.label_btn_link_datasheet.setText(QCoreApplication.translate("EquipmentsPage", u"Link", None))
        self.btn_link_datasheet.setText(QCoreApplication.translate("EquipmentsPage", u"LINK", None))
        self.label_btn_open_support_docs.setText(QCoreApplication.translate("EquipmentsPage", u"Folder", None))
        self.btn_open_support_docs.setText(QCoreApplication.translate("EquipmentsPage", u"OPEN FOLDER", None))
        self.label_btn_add_support_doc.setText(QCoreApplication.translate("EquipmentsPage", u"Add", None))
        self.btn_add_support_doc.setText(QCoreApplication.translate("EquipmentsPage", u"ADD DOC", None))
        pass
    # retranslateUi

