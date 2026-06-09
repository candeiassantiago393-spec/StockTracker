# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_cardVTvtyU.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Card(object):
    def setupUi(self, Card):
        if not Card.objectName():
            Card.setObjectName(u"Card")
        Card.resize(590, 258)
        Card.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background: #000028;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #f3f3f0;\n"
"	font-family: \"SiemensSansPro_A_Bd\";\n"
"	font-size: 14px;\n"
"}")
        self.centralwidget = QWidget(Card)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.container_main_body = QWidget(self.centralwidget)
        self.container_main_body.setObjectName(u"container_main_body")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.container_main_body.sizePolicy().hasHeightForWidth())
        self.container_main_body.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.container_main_body)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title_frame = QFrame(self.container_main_body)
        self.title_frame.setObjectName(u"title_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.title_frame.sizePolicy().hasHeightForWidth())
        self.title_frame.setSizePolicy(sizePolicy1)
        self.title_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.title_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.title_frame)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(self.title_frame)
        self.title.setObjectName(u"title")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy2)
        self.title.setStyleSheet(u"QLabel {\n"
"	font-size: 18px;\n"
"}\n"
"")

        self.verticalLayout_7.addWidget(self.title)


        self.verticalLayout.addWidget(self.title_frame)

        self.entries_group = QFrame(self.container_main_body)
        self.entries_group.setObjectName(u"entries_group")
        sizePolicy.setHeightForWidth(self.entries_group.sizePolicy().hasHeightForWidth())
        self.entries_group.setSizePolicy(sizePolicy)
        self.entries_group.setFrameShape(QFrame.Shape.StyledPanel)
        self.entries_group.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.entries_group)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.scroll_area = QScrollArea(self.entries_group)
        self.scroll_area.setObjectName(u"scroll_area")
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName(u"scroll_widget")
        self.scroll_widget.setGeometry(QRect(0, 0, 536, 54))
        sizePolicy.setHeightForWidth(self.scroll_widget.sizePolicy().hasHeightForWidth())
        self.scroll_widget.setSizePolicy(sizePolicy)
        self.verticalLayout_9 = QVBoxLayout(self.scroll_widget)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.entries_layout = QVBoxLayout()
        self.entries_layout.setObjectName(u"entries_layout")

        self.verticalLayout_9.addLayout(self.entries_layout)

        self.scroll_area.setWidget(self.scroll_widget)

        self.verticalLayout_8.addWidget(self.scroll_area, 0, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout.addWidget(self.entries_group)


        self.verticalLayout_2.addWidget(self.container_main_body)

        Card.setCentralWidget(self.centralwidget)

        self.retranslateUi(Card)

        QMetaObject.connectSlotsByName(Card)
    # setupUi

    def retranslateUi(self, Card):
        Card.setWindowTitle(QCoreApplication.translate("Card", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("Card", u"Entry Group Title", None))
    # retranslateUi

