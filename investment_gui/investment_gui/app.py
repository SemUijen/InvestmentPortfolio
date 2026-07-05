"""A simple GUI application for data input using PySide6."""

import sys

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from investment_gui.application import MainApplication


def main() -> int:
    """Start the application."""
    load_dotenv()  # moved here from base_screen.py: env setup is app startup, not a screen concern
    app = QApplication(sys.argv)
    window = MainApplication()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
