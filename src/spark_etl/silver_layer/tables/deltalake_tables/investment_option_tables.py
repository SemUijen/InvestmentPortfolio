import pyarrow as pa

from .deltalake_base_table import BaseTable


class InvestmentOption(BaseTable):
    """Investment Option Table in Silver Layer."""

    def return_defined_schema(self) -> pa.Schema:
        """Return the schema for the InvestmentOption table."""
        return pa.schema(
            [
                pa.field("symbol", pa.string()),
                pa.field("name", pa.string()),
                pa.field("type", pa.string()),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the InvestmentOption table."""
        return ["symbol"]


class IoStockExchange(BaseTable):
    """Investment Option Stock Exchange Table in Silver Layer."""

    def return_defined_schema(self) -> pa.Schema:
        """Return the schema for the IoStockExchange table."""
        return pa.schema(
            [
                pa.field("io_symbol", pa.string()),
                pa.field("exchange_symbol", pa.string()),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the IoStockExchange table."""
        return ["io_symbol", "exchange_symbol"]


class StockExchange(BaseTable):
    """Stock Exchange Table in Silver Layer."""

    def return_defined_schema(self) -> pa.Schema:
        """Return the schema for the StockExchange table."""
        return pa.schema(
            [
                pa.field("symbol", pa.string()),
                pa.field("region", pa.string()),
                pa.field("markt_open", pa.string()),
                pa.field("markt_close", pa.string()),
                pa.field("currency", pa.string()),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the StockExchange table."""
        return ["symbol"]
