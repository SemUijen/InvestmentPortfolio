"""FactDailyResult DeltaLake table definition."""
import pyarrow as pa
from investment_etl.utils import DeltaLakeTable


class FactDailyResult(DeltaLakeTable):
    def __init__(self):
        """Initialize the StockExchange table."""
        super().__init__(medaillon_layer="gold")

    def return_defined_schema(self) -> pa.Schema:
        """Return the schema for the StockExchange table."""
        fields: list[tuple[str, pa.DataType]] = [
            ("date_id", pa.int32()),
            ("date", pa.date32()),
            ("symbol", pa.string()),
            ("currency", pa.string()),
            ("currency_exchange_rate", pa.decimal128(38, 19)),
            ("total_investment", pa.decimal128(20, 10)),
            ("local_total_investment", pa.decimal128(20, 10)),
            ("total_value", pa.decimal128(20, 10)),
            ("number_owned", pa.decimal128(20, 10)),
            ("avg_buy_price", pa.decimal128(20, 10)),
            ("value_single_io", pa.decimal128(20, 10)),
            ("product_profit", pa.decimal128(20, 10)),
            ("currency_profit", pa.decimal128(20, 10)),
            ("unrealized_total_profit", pa.decimal128(20, 10)),
        ]
        return pa.schema(fields=fields)

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the StockExchange table."""
        return ["symbol", "date_id"]
