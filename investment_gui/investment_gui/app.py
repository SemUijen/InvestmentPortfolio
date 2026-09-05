"""A simple GUI application for data input using PySide6."""

import sys

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from investment_gui.application import MainApplication
from investment_gui.application.screens.settings_dialog import GUI_ENV_PATH


def main() -> int:
    """Start the application."""
    load_dotenv(GUI_ENV_PATH)  # the .env next to the GUI package; Settings writes it
    app = QApplication(sys.argv)
    window = MainApplication()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
