"""Screen for searching and adding investment options (PySide6)."""

import logging
import os
from typing import TYPE_CHECKING

import requests
from investment_etl.bronze_layer.stockprobe.alphavantage.url_generator import (
    TimeSeriesDailyURL,
)
from investment_etl.silver_layer.tables.deltalake_tables import (
    InvestmentOption,
    IoStockExchange,
    StockExchange,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QButtonGroup,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

from .base_screen import BaseScreen, InputField, ValidationError

if TYPE_CHECKING:
    from investment_gui.application import MainApplication


class InvestmentOptionsScreen(BaseScreen):
    """Search AlphaVantage for symbols and save the chosen option."""

    def __init__(
        self,
        app_controller: "MainApplication",
        input_fields: list[InputField],
    ) -> None:
        super().__init__(app_controller)

        self.add_input_fields(input_fields)

        # Search / navigation buttons
        buttons = QHBoxLayout()
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self._search_investment_options)
        buttons.addWidget(self.search_btn)

        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.app_controller.show_startup_screen)
        buttons.addWidget(back_btn)
        self.layout.addLayout(buttons)

        # Results area (hidden until the first search)
        self.results_group = QGroupBox("Search Results")
        self.results_layout = QVBoxLayout(self.results_group)
        self.results_group.hide()
        self.layout.addWidget(self.results_group)

        self.radio_group = QButtonGroup(self)
        self._results: list[dict] = []  # raw API results, indexed by radio id

        self.layout.addStretch()

    # ------------------------------------------------------------ precondition
    def prepare(self) -> bool:
        """Check preconditions before the screen is shown.

        Returns False (blocking navigation) when the AlphaVantage API key is
        missing, since the screen is unusable without it.
        """
        if not os.getenv("ALPHAVANTAGE_API_KEY"):
            self.app_controller.show_error(
                "ALPHAVANTAGE_API_KEY is not set in the environment variables.",
            )
            return False
        return True

    # ---------------------------------------------------------------- search
    def _search_investment_options(self) -> None:
        """Search for investment options based on user input."""
        try:
            values = self.get_values()
        except ValidationError:
            self.app_controller.show_error("Please enter a stock symbol.")
            return

        symbol = str(values["Symbol"])

        # Synchronous request (max 10s); show the user something is happening.
        self.search_btn.setEnabled(False)
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))
        try:
            data = self._get_symbol_data(symbol)
        finally:
            self.search_btn.setEnabled(True)
            self.unsetCursor()

        self._display_search_results(data)

    def _get_symbol_data(self, symbol: str) -> dict:
        """Fetch data for a given symbol."""
        if not (apikey := os.getenv("ALPHAVANTAGE_API_KEY")):
            self.app_controller.show_error(
                "ALPHAVANTAGE_API_KEY is not set in the environment variables.",
            )
            return {}
        try:
            base_url = TimeSeriesDailyURL(apikey=apikey, symbol=symbol)
            response = requests.get(base_url.return_search_url(), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            self.app_controller.show_error(f"Error fetching data: {exc}")
            return {}

    # --------------------------------------------------------------- results
    def _display_search_results(self, data: dict) -> None:
        """Display the search results as radio buttons for user selection."""
        self._clear_results()
        self.results_group.show()

        results = data.get("bestMatches", [])
        if not results:
            self.results_layout.addWidget(QLabel("No results found"))
            return

        self._results = results
        for i, result in enumerate(results):
            name = result.get("2. name")
            symbol = result.get("1. symbol")
            io_type = result.get("3. type")
            region = result.get("4. region")
            currency = result.get("8. currency")

            radio = QRadioButton(
                f"{name}:\n  {io_type} - {symbol} - {region} - {currency}"
            )
            self.radio_group.addButton(radio, i)  # id == index into self._results
            self.results_layout.addWidget(radio)

        select_btn = QPushButton("Select Option")
        select_btn.clicked.connect(self._save_selected_option)
        self.results_layout.addWidget(select_btn)

    def _clear_results(self) -> None:
        """Remove all widgets from the results group."""
        for button in self.radio_group.buttons():
            self.radio_group.removeButton(button)
        while (item := self.results_layout.takeAt(0)) is not None:
            if (widget := item.widget()) is not None:
                widget.deleteLater()
        self._results = []

    # ------------------------------------------------------------------ save
    def _save_selected_option(self) -> None:
        """Save the selected investment option to the database."""
        checked_id = self.radio_group.checkedId()
        if checked_id == -1:
            self.app_controller.show_error("Please select an investment option.")
            return

        result = self._results[checked_id]
        symbol = result.get("1. symbol") or ""

        if "." not in symbol:
            self.app_controller.show_error(
                f"Symbol '{symbol}' has no exchange suffix (expected e.g. 'VWCE.DEX'). "
                "Cannot determine the stock exchange.",
            )
            return
        io_symbol, _, exchange_symbol = symbol.partition(".")

        data = {
            "investment_option": {
                "symbol": [io_symbol],
                "name": [result.get("2. name")],
                "type": [result.get("3. type")],
            },
            "io_stock_exchange": {
                "io_symbol": [io_symbol],
                "exchange_symbol": [exchange_symbol],
            },
            "stock_exchange": {
                "symbol": [exchange_symbol],
                "region": [result.get("4. region")],
                "markt_open": [result.get("5. marketOpen")],
                "markt_close": [result.get("6. marketClose")],
                "currency": [result.get("8. currency")],
            },
        }

        try:
            InvestmentOption().merge_from_dict(data["investment_option"])
            IoStockExchange().merge_from_dict(data["io_stock_exchange"])
            StockExchange().merge_from_dict(data["stock_exchange"])
            self.app_controller.show_info("Investment option saved successfully!")
        except Exception as exc:  # noqa: BLE001 - surface any persistence failure
            self.app_controller.show_error(f"Error saving investment option: {exc}")
            logging.exception("Error saving investment option")