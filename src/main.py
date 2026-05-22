"""
Stock Tracker — ponto de entrada da aplicacao.

Arranque da interface grafica PySide6 (inventario de componentes).
"""
import sys

from PySide6.QtWidgets import QApplication

from src.gui.stock_tracker_window import StockTrackerWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Stock Tracker")
    app.setOrganizationName("Siemens")
    window = StockTrackerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
