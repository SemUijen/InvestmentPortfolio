from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DateType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from src.spark_etl.utils import BaseTable

load_dotenv()


class FactDailyResult(BaseTable):
    def __init__(self, spark: SparkSession | None = None):
        """Initialize the StockExchange table."""
        super().__init__(medaillon_layer="gold", spark=spark)

    def return_defined_schema(self) -> StructType:
        """Return the schema for the StockExchange table."""
        return StructType(
            [
                StructField("date_id", IntegerType(), True),
                StructField("date", DateType(), True),
                StructField("symbol", StringType(), True),
                StructField("total_investment", FloatType(), True),
                StructField("total_value", FloatType(), True),
                StructField("number_owned", FloatType(), True),
                StructField("avg_buy_price", FloatType(), True),
                StructField("value_single_io", FloatType(), True),
                StructField("product_profit", FloatType(), True),
                StructField("currency_profit", FloatType(), True),
                StructField("total_profit", FloatType(), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the StockExchange table."""
        return ["symbol", "date_id"]
