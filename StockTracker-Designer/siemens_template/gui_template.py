# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_templatesokHGY.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
from .resources import resources_rc

class Ui_Template(object):
    def setupUi(self, Template):
        if not Template.objectName():
            Template.setObjectName(u"Template")
        Template.setEnabled(True)
        Template.resize(1284, 720)
        icon = QIcon()
        icon.addFile(u":/siemens_logo/logos/sie-favicon_internet.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Template.setWindowIcon(icon)
        Template.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background: #000028;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #FFFFFF;\n"
"	font-family: \"SiemensSansPro_A_Bd\";\n"
"	font-size: 14px;\n"
"}\n"
"")
        self.centralwidget = QWidget(Template)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QWidget(self.centralwidget)
        self.header.setObjectName(u"header")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setStyleSheet(u"*{\n"
"	background: #333353;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(16)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.brand_identifier = QLabel(self.header)
        self.brand_identifier.setObjectName(u"brand_identifier")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.brand_identifier.sizePolicy().hasHeightForWidth())
        self.brand_identifier.setSizePolicy(sizePolicy1)
        self.brand_identifier.setPixmap(QPixmap(u":/siemens_logo/logos/Siemens Logo.png"))

        self.horizontalLayout.addWidget(self.brand_identifier)

        self.product_name = QLabel(self.header)
        self.product_name.setObjectName(u"product_name")
        self.product_name.setStyleSheet(u"*{\n"
"	font-size: 18px;\n"
"}")

        self.horizontalLayout.addWidget(self.product_name)


        self.verticalLayout.addWidget(self.header)

        self.container_main_body = QWidget(self.centralwidget)
        self.container_main_body.setObjectName(u"container_main_body")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.container_main_body.sizePolicy().hasHeightForWidth())
        self.container_main_body.setSizePolicy(sizePolicy2)
        self.gridLayout = QGridLayout(self.container_main_body)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(16, -1, -1, -1)
        self.frame_title_tab1 = QFrame(self.container_main_body)
        self.frame_title_tab1.setObjectName(u"frame_title_tab1")
        sizePolicy.setHeightForWidth(self.frame_title_tab1.sizePolicy().hasHeightForWidth())
        self.frame_title_tab1.setSizePolicy(sizePolicy)
        self.frame_title_tab1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_title_tab1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_title_tab1)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.tab1_title = QLabel(self.frame_title_tab1)
        self.tab1_title.setObjectName(u"tab1_title")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tab1_title.sizePolicy().hasHeightForWidth())
        self.tab1_title.setSizePolicy(sizePolicy3)
        self.tab1_title.setStyleSheet(u"QLabel {\n"
"	font-size: 40px;\n"
"}\n"
"")

        self.verticalLayout_7.addWidget(self.tab1_title)


        self.gridLayout.addWidget(self.frame_title_tab1, 0, 0, 1, 2)

        self.container_tab1_left = QFrame(self.container_main_body)
        self.container_tab1_left.setObjectName(u"container_tab1_left")
        self.container_tab1_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_tab1_left.setFrameShadow(QFrame.Shadow.Raised)
        self.container_tab1_left.setLineWidth(-1)
        self.gridLayout_7 = QGridLayout(self.container_tab1_left)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setVerticalSpacing(0)
        self.gridLayout_7.setContentsMargins(-1, 15, -1, -1)
        self.label = QLabel(self.container_tab1_left)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"QLabel {\n"
