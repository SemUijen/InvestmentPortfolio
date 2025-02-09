import json
import os
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk

from dotenv import load_dotenv

from src.stockprobe.alphavantage.url_generator.base_url import BaseAPIurl

load_dotenv()


class DataInputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Input Application")
        self.root.geometry("400x500")

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initialize input fields
        self.create_input_fields()

        # Create buttons
        self.create_buttons()

    def create_input_fields(self):
        # Name symbol
        ttk.Label(self.main_frame, text="Symbol:").grid(
            row=0,
            column=0,
            sticky=tk.W,
            pady=5,
        )
        self.symbol = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.symbol).grid(
            row=0,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5,
        )

        # date_bought input
        ttk.Label(self.main_frame, text="Date bought ('YYYY-mm-dd'): 2024-12-31").grid(
            row=1,
            column=0,
            sticky=tk.W,
            pady=5,
        )
        self.date_bought_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.date_bought_var).grid(
            row=1,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5,
        )

        # Price input
        ttk.Label(self.main_frame, text="Price Bought:").grid(
            row=2,
            column=0,
            sticky=tk.W,
            pady=5,
        )
        self.price_bought = tk.DoubleVar()
        ttk.Entry(self.main_frame, textvariable=self.price_bought).grid(
            row=2,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5,
        )

        # Quantity input
        ttk.Label(self.main_frame, text="Quantity:").grid(
            row=3,
            column=0,
            sticky=tk.W,
            pady=5,
        )

        self.quantity = tk.IntVar()
        ttk.Entry(self.main_frame, textvariable=self.quantity).grid(
            row=3,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5,
        )

        # Comment
        ttk.Label(
            self.main_frame,
            text="Note: Setting quantity to zero will overwrite existing data.",
            foreground="red",
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky=tk.W,
            pady=5,
        )

    def create_buttons(self):
        # Save button
        ttk.Button(self.main_frame, text="Save", command=self.save_data).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=20,
        )

        # Clear button
        ttk.Button(self.main_frame, text="Clear", command=self.clear_fields).grid(
            row=6,
            column=0,
            columnspan=2,
        )

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

        # Validate date format
        try:
            datetime.strptime(self.date_bought_var.get(), "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid date format. Please use 'YYYY-mm-dd'.")

        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return False

        return True

    def save_data(self):
        if not self.validate_input():
            return

        data = {
            "symbol": self.symbol.get(),
            "date_bought": self.date_bought_var.get(),
            "price": self.price_bought.get(),
            "quantity": self.quantity.get(),
        }
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

    def clear_fields(self):
        self.symbol.set("")
        self.date_bought_var.set("")
        self.price_bought.set(0.0)
        self.quantity.set(0)


def main():
    root = tk.Tk()
    app = DataInputGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
