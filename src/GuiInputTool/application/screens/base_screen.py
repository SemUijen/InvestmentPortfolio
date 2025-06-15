import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GuiInputTool.application.application import (
        MainApplication as MainApplication,
    )


class InputField:
    def __init__(
        self,
        label: str,
        input_type: tk.StringVar | tk.DoubleVar | tk.IntVar,
        placeholder: str | None = None,
    ):
        self.label = label
        self.input_type = input_type
        self.field = input_type
        self.placeholder = placeholder


class BaseScreen:
    """Base class for all screens with common functionality."""

    def __init__(self, root: tk.Tk, app_controller: "MainApplication"):
        self.root = root
        self.app_controller = app_controller
        self.current_row = 0
        self.main_frame = ttk.Frame(self.root, padding="10")

    def add_input_fields(
        self,
        input_fields: list[InputField],
    ) -> None:
        """Create input fields for the GUI with placeholder support."""
        for field in input_fields:
            ttk.Label(self.main_frame, text=f"{field.label}:").grid(
                row=self.current_row,
                column=0,
                sticky=tk.W,
                pady=5,
            )

            entry = ttk.Entry(self.main_frame, textvariable=field.field)
            entry.grid(
                row=self.current_row,
                column=1,
                sticky="we",
                pady=5,
            )

            # Add placeholder functionality if placeholder text is provided
            if field.placeholder:
                self._add_placeholder(entry, field)

            self.current_row += 1

    def _add_placeholder(self, entry: ttk.Entry, field: InputField):
        """Add placeholder functionality to an entry widget."""

        def on_focus_in(event):
            """Remove placeholder text when entry gets focus."""
            if entry.get() == field.placeholder:
                entry.delete(0, tk.END)
                entry.configure(foreground="black")

        def on_focus_out(event):
            """Add placeholder text when entry loses focus and is empty."""
            if not entry.get():
                entry.insert(0, field.placeholder)
                entry.configure(foreground="gray")

        # Set initial placeholder
        entry.insert(0, field.placeholder)
        entry.configure(foreground="gray")

        # Bind focus events
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def destroy(self) -> None:
        """Clean up the screen."""
        self.main_frame.destroy()
