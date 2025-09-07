import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from .base_screen import BaseScreen


class StartupScreen(BaseScreen):
    """Startup screen with navigation options."""

    def __init__(self, root, app_controller):
        """Initialize the startup screen with navigation buttons."""
        super().__init__(root, app_controller)
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure frame grid
        self.main_frame.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="Stock Investment Manager",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(0, 30))

        # Navigation buttons
        data_input_btn = ttk.Button(
            self.main_frame,
            text="Data Input",
            command=self.app_controller.show_data_input_screen,
            width=20,
        )
        data_input_btn.grid(row=1, column=0, pady=10)

        investment_options_btn = ttk.Button(
            self.main_frame,
            text="Add Investment Options",
            command=self.app_controller.show_investment_options_screen,
            width=20,
        )
        investment_options_btn.grid(row=2, column=0, pady=10)

        run_pipeline_btn = ttk.Button(
            self.main_frame,
            text="Run Medaillon Pipeline",
            command=self.run_medaillon_pipeline,
            width=20,
        )
        run_pipeline_btn.grid(row=3, column=0, pady=10)

    def run_medaillon_pipeline(self):
        """Run the Medaillon ETL pipeline."""
        try:
            self.app_controller.show_info("Running Medaillon pipeline...")
            root_folder = Path(__file__).resolve().parents[3]
            subprocess.run(
                ["docker-compose", "run", "--rm", "run-medaillon-pipeline"],
                check=True,
                cwd=root_folder,
            )
            self.app_controller.show_info("Medaillon pipeline completed successfully!")
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running Medaillon pipeline: {e}"
            self.app_controller.show_error(error_msg)
