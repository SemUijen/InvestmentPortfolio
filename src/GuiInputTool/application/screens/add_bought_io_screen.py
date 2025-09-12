import logging
import os
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import ttk
from typing import TYPE_CHECKING
from enum import StrEnum
from deltalake import DeltaTable

from src.spark_etl.silver_layer.tables.deltalake_tables import InvestmentOptionBought

from .base_screen import BaseScreen, InputField

if TYPE_CHECKING:
    from src.GuiInputTool.application.application import (
        MainApplication as MainApplication,
    )

class CurrencyEnum(StrEnum):
    """Enumeration for currency options."""
    USD = "USD"
    EUR = "EUR"


class BoughtInvestmentScreen(BaseScreen):
    """Screen for inputting stock investment data."""

    def __init__(
        self,
        root: tk.Tk,
        app_controller: "MainApplication",
        input_fields: list[InputField],
    ):
        super().__init__(root, app_controller)
        self.input_fields = input_fields

        # Create main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        self.current_row = 0

        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="Stock Investment Manager",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(0, 30), columnspan=2)
        self.current_row += 1

        self.add_symbol_dropdown()
        self.current_row += 1
        # Create all input fields
        self.add_input_fields(input_fields)
        # Create buttons
        self.create_buttons()

    def _get_symbols(self) -> list[str] | None:
        if not (DATA_DIR := os.getenv("DATA_DIR")):
            self.app_controller.show_error(
                "DATA_DIR is not set in the environment variables.",
            )
            return None

        path = Path(DATA_DIR) / "silver" / "investment_option"
        dt = DeltaTable(path).to_pyarrow_table()
        symbols = dt.column("symbol").to_pylist()
        if not symbols:
            self.app_controller.show_error("No symbols found in the database.")
            return None

        return symbols

    def add_symbol_dropdown(self) -> None:
        """Create a dropdown for selecting stock symbols."""
        symbols = self._get_symbols()
        if symbols is None:
            self.app_controller.show_error(
                "Failed to load symbols or no symbols found.",
            )
            return

        ttk.Label(self.main_frame, text="Symbol:").grid(
            row=self.current_row,
            column=0,
            sticky=tk.W,
            padx=5,
        )
        self.symbol_dropdown = ttk.Combobox(
            self.main_frame,
            values=symbols,
            state="readonly",
            width=20,
        )
        self.symbol_dropdown.grid(row=self.current_row, column=1, pady=5, sticky="we")
        self.symbol_dropdown.set("Select Symbol")

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
        ttk.Button(button_frame, text="Save", command=self.save_data).pack(
            side=tk.LEFT,
            padx=(0, 10),
        )

        # Clear button
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(
            side=tk.LEFT,
            padx=(0, 10),
        )

        ttk.Button(
            button_frame,
            text="Back to Main",
            command=self.app_controller.show_startup_screen,
        ).pack(side=tk.LEFT)


    def save_data(self) -> None:
        """Save the input data to the Delta table."""
        # Get the selected symbol from dropdown
        selected_symbol = self.symbol_dropdown.get()
        if selected_symbol == "Select Symbol" or not selected_symbol:
            self.app_controller.show_error("Please select a symbol.")
            return

        # Collect data from input fields
        data = {}
        for field in self.input_fields:
            field_name = field.label.lower().replace(" ", "_")
            if not field.field.get() or field.field.get() == field.placeholder:
                self.app_controller.show_error(
                    f"Please fill in the {field.label} field.",
                )
                return
            data[field_name] = field.field.get()  # Validate required fields

        date_str = str(data.get("purchase_date", ""))
        try:
            parsed_date = datetime.strptime(
                date_str,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            error_msg = "Please enter date in YYYY-MM-DD format."
            self.app_controller.show_error(error_msg)
            return

        try:
            currency = CurrencyEnum(data.get("currency", ""))
        except ValueError:
            self.app_controller.show_error(
                f"Invalid currency selected, should be one of:"
                 f" {', '.join([c.value for c in CurrencyEnum])}"
            )
            return

        # Map the GUI field names to the expected schema field names
        try:
            # Prepare data for the delta table with correct field names
            table_data = {
                "symbol": [selected_symbol],
                "date_bought": [parsed_date],
                "price": [float(data.get("purchase_price", ""))],
                "amount": [int(data.get("quantity", 0))],
                "cost_of_buy": [float(data.get("cost_of_buy", ""))],
                "currency": [currency.value],
                "broker": [data.get("broker")],
            }

            # Create table instance and merge data
            bought_investment_table = InvestmentOptionBought()
            bought_investment_table.merge_from_dict(table_data)

            self.app_controller.show_info("Investment data saved successfully!")
            self.clear_fields()

        except (ValueError, ImportError, OSError) as e:
            self.app_controller.show_error(f"Error saving data: {e!s}")
            logging.exception("Error saving investment data")

    def clear_fields(self) -> None:
        """Clear all input fields."""
        # Clear the symbol dropdown
        self.symbol_dropdown.set("Select Symbol")

        # Clear all input fields
        for field in self.input_fields:
            if isinstance(field.field, tk.StringVar):
                field.field.set("")
            elif isinstance(field.field, tk.DoubleVar):
                field.field.set(0.0)
            elif isinstance(field.field, tk.IntVar):
                field.field.set(0)
