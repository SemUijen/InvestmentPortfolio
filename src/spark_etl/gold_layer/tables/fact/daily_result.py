from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DateType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    DecimalType
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
                StructField("currency", StringType(), True),
                StructField("currency_exchange_rate", DecimalType(38,19), True),
                StructField("total_investment", DecimalType(20,10), True),
                StructField("local_total_investment", DecimalType(20,10), True),
                StructField("total_value", DecimalType(20,10), True),
                StructField("number_owned", DecimalType(20,10), True),
                StructField("avg_buy_price", DecimalType(20,10), True),
                StructField("value_single_io", DecimalType(20,10), True),
                StructField("product_profit", DecimalType(20,10), True),
                StructField("currency_profit", DecimalType(20,10), True),
                StructField("unrealized_total_profit", DecimalType(20,10), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the StockExchange table."""
        return ["symbol", "date_id"]
