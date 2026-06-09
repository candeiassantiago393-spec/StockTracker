###############################################################################
# 1. Module Documentation
###############################################################################
"""
Module Name:
    Card ComboBox Setup
Description:    

Author:
    JD
Date:
    2026-04-20
"""

###############################################################################
# 2. Imports
###############################################################################
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Signal

from src.gui.siemens_template.widgets.card.card_combobox import Ui_CardCombBox
from src.gui.siemens_template.widgets.card.card_entry_setup import Ui_CardEntrySetup

class Ui_CardComboBoxSetup(Ui_CardEntrySetup):
    """
    Class:
        Provides a interface with the card_combobox UI.
    
    Args:
        [optional] selector_list (list) : options for the combobox.
        [optional] key (str) : Identifier for the entry.
        [optional] label (str) : Text to be displayed in label field.
        [optional] value (str) : Text to be displayed in value field.
        [optional] unit (str) : Text to be displayed in unit field.
        [optional] readonly (bool) : If value field is read only.
    """

    gui_update_request = Signal(object, object, object, object, object, bool)

    def __init__(self, key="", label="", value="", unit="", readonly= False, monitor_pressed=False, btn1_label="btn1", btn1_callback=None, btn2_label="btn2",  btn2_callback=None, selector_list=["","",""]):
        # disable update
        update_method= self.update_gui
        self.update_gui=None
        
        super().__init__()

        self.update_gui= update_method

        # Variables Initializaion
        self.key = key
        self.label= label
        self.value= value
        self.unit= unit
        self.readonly= readonly
        self.monitor_pressed = monitor_pressed        
        self.selector_list= selector_list
        
        # Connect the signal to the GUI update method
        self.gui_update_request.connect(self._update)

        # Build UI
        self.ui = Ui_CardCombBox()
        self.ui.setupUi(self)

        # If monitoring for presses is enabled, install an event filter on the value field to detect clicks
        if self.monitor_pressed:
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
        self.update_gui(label= label, value=value, unit=unit, readonly=readonly, selector_list=selector_list, clear_list=True)

    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
    def update_gui(self, label=None, value=None, unit=None, readonly=None, selector_list=None, clear_list=False):
        """
        Public Method:
            Updates the GUI elements.
            If no value is provided for a certain field the previous one will be used. 
        Args:
            [optional] label (str) : Text to be displayed in label field.
            [optional] value (str) : Text to be displayed in value field.
            [optional] unit (str) : Text to be displayed in unit field.
            [optional] readonly (bool) : If value field is read only.
            [optional] selector_list (list) : list of possible values.
            [optional] clear_list (bool) : if the already existing values should be erased.
        """
        self.gui_update_request.emit(label, value, unit, readonly, selector_list, clear_list)
        return
    
    def get_value(self):
        '''
        Public Method:
            Retrieves the current text displayed in the value field.
        
        Returns:
            str: Text currently displayed in value field.        
        '''
        return self.ui.value.currentText()

    
    def _update(self, label, value, unit, readonly, selector_list, clear_list):
        """
        Protected Method:
            Updates the GUI elements.
        Args:
            label (str) : Text to be displayed in label field.
            value (str) : Text to be displayed in value field.
            unit (str) : Text to be displayed in unit field.
            readonly (bool) : If value field is read only.
            selector_list (list) : list of possible values.
            clear_list (bool) : if the already existing values should be erased.
        """
        if label is not None:
            self.ui.label.setText(str(label))
            
        if unit is not None:
            self.ui.unit.setText(str(unit))

        if readonly is not None:
            self.ui.value.setEditable(False)
            if readonly:                        
                self.ui.value.setEnabled(False)   
                self.ui.value.setStyleSheet(self.value_base_stylesheet)            
            else:            
                self.ui.value.setEnabled(True)
                self.ui.value.setStyleSheet(self.value_base_stylesheet + 
                    """QLineEdit:hover{
                    background-color: #001F39;
                    border: 1px solid #00FFB9;
                    }
                    """)          
        if clear_list:
            self.ui.value.clear()    

        if selector_list is not None:
            self.ui.value.addItems(selector_list)

        if value is not None:
            self.ui.value.setCurrentText(str(value))
        return    
    
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
        self.window = Ui_CardComboBoxSetup(label="Medição", value="muitas", unit="batatas", readonly= False, selector_list=["muitas", "algumas", "poucas"])

###############################################################################
# 5. Test Main
###############################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = TestUser()
    user.window.show()
    
    app.exec()
