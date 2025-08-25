from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType

from src.spark_etl.utils import BaseTable

load_dotenv()


class FactDailyResult(BaseTable):
    def __init__(self, spark: SparkSession | None = None):
        """Initialize the StockExchange table."""
        super().__init__(spark)

    def return_defined_schema(self) -> StructType:
        """Return the schema for the StockExchange table."""
        return StructType(
            [
                StructField("date_id", StringType(), True),
                StructField("symbol", StringType(), True),
                StructField("total_value", StringType(), True),
                StructField("number_owned", StringType(), True),
                StructField("value_single", StringType(), True),
                StructField("product_profit", StringType(), True),
                StructField("currency_profit", StringType(), True),
                StructField("total_profit", StringType(), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the StockExchange table."""
        return ["symbol", "date_id"]
