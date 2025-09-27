"""Investment Option related Delta Lake Tables in Silver Layer."""

import pyarrow as pa

from investment_etl.utils import DeltaLakeTable


class InvestmentOption(DeltaLakeTable):
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


class IoStockExchange(DeltaLakeTable):
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


class StockExchange(DeltaLakeTable):
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
        return ["symbol", "region"]


class InvestmentOptionBought(DeltaLakeTable):
    """Investment Option Bought Table in Silver Layer."""

    def return_defined_schema(self) -> pa.Schema:
        """Return the schema for the InvestmentOptionBought table."""
        fields: list[tuple[str, pa.DataType]] = [
            ("symbol", pa.string()),
            ("date_bought", pa.date32()),
            ("price", pa.decimal128(20, 10)),
            ("amount", pa.decimal128(20, 10)),
            ("cost_of_buy", pa.decimal128(20, 10)),
            ("currency", pa.string()),
            ("exchange_rate", pa.decimal128(38, 19)),
            ("broker", pa.string()),
        ]

        return pa.schema(fields=fields)

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the InvestmentOptionBought table."""
        return ["symbol", "date_bought", "price", "broker"]


class InvestmentOptionValueOvertime(DeltaLakeTable):
    """Investment Option Value Overtime Table in Silver Layer."""

    def return_defined_schema(self) -> pa.Schema:
        """Return the schema for the InvestmentOptionValueOvertime table."""
        fields: list[tuple[str, pa.DataType]] = [
            ("symbol", pa.string()),
            ("date", pa.date32()),
            ("open", pa.decimal128(20, 10)),
            ("high", pa.decimal128(20, 10)),
            ("low", pa.decimal128(20, 10)),
            ("close", pa.decimal128(20, 10)),
            ("volume", pa.int64()),
        ]

        return pa.schema(fields=fields)

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the table."""
        return ["symbol", "date"]
