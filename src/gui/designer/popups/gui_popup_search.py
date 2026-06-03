# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_popup_search.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_PopupSearch(object):
    def setupUi(self, PopupSearch):
        if not PopupSearch.objectName():
            PopupSearch.setObjectName(u"PopupSearch")
        PopupSearch.resize(900, 480)
        PopupSearch.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background: #000028;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #f3f3f0;\n"
"	font-family: \"SiemensSansPro_A_Bd\";\n"
"	font-size: 14px;\n"
"}\n"
"")
        self.gridLayout = QGridLayout(PopupSearch)
        self.gridLayout.setObjectName(u"gridLayout")
        self.container_main_body = QWidget(PopupSearch)
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

        self.table_search = QTableWidget(self.container_main_body)
        if (self.table_search.columnCount() < 5):
            self.table_search.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.table_search.setObjectName(u"table_search")
        self.table_search.setMinimumSize(QSize(0, 280))
        self.table_search.setStyleSheet(u"\n"
"QTableWidget {\n"
"    background-color: #00183B;\n"
"    gridline-color: #333353;\n"
"    border: 1px solid #B3B3BE;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #333353;\n"
"    color: #FFFFFF;\n"
"    padding: 6px;\n"
"    border: 1px solid #B3B3BE;\n"
"    font-weight: bold;\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.table_search)

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


        self.retranslateUi(PopupSearch)

        QMetaObject.connectSlotsByName(PopupSearch)
    # setupUi

    def retranslateUi(self, PopupSearch):
        PopupSearch.setWindowTitle(QCoreApplication.translate("PopupSearch", u"Dialog", None))
        self.tittle.setText(QCoreApplication.translate("PopupSearch", u"Search results", None))
        self.description.setText(QCoreApplication.translate("PopupSearch", u"Select a row and press Ok, or double-click a row.", None))
        ___qtablewidgetitem = self.table_search.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PopupSearch", u"Supplier Reference", None))
        ___qtablewidgetitem1 = self.table_search.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PopupSearch", u"Manufacturer", None))
        ___qtablewidgetitem2 = self.table_search.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PopupSearch", u"Manufacturer Reference", None))
        ___qtablewidgetitem3 = self.table_search.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PopupSearch", u"Description", None))
        ___qtablewidgetitem4 = self.table_search.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PopupSearch", u"Stock", None))
        self.btn_ok.setText(QCoreApplication.translate("PopupSearch", u"Ok", None))
        self.btn_cancel.setText(QCoreApplication.translate("PopupSearch", u"Cancel", None))
    # retranslateUi

