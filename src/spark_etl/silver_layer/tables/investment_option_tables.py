"""Investment Option Table Module."""

from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType

from .base_table import BaseTable

load_dotenv()


class InvestmentOption(BaseTable):
    """Investment Option Table in Silver Layer."""

    def __init__(self, spark: SparkSession | None = None):
        """Initialize the InvestmentOption table."""
        super().__init__(spark)

    def return_defined_schema(self) -> StructType:
        """Return the schema for the InvestmentOption table."""
        return StructType(
            [
                StructField("symbol", StringType(), True),
                StructField("name", StringType(), True),
                StructField("type", StringType(), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the InvestmentOption table."""
        return ["symbol"]


class IoStockExchange(BaseTable):
    """Investment Option Stock Exchange Table in Silver Layer."""

    def __init__(self, spark: SparkSession | None = None):
        """Initialize the IoStockExchange table."""
        super().__init__(spark)

    def return_defined_schema(self) -> StructType:
        """Return the schema for the IoStockExchange table."""
        return StructType(
            [
                StructField("io_symbol", StringType(), True),
                StructField("exchange_symbol", StringType(), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the IoStockExchange table."""
        return ["io_symbol", "exchange_symbol"]


class StockExchange(BaseTable):
    """Stock Exchange Table in Silver Layer."""

    def __init__(self, spark: SparkSession | None = None):
        """Initialize the StockExchange table."""
        super().__init__(spark)

    def return_defined_schema(self) -> StructType:
        """Return the schema for the StockExchange table."""
        return StructType(
            [
                StructField("symbol", StringType(), True),
                StructField("region", StringType(), True),
                StructField("markt_open", StringType(), True),
                StructField("markt_close", StringType(), True),
                StructField("currency", StringType(), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the StockExchange table."""
        return ["symbol"]
