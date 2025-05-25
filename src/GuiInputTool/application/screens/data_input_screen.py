import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

from dotenv import load_dotenv

from src.stockprobe.alphavantage.url_generator.base_url import BaseAPIurl

from .base_screen import BaseScreen, InputField

load_dotenv()
if TYPE_CHECKING:
    from src.GuiInputTool.application.application import (
        MainApplication as MainApplication,
    )


class DataInputScreen(BaseScreen):
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
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
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

        # add input fields
        self.add_standard_fields()
        self.input_fields = input_fields
        self.add_input_fields(input_fields)

        # Create buttons
        self.create_buttons()

    def add_standard_fields(self) -> None:
        """Add standard input fields to the GUI."""
        ttk.Label(self.main_frame, text="Symbol:").grid(
            row=self.current_row,
            column=0,
            sticky=tk.W,
            pady=5,
        )
        self.symbol = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.symbol).grid(
            row=self.current_row,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5,
        )
        self.current_row += 1

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

    def validate_input(self):
        api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if not api_key:
            error_message = (
                "No API key found. Please set the API_KEY environment variable."
            )
            raise ValueError(error_message)
        # validate symbol
        errors = []

        # Validate symbol
        try:
            self.url_generator = BaseAPIurl(
                apikey=api_key,
                symbol=self.symbol.get(),
                validate_symbol=True,
            )
        except ValueError as e:
            errors.append(f"Invalid symbol: {e!s}")

        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return False

        return True

    def save_data(self) -> None:
        """Save the input data to a JSON file."""
        if not self.validate_input():
            return

        data = {}
        for field in self.input_fields:
            data[field.label.lower().replace(" ", "_")] = field.field.get()

        try:
            data_dir = Path(os.getenv("DATA_DIR")) / "bronze" / "bought_stocks"
            # Create data directory if it doesn't exist
            data_dir.mkdir(parents=True, exist_ok=True)

            # Save data to JSON file
            with open(data_dir / "user_data.json", "w") as f:
                json.dump(data, f, indent=4)

            messagebox.showinfo("Success", "Data saved successfully!")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e!s}")

    def clear_fields(self) -> None:
        """Clear all input fields."""
        self.symbol.set("")
        # Clear all input fields
        for field in self.input_fields:
            field.field.set("")

    def destroy(self):
        """Clean up the screen."""
        self.main_frame.destroy()
