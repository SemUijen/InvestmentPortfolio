"""Investment Option Table Module."""

from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DateType,
    DecimalType,
    StringType,
    StructField,
    StructType,
)

from investment_etl.utils import SparkTable

load_dotenv()


class CurrencyExchangeRate(SparkTable):
    """Currency Exchange Rate Table in Silver Layer."""

    def __init__(self, spark: SparkSession | None = None):
        """Initialize the CurrencyExchangeRate table."""
        super().__init__(medaillon_layer="silver", spark=spark)

    def return_defined_schema(self) -> StructType:
        """Return the schema for the CurrencyExchangeRate table."""
        return StructType(
            [
                StructField("from_currency", StringType(), True),
                StructField("to_currency", StringType(), True),
                StructField("date", DateType(), True),
                StructField("open", DecimalType(38, 19), True),
                StructField("high", DecimalType(38, 19), True),
                StructField("close", DecimalType(38, 19), True),
                StructField("low", DecimalType(38, 19), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the InvestmentOptionValueOvertime table."""
        return ["from_currency", "to_currency", "date"]
