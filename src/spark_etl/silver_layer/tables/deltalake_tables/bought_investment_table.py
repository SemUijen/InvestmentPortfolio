import pyarrow as pa

from .deltalake_base_table import BaseTable


class InvestmentOptionBought(BaseTable):
    """Investment Option Bought Table in Silver Layer."""

    def __init__(self):
        """Initialize the InvestmentOptionBought table."""
        super().__init__()

    def return_defined_schema(self) -> pa.Schema:
        """Return the schema for the InvestmentOptionBought table."""
        fields: list[tuple[str, pa.DataType]] = [
            ("symbol", pa.string()),
            ("date_bought", pa.date32()),
            ("price", pa.float64()),
            ("amount", pa.float64()),
            ("cost_of_buy", pa.float64()),
            ("broker", pa.string()),
        ]

        return pa.schema(fields=fields)

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the InvestmentOptionBought table."""
        return ["symbol", "date_bought", "price", "broker"]
