"""Stock Tracker — legacy demo UI (green/red buttons, pre-Siemens template)."""
import sys

from PySide6.QtWidgets import QApplication

from src.gui.demo.window import DemoStockTrackerWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Stock Tracker Demo")
    app.setOrganizationName("Siemens")
    window = DemoStockTrackerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
