###############################################################################
# 1. Module Documentation
###############################################################################
"""
Module Name:
    gui_toggle_setup.py

Description:    
    This module implements the GuiToggleSetup class, which provides a user interface for a toggle switch.
    The toggle switch consists of a button that can be toggled between ON and OFF states, and a sliding 
    knob that animates to indicate the current state. The class also includes a callback mechanism to handle toggle events.

Author:
    PF.
Date:
    2026-05-06
"""


###############################################################################
# 2. Imports
###############################################################################
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from .gui_toggle import Ui_Toggle as UiToggle


###############################################################################
# 3. Production Class
###############################################################################
class GuiToggleSetup(QMainWindow):
    """
    Class:
        GuiToggleSetup provides an interface for a toggle switch UI. 
        It includes a toggle button and a sliding knob that animates between ON and OFF positions. 
    """
    gui_update_request = Signal(object)
    visible_request = Signal(bool)
    # -------------------------------------------------------------------------
    # Class initialization
    # -------------------------------------------------------------------------
    def __init__(self, label="", toggle_callback=None):

        super().__init__()

        # Variables Initializaion
        self.label= label
        self.toggle_callback = toggle_callback

        # Build UI
        self.ui = UiToggle()
        self.ui.setupUi(self)

        # Connect the signal to the GUI update method
        self.gui_update_request.connect(self._animate)
        self.visible_request.connect(self._visible)

        # Configure toggle button
        self.ui.toggle_btn.setCheckable(True)
        self.ui.toggle_btn.setText("")
        self.ui.label.setText(label)

        # Slider knob
        self.knob = QWidget(self)
        self.knob.setGeometry(180, 12, 18, 18)
        self.knob.setStyleSheet("""
            background-color: #000028;
            border-radius: 9px;
        """)        
        self.knob.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        # Animation setup
        self.anim = QPropertyAnimation(self.knob, b"pos", self)
        self.anim.setDuration(180)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

        # Connect toggle button signal to animation slot
        self.ui.toggle_btn.toggled.connect(self._toggled)

    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
    def force_state(self, state: bool) -> None :
        """
        Public Method:
            Forces the toggle button to a specified state.
            This will execute the assigned callback function.
        Args:
            state (bool): State to be used.
        """
        self.ui.toggle_btn.setChecked(state)
        self._animate(state)
        

    def set_visible(self, visible: bool) -> None:
        """
        Public Method:
            Sets the visibility of the toggle widget.

        Args:
            visible (bool): True to show the widget, False to hide it.
        """
        self.visible_request.emit(visible)

    # -------------------------------------------------------------------------
    # Protected methods
    # -------------------------------------------------------------------------
    def _toggled(self, checked: bool) -> None:
        """
        Protected Method:
            Called when the toggle button is toggled. It triggers the provided callback 
            function with the new toggle state and starts the animation to move the knob to the new position.

        Args:
            checked (bool): The new state of the toggle button (True for ON, False for OFF).
        """
        # Call the provided callback function with the new toggle state
        if self.toggle_callback:
            self.toggle_callback(checked)
        
        # Animate the knob to the new position based on the toggle state
        self.gui_update_request.emit(checked)
    
    def _animate(self, checked: bool) -> None:
        """
        Protected Method:
            Animates the toggle knob to the new position based on the toggle state.

        Args:
            checked (bool): The new state of the toggle button (True for ON, False for OFF).
        """
        # Stop any ongoing animation and set the start value to the current position of the knob
        self.anim.stop()
        self.anim.setStartValue(self.knob.pos())

        # Set the end value based on the toggle state (200 for ON, 180 for OFF) and start the animation
        self.anim.setEndValue(QPoint(200 if checked else 180, 12))
        self.anim.start()

    def _visible(self, visible: bool) -> None:
        """
        Protected Method:
            Sets the visibility of the toggle widget.

        Args:
            visible (bool): True to show the widget, False to hide it.
        """
        self.setVisible(visible)

        # If the widget is being hidden, also reset the toggle state to OFF and move the knob back to the OFF position.
        if not visible:
            self.ui.toggle_btn.setChecked(False)
            self._animate(False)

###############################################################################
# 4. Test Main
###############################################################################

if __name__ == "__main__":
    import time
    import threading

    app = QApplication(sys.argv)
    def testcallback(state):
        if state:
            print("hello")
        else:
            print("goodbye")
    window = GuiToggleSetup(label= "toggle button", toggle_callback= testcallback)
    window.show()

    def delayed_force():
        time.sleep(3)
        print("forcing state to True")
        window.force_state(True)

    t2 = threading.Thread(target=delayed_force)
    t2.start()

    app.exec()
    t2.join()
