"""Screen for inputting bought stock investment data (PySide6)."""

import logging
import os
from decimal import Decimal
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

from deltalake import DeltaTable
from investment_etl.silver_layer.tables.deltalake_tables import InvestmentOptionBought
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton

from .base_screen import BaseScreen, InputField, ValidationError

if TYPE_CHECKING:
    from investment_gui.application import MainApplication


class CurrencyEnum(StrEnum):
    """Enumeration for currency options."""

    USD = "USD"
    EUR = "EUR"


class BoughtInvestmentScreen(BaseScreen):
    """Screen for inputting stock investment data."""

    def __init__(
        self,
        app_controller: "MainApplication",
        input_fields: list[InputField],
    ) -> None:
        super().__init__(app_controller)

        title = QLabel("Stock Investment Manager")
        font = title.font()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.insertWidget(0, title)  # above the form

        # Symbol dropdown as the first form row
        self.symbol_combo = QComboBox()
        self.symbol_combo.setPlaceholderText("Select Symbol")
        self.symbol_combo.setCurrentIndex(-1)
        self.form.addRow("Symbol:", self.symbol_combo)

        self.add_input_fields(input_fields)
        self._create_buttons()
        self.layout.addStretch()

    # ------------------------------------------------------------------ setup
    def _create_buttons(self) -> None:
        buttons = QHBoxLayout()

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_data)
        buttons.addWidget(save_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_fields)
        buttons.addWidget(clear_btn)

        back_btn = QPushButton("Back to Main")
        back_btn.clicked.connect(self.app_controller.show_startup_screen)
        buttons.addWidget(back_btn)

        self.layout.addLayout(buttons)

    # ---------------------------------------------------------------- symbols
    def prepare(self) -> bool:
        """Load symbols before the screen is shown.

        Called by the controller on every navigation to this screen, so newly
        added investment options always appear. Returns False (blocking
        navigation) when symbols cannot be loaded.
        """
        return self._refresh_symbols()

    def _refresh_symbols(self) -> bool:
        symbols = self._get_symbols()
        if symbols is None:
            return False

        previous = self.symbol_combo.currentText()
        self.symbol_combo.clear()
        self.symbol_combo.addItems(symbols)
        if previous in symbols:
            self.symbol_combo.setCurrentText(previous)
        else:
            self.symbol_combo.setCurrentIndex(-1)  # show placeholder
        return True

    def _get_symbols(self) -> list[str] | None:
        if not (data_dir := os.getenv("DATA_DIR")):
            self.app_controller.show_error(
                "DATA_DIR is not set in the environment variables.",
            )
            return None

        path = Path(data_dir) / "silver" / "investment_option"
        try:
            table = DeltaTable(path).to_pyarrow_table()
        except Exception as exc:  # noqa: BLE001 - surface any table failure to the user
            self.app_controller.show_error(f"Failed to load symbols: {exc!s}")
            logging.exception("Failed to load symbols from Delta table")
            return None

        symbols = table.column("symbol").to_pylist()
        if not symbols:
            self.app_controller.show_error("No symbols found in the database.")
            return None
        return symbols

    # ------------------------------------------------------------------- save
    def save_data(self) -> None:
        """Save the input data to the Delta table."""
        if self.symbol_combo.currentIndex() == -1:
            self.app_controller.show_error("Please select a symbol.")
            return
        selected_symbol = self.symbol_combo.currentText()

        try:
            values = self.get_values()
        except ValidationError as exc:
            self.app_controller.show_error(str(exc))
            return

        def quantize_decimal(value: object, scale: int) -> Decimal:
            """Quantize a decimal value to the specified precision and scale."""
            quantize_str = "1." + "0" * scale
            return Decimal(str(value)).quantize(Decimal(quantize_str))

        try:
            table_data = {
                "symbol": [selected_symbol],
                "date_bought": [values["Purchase Date"]],  # datetime.date from QDateEdit
                "price": [quantize_decimal(values["Purchase Price"], 10)],
                "amount": [quantize_decimal(values["Quantity"], 10)],
                "cost_of_buy": [quantize_decimal(values["Cost of Buy"], 10)],
                "currency": [CurrencyEnum(values["Currency"]).value],
                "exchange_rate": [quantize_decimal(values["Exchange Rate"], 19)],
                "broker": [values["Broker"]],
            }

            bought_investment_table = InvestmentOptionBought()
            bought_investment_table.merge_from_dict(table_data)

            self.app_controller.show_info("Investment data saved successfully!")
            self.clear_fields()

        except (ValueError, ImportError, OSError) as exc:
            self.app_controller.show_error(f"Error saving data: {exc!s}")
            logging.exception("Error saving investment data")

    # ------------------------------------------------------------------ clear
    def clear_fields(self) -> None:
        """Clear all input fields and reset the symbol dropdown."""
        self.symbol_combo.setCurrentIndex(-1)
        super().clear_fields()