# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_popup_material.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_PopupMaterial(object):
    def setupUi(self, PopupMaterial):
        if not PopupMaterial.objectName():
            PopupMaterial.setObjectName(u"PopupMaterial")
        PopupMaterial.resize(641, 520)
        PopupMaterial.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background: #000028;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #f3f3f0;\n"
"	font-family: \"SiemensSansPro_A_Bd\";\n"
"	font-size: 14px;\n"
"}\n"
"")
        self.gridLayout = QGridLayout(PopupMaterial)
        self.gridLayout.setObjectName(u"gridLayout")
        self.container_main_body = QWidget(PopupMaterial)
        self.container_main_body.setObjectName(u"container_main_body")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.container_main_body.sizePolicy().hasHeightForWidth())
        self.container_main_body.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.container_main_body)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_title = QFrame(self.container_main_body)
        self.frame_title.setObjectName(u"frame_title")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_title.sizePolicy().hasHeightForWidth())
        self.frame_title.setSizePolicy(sizePolicy1)
        self.frame_title.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_title)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.tittle = QLabel(self.frame_title)
        self.tittle.setObjectName(u"tittle")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tittle.sizePolicy().hasHeightForWidth())
        self.tittle.setSizePolicy(sizePolicy2)
        self.tittle.setStyleSheet(u"QLabel {\n"
"	color: #009999;\n"
"	font-size: 30px;\n"
"	font-weight: bold;\n"
"}\n"
"")

        self.verticalLayout_12.addWidget(self.tittle)


        self.verticalLayout.addWidget(self.frame_title)

        self.widget = QWidget(self.container_main_body)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 20, -1, -1)
        self.description = QLabel(self.widget)
        self.description.setObjectName(u"description")
        self.description.setMinimumSize(QSize(0, 100))
        self.description.setStyleSheet(u"background-color: #333353;\n"
"border-radius: 2px;\n"
"padding: 5px;\n"
"padding-bottom: 7px;\n"
"margin-top: 0px;\n"
"color: #f3f3f0;\n"
"border: 1px solid #009999;")

        self.horizontalLayout_2.addWidget(self.description)


        self.verticalLayout.addWidget(self.widget)

        self.body_form = QWidget(self.container_main_body)
        self.body_form.setObjectName(u"body_form")
        self.form_material = QFormLayout(self.body_form)
        self.form_material.setSpacing(6)
        self.form_material.setObjectName(u"form_material")
        self.label_Supplier_Reference = QLabel(self.body_form)
        self.label_Supplier_Reference.setObjectName(u"label_Supplier_Reference")

        self.form_material.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_Supplier_Reference)

        self.supplier_reference = QLineEdit(self.body_form)
        self.supplier_reference.setObjectName(u"supplier_reference")
        self.supplier_reference.setStyleSheet(u"\n"
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

        self.form_material.setWidget(0, QFormLayout.ItemRole.FieldRole, self.supplier_reference)

        self.label_Serial_Number = QLabel(self.body_form)
        self.label_Serial_Number.setObjectName(u"label_Serial_Number")

        self.form_material.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_Serial_Number)

        self.serial_number = QLineEdit(self.body_form)
        self.serial_number.setObjectName(u"serial_number")
        self.serial_number.setStyleSheet(u"\n"
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

        self.form_material.setWidget(1, QFormLayout.ItemRole.FieldRole, self.serial_number)

        self.label_Description = QLabel(self.body_form)
        self.label_Description.setObjectName(u"label_Description")

        self.form_material.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_Description)

        self.description_field = QLineEdit(self.body_form)
        self.description_field.setObjectName(u"description_field")
        self.description_field.setStyleSheet(u"\n"
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

        self.form_material.setWidget(2, QFormLayout.ItemRole.FieldRole, self.description_field)

        self.label_Calibration_Date = QLabel(self.body_form)
        self.label_Calibration_Date.setObjectName(u"label_Calibration_Date")

        self.form_material.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_Calibration_Date)

        self.calibration_date = QLineEdit(self.body_form)
        self.calibration_date.setObjectName(u"calibration_date")
        self.calibration_date.setStyleSheet(u"\n"
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

        self.form_material.setWidget(3, QFormLayout.ItemRole.FieldRole, self.calibration_date)

        self.label_Calibration_Expiration = QLabel(self.body_form)
        self.label_Calibration_Expiration.setObjectName(u"label_Calibration_Expiration")

        self.form_material.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_Calibration_Expiration)

        self.calibration_expiration = QLineEdit(self.body_form)
        self.calibration_expiration.setObjectName(u"calibration_expiration")
        self.calibration_expiration.setStyleSheet(u"\n"
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

        self.form_material.setWidget(4, QFormLayout.ItemRole.FieldRole, self.calibration_expiration)


        self.verticalLayout.addWidget(self.body_form)

        self.container_button = QWidget(self.container_main_body)
        self.container_button.setObjectName(u"container_button")
        sizePolicy1.setHeightForWidth(self.container_button.sizePolicy().hasHeightForWidth())
        self.container_button.setSizePolicy(sizePolicy1)
        self.container_button.setStyleSheet(u"QPushButton {\n"
"	min-width: 100px;\n"
"	max-width: 100px;\n"
"    padding: 6px 12px 6px 12px;\n"
"    border-radius: 2px;\n"
"    opacity: 1;\n"
"	text-align:center;\n"
"	background-color: #00CCCC;	\n"
"	color: #000028;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #00FFB9;\n"
"}\n"
"\n"
"QPushButton:pressed {	\n"
"	background-color: #00E5AA;\n"
"}")
        self.horizontalLayout_4 = QHBoxLayout(self.container_button)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 40)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.btn_ok = QPushButton(self.container_button)
        self.btn_ok.setObjectName(u"btn_ok")
        self.btn_ok.setMinimumSize(QSize(124, 0))

        self.horizontalLayout_4.addWidget(self.btn_ok)

        self.btn_cancel = QPushButton(self.container_button)
        self.btn_cancel.setObjectName(u"btn_cancel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_cancel.sizePolicy().hasHeightForWidth())
        self.btn_cancel.setSizePolicy(sizePolicy3)
        self.btn_cancel.setMinimumSize(QSize(124, 0))

        self.horizontalLayout_4.addWidget(self.btn_cancel)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addWidget(self.container_button)


        self.gridLayout.addWidget(self.container_main_body, 0, 0, 1, 1)


        self.retranslateUi(PopupMaterial)

        QMetaObject.connectSlotsByName(PopupMaterial)
    # setupUi

    def retranslateUi(self, PopupMaterial):
        PopupMaterial.setWindowTitle(QCoreApplication.translate("PopupMaterial", u"Dialog", None))
        self.tittle.setText(QCoreApplication.translate("PopupMaterial", u"Material", None))
        self.description.setText(QCoreApplication.translate("PopupMaterial", u"Provide Supplier Reference, Serial Number or Description.", None))
        self.label_Supplier_Reference.setText(QCoreApplication.translate("PopupMaterial", u"Supplier Reference", None))
        self.label_Serial_Number.setText(QCoreApplication.translate("PopupMaterial", u"Serial Number", None))
        self.label_Description.setText(QCoreApplication.translate("PopupMaterial", u"Description", None))
        self.label_Calibration_Date.setText(QCoreApplication.translate("PopupMaterial", u"Calibration Date", None))
        self.label_Calibration_Expiration.setText(QCoreApplication.translate("PopupMaterial", u"Calibration Expiration", None))
        self.btn_ok.setText(QCoreApplication.translate("PopupMaterial", u"Save", None))
        self.btn_cancel.setText(QCoreApplication.translate("PopupMaterial", u"Cancel", None))
    # retranslateUi

