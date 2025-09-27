"""Investment Option Table Module."""

import pyarrow as pa

from investment_etl.utils import DeltaLakeTable


class CurrencyExchangeRate(DeltaLakeTable):
    """Currency Exchange Rate Table in Silver Layer."""

    def __init__(self) -> None:
        """Initialize the CurrencyExchangeRate table."""
        super().__init__(medaillon_layer="silver")

    def return_defined_schema(self) -> pa.Schema:
        """Return the schema for the CurrencyExchangeRate table."""
        fields: list[tuple[str, pa.DataType]] = [
            ("from_currency", pa.string()),
            ("to_currency", pa.string()),
            ("date", pa.date32()),
            ("open", pa.decimal128(38, 19)),
            ("high", pa.decimal128(38, 19)),
            ("close", pa.decimal128(38, 19)),
            ("low", pa.decimal128(38, 19)),
        ]

        return pa.schema(fields=fields)

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the CurrencyExchangeRate table."""
        return ["from_currency", "to_currency", "date"]