"	font-size: 20px;\n"
"	font-weight: bold;\n"
"}\n"
"")

        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1)

        self.widget_3 = QWidget(self.container_tab1_left)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.field_data_out = QLabel(self.widget_3)
        self.field_data_out.setObjectName(u"field_data_out")
        self.field_data_out.setStyleSheet(u"QLabel{	\n"
"	min-width: 100px;\n"
"	max-width: 100px;\n"
"	max-height: 18px;\n"
"	padding: 5px;\n"
"	padding-bottom: 7px;\n"
"	margin-top: 0px;\n"
"	border-radius: 2px;\n"
"	border: 1px solid #B3B3BE;\n"
"	background-color: #00183B;\n"
"	color: #FFFFFF;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")

        self.horizontalLayout_5.addWidget(self.field_data_out)


        self.gridLayout_7.addWidget(self.widget_3, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 414, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer_2, 5, 1, 1, 1)

        self.widget_2 = QWidget(self.container_tab1_left)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.btn_exit = QPushButton(self.widget_2)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setMinimumSize(QSize(124, 0))
        self.btn_exit.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_6.addWidget(self.btn_exit)


        self.gridLayout_7.addWidget(self.widget_2, 4, 0, 1, 2)

        self.widget = QWidget(self.container_tab1_left)
        self.widget.setObjectName(u"widget")
        self.gridLayout_5 = QGridLayout(self.widget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.selector = QComboBox(self.widget)
        self.selector.addItem("")
        self.selector.addItem("")
        self.selector.addItem("")
        self.selector.setObjectName(u"selector")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.selector.sizePolicy().hasHeightForWidth())
        self.selector.setSizePolicy(sizePolicy4)
        self.selector.setMinimumSize(QSize(172, 30))
        self.selector.setAutoFillBackground(False)
        self.selector.setStyleSheet(u"/* Base */\n"
"QComboBox{	\n"
"	padding: 5px;\n"
"	padding-left: 20px;\n"
"	padding-right: 20px;	\n"
"	min-width: 130;\n"
"	min-height: 18px;\n"
"	max-width: 130px;\n"
"	max-height: 18px;\n"
"	border-radius: 2px;\n"
"	border: 1px solid #B3B3BE;\n"
"	background-color: #00183B;\n"
"}\n"
"\n"
"/* Mouser over Selector */\n"
"QComboBox:hover{\n"
"	background-color: #001F39;\n"
"	border: 1px solid #00FFB9;\n"
"}\n"
"\n"
"/* Selection list colors */\n"
"QComboBox QAbstractItemView {\n"
"	background-color: #2D2D45;		/* background color */\n"
"	padding: 0px;\n"
"}\n"
"\n"
"/*  Mouser over selection list   */\n"
"QComboBox QAbstractItemView::item:hover {\n"
"	padding: 0px;     \n"
"	padding-left: 10px;	\n"
"}\n"
"")
        self.selector.setMaxVisibleItems(10)
        self.selector.setFrame(True)

        self.gridLayout_5.addWidget(self.selector, 1, 1, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.widget, 1, 0, 1, 2)

        self.widget_data_input = QWidget(self.container_tab1_left)
        self.widget_data_input.setObjectName(u"widget_data_input")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_data_input)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 9, 9, 9)
        self.label_5 = QLabel(self.widget_data_input)
        self.label_5.setObjectName(u"label_5")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy5)
        self.label_5.setMinimumSize(QSize(74, 0))
        self.label_5.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.field_data_in = QLineEdit(self.widget_data_input)
        self.field_data_in.setObjectName(u"field_data_in")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.field_data_in.sizePolicy().hasHeightForWidth())
        self.field_data_in.setSizePolicy(sizePolicy6)
        self.field_data_in.setStyleSheet(u"/* Base */\n"
"QLineEdit{	\n"
"	min-width: 100px;\n"
"	max-width: 100px;\n"
"	max-height: 18px;\n"
"	padding: 5px;\n"
"	padding-bottom: 7px;\n"
"	margin-top: 0px;\n"
"	border-radius: 2px;\n"
"	border: 1px solid #B3B3BE;\n"
"	background-color: #00183B;\n"
"	color: #FFFFFF;\n"
"}\n"
"\n"
"/* Mouser over Selector */\n"
"QLineEdit:hover{\n"
"	background-color: #001F39;\n"
"	border: 1px solid #00FFB9;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"")

        self.horizontalLayout_4.addWidget(self.field_data_in)

        self.btn_ok = QPushButton(self.widget_data_input)
        self.btn_ok.setObjectName(u"btn_ok")
        self.btn_ok.setMinimumSize(QSize(124, 0))
        self.btn_ok.setStyleSheet(u"QPushButton {\n"
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
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")

        self.horizontalLayout_4.addWidget(self.btn_ok)


        self.gridLayout_7.addWidget(self.widget_data_input, 2, 0, 1, 2)


        self.gridLayout.addWidget(self.container_tab1_left, 1, 0, 1, 1)

        self.container_tab1_right = QFrame(self.container_main_body)
        self.container_tab1_right.setObjectName(u"container_tab1_right")
        self.container_tab1_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_tab1_right.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.container_tab1_right)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 15, -1, -1)
        self.horizontalSpacer = QSpacerItem(828, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.gridLayout.addWidget(self.container_tab1_right, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.container_main_body)

        Template.setCentralWidget(self.centralwidget)

        self.retranslateUi(Template)

        QMetaObject.connectSlotsByName(Template)
    # setupUi

    def retranslateUi(self, Template):
        Template.setWindowTitle(QCoreApplication.translate("Template", u"Platform Test Bench", None))
        self.brand_identifier.setText("")
        self.product_name.setText(QCoreApplication.translate("Template", u"Platform Test Bench", None))
        self.tab1_title.setText(QCoreApplication.translate("Template", u"Tab 1 Title", None))
        self.label.setText(QCoreApplication.translate("Template", u"Templates", None))
        self.label_4.setText(QCoreApplication.translate("Template", u"Data output", None))
        self.field_data_out.setText("")
        self.label_3.setText(QCoreApplication.translate("Template", u"Button", None))
        self.btn_exit.setText(QCoreApplication.translate("Template", u"Exit", None))
        self.selector.setItemText(0, QCoreApplication.translate("Template", u"Option 1", None))
        self.selector.setItemText(1, QCoreApplication.translate("Template", u"Option 2", None))
        self.selector.setItemText(2, QCoreApplication.translate("Template", u"Option 3", None))

        self.selector.setPlaceholderText(QCoreApplication.translate("Template", u"Select ...", None))
        self.label_2.setText(QCoreApplication.translate("Template", u"Selector", None))
        self.label_5.setText(QCoreApplication.translate("Template", u"Data input", None))
        self.btn_ok.setText(QCoreApplication.translate("Template", u"Ok", None))
    # retranslateUi

