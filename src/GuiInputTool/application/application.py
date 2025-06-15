import tkinter as tk

from .screens import (
    BaseScreen,
    BoughtInvestmentScreen,
    InputField,
    InvestmentOptionsScreen,
    StartupScreen,
)


class MainApplication:
    """Main application controller that manages different screens."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Stock Investment Manager")
        self.root.geometry("500x600")

        # Configure grid weight for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Current screen reference
        self.current_screen: BaseScreen | None = None

        # Show startup screen initially
        self.show_startup_screen()

    def clear_screen(self) -> None:
        """Clear the current screen."""
        if self.current_screen:
            self.current_screen.destroy()

    def show_startup_screen(self) -> None:
        """Display the startup/main menu screen."""
        self.clear_screen()
        self.current_screen = StartupScreen(self.root, self)

    def show_data_input_screen(self) -> None:
        """Display the data input screen."""
        self.clear_screen()

        # Define the input fields you want
        input_fields = [
            InputField(
                "Symbol",
                tk.StringVar(),
                "e.g. 'VWCE' for Vanguard FTSE All-World ",
            ),
            InputField("Quantity", tk.DoubleVar()),
            InputField("Purchase Price", tk.DoubleVar()),
            InputField("Purchase Date", tk.StringVar(), "YYYY-mm-dd"),
            InputField("Cost of Buy", tk.DoubleVar()),
            InputField("Stock Exchange", tk.StringVar(), "e.g. 'AMS' for Amsterdam"),
            InputField(
                "Broker",
                tk.StringVar(),
                "e.g. degiro",
            ),
        ]

        self.current_screen = BoughtInvestmentScreen(self.root, self, input_fields)

    def show_investment_options_screen(self) -> None:
        """Display the add investment options screen."""
        self.clear_screen()

        # Define the input fields you want
        input_fields = [
            InputField(
                "Symbol",
                tk.StringVar(),
                "e.g. 'VWCE' for Vanguard FTSE All-World ",
            ),
        ]

        self.current_screen = InvestmentOptionsScreen(self.root, self, input_fields)

    def run(self) -> None:
        """Start the application."""
        self.root.mainloop()
