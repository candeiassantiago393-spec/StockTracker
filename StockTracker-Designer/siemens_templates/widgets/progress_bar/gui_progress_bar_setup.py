###############################################################################
# 1. Module Documentation
###############################################################################
"""
Module Name:
    gui_progress_bar.py

Description:    
    This module implements the GuiProgressBarSetup class, which provides a GUI
    window containing a circular progress bar and percentage indicator.  
    The class allows updating the displayed progress value and automatically
    applies different visual colors depending on progress state 
    (initial, in-progress, completed, or error)

Author:
    PF.
Date:
    2026-03-30
"""


###############################################################################
# 2. Imports
###############################################################################
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from .gui_progress_bar import Ui_ProgressBar as UiProgressBar

###############################################################################
# 3. Constants and Global Variables
###############################################################################
# Progress Colors
PROGRESS_NONE = "#009999"   # Initial state
PROGRESS_GOING = "#ff9000"  # In progress
PROGRESS_DONE = "#00d7a0"   # Completed (100%)
PROGRESS_ERROR = "#ef0137"  # Error state
PROGRESS_PAUSED = "#f7c600"    # Paused state


###############################################################################
# 4. Production Class
###############################################################################
class GuiProgressBarSetup(QMainWindow):
    """
    Class:
        GUI window displaying a circular progress bar with percentage text.        
        The progress bar color dynamically changes to reflect progress state.
    """
    
    # -------------------------------------------------------------------------
    # Class initialization
    # -------------------------------------------------------------------------
    def __init__(self):

        super().__init__()

        # Variables Initializaion
        self.previous_percentage = 0

        # Build UI
        self.ui = UiProgressBar()
        self.ui.setupUi(self)

    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
    def update_progressbar(self, value) -> None:        
        """
        Updates both the circular progress bar and its percentage label.

        Args:
            value (float):
                Progress value between 0 and 100.

                Special behavior:
                - 0     → Sets progress to “initial state” color.
                - 1-99  → Normal in-progress state.
                - 100   → Completed state.
                - -1    → Error state - keeps last displayed percentage
                - -2    → Paused state - keeps last displayed percentage
        """     
        percentage = value

        # Determine color based on state
        if value == 0:
            color = PROGRESS_NONE
            self.previous_percentage = value
        elif 0 < value < 100:
            color = PROGRESS_GOING
            self.previous_percentage = value
        elif value == 100:
            color = PROGRESS_DONE
            self.previous_percentage = value
        elif value == -1:
            color = PROGRESS_ERROR
            percentage = self.previous_percentage
        elif value == -2:
            color = PROGRESS_PAUSED
            percentage = self.previous_percentage
        
        fpercentage = f"{percentage:.0f}"        
     
        # Update percentage text label
        htmlText = """<p align="center"><span style="font-size:50pt; color:{COLOR};">{VALUE}</span><span style="font-size:40pt; vertical-align:super; color:{COLOR};">%</span></p>"""
        self.ui.label_percentage.setText(htmlText.replace("{VALUE}", str(fpercentage)).replace("{COLOR}", str(color)))

        # Update circular progress bar
        self._set_progressbar(percentage, color)

    # -------------------------------------------------------------------------
    # Protected methods
    # -------------------------------------------------------------------------
    def _set_progressbar(self, value, color) -> None:
        """
        Protected Method:
            Updates the circular progress bar.

        Args:
            value (float): Progress value (0-100)
            color (str): Hex color to apply
        """        
        styleSheet =    """
                        QFrame{
                            border-radius: 110px;
                            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} #19193d, stop:{STOP_2} {COLOR});
                        }
                        """

        # Get progress bar value 
        progress = (100-value) / 100.0        
        stop_1 = str(progress - 0.005)
        stop_2 = str(progress)

        # Special case for 100%
        if value == 100:
            stop_1 = "1.000"
            stop_2 = "1.000"

        # Define and apply new stylesheet
        stylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2).replace("{COLOR}", color)
        self.ui.circular_progress.setStyleSheet(stylesheet)

###############################################################################
# 6. Test Main
###############################################################################
if __name__ == "__main__":
       
    app = QApplication(sys.argv)
    window = GuiProgressBarSetup()    
    window.update_progressbar(42)
    app.exec()



   

        

        
           
    

    