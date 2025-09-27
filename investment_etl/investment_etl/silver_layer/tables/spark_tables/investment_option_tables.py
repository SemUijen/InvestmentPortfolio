"""Investment Option Table Module."""

from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DateType,
    DecimalType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from investment_etl.utils import SparkTable

load_dotenv()


class InvestmentOption(SparkTable):
    """Investment Option Table in Silver Layer."""

    def __init__(self, spark: SparkSession | None = None):
        """Initialize the InvestmentOption table."""
        super().__init__(medaillon_layer="silver", spark=spark)

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


class IoStockExchange(SparkTable):
    """Investment Option Stock Exchange Table in Silver Layer."""

    def __init__(self, spark: SparkSession | None = None):
        """Initialize the IoStockExchange table."""
        super().__init__(medaillon_layer="silver", spark=spark)

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


class StockExchange(SparkTable):
    """Stock Exchange Table in Silver Layer."""

    def __init__(self, spark: SparkSession | None = None):
        """Initialize the StockExchange table."""
        super().__init__(medaillon_layer="silver", spark=spark)

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


class InvestmentOptionValueOvertime(SparkTable):
    """Investment Option Value Over Time Table in Silver Layer."""

    def __init__(self, spark: SparkSession | None = None):
        """Initialize the InvestmentOptionValueOvertime table."""
        super().__init__(medaillon_layer="silver", spark=spark)

    def return_defined_schema(self) -> StructType:
        """Return the schema for the InvestmentOptionValueOvertime table."""
        return StructType(
            [
                StructField("symbol", StringType(), True),
                StructField("date", DateType(), True),
                StructField("open", DecimalType(20, 10), True),
                StructField("high", DecimalType(20, 10), True),
                StructField("close", DecimalType(20, 10), True),
                StructField("low", DecimalType(20, 10), True),
                StructField("volume", IntegerType(), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the InvestmentOptionValueOvertime table."""
        return ["symbol", "date"]


class InvestmentOptionBought(SparkTable):
    """Investment Option Bought Table in Silver Layer."""

    def __init__(self, spark: SparkSession | None = None):
        """Initialize the InvestmentOptionBought table."""
        super().__init__(medaillon_layer="silver", spark=spark)

    def return_defined_schema(self) -> StructType:
        """Return the schema for the InvestmentOptionBought table."""
        return StructType(
            [
                StructField("symbol", StringType(), True),
                StructField("date_bought", DateType(), True),
                StructField("price", DecimalType(20, 10), True),
                StructField("amount", DecimalType(20, 10), True),
                StructField("cost_of_buy", DecimalType(20, 10), True),
                StructField("broker", StringType(), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the InvestmentOptionBought table."""
        return ["symbol", "date_bought", "price", "broker"]
