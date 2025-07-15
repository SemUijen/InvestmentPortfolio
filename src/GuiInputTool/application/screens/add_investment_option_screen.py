import os
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

import requests
from dotenv import load_dotenv

from src.stockprobe.alphavantage.url_generator.base_url import BaseAPIurl

from .base_screen import BaseScreen, InputField

if TYPE_CHECKING:
    from src.GuiInputTool.application.application import MainApplication

load_dotenv()


class InvestmentOptionsScreen(BaseScreen):
    def __init__(
        self,
        root: tk.Tk,
        app_controller: "MainApplication",
        input_fields: list[InputField],
    ):
        """Initialize the Investment Options screen"""
        super().__init__(root, app_controller)
        self.input_fields = input_fields
        # Setup main frame
        self.main_frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        self.main_frame.columnconfigure(1, weight=1)

        self.results_frame: ttk.Labelframe | None = None
        self.add_input_fields(input_fields)
        self.create_buttons()

    def create_buttons(self) -> None:
        """Create buttons for saving and clearing data."""
        # NEW - buttons are placed in a horizontal frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(
            row=self.current_row,
            column=0,
            columnspan=2,
            pady=20,
        )

        # Save button
        ttk.Button(
            button_frame,
            text="Search",
            command=self._search_investment_options,
        ).pack(
            side=tk.LEFT,
            padx=(0, 10),
        )

        # Save button
        ttk.Button(
            button_frame,
            text="Back to Main Menu",
            command=self.app_controller.show_startup_screen,
        ).pack(
            side=tk.LEFT,
            padx=(0, 10),
        )

    def _search_investment_options(self) -> None:
        """Search for investment options based on user input."""
        # Implement search logic here
        symbol = self.input_fields[0].field.get()
        if not symbol:
            self.app_controller.show_error("Please enter a stock symbol.")
            return

        data = self._get_symbol_data(str(symbol))

        self._display_search_results(data)

    def _get_symbol_data(self, symbol: str) -> dict:
        """Fetch data for a given symbol."""
        # Implement data fetching logic here
        try:
            if not (apikey := os.getenv("ALPHAVANTAGE_API_KEY")):
                self.app_controller.show_error(
                    "ALPHAVANTAGE_API_KEY is not set in the environment variables.",
                )
                return {}
            base_url = BaseAPIurl(
                apikey=apikey,
                symbol=symbol,
                validate_symbol=False,
            )
            response = requests.get(base_url.return_search_url(), timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.RequestException as e:
            self.app_controller.show_error(f"Error fetching data: {e}")
            return {}

    def _display_search_results(self, data: dict) -> None:
        """Display the top 5 search results for user selection."""
        # Clear any existing results
        if self.results_frame:
            self.results_frame.destroy()

        # Create results frame
        self.results_frame = ttk.Labelframe(
            self.main_frame,
            text="Search Results",
            padding="10",
        )
        self.results_frame.grid(
            row=self.current_row + 1,
            column=0,
            columnspan=2,
            sticky=tk.W + tk.E,
            pady=20,
        )

        # Get top 5 results (adjust based on your API response structure)
        results = data.get("bestMatches", [])  # Assuming 'bestMatches' key

        if not results:
            ttk.Label(self.results_frame, text="No results found").pack()
            return

        # Variable to store selected option
        self.selected_option = tk.StringVar()

        # Display each result as a radio button
        for i, result in enumerate(results):
            # Adjust these keys based on your API response structure
            try:
                symbol = result.get("1. symbol")
                name = result.get("2. name")
                io_type = result.get("3. type")
                region = result.get("4. region")
                market_open = result.get("5. marketOpen")
                market_close = result.get("6. marketClose")
                time_zone = result.get("7. timezone")
                currency = result.get("8. currency")
            except KeyError as e:
                self.app_controller.show_error(
                    f"Missing data in result: {e}. Please check the API response.",
                )
                return

            option_text = f" {name}: \n {io_type} - {symbol} - {region} - {currency}"

            ttk.Radiobutton(
                self.results_frame,
                text=option_text,
                variable=self.selected_option,
                value=(
                    f"{symbol}|{name}|{io_type}|{region}|"
                    f"{market_open}|{market_close}|{time_zone}|{currency}"
                ),  # Store all relevant data in the value
            ).pack(anchor=tk.W, pady=2)

        # Add select button
        ttk.Button(
            self.results_frame,
            text="Select Option",
            command=self._save_selected_option,
        ).pack(pady=10)

    def _save_selected_option(self) -> None:
        """Save the selected investment option to the database."""
        selected_value = str(self.selected_option.get())
        if not selected_value:
            self.app_controller.show_error("Please select an investment option.")
            return

        (
            symbol,
            name,
            io_type,
            region,
            market_open,
            market_close,
            time_zone,
            currency,
        ) = selected_value.split("|")
        io_symbol, exchange_symbol = symbol.split(".")

        # Prepare data as JSON
        data = {
            "investment_option": {
                "symbol": io_symbol,
                "name": name,
                "type": io_type,
            },
            "io_stock_exchange": {
                "io_symbol": io_symbol,
                "exchange_symbol": exchange_symbol,
            },
            "stock_exchange": {
                "symbol": exchange_symbol,
                "region": region,
                "markt_open": market_open,
                "markt_close": market_close,
                "currency": currency,
            },
        }

        # Call Docker container to process the data
        try:
            import json
            import subprocess

            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--entrypoint=",  # Add this line to override default entrypoint
                    "-v",
                    f"{os.getenv('DATA_DIR')}:/data",
                    "-e",
                    "DATA_DIR=/data",
                    "investment-portfolio",
                    "python3",
                    "-c",
                    f"import json; from src.spark_etl.silver_layer.tables import *; data={json.dumps(data)}; InvestmentOption().merge_dict_data(data['investment_option']); IoStockExchange().merge_dict_data(data['io_stock_exchange']); StockExchange().merge_dict_data(data['stock_exchange'])",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                self.app_controller.show_info("Investment option saved successfully.")
            else:
                self.app_controller.show_error(f"Error saving data: {result.stderr}")

        except Exception as e:
            self.app_controller.show_error(f"Error running Docker: {e}")
