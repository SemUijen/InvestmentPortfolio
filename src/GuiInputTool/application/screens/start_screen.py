import tkinter as tk
from tkinter import ttk


class StartupScreen:
    """Startup screen with navigation options."""

    def __init__(self, root, app_controller):
        self.root = root
        self.app_controller = app_controller

        # Create main frame
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure frame grid
        self.frame.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(
            self.frame,
            text="Stock Investment Manager",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(0, 30))

        # Navigation buttons
        data_input_btn = ttk.Button(
            self.frame,
            text="Data Input",
            command=self.app_controller.show_data_input_screen,
            width=20,
        )
        data_input_btn.grid(row=1, column=0, pady=10)

        investment_options_btn = ttk.Button(
            self.frame,
            text="Add Investment Options",
            command=self.app_controller.show_investment_options_screen,
            width=20,
        )
        investment_options_btn.grid(row=2, column=0, pady=10)

    def destroy(self):
        """Clean up the screen."""
        self.frame.destroy()
