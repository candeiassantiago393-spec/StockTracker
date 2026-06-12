# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_popup_edit.ui'
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

class Ui_PopupEdit(object):
    def setupUi(self, PopupEdit):
        if not PopupEdit.objectName():
            PopupEdit.setObjectName(u"PopupEdit")
        PopupEdit.resize(641, 480)
        PopupEdit.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background: #000028;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #f3f3f0;\n"
"	font-family: \"SiemensSansPro_A_Bd\";\n"
"	font-size: 14px;\n"
"}\n"
"")
        self.gridLayout = QGridLayout(PopupEdit)
        self.gridLayout.setObjectName(u"gridLayout")
        self.container_main_body = QWidget(PopupEdit)
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
        self.form_edit = QFormLayout(self.body_form)
        self.form_edit.setSpacing(6)
        self.form_edit.setObjectName(u"form_edit")
        self.label_Supplier_Reference = QLabel(self.body_form)
        self.label_Supplier_Reference.setObjectName(u"label_Supplier_Reference")

        self.form_edit.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_Supplier_Reference)

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

        self.form_edit.setWidget(0, QFormLayout.ItemRole.FieldRole, self.supplier_reference)

        self.label_Manufacturer = QLabel(self.body_form)
        self.label_Manufacturer.setObjectName(u"label_Manufacturer")

        self.form_edit.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_Manufacturer)

        self.manufacturer = QLineEdit(self.body_form)
        self.manufacturer.setObjectName(u"manufacturer")
        self.manufacturer.setStyleSheet(u"\n"
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

        self.form_edit.setWidget(1, QFormLayout.ItemRole.FieldRole, self.manufacturer)

        self.label_Manufacturer_Reference = QLabel(self.body_form)
        self.label_Manufacturer_Reference.setObjectName(u"label_Manufacturer_Reference")

        self.form_edit.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_Manufacturer_Reference)

        self.manufacturer_reference = QLineEdit(self.body_form)
        self.manufacturer_reference.setObjectName(u"manufacturer_reference")
        self.manufacturer_reference.setStyleSheet(u"\n"
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

        self.form_edit.setWidget(2, QFormLayout.ItemRole.FieldRole, self.manufacturer_reference)

        self.label_Description = QLabel(self.body_form)
        self.label_Description.setObjectName(u"label_Description")

        self.form_edit.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_Description)

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

        self.form_edit.setWidget(3, QFormLayout.ItemRole.FieldRole, self.description_field)

        self.label_Current_Stock = QLabel(self.body_form)
        self.label_Current_Stock.setObjectName(u"label_Current_Stock")

        self.form_edit.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_Current_Stock)

        self.label_current_stock = QLabel(self.body_form)
        self.label_current_stock.setObjectName(u"label_current_stock")
        self.label_current_stock.setStyleSheet(u"\n"
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

        self.form_edit.setWidget(4, QFormLayout.ItemRole.FieldRole, self.label_current_stock)


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


        self.retranslateUi(PopupEdit)

        QMetaObject.connectSlotsByName(PopupEdit)
    # setupUi

    def retranslateUi(self, PopupEdit):
        PopupEdit.setWindowTitle(QCoreApplication.translate("PopupEdit", u"Dialog", None))
        self.tittle.setText(QCoreApplication.translate("PopupEdit", u"Edit Component", None))
        self.description.setText(QCoreApplication.translate("PopupEdit", u"Update component data. Use ADD/REMOVE STOCK to change quantity.", None))
        self.label_Supplier_Reference.setText(QCoreApplication.translate("PopupEdit", u"Supplier Reference", None))
        self.label_Manufacturer.setText(QCoreApplication.translate("PopupEdit", u"Manufacturer", None))
        self.label_Manufacturer_Reference.setText(QCoreApplication.translate("PopupEdit", u"Manufacturer Reference", None))
        self.label_Description.setText(QCoreApplication.translate("PopupEdit", u"Description", None))
        self.label_Current_Stock.setText(QCoreApplication.translate("PopupEdit", u"Current Stock", None))
        self.label_current_stock.setText(QCoreApplication.translate("PopupEdit", u"0", None))
        self.btn_ok.setText(QCoreApplication.translate("PopupEdit", u"Save", None))
        self.btn_cancel.setText(QCoreApplication.translate("PopupEdit", u"Cancel", None))
    # retranslateUi

