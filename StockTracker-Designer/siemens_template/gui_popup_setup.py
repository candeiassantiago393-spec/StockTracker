###############################################################################
# 1. Module Documentation
###############################################################################
"""
Module Name:
    gui_popup_setup.py

Description:
    Provides the GUI_POPUP_SETUP class, which displays a simple popup window with
    a title, description, and OK/Cancel buttons. The popup blocks user interaction
    until one of the buttons is pressed, and the selected button can be queried.

Author:
    PF.
Date:
    2026-03-25
"""


###############################################################################
# 2. Imports
###############################################################################
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from .gui_popup import Ui_Popup as UiPopup


###############################################################################
# 3. Popup Class
###############################################################################
class GuiPopupSetup(QDialog):
    """
    Class:
        Simple popup window providing a title, description, and OK/Cancel buttons.

    Attributes:
        title (str): Text displayed in the popup title field.
        description (str): Text displayed in the popup description area.
    """

    # -------------------------------------------------------------------------
    # Class initialization
    # -------------------------------------------------------------------------
    def __init__(self, title: str = "Popup", description: str = "Someone forgot the description 😞"):
        
        super().__init__()

        # Build UI
        self.ui = UiPopup()
        self.ui.setupUi(self)

        # Set UI text
        self.ui.tittle.setText(title)
        self.ui.description.setText(description)
        
        # Connect buttons
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)