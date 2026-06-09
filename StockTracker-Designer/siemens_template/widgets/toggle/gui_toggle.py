# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_togglelueLQs.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_Toggle(object):
    def setupUi(self, Toggle):
        if not Toggle.objectName():
            Toggle.setObjectName(u"Toggle")
        Toggle.resize(232, 42)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Toggle.sizePolicy().hasHeightForWidth())
        Toggle.setSizePolicy(sizePolicy)
        Toggle.setMinimumSize(QSize(232, 42))
        Toggle.setMaximumSize(QSize(232, 42))
        Toggle.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background: #000028;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #f3f3f0;\n"
"	font-family: \"SiemensSansPro_A_Bd\";\n"
"	font-size: 14px;\n"
"}\n"
"\n"
"QPushButton {\n"
"	min-width: 48px;\n"
"	min-height: 24px;\n"
"	max-width: 48px;\n"
"	max-height: 24px;\n"
"    border-radius: 12px;    	\n"
"	background-color: #737389;		\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #9999A9;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: #00FFB9;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.centralwidget = QWidget(Toggle)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(232)
        sizePolicy1.setVerticalStretch(42)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMaximumSize(QSize(232, 42))
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(232, 42))
        self.widget.setMaximumSize(QSize(232, 42))
        self.widget.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMinimumSize(QSize(160, 0))
        self.label.setMaximumSize(QSize(160, 48))
        palette = QPalette()
        brush = QBrush(QColor(243, 243, 240, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 40, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        brush2 = QBrush(QColor(243, 243, 240, 128))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        self.label.setPalette(palette)
        self.label.setStyleSheet(u"/* Base */\n"
"QLabel{	\n"
"	min-width: 160px;\n"
"	max-width: 160px;	\n"
"	qproperty-alignment: AlignRight;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_2.addWidget(self.label, 0, Qt.AlignmentFlag.AlignVCenter)

        self.toggle_btn = QPushButton(self.widget)
        self.toggle_btn.setObjectName(u"toggle_btn")
        self.toggle_btn.setEnabled(True)
        sizePolicy.setHeightForWidth(self.toggle_btn.sizePolicy().hasHeightForWidth())
        self.toggle_btn.setSizePolicy(sizePolicy)
        self.toggle_btn.setMinimumSize(QSize(48, 24))
        self.toggle_btn.setMaximumSize(QSize(48, 24))

        self.horizontalLayout_2.addWidget(self.toggle_btn)


        self.horizontalLayout.addWidget(self.widget)

        Toggle.setCentralWidget(self.centralwidget)

        self.retranslateUi(Toggle)

        QMetaObject.connectSlotsByName(Toggle)
    # setupUi

    def retranslateUi(self, Toggle):
        Toggle.setWindowTitle(QCoreApplication.translate("Toggle", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("Toggle", u"Label", None))
        self.toggle_btn.setText("")
    # retranslateUi

