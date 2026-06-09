# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_popup_template.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Popup(object):
    def setupUi(self, Popup):
        if not Popup.objectName():
            Popup.setObjectName(u"Popup")
        Popup.resize(641, 283)
        Popup.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background: #000028;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #f3f3f0;\n"
"	font-family: \"SiemensSansPro_A_Bd\";\n"
"	font-size: 14px;\n"
"}\n"
"")
        self.gridLayout = QGridLayout(Popup)
        self.gridLayout.setObjectName(u"gridLayout")
        self.container_main_body = QWidget(Popup)
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


        self.retranslateUi(Popup)

        QMetaObject.connectSlotsByName(Popup)
    # setupUi

    def retranslateUi(self, Popup):
        Popup.setWindowTitle(QCoreApplication.translate("Popup", u"Dialog", None))
        self.tittle.setText(QCoreApplication.translate("Popup", u"Popup Title", None))
        self.description.setText(QCoreApplication.translate("Popup", u"Popup description", None))
        self.btn_ok.setText(QCoreApplication.translate("Popup", u"Ok", None))
        self.btn_cancel.setText(QCoreApplication.translate("Popup", u"Cancel", None))
    # retranslateUi

