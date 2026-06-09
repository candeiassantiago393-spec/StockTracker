###############################################################################
# 1. Module Documentation
###############################################################################
"""
Module Name:
    Card Entry Setup
Description:    

Author:
    JD
Date:
    2026-04-08
"""


###############################################################################
# 2. Imports
###############################################################################
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Signal

from src.gui.siemens_template.widgets.card.card_entry import Ui_CardEntry

###############################################################################
# 3.Ui_CardEntry Class
###############################################################################
class Ui_CardEntrySetup(QMainWindow):
    """
    Class:
        Provides a interface with the card_entry UI.
    
    Args:
        [optional] key (str) : Identifier for the entry.
        [optional] label (str) : Text to be displayed in label field.
        [optional] value (str) : Text to be displayed in value field.
        [optional] unit (str) : Text to be displayed in unit field.
        [optional] readonly (bool) : If value field is read only.
    """
    # -------------------------------------------------------------------------
    # Class initialization
    # -------------------------------------------------------------------------
    
    gui_update_request = Signal(object, object, object, object, object)
    entry_events = Signal(str, QEvent)
    
    def __init__(self, key="", label="", value="", unit="", readonly= False, btn1_label="btn1", btn1_callback=None, btn2_label="btn2",  btn2_callback=None):
        super().__init__()

        # Variables Initializaion
        self.key = key
        self.label= label
        self.value= value
        self.unit= unit
        self.readonly= readonly        
        
        # Connect the signal to the GUI update method
        self.gui_update_request.connect(self._update)

        # Build UI
        self.ui = Ui_CardEntry()
        self.ui.setupUi(self)

        # Install event filter on value field
        self.ui.value.installEventFilter(self)

        # Get base stylesheet for value field
        self.value_base_stylesheet = self.ui.value.styleSheet()

        # Hide buttons by default
        self.configure_btn1(callback=btn1_callback, label=btn1_label, visibility=False)
        self.configure_btn2(callback=btn2_callback, label=btn2_label, visibility=False)

        # button callbacks
        self.ui.btn1.clicked.connect(self._btn1)
        self.ui.btn2.clicked.connect(self._btn2)
        self.btn1_callback = btn1_callback
        self.btn2_callback = btn2_callback

        # Initial update
        if callable(self.update_gui):
            self.update_gui(label= label, value=value, unit=unit, readonly=readonly)

    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
    def update_gui(self, label=None, value=None, unit=None, readonly=False, status=None):
        """
        Public Method:
            Updates the GUI elements.
            If no value is provided for a certain field the previous one will be used. 
        Args:
            [optional] label (str) : Text to be displayed in label field.
            [optional] value (str) : Text to be displayed in value field.
            [optional] unit (str) : Text to be displayed in unit field.
            [optional] readonly (bool) : If value field is read only.
            [optional] status (bool) : Status of the entry.
        """

        self.gui_update_request.emit(label, value, unit, readonly, status)
        return

    def get_value(self):
        '''
        Public Method:
            Retrieves the current text displayed in the value field.
        
        Returns:
            str: Text currently displayed in value field.        
        '''
        return self.ui.value.text()
    
    def set_value(self, value):
        '''
        Public Method:
            Sets the text displayed in the value field.

        Args:
            value (str): Text to be displayed in value field.
        '''
        self.update_gui(value=value)

    def set_status(self, status: bool):
        '''
        Public Method:
            Highlights the value field with a border color to indicate a fault or error state.

        Args:
            status (str): Status of the entry. If True, the value field will be highlighted with a red border to indicate a fault or error state. If False, the value field will return to its default appearance.
        '''
        self.update_gui(status=status)

    def configure_btn1(self, callback=None, label=None, visibility=None):
        if callback is not None:
            self.btn1_callback = callback
        if label is not None:
            self.ui.btn1.setText(label)
        if visibility is not None:
            self.ui.btn1.setVisible(visibility)

    def configure_btn2(self, callback=None, label=None, visibility=None):
        if callback is not None:
            self.btn2_callback = callback
        if label is not None:
            self.ui.btn2.setText(label)
        if visibility is not None:
            self.ui.btn2.setVisible(visibility)

    # -------------------------------------------------------------------------
    # Protected methods
    # -------------------------------------------------------------------------
    def _update(self, label, value, unit, readonly, status):
        """
        Protected Method:
            Updates the GUI elements.
        Args:
            label (str) : Text to be displayed in label field.
            value (str) : Text to be displayed in value field.
            unit (str) : Text to be displayed in unit field.
            readonly (bool) : If value field is read only.
            border_color (str) : Border color to be applied to value field (e.g., "red", "#FF0000").
        """
        if label is not None:
            self.ui.label.setText(str(label))

        if value is not None:
            self.ui.value.setText(str(value))

        if unit is not None:
            self.ui.unit.setText(str(unit))

        # Check if readonly status is provided and update the value field accordingly
        if readonly is not None:
            self.ui.value.setReadOnly(readonly)

            # If the field is set to read-only, apply the base stylesheet.
            if readonly:                        
                self.ui.value.setStyleSheet(self.value_base_stylesheet)            
            
            # Otherwise, apply the interactive stylesheet with hover effects.
            else:            
                self.ui.value.setStyleSheet(self.value_base_stylesheet + 
                    """QLineEdit:hover{
                    background-color: #001F39;
                    border: 1px solid #00FFB9;
                    }
                    """)
                
                # If the field is interactive, also check the status to determine if an error state should be indicated.
                if status is not None:                                 
                    if not status:                        
                        self.ui.value.setStyleSheet(self.value_base_stylesheet + 
                            """QLineEdit{
                            border: 1px solid #FF2640;
                            background-color: #331131;
                            }
                            QLineEdit:hover{
                            background-color: #331131;
                            border: 1px solid #00FFB9;
                            }
                            """)   

        return    
    
    def eventFilter(self, obj, event):
        """
        Protected Method:
            Event filter to detect when the value field is focused and emit the entry_events signal with the associated key and event information.
        
        Args:
            obj (QObject): The object that received the event.
            event (QEvent): The event that occurred.
        
        Returns:            
            bool: True if the event was handled, False otherwise.
        """
        # Check if the event is related to the value field of this entry
        if obj is self.ui.value:

            if event.type() == QEvent.FocusIn or event.type() == QEvent.FocusOut:                            
                # Emit the entry_events signal with the associated key when the value field is focused
                self.entry_events.emit(self.key, event)                           
                    
        return super().eventFilter(obj, event)

    def _btn1(self):
        if callable(self.btn1_callback):
            self.btn1_callback()
    
    def _btn2(self):
        if callable(self.btn2_callback):
            self.btn2_callback()


###############################################################################
# 4. Test User Class (Simulation)
###############################################################################
class TestUser(QMainWindow):
    """
    Class:
        Simulates user interaction to demonstrate the production GUI.
    """

    # -------------------------------------------------------------------------
    # Class initialization
    # -------------------------------------------------------------------------
    def __init__(self):
        self.window = Ui_CardEntrySetup(label="Medição", value="65", unit="batatas", readonly= False)


###############################################################################
# 5. Test Main
###############################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = TestUser()
    user.window.show()
    
    app.exec()

