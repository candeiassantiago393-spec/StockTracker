# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_materials.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_MaterialsPage(object):
    def setupUi(self, MaterialsPage):
        if not MaterialsPage.objectName():
            MaterialsPage.setObjectName(u"MaterialsPage")
        MaterialsPage.resize(1284, 520)
        MaterialsPage.setStyleSheet(u"\n"
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
        self.gridLayout_materials = QGridLayout(MaterialsPage)
        self.gridLayout_materials.setObjectName(u"gridLayout_materials")
        self.gridLayout_materials.setHorizontalSpacing(0)
        self.gridLayout_materials.setProperty(u"columnStretch", 1)
        self.gridLayout_materials.setContentsMargins(16, -1, 16, -1)
        self.container_materials_left = QFrame(MaterialsPage)
        self.container_materials_left.setObjectName(u"container_materials_left")
        self.container_materials_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_materials_left.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_container_materials_left = QGridLayout(self.container_materials_left)
        self.gridLayout_container_materials_left.setObjectName(u"gridLayout_container_materials_left")
        self.gridLayout_container_materials_left.setVerticalSpacing(0)
        self.gridLayout_container_materials_left.setContentsMargins(-1, 15, -1, -1)
        self.label_operations = QLabel(self.container_materials_left)
        self.label_operations.setObjectName(u"label_operations")
        self.label_operations.setStyleSheet(u"\n"
"QLabel {\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"")

        self.gridLayout_container_materials_left.addWidget(self.label_operations, 0, 0, 1, 2)

        self.row_search_entry = QWidget(self.container_materials_left)
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


        self.gridLayout_container_materials_left.addWidget(self.row_search_entry, 1, 0, 1, 2)

        self.row_supplier_ref_entry = QWidget(self.container_materials_left)
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


        self.gridLayout_container_materials_left.addWidget(self.row_supplier_ref_entry, 2, 0, 1, 2)

        self.verticalSpacer_materials_left = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_container_materials_left.addItem(self.verticalSpacer_materials_left, 3, 1, 1, 1)


        self.gridLayout_materials.addWidget(self.container_materials_left, 0, 0, 1, 1)

        self.container_materials_right = QFrame(MaterialsPage)
        self.container_materials_right.setObjectName(u"container_materials_right")
        self.container_materials_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_materials_right.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_container_materials_right = QGridLayout(self.container_materials_right)
        self.gridLayout_container_materials_right.setObjectName(u"gridLayout_container_materials_right")
        self.gridLayout_container_materials_right.setVerticalSpacing(0)
        self.gridLayout_container_materials_right.setContentsMargins(-1, 15, -1, -1)
        self.label_details = QLabel(self.container_materials_right)
        self.label_details.setObjectName(u"label_details")
        self.label_details.setStyleSheet(u"\n"
"QLabel {\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"")

        self.gridLayout_container_materials_right.addWidget(self.label_details, 0, 0, 1, 1)

        self.row_val_supplier_reference = QWidget(self.container_materials_right)
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


        self.gridLayout_container_materials_right.addWidget(self.row_val_supplier_reference, 1, 0, 1, 2)

        self.row_val_serial_number = QWidget(self.container_materials_right)
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


        self.gridLayout_container_materials_right.addWidget(self.row_val_serial_number, 2, 0, 1, 2)

        self.row_val_description = QWidget(self.container_materials_right)
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


        self.gridLayout_container_materials_right.addWidget(self.row_val_description, 3, 0, 1, 2)

        self.row_val_calibration = QWidget(self.container_materials_right)
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


        self.gridLayout_container_materials_right.addWidget(self.row_val_calibration, 4, 0, 1, 2)

        self.row_val_expiration = QWidget(self.container_materials_right)
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


        self.gridLayout_container_materials_right.addWidget(self.row_val_expiration, 5, 0, 1, 2)

        self.verticalSpacer_materials_right = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_container_materials_right.addItem(self.verticalSpacer_materials_right, 6, 1, 1, 1)


        self.gridLayout_materials.addWidget(self.container_materials_right, 0, 1, 1, 1)


        self.retranslateUi(MaterialsPage)

        QMetaObject.connectSlotsByName(MaterialsPage)
    # setupUi

    def retranslateUi(self, MaterialsPage):
        self.label_operations.setText(QCoreApplication.translate("MaterialsPage", u"Operations", None))
        self.label_search_entry.setText(QCoreApplication.translate("MaterialsPage", u"Search Material", None))
        self.btn_search.setText(QCoreApplication.translate("MaterialsPage", u"SEARCH", None))
        self.label_supplier_ref_entry.setText(QCoreApplication.translate("MaterialsPage", u"Scan Barcode / Supplier Ref.", None))
#if QT_CONFIG(tooltip)
        self.btn_copy_supplier_ref.setToolTip(QCoreApplication.translate("MaterialsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_supplier_ref.setText(QCoreApplication.translate("MaterialsPage", u"Copy", None))
        self.label_details.setText(QCoreApplication.translate("MaterialsPage", u"Material Details", None))
        self.title_val_supplier_reference.setText(QCoreApplication.translate("MaterialsPage", u"Supplier Reference", None))
        self.val_supplier_reference.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_supplier_reference.setToolTip(QCoreApplication.translate("MaterialsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_supplier_reference.setText(QCoreApplication.translate("MaterialsPage", u"Copy", None))
        self.title_val_serial_number.setText(QCoreApplication.translate("MaterialsPage", u"Serial Number", None))
        self.val_serial_number.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_serial_number.setToolTip(QCoreApplication.translate("MaterialsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_serial_number.setText(QCoreApplication.translate("MaterialsPage", u"Copy", None))
        self.title_val_description.setText(QCoreApplication.translate("MaterialsPage", u"Description", None))
        self.val_description.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_description.setToolTip(QCoreApplication.translate("MaterialsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_description.setText(QCoreApplication.translate("MaterialsPage", u"Copy", None))
        self.title_val_calibration.setText(QCoreApplication.translate("MaterialsPage", u"Calibration Date", None))
        self.val_calibration.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_calibration.setToolTip(QCoreApplication.translate("MaterialsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_calibration.setText(QCoreApplication.translate("MaterialsPage", u"Copy", None))
        self.title_val_expiration.setText(QCoreApplication.translate("MaterialsPage", u"Calibration Expiration", None))
        self.val_expiration.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_expiration.setToolTip(QCoreApplication.translate("MaterialsPage", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_expiration.setText(QCoreApplication.translate("MaterialsPage", u"Copy", None))
        pass
    # retranslateUi

