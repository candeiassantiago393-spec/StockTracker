# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_stocktracker.ui'
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
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from src.gui.siemens_template.resources import resources_rc

class Ui_StockTracker(object):
    def setupUi(self, StockTracker):
        if not StockTracker.objectName():
            StockTracker.setObjectName(u"StockTracker")
        StockTracker.resize(1284, 720)
        icon = QIcon()
        icon.addFile(u":/siemens_logo/logos/sie-favicon_internet.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        StockTracker.setWindowIcon(icon)
        StockTracker.setStyleSheet(u"\n"
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
        self.centralwidget = QWidget(StockTracker)
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
        self.header.setStyleSheet(u"\n"
"* {\n"
"    background: #333353;\n"
"}\n"
"")
        self.horizontalLayout_header = QHBoxLayout(self.header)
        self.horizontalLayout_header.setSpacing(16)
        self.horizontalLayout_header.setObjectName(u"horizontalLayout_header")
        self.horizontalLayout_header.setContentsMargins(16, -1, 16, -1)
        self.brand_identifier = QLabel(self.header)
        self.brand_identifier.setObjectName(u"brand_identifier")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.brand_identifier.sizePolicy().hasHeightForWidth())
        self.brand_identifier.setSizePolicy(sizePolicy1)
        self.brand_identifier.setPixmap(QPixmap(u":/siemens_logo/logos/Siemens Logo.png"))

        self.horizontalLayout_header.addWidget(self.brand_identifier)

        self.product_name = QLabel(self.header)
        self.product_name.setObjectName(u"product_name")
        self.product_name.setStyleSheet(u"\n"
"* {\n"
"    font-size: 18px;\n"
"}\n"
"")

        self.horizontalLayout_header.addWidget(self.product_name)


        self.verticalLayout.addWidget(self.header)

        self.container_main_body = QWidget(self.centralwidget)
        self.container_main_body.setObjectName(u"container_main_body")
        self.gridLayout_main = QGridLayout(self.container_main_body)
        self.gridLayout_main.setObjectName(u"gridLayout_main")
        self.gridLayout_main.setHorizontalSpacing(0)
        self.gridLayout_main.setProperty(u"columnStretch", 1)
        self.gridLayout_main.setContentsMargins(16, 0, 16, -1)
        self.frame_title = QFrame(self.container_main_body)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_title = QVBoxLayout(self.frame_title)
        self.verticalLayout_title.setSpacing(0)
        self.verticalLayout_title.setObjectName(u"verticalLayout_title")
        self.verticalLayout_title.setContentsMargins(0, 0, 0, 0)
        self.tab1_title = QLabel(self.frame_title)
        self.tab1_title.setObjectName(u"tab1_title")
        self.tab1_title.setStyleSheet(u"\n"
"QLabel {\n"
"    font-size: 40px;\n"
"}\n"
"")

        self.verticalLayout_title.addWidget(self.tab1_title)


        self.gridLayout_main.addWidget(self.frame_title, 0, 0, 1, 2)

        self.container_tab1_left = QFrame(self.container_main_body)
        self.container_tab1_left.setObjectName(u"container_tab1_left")
        self.container_tab1_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_tab1_left.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_left = QGridLayout(self.container_tab1_left)
        self.gridLayout_left.setObjectName(u"gridLayout_left")
        self.gridLayout_left.setVerticalSpacing(0)
        self.gridLayout_left.setContentsMargins(-1, 15, -1, -1)
        self.label_operations = QLabel(self.container_tab1_left)
        self.label_operations.setObjectName(u"label_operations")
        self.label_operations.setStyleSheet(u"\n"
"QLabel {\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"")

        self.gridLayout_left.addWidget(self.label_operations, 0, 0, 1, 1)

        self.row_user_entry = QWidget(self.container_tab1_left)
        self.row_user_entry.setObjectName(u"row_user_entry")
        self.layout_user_entry = QHBoxLayout(self.row_user_entry)
        self.layout_user_entry.setSpacing(6)
        self.layout_user_entry.setObjectName(u"layout_user_entry")
        self.layout_user_entry.setContentsMargins(-1, 9, 9, 9)
        self.label_user_entry = QLabel(self.row_user_entry)
        self.label_user_entry.setObjectName(u"label_user_entry")
        self.label_user_entry.setMinimumSize(QSize(74, 0))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_user_entry.sizePolicy().hasHeightForWidth())
        self.label_user_entry.setSizePolicy(sizePolicy2)

        self.layout_user_entry.addWidget(self.label_user_entry)

        self.user_entry = QLineEdit(self.row_user_entry)
        self.user_entry.setObjectName(u"user_entry")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.user_entry.sizePolicy().hasHeightForWidth())
        self.user_entry.setSizePolicy(sizePolicy3)
        self.user_entry.setStyleSheet(u"\n"
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

        self.layout_user_entry.addWidget(self.user_entry)


        self.gridLayout_left.addWidget(self.row_user_entry, 1, 0, 1, 2)

        self.row_search_entry = QWidget(self.container_tab1_left)
        self.row_search_entry.setObjectName(u"row_search_entry")
        self.layout_search_entry = QHBoxLayout(self.row_search_entry)
        self.layout_search_entry.setSpacing(6)
        self.layout_search_entry.setObjectName(u"layout_search_entry")
        self.layout_search_entry.setContentsMargins(-1, 9, 9, 9)
        self.label_search_entry = QLabel(self.row_search_entry)
        self.label_search_entry.setObjectName(u"label_search_entry")
        self.label_search_entry.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.label_search_entry.sizePolicy().hasHeightForWidth())
        self.label_search_entry.setSizePolicy(sizePolicy2)

        self.layout_search_entry.addWidget(self.label_search_entry)

        self.search_entry = QLineEdit(self.row_search_entry)
        self.search_entry.setObjectName(u"search_entry")
        sizePolicy3.setHeightForWidth(self.search_entry.sizePolicy().hasHeightForWidth())
        self.search_entry.setSizePolicy(sizePolicy3)
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


        self.gridLayout_left.addWidget(self.row_search_entry, 2, 0, 1, 2)

        self.row_barcode_entry = QWidget(self.container_tab1_left)
        self.row_barcode_entry.setObjectName(u"row_barcode_entry")
        self.layout_barcode_entry = QHBoxLayout(self.row_barcode_entry)
        self.layout_barcode_entry.setSpacing(6)
        self.layout_barcode_entry.setObjectName(u"layout_barcode_entry")
        self.layout_barcode_entry.setContentsMargins(-1, 9, 9, 9)
        self.label_barcode_entry = QLabel(self.row_barcode_entry)
        self.label_barcode_entry.setObjectName(u"label_barcode_entry")
        self.label_barcode_entry.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.label_barcode_entry.sizePolicy().hasHeightForWidth())
        self.label_barcode_entry.setSizePolicy(sizePolicy2)

        self.layout_barcode_entry.addWidget(self.label_barcode_entry)

        self.barcode_entry = QLineEdit(self.row_barcode_entry)
        self.barcode_entry.setObjectName(u"barcode_entry")
        sizePolicy3.setHeightForWidth(self.barcode_entry.sizePolicy().hasHeightForWidth())
        self.barcode_entry.setSizePolicy(sizePolicy3)
        self.barcode_entry.setStyleSheet(u"\n"
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

        self.layout_barcode_entry.addWidget(self.barcode_entry)

        self.btn_scan = QPushButton(self.row_barcode_entry)
        self.btn_scan.setObjectName(u"btn_scan")
        self.btn_scan.setMinimumSize(QSize(124, 0))
        self.btn_scan.setStyleSheet(u"\n"
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

        self.layout_barcode_entry.addWidget(self.btn_scan)

        self.btn_copy_barcode_entry = QPushButton(self.row_barcode_entry)
        self.btn_copy_barcode_entry.setObjectName(u"btn_copy_barcode_entry")
        self.btn_copy_barcode_entry.setMinimumSize(QSize(60, 0))
        self.btn_copy_barcode_entry.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_barcode_entry.setStyleSheet(u"\n"
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

        self.layout_barcode_entry.addWidget(self.btn_copy_barcode_entry)


        self.gridLayout_left.addWidget(self.row_barcode_entry, 3, 0, 1, 2)

        self.row_quantity_entry = QWidget(self.container_tab1_left)
        self.row_quantity_entry.setObjectName(u"row_quantity_entry")
        self.layout_quantity_entry = QHBoxLayout(self.row_quantity_entry)
        self.layout_quantity_entry.setSpacing(6)
        self.layout_quantity_entry.setObjectName(u"layout_quantity_entry")
        self.layout_quantity_entry.setContentsMargins(-1, 9, 9, 9)
        self.label_quantity_entry = QLabel(self.row_quantity_entry)
        self.label_quantity_entry.setObjectName(u"label_quantity_entry")
        self.label_quantity_entry.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.label_quantity_entry.sizePolicy().hasHeightForWidth())
        self.label_quantity_entry.setSizePolicy(sizePolicy2)

        self.layout_quantity_entry.addWidget(self.label_quantity_entry)

        self.quantity_entry = QLineEdit(self.row_quantity_entry)
        self.quantity_entry.setObjectName(u"quantity_entry")
        sizePolicy3.setHeightForWidth(self.quantity_entry.sizePolicy().hasHeightForWidth())
        self.quantity_entry.setSizePolicy(sizePolicy3)
        self.quantity_entry.setStyleSheet(u"\n"
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

        self.layout_quantity_entry.addWidget(self.quantity_entry)


        self.gridLayout_left.addWidget(self.row_quantity_entry, 4, 0, 1, 2)

        self.row_stock_buttons = QWidget(self.container_tab1_left)
        self.row_stock_buttons.setObjectName(u"row_stock_buttons")
        self.layout_stock_buttons = QHBoxLayout(self.row_stock_buttons)
        self.layout_stock_buttons.setSpacing(6)
        self.layout_stock_buttons.setObjectName(u"layout_stock_buttons")
        self.layout_stock_buttons.setContentsMargins(-1, 9, 9, 9)
        self.label_stock_btn = QLabel(self.row_stock_buttons)
        self.label_stock_btn.setObjectName(u"label_stock_btn")
        self.label_stock_btn.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.label_stock_btn.sizePolicy().hasHeightForWidth())
        self.label_stock_btn.setSizePolicy(sizePolicy2)

        self.layout_stock_buttons.addWidget(self.label_stock_btn)

        self.btn_add_stock = QPushButton(self.row_stock_buttons)
        self.btn_add_stock.setObjectName(u"btn_add_stock")
        self.btn_add_stock.setMinimumSize(QSize(124, 0))
        self.btn_add_stock.setStyleSheet(u"\n"
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

        self.layout_stock_buttons.addWidget(self.btn_add_stock)

        self.btn_remove_stock = QPushButton(self.row_stock_buttons)
        self.btn_remove_stock.setObjectName(u"btn_remove_stock")
        self.btn_remove_stock.setMinimumSize(QSize(124, 0))
        self.btn_remove_stock.setStyleSheet(u"\n"
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

        self.layout_stock_buttons.addWidget(self.btn_remove_stock)


        self.gridLayout_left.addWidget(self.row_stock_buttons, 5, 0, 1, 2)

        self.verticalSpacer_left = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_left.addItem(self.verticalSpacer_left, 6, 1, 1, 1)


        self.gridLayout_main.addWidget(self.container_tab1_left, 1, 0, 1, 1)

        self.container_tab1_right = QFrame(self.container_main_body)
        self.container_tab1_right.setObjectName(u"container_tab1_right")
        self.container_tab1_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_tab1_right.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_right = QGridLayout(self.container_tab1_right)
        self.gridLayout_right.setObjectName(u"gridLayout_right")
        self.gridLayout_right.setVerticalSpacing(0)
        self.gridLayout_right.setContentsMargins(-1, 15, -1, -1)
        self.label_details = QLabel(self.container_tab1_right)
        self.label_details.setObjectName(u"label_details")
        self.label_details.setStyleSheet(u"\n"
"QLabel {\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"")

        self.gridLayout_right.addWidget(self.label_details, 0, 0, 1, 1)

        self.row_val_mouser = QWidget(self.container_tab1_right)
        self.row_val_mouser.setObjectName(u"row_val_mouser")
        self.layout_val_mouser = QHBoxLayout(self.row_val_mouser)
        self.layout_val_mouser.setSpacing(6)
        self.layout_val_mouser.setObjectName(u"layout_val_mouser")
        self.layout_val_mouser.setContentsMargins(-1, 9, 9, 9)
        self.title_val_mouser = QLabel(self.row_val_mouser)
        self.title_val_mouser.setObjectName(u"title_val_mouser")
        self.title_val_mouser.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.title_val_mouser.sizePolicy().hasHeightForWidth())
        self.title_val_mouser.setSizePolicy(sizePolicy2)

        self.layout_val_mouser.addWidget(self.title_val_mouser)

        self.val_mouser = QLabel(self.row_val_mouser)
        self.val_mouser.setObjectName(u"val_mouser")
        self.val_mouser.setStyleSheet(u"\n"
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

        self.layout_val_mouser.addWidget(self.val_mouser)

        self.btn_copy_val_mouser = QPushButton(self.row_val_mouser)
        self.btn_copy_val_mouser.setObjectName(u"btn_copy_val_mouser")
        self.btn_copy_val_mouser.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_mouser.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_mouser.setStyleSheet(u"\n"
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

        self.layout_val_mouser.addWidget(self.btn_copy_val_mouser)


        self.gridLayout_right.addWidget(self.row_val_mouser, 1, 0, 1, 2)

        self.row_val_manufacturer = QWidget(self.container_tab1_right)
        self.row_val_manufacturer.setObjectName(u"row_val_manufacturer")
        self.layout_val_manufacturer = QHBoxLayout(self.row_val_manufacturer)
        self.layout_val_manufacturer.setSpacing(6)
        self.layout_val_manufacturer.setObjectName(u"layout_val_manufacturer")
        self.layout_val_manufacturer.setContentsMargins(-1, 9, 9, 9)
        self.title_val_manufacturer = QLabel(self.row_val_manufacturer)
        self.title_val_manufacturer.setObjectName(u"title_val_manufacturer")
        self.title_val_manufacturer.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.title_val_manufacturer.sizePolicy().hasHeightForWidth())
        self.title_val_manufacturer.setSizePolicy(sizePolicy2)

        self.layout_val_manufacturer.addWidget(self.title_val_manufacturer)

        self.val_manufacturer = QLabel(self.row_val_manufacturer)
        self.val_manufacturer.setObjectName(u"val_manufacturer")
        self.val_manufacturer.setStyleSheet(u"\n"
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

        self.layout_val_manufacturer.addWidget(self.val_manufacturer)

        self.btn_copy_val_manufacturer = QPushButton(self.row_val_manufacturer)
        self.btn_copy_val_manufacturer.setObjectName(u"btn_copy_val_manufacturer")
        self.btn_copy_val_manufacturer.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_manufacturer.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_manufacturer.setStyleSheet(u"\n"
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

        self.layout_val_manufacturer.addWidget(self.btn_copy_val_manufacturer)


        self.gridLayout_right.addWidget(self.row_val_manufacturer, 2, 0, 1, 2)

        self.row_val_manufacturer_ref = QWidget(self.container_tab1_right)
        self.row_val_manufacturer_ref.setObjectName(u"row_val_manufacturer_ref")
        self.layout_val_manufacturer_ref = QHBoxLayout(self.row_val_manufacturer_ref)
        self.layout_val_manufacturer_ref.setSpacing(6)
        self.layout_val_manufacturer_ref.setObjectName(u"layout_val_manufacturer_ref")
        self.layout_val_manufacturer_ref.setContentsMargins(-1, 9, 9, 9)
        self.title_val_manufacturer_ref = QLabel(self.row_val_manufacturer_ref)
        self.title_val_manufacturer_ref.setObjectName(u"title_val_manufacturer_ref")
        self.title_val_manufacturer_ref.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.title_val_manufacturer_ref.sizePolicy().hasHeightForWidth())
        self.title_val_manufacturer_ref.setSizePolicy(sizePolicy2)

        self.layout_val_manufacturer_ref.addWidget(self.title_val_manufacturer_ref)

        self.val_manufacturer_ref = QLabel(self.row_val_manufacturer_ref)
        self.val_manufacturer_ref.setObjectName(u"val_manufacturer_ref")
        self.val_manufacturer_ref.setStyleSheet(u"\n"
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

        self.layout_val_manufacturer_ref.addWidget(self.val_manufacturer_ref)

        self.btn_copy_val_manufacturer_ref = QPushButton(self.row_val_manufacturer_ref)
        self.btn_copy_val_manufacturer_ref.setObjectName(u"btn_copy_val_manufacturer_ref")
        self.btn_copy_val_manufacturer_ref.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_manufacturer_ref.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_manufacturer_ref.setStyleSheet(u"\n"
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

        self.layout_val_manufacturer_ref.addWidget(self.btn_copy_val_manufacturer_ref)


        self.gridLayout_right.addWidget(self.row_val_manufacturer_ref, 3, 0, 1, 2)

        self.row_val_description = QWidget(self.container_tab1_right)
        self.row_val_description.setObjectName(u"row_val_description")
        self.layout_val_description = QHBoxLayout(self.row_val_description)
        self.layout_val_description.setSpacing(6)
        self.layout_val_description.setObjectName(u"layout_val_description")
        self.layout_val_description.setContentsMargins(-1, 9, 9, 9)
        self.title_val_description = QLabel(self.row_val_description)
        self.title_val_description.setObjectName(u"title_val_description")
        self.title_val_description.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.title_val_description.sizePolicy().hasHeightForWidth())
        self.title_val_description.setSizePolicy(sizePolicy2)

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


        self.gridLayout_right.addWidget(self.row_val_description, 4, 0, 1, 2)

        self.row_val_stock = QWidget(self.container_tab1_right)
        self.row_val_stock.setObjectName(u"row_val_stock")
        self.layout_val_stock = QHBoxLayout(self.row_val_stock)
        self.layout_val_stock.setSpacing(6)
        self.layout_val_stock.setObjectName(u"layout_val_stock")
        self.layout_val_stock.setContentsMargins(-1, 9, 9, 9)
        self.title_val_stock = QLabel(self.row_val_stock)
        self.title_val_stock.setObjectName(u"title_val_stock")
        self.title_val_stock.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.title_val_stock.sizePolicy().hasHeightForWidth())
        self.title_val_stock.setSizePolicy(sizePolicy2)

        self.layout_val_stock.addWidget(self.title_val_stock)

        self.val_stock = QLabel(self.row_val_stock)
        self.val_stock.setObjectName(u"val_stock")
        self.val_stock.setStyleSheet(u"\n"
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

        self.layout_val_stock.addWidget(self.val_stock)

        self.btn_copy_val_stock = QPushButton(self.row_val_stock)
        self.btn_copy_val_stock.setObjectName(u"btn_copy_val_stock")
        self.btn_copy_val_stock.setMinimumSize(QSize(60, 0))
        self.btn_copy_val_stock.setMaximumSize(QSize(60, 16777215))
        self.btn_copy_val_stock.setStyleSheet(u"\n"
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

        self.layout_val_stock.addWidget(self.btn_copy_val_stock)


        self.gridLayout_right.addWidget(self.row_val_stock, 5, 0, 1, 2)

        self.row_catalog_links = QWidget(self.container_tab1_right)
        self.row_catalog_links.setObjectName(u"row_catalog_links")
        self.layout_catalog_links = QHBoxLayout(self.row_catalog_links)
        self.layout_catalog_links.setSpacing(6)
        self.layout_catalog_links.setObjectName(u"layout_catalog_links")
        self.layout_catalog_links.setContentsMargins(-1, 4, 9, 4)
        self.label_catalog_links = QLabel(self.row_catalog_links)
        self.label_catalog_links.setObjectName(u"label_catalog_links")
        self.label_catalog_links.setMinimumSize(QSize(74, 0))
        sizePolicy2.setHeightForWidth(self.label_catalog_links.sizePolicy().hasHeightForWidth())
        self.label_catalog_links.setSizePolicy(sizePolicy2)

        self.layout_catalog_links.addWidget(self.label_catalog_links)

        self.btn_open_product = QPushButton(self.row_catalog_links)
        self.btn_open_product.setObjectName(u"btn_open_product")
        self.btn_open_product.setMinimumSize(QSize(60, 0))
        self.btn_open_product.setMaximumSize(QSize(60, 16777215))
        self.btn_open_product.setStyleSheet(u"\n"
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

        self.layout_catalog_links.addWidget(self.btn_open_product)

        self.btn_open_datasheet = QPushButton(self.row_catalog_links)
        self.btn_open_datasheet.setObjectName(u"btn_open_datasheet")
        self.btn_open_datasheet.setMinimumSize(QSize(60, 0))
        self.btn_open_datasheet.setMaximumSize(QSize(60, 16777215))
        self.btn_open_datasheet.setStyleSheet(u"\n"
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

        self.layout_catalog_links.addWidget(self.btn_open_datasheet)

        self.horizontalSpacer_catalog_links = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_catalog_links.addItem(self.horizontalSpacer_catalog_links)


        self.gridLayout_right.addWidget(self.row_catalog_links, 6, 0, 1, 2)

        self.component_image_preview = QLabel(self.container_tab1_right)
        self.component_image_preview.setObjectName(u"component_image_preview")
        self.component_image_preview.setMinimumSize(QSize(240, 240))
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.component_image_preview.sizePolicy().hasHeightForWidth())
        self.component_image_preview.setSizePolicy(sizePolicy4)
        self.component_image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.component_image_preview.setStyleSheet(u"\n"
"QLabel {\n"
"    border: 1px dashed #B3B3BE;\n"
"    border-radius: 2px;\n"
"    background-color: #00183B;\n"
"    color: #B3B3BE;\n"
"    font-size: 12px;\n"
"}\n"
"")

        self.gridLayout_right.addWidget(self.component_image_preview, 7, 0, 1, 2)

        self.verticalSpacer_right = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_right.addItem(self.verticalSpacer_right, 8, 1, 1, 1)


        self.gridLayout_main.addWidget(self.container_tab1_right, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.container_main_body)

        self.widget_actions = QWidget(self.centralwidget)
        self.widget_actions.setObjectName(u"widget_actions")
        self.horizontalLayout_actions = QHBoxLayout(self.widget_actions)
        self.horizontalLayout_actions.setSpacing(6)
        self.horizontalLayout_actions.setObjectName(u"horizontalLayout_actions")
        self.horizontalLayout_actions.setContentsMargins(16, 9, 16, 9)
        self.btn_history_all = QPushButton(self.widget_actions)
        self.btn_history_all.setObjectName(u"btn_history_all")
        self.btn_history_all.setMinimumSize(QSize(124, 0))
        self.btn_history_all.setStyleSheet(u"\n"
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

        self.horizontalLayout_actions.addWidget(self.btn_history_all)

        self.btn_history_component = QPushButton(self.widget_actions)
        self.btn_history_component.setObjectName(u"btn_history_component")
        self.btn_history_component.setMinimumSize(QSize(124, 0))
        self.btn_history_component.setStyleSheet(u"\n"
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

        self.horizontalLayout_actions.addWidget(self.btn_history_component)

        self.btn_add_manual = QPushButton(self.widget_actions)
        self.btn_add_manual.setObjectName(u"btn_add_manual")
        self.btn_add_manual.setMinimumSize(QSize(124, 0))
        self.btn_add_manual.setStyleSheet(u"\n"
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

        self.horizontalLayout_actions.addWidget(self.btn_add_manual)

        self.btn_edit_component = QPushButton(self.widget_actions)
        self.btn_edit_component.setObjectName(u"btn_edit_component")
        self.btn_edit_component.setMinimumSize(QSize(124, 0))
        self.btn_edit_component.setStyleSheet(u"\n"
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

        self.horizontalLayout_actions.addWidget(self.btn_edit_component)

        self.horizontalSpacer_actions = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_actions.addItem(self.horizontalSpacer_actions)

        self.btn_clear = QPushButton(self.widget_actions)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setMinimumSize(QSize(124, 0))
        self.btn_clear.setStyleSheet(u"\n"
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

        self.horizontalLayout_actions.addWidget(self.btn_clear)

        self.btn_exit = QPushButton(self.widget_actions)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setMinimumSize(QSize(124, 0))
        self.btn_exit.setStyleSheet(u"\n"
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

        self.horizontalLayout_actions.addWidget(self.btn_exit)


        self.verticalLayout.addWidget(self.widget_actions)

        self.status_label = QLabel(self.centralwidget)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setStyleSheet(u"\n"
"QLabel {\n"
"    color: #B3B3BE;\n"
"    font-size: 12px;\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.status_label)

        StockTracker.setCentralWidget(self.centralwidget)

        self.retranslateUi(StockTracker)

        QMetaObject.connectSlotsByName(StockTracker)
    # setupUi

    def retranslateUi(self, StockTracker):
        StockTracker.setWindowTitle(QCoreApplication.translate("StockTracker", u"Stock Tracker", None))
        self.product_name.setText(QCoreApplication.translate("StockTracker", u"Stock Tracker", None))
        self.tab1_title.setText(QCoreApplication.translate("StockTracker", u"Inventory", None))
        self.label_operations.setText(QCoreApplication.translate("StockTracker", u"Operations", None))
        self.label_user_entry.setText(QCoreApplication.translate("StockTracker", u"User Name", None))
        self.label_search_entry.setText(QCoreApplication.translate("StockTracker", u"Search Component", None))
        self.btn_search.setText(QCoreApplication.translate("StockTracker", u"SEARCH", None))
        self.label_barcode_entry.setText(QCoreApplication.translate("StockTracker", u"Scan Barcode / Supplier Ref.", None))
        self.btn_scan.setText(QCoreApplication.translate("StockTracker", u"SCAN", None))
#if QT_CONFIG(tooltip)
        self.btn_copy_barcode_entry.setToolTip(QCoreApplication.translate("StockTracker", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_barcode_entry.setText(QCoreApplication.translate("StockTracker", u"Copy", None))
        self.label_quantity_entry.setText(QCoreApplication.translate("StockTracker", u"Quantity", None))
        self.label_stock_btn.setText(QCoreApplication.translate("StockTracker", u"Stock Actions", None))
        self.btn_add_stock.setText(QCoreApplication.translate("StockTracker", u"ADD STOCK", None))
        self.btn_remove_stock.setText(QCoreApplication.translate("StockTracker", u"REMOVE STOCK", None))
        self.label_details.setText(QCoreApplication.translate("StockTracker", u"Component Details", None))
        self.title_val_mouser.setText(QCoreApplication.translate("StockTracker", u"Supplier Reference", None))
        self.val_mouser.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_mouser.setToolTip(QCoreApplication.translate("StockTracker", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_mouser.setText(QCoreApplication.translate("StockTracker", u"Copy", None))
        self.title_val_manufacturer.setText(QCoreApplication.translate("StockTracker", u"Manufacturer", None))
        self.val_manufacturer.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_manufacturer.setToolTip(QCoreApplication.translate("StockTracker", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_manufacturer.setText(QCoreApplication.translate("StockTracker", u"Copy", None))
        self.title_val_manufacturer_ref.setText(QCoreApplication.translate("StockTracker", u"Manufacturer Reference", None))
        self.val_manufacturer_ref.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_manufacturer_ref.setToolTip(QCoreApplication.translate("StockTracker", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_manufacturer_ref.setText(QCoreApplication.translate("StockTracker", u"Copy", None))
        self.title_val_description.setText(QCoreApplication.translate("StockTracker", u"Description", None))
        self.val_description.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_description.setToolTip(QCoreApplication.translate("StockTracker", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_description.setText(QCoreApplication.translate("StockTracker", u"Copy", None))
        self.title_val_stock.setText(QCoreApplication.translate("StockTracker", u"Current Stock", None))
        self.val_stock.setText("")
#if QT_CONFIG(tooltip)
        self.btn_copy_val_stock.setToolTip(QCoreApplication.translate("StockTracker", u"Copy to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.btn_copy_val_stock.setText(QCoreApplication.translate("StockTracker", u"Copy", None))
        self.label_catalog_links.setText(QCoreApplication.translate("StockTracker", u"Catalog", None))
#if QT_CONFIG(tooltip)
        self.btn_open_product.setToolTip(QCoreApplication.translate("StockTracker", u"Open product page on distributor site", None))
#endif // QT_CONFIG(tooltip)
        self.btn_open_product.setText(QCoreApplication.translate("StockTracker", u"WEB", None))
#if QT_CONFIG(tooltip)
        self.btn_open_datasheet.setToolTip(QCoreApplication.translate("StockTracker", u"Open datasheet in browser", None))
#endif // QT_CONFIG(tooltip)
        self.btn_open_datasheet.setText(QCoreApplication.translate("StockTracker", u"DS", None))
        self.component_image_preview.setText(QCoreApplication.translate("StockTracker", u"No image", None))
        self.btn_history_all.setText(QCoreApplication.translate("StockTracker", u"Last 20", None))
        self.btn_history_component.setText(QCoreApplication.translate("StockTracker", u"Comp. hist.", None))
        self.btn_add_manual.setText(QCoreApplication.translate("StockTracker", u"ADD MANUAL COMPONENT", None))
        self.btn_edit_component.setText(QCoreApplication.translate("StockTracker", u"EDIT COMPONENT", None))
        self.btn_clear.setText(QCoreApplication.translate("StockTracker", u"CLEAR", None))
        self.btn_exit.setText(QCoreApplication.translate("StockTracker", u"Exit", None))
        self.status_label.setText("")
    # retranslateUi

