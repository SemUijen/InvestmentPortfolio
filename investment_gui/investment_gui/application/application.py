"""Main application controller for the investment GUI (PySide6)."""

import datetime

from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from .screens import (
    BoughtInvestmentScreen,
    CurrencyEnum,
    InputField,
    InvestmentOptionsScreen,
    StartupScreen,
)


class MainApplication(QMainWindow):
    """Main window that manages the different screens via a QStackedWidget."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Stock Investment Manager")
        self.resize(500, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Screens are created once and switched, not destroyed and rebuilt.
        self.startup_screen = StartupScreen(self)

        self.bought_screen = BoughtInvestmentScreen(
            self,
            input_fields=[
                InputField("Quantity", float),
                InputField("Purchase Price", float),
                InputField("Purchase Date", datetime.date),
                InputField("Cost of Buy", float),
                InputField("Currency", str, choices=[c.value for c in CurrencyEnum]),
                InputField("Exchange Rate", float),
                InputField("Broker", str, "e.g. degiro"),
            ],
        )

        self.options_screen = InvestmentOptionsScreen(
            self,
            input_fields=[
                InputField("Symbol", str, "e.g. 'VWCE' for Vanguard FTSE All-World"),
            ],
        )

        for screen in (self.startup_screen, self.bought_screen, self.options_screen):
            self.stack.addWidget(screen)

        self.show_startup_screen()

    # ------------------------------------------------------------ navigation
    def show_startup_screen(self) -> None:
        """Display the startup/main menu screen."""
        self.stack.setCurrentWidget(self.startup_screen)

    def show_data_input_screen(self) -> None:
        """Display the data input screen if its data can be loaded."""
        if self.bought_screen.prepare():
            self.stack.setCurrentWidget(self.bought_screen)

    def show_investment_options_screen(self) -> None:
        """Display the add investment options screen if it is usable."""
        if self.options_screen.prepare():
            self.stack.setCurrentWidget(self.options_screen)

    # --------------------------------------------------------------- dialogs
    def show_error(self, message: str) -> None:
        """Display an error message in a popup."""
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message: str) -> None:
        """Display an informational message in a popup."""
        QMessageBox.information(self, "Info", message)
