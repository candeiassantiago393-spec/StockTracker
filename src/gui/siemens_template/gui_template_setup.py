###############################################################################
# 1. Module Documentation
###############################################################################
"""
Module Name:
    gui_template.py

Description:
    Template for a generic GUI window. 

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

from .gui_template import Ui_Template as UiTemplate

###############################################################################
# 3. Popup Class
###############################################################################
class GuiTemplateSetup(QMainWindow):
    """
    Class:
        Template for a generic GUI window.
    """

    # -------------------------------------------------------------------------
    # Class initialization
    # -------------------------------------------------------------------------
    def __init__(self):

        super().__init__()

        # Build UI
        self.ui = UiTemplate()
        self.ui.setupUi(self)        

        # Connect remaining button callbacks
        self.ui.btn_ok.clicked.connect(self._btn_ok)
        self.ui.btn_exit.clicked.connect(self._btn_exit)

        # Clear selectors
        self.ui.selector.clear()
        
        # Fill selector with available options
        self.ui.selector.addItems(["Option 1", "Option 2", "Option 3"])

        # Display popup
        self.show()

    # -------------------------------------------------------------------------
    # Protected methods
    # -------------------------------------------------------------------------
    def _btn_ok(self) -> None:
        """
        Protected Method:
            Called when the user presses OK.
        """
        # Read data input
        data_input = self.ui.field_data_in.text()

        # Output data
        self.ui.field_data_out.setText(data_input)
    
    def _btn_exit(self) -> None:
        """
        Protected Method:
            Called when the user presses EXIT.clear
        """
        self.close()


###############################################################################
# 4. Test Main
###############################################################################
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = GuiTemplateSetup()
    app.exec()

    