###############################################################################
# 1. Module Level Documentation
###############################################################################
"""
Stock Tracker — application entry point.

Starts the PySide6 main window (`StockTrackerWindow`).
Business logic is not executed here; see `src.core.stock.StockTracker`.
"""

###############################################################################
# 2. Imports
###############################################################################
import sys

from PySide6.QtWidgets import QApplication

from src.gui.stock_tracker_window import StockTrackerWindow

###############################################################################
# 3. Constants and Global Variables
###############################################################################

###############################################################################
# 4. Public functions
###############################################################################


def main() -> None:
    """
    Public Function:
        Create the Qt application, show the main window, and run the event loop.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Stock Tracker")
    app.setOrganizationName("Siemens")
    window = StockTrackerWindow()
    window.show()
    sys.exit(app.exec())


###############################################################################
# 5. Script entry
###############################################################################
if __name__ == "__main__":
    main()
