from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    BooleanType,
    DateType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from investment_etl.utils import BaseTable

load_dotenv()


class DimDate(BaseTable):
    def __init__(self, spark: SparkSession | None = None):
        """Initialize the StockExchange table."""
        super().__init__(medaillon_layer="gold", spark=spark)

    def return_defined_schema(self) -> StructType:
        """Return the schema for the StockExchange table."""
        return StructType(
            [
                StructField("date_id", StringType(), True),
                StructField("date", DateType(), True),
                StructField("year", IntegerType(), True),
                StructField("month", IntegerType(), True),
                StructField("day", IntegerType(), True),
                StructField("quarter", IntegerType(), True),
                StructField("week", IntegerType(), True),
                StructField("day_of_year", IntegerType(), True),
                StructField("is_weekend", BooleanType(), True),
                StructField("day_of_week_name", StringType(), True),
            ],
        )

    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the StockExchange table."""
        return ["date_id"]
