###############################################################################
# 1. Module Documentation
###############################################################################
"""
Module Name:
    gui_card_setup.py

Description:
    Provides the GUI_CARD_SETUP class, which implements a card widget used to
    display information in a structured format. Each card can contain multiple
    entries, where each entry consists of a label, value, and unit. The card
    can be customized with a title and supports both read-only and editable
    entries. 

Author:
    PF.
Date:
    2026-04-13
"""


###############################################################################
# 2. Imports
###############################################################################
# Standard library imports
import sys
from dataclasses import dataclass
import threading
from time import sleep

# Qt imports (PySide6)
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# Project-specific imports
from .gui_card import Ui_Card as UiCard
from .card_entry_setup import Ui_CardEntrySetup as GuiCardEntrySetup


###############################################################################
# 3. GUI Card Class
###############################################################################
class GuiCardSetup(QMainWindow):
    """
    Class:
        Provides an interface for the card UI.
    """

    events = Signal(str, QEvent)

    # -------------------------------------------------------------------------
    # Class initialization
    # -------------------------------------------------------------------------
    def __init__(self, title="Card Title", entries: object = []):

        super().__init__()

        # Variables Initializaion
        self.entries = entries

        # Build UI
        self.ui = UiCard()
        self.ui.setupUi(self)        

        # Set title
        self.ui.title.setText(title)
        
        # Add Entries
        self.entries_list = []        
        for entry in entries:     
            
            # Create a GUI entry for each provided entry and store it in the entries list
            register_ui = GuiCardEntrySetup(entry.attribute, entry.label, entry.value, entry.unit, entry.readonly)
            
            # Dynamically create an attribute for each entry using the provided attribute name
            setattr(self, entry.attribute, register_ui)

            # Connect the entry_events signal from the GUI entry to the card's _on_event handler, passing the entry's attribute as the key
            register_ui.entry_events.connect(self._on_event)

            # Append the created GUI entry to the entries list and add it to the card's layout
            self.entries_list.append(register_ui)
            self.ui.entries_layout.addWidget(register_ui)
            
    @dataclass    
    class CardEntry:
        """
        Class:
            Represents a single entry in the card, consisting of a label, value, unit, and read-only status.
        """
        attribute: str 
        label: str = ""
        value: str = ""
        unit: str = ""
        readonly: bool = False
        monitor_pressed: bool = False 

    # -------------------------------------------------------------------------
    # Protected methods
    # -------------------------------------------------------------------------
    def _on_event(self, key: str, event: QEvent):
        """
        Protected Method:
            Handler for when an entry emits an event (e.g., when its value field is pressed).     

        Args:
            key (str): The key associated with the entry value that was pressed.
        """
        self.events.emit(key, event)


###############################################################################
# 4. Test User Class (Simulation)
###############################################################################
class TestUser(QMainWindow):
    """
    Class:
        Simulates a user interacting with the GUI card by creating an instance of the card,
        populating it with example entries, and updating the values after a short delay.
    """

    # -------------------------------------------------------------------------
    # Class initialization
    # -------------------------------------------------------------------------
    def __init__(self):
                
        self.user_thread = None
        self.user_thread_event = threading.Event()        
        
        # Example entries    
        self.entries = [
            GuiCardSetup.CardEntry(attribute = "voltage_analog", label="Voltage AVDD", value = "22", unit="V", readonly=False),
            GuiCardSetup.CardEntry(attribute = "voltage_digital", label="Voltage DVDD", unit="V", readonly=False),
            GuiCardSetup.CardEntry(attribute = "plat_sn", label="Platform Serial Number", unit="V", readonly=True),    
            GuiCardSetup.CardEntry(attribute = "prod_sn", label="Product Serial Number", unit="V", readonly=True)        
        ]

        self.gui_card = GuiCardSetup(title="Electrical Parameters", entries=self.entries)     

        self.user_thread = threading.Thread(target=self._user_interaction, daemon=True)
        self.user_thread.start()      

    # -------------------------------------------------------------------------
    # Protected methods
    # -------------------------------------------------------------------------    
    def _user_interaction(self):
        """
        Protected Method:
            Simulates user interaction by updating the values of the card entries after a short delay.
        """
        print("Analog voltage:", self.gui_card.voltage_analog.get_value())

        self.gui_card.plat_sn.set_value("SI-0-0030-00.02.00-000022")
        self.gui_card.prod_sn.set_value("SI-0-0001-00.00.00-000006")


###############################################################################
# 5. Test Main
###############################################################################
if __name__ == "__main__":
       
    app = QApplication(sys.argv)
    user = TestUser()    
    user.gui_card.show()
    app.exec()