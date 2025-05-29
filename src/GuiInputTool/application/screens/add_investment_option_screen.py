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
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(1, weight=1)

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

    def _search_investment_options(self) -> None:
        """Search for investment options based on user input."""
        # Implement search logic here
        symbol = self.input_fields[0].field.get()
        if not symbol:
            self.app_controller.show_error("Please enter a stock symbol.")
            return

        data = self._get_symbol_data(symbol)

        self._display_search_results(data)

    def _get_symbol_data(self, symbol: str) -> dict:
        """Fetch data for a given symbol."""
        # Implement data fetching logic here
        try:
            base_url = BaseAPIurl(
                apikey=os.getenv("ALPHAVANTAGE_API_KEY"),
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
        if hasattr(self, "results_frame"):
            self.results_frame.destroy()

        # Create results frame
        self.results_frame = ttk.LabelFrame(
            self.main_frame,
            text="Search Results",
            padding="10",
        )
        self.results_frame.grid(
            row=self.current_row + 1,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E),
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
            io_type = result.get("3. type", "N/A")
            symbol = result.get("1. symbol", "N/A")
            name = result.get("2. name", "N/A")
            region = result.get("4. region", "N/A")
            currency = result.get("8. currency", "N/A")
            option_text = f" {name}: \n {io_type} - {symbol} - {region} - {currency}"

            ttk.Radiobutton(
                self.results_frame,
                text=option_text,
                variable=self.selected_option,
                value=f"{symbol}|{name}",  # Store both symbol and name
            ).pack(anchor=tk.W, pady=2)

        # Add select button
        ttk.Button(
            self.results_frame,
            text="Select Option",
            command=self._save_selected_option,
        ).pack(pady=10)

    def _save_selected_option(self) -> None:
        pass
