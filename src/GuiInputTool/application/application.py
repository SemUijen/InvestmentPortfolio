import tkinter as tk

from .screens import DataInputScreen, InputField, StartupScreen


class MainApplication:
    """Main application controller that manages different screens."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock Investment Manager")
        self.root.geometry("500x600")

        # Configure grid weight for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Current screen reference
        self.current_screen = None

        # Show startup screen initially
        self.show_startup_screen()

    def clear_screen(self):
        """Clear the current screen."""
        if self.current_screen:
            self.current_screen.destroy()

    def show_startup_screen(self):
        """Display the startup/main menu screen."""
        self.clear_screen()
        self.current_screen = StartupScreen(self.root, self)

    def show_data_input_screen(self):
        """Display the data input screen."""
        self.clear_screen()

        # Define the input fields you want
        input_fields = [
            InputField("Quantity", None, tk.DoubleVar),
            InputField("Purchase Price", None, tk.DoubleVar),
            InputField("Purchase Date", "YYYY-mm-dd", tk.StringVar),
            InputField("Cost of Buy", "23.95", tk.DoubleVar),
            InputField("Stock Exchange", "AMS for Amsterdam", tk.StringVar),
            InputField("Broker", "DeGiro", tk.StringVar),
        ]

        self.current_screen = DataInputScreen(self.root, self, input_fields)

    def show_investment_options_screen(self):
        """Display the add investment options screen."""
        self.clear_screen()
        # We'll implement this later
        print("Navigate to Investment Options Screen")

    def run(self):
        """Start the application."""
        self.root.mainloop()
