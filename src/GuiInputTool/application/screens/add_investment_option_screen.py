import tkinter as tk
from typing import TYPE_CHECKING

from .base_screen import BaseScreen

if TYPE_CHECKING:
    from src.GuiInputTool.application.application import MainApplication


class InvestmentOptionsScreen(BaseScreen):
    def __init__(self, root: tk.Tk, app_controller: "MainApplication"):
        super().__init__(root, app_controller)

        # Setup main frame
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(1, weight=1)
