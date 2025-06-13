"""A simple GUI application for data input using Tkinter."""

import tkinter as tk

from .data_input_gui import DataInputGUI, InputField


def main() -> None:
    """Main function to run the GUI application."""
    root = tk.Tk()
    input_fields = [
        InputField("Date Bought", tk.StringVar),
        InputField("Quantity Bought", tk.IntVar),
        InputField("Price Bought", tk.DoubleVar),
        InputField("Cost of Buy", tk.DoubleVar),
    ]
    DataInputGUI(root, input_fields=input_fields)
    root.mainloop()


if __name__ == "__main__":
    main()
