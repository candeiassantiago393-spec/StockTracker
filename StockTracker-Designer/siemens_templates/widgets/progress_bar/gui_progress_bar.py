# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_progress_barfSfuAi.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QSizePolicy, QVBoxLayout,
    QWidget)
from ..resources import resources_rc

class Ui_ProgressBar(object):
    def setupUi(self, ProgressBar):
        if not ProgressBar.objectName():
            ProgressBar.setObjectName(u"ProgressBar")
        ProgressBar.resize(269, 240)
        icon = QIcon()
        icon.addFile(u":/siemens_logo/logos/sie-favicon_internet.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ProgressBar.setWindowIcon(icon)
        ProgressBar.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background: #000028;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #f3f3f0;\n"
"	font-family: \"SiemensSansPro_A_Bd\";\n"
"	font-size: 14px;\n"
"}\n"
"")
        self.centralwidget = QWidget(ProgressBar)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(0, 240))
        self.centralwidget.setMaximumSize(QSize(16777215, 100))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.container_tab1_right = QFrame(self.centralwidget)
        self.container_tab1_right.setObjectName(u"container_tab1_right")
        self.container_tab1_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_tab1_right.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.container_tab1_right)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, 0, -1)
        self.widget_progress = QWidget(self.container_tab1_right)
        self.widget_progress.setObjectName(u"widget_progress")
        sizePolicy.setHeightForWidth(self.widget_progress.sizePolicy().hasHeightForWidth())
        self.widget_progress.setSizePolicy(sizePolicy)
        self.widget_progress.setMinimumSize(QSize(0, 260))
        self.widget_progress.setMaximumSize(QSize(16777215, 250))
        self.widget_progress.setStyleSheet(u"background-color: none;")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_progress)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.circular_progressbar = QFrame(self.widget_progress)
        self.circular_progressbar.setObjectName(u"circular_progressbar")
        self.circular_progressbar.setStyleSheet(u"background-color: none;")
        self.circular_progressbar.setFrameShape(QFrame.Shape.NoFrame)
        self.circular_progressbar.setFrameShadow(QFrame.Shadow.Raised)
        self.circular_progress = QFrame(self.circular_progressbar)
        self.circular_progress.setObjectName(u"circular_progress")
        self.circular_progress.setGeometry(QRect(10, 10, 220, 220))
        self.circular_progress.setStyleSheet(u"QFrame{\n"
"	border-radius: 110px;	\n"
"	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:1.0 #009999, stop:0.995 #19193d);\n"
"}")
        self.circular_progress.setFrameShape(QFrame.Shape.StyledPanel)
        self.circular_progress.setFrameShadow(QFrame.Shadow.Raised)
        self.circular_bg = QFrame(self.circular_progressbar)
        self.circular_bg.setObjectName(u"circular_bg")
        self.circular_bg.setGeometry(QRect(10, 10, 220, 220))
        self.circular_bg.setStyleSheet(u"QFrame{\n"
"	border-radius: 110px;	\n"
"	background-color: #4c4c68;\n"
"}")
        self.circular_bg.setFrameShape(QFrame.Shape.StyledPanel)
        self.circular_bg.setFrameShadow(QFrame.Shadow.Raised)
        self.circular_container = QFrame(self.circular_progressbar)
        self.circular_container.setObjectName(u"circular_container")
        self.circular_container.setGeometry(QRect(25, 25, 190, 190))
        self.circular_container.setBaseSize(QSize(0, 0))
        self.circular_container.setStyleSheet(u"QFrame{\n"
"	border-radius: 95px;	\n"
"	background-color: #333353;\n"
"}")
        self.circular_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.circular_container.setFrameShadow(QFrame.Shadow.Raised)
        self.layoutWidget_4 = QWidget(self.circular_container)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(0, 30, 203, 129))
        self.info_layout = QGridLayout(self.layoutWidget_4)
        self.info_layout.setObjectName(u"info_layout")
        self.info_layout.setContentsMargins(0, 0, 0, 0)
        self.label_percentage = QLabel(self.layoutWidget_4)
        self.label_percentage.setObjectName(u"label_percentage")
        font = QFont()
        font.setFamilies([u"SiemensSansPro_A_Bd"])
        self.label_percentage.setFont(font)
        self.label_percentage.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background: None;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #009999;\n"
"	font-family: \"SiemensSansPro_A_Bd\";\n"
"	font-size: 14px;\n"
"}")
        self.label_percentage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_percentage.setIndent(-1)

        self.info_layout.addWidget(self.label_percentage, 1, 1, 1, 1)

        self.circular_bg.raise_()
        self.circular_progress.raise_()
        self.circular_container.raise_()

        self.horizontalLayout_5.addWidget(self.circular_progressbar)


        self.verticalLayout_3.addWidget(self.widget_progress)


        self.gridLayout.addWidget(self.container_tab1_right, 0, 0, 1, 1)

        ProgressBar.setCentralWidget(self.centralwidget)

        self.retranslateUi(ProgressBar)

        QMetaObject.connectSlotsByName(ProgressBar)
    # setupUi

    def retranslateUi(self, ProgressBar):
        ProgressBar.setWindowTitle(QCoreApplication.translate("ProgressBar", u"Platform Test Bench", None))
        self.label_percentage.setText(QCoreApplication.translate("ProgressBar", u"<html><head/><body><p align=\"center\"><span style=\" font-size:50pt;\">0</span><span style=\" font-size:40pt; vertical-align:super;\">%</span></p></body></html>", None))
    # retranslateUi

