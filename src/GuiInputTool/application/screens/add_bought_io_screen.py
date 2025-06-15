import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

from .base_screen import BaseScreen, InputField

if TYPE_CHECKING:
    from src.GuiInputTool.application.application import (
        MainApplication as MainApplication,
    )


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

        # Create all input fields
        self.add_input_fields(input_fields)
        # Create buttons
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
