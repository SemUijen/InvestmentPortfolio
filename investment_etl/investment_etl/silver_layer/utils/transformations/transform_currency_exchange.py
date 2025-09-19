import logging

import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import col, explode, to_date
from pyspark.sql.types import DecimalType

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def extract_nested_json(df: DataFrame) -> DataFrame:
    """Extract nested JSON fields from the DataFrame.

    return : DataFrame with extracted fields.
    """
    # Explode the daily time series
    logger.info("Extracting nested JSON fields from DataFrame")
    df = df.select(
        col("Meta Data.`2. from Symbol`").alias("from_currency"),
        col("Meta Data.`3. To Symbol`").alias("to_currency"),
        col("Time Series FX (Daily)"),
    )
    df = df.select(
        col("from_currency"),
        col("to_currency"),
        explode(col("Time Series FX (Daily)")).alias("date", "values"),
    )
    logger.info("Cleaning symbol and converting date to date format")
    df = df.withColumn("date", to_date(col("date"), "yyyy-MM-dd"))
    # # Expand nested structure
    logger.info("Selecting and value renaming columns")
    df = df.select(
        col("from_currency"),
        col("to_currency"),
        col("date"),
        col("values.`1. open`").cast(DecimalType(38, 19)).alias("open"),
        col("values.`2. high`").cast(DecimalType(38, 19)).alias("high"),
        col("values.`3. low`").cast(DecimalType(38, 19)).alias("low"),
        col("values.`4. close`").cast(DecimalType(38, 19)).alias("close"),
    )
    return df


def fill_missing_weekends(df: DataFrame) -> DataFrame:
    """Fill missing weekend dates in the DataFrame."""
    logger.info("Filling missing weekend dates in DataFrame")
    # Identify the first date with non-null 'close' value for each symbol
    first_dates = (
        df.filter(col("close").isNotNull())
        .groupBy("from_currency", "to_currency")
        .agg(F.min("date").alias("first_date"))
    )

    # Generate complete date series per currency pair
    complete_series = first_dates.select(
        col("from_currency"),
        col("to_currency"),
        explode(
            F.sequence(
                col("first_date"),
                F.current_date(),
                F.expr("interval 1 day"),
            ),
        ).alias("date"),
    )

    # Join and fill missing values
    window_spec = Window.partitionBy("from_currency", "to_currency").orderBy("date")

    result = (
        complete_series.join(df, ["from_currency", "to_currency", "date"], "left")
        .withColumn(
            "close_filled",
            F.last("close", ignorenulls=True).over(
                window_spec.rowsBetween(
                    Window.unboundedPreceding,
                    Window.currentRow,
                ),
            ),
        )
        .withColumn(
            "open_filled",
            F.last("open", ignorenulls=True).over(
                window_spec.rowsBetween(
                    Window.unboundedPreceding,
                    Window.currentRow,
                ),
            ),
        )
        .withColumn(
            "high_filled",
            F.last("high", ignorenulls=True).over(
                window_spec.rowsBetween(
                    Window.unboundedPreceding,
                    Window.currentRow,
                ),
            ),
        )
        .withColumn(
            "low_filled",
            F.last("low", ignorenulls=True).over(
                window_spec.rowsBetween(
                    Window.unboundedPreceding,
                    Window.currentRow,
                ),
            ),
        )
        .select(
            "from_currency",
            "to_currency",
            "date",
            col("open_filled").alias("open"),
            col("high_filled").alias("high"),
            col("low_filled").alias("low"),
            col("close_filled").alias("close"),
        )
        .orderBy("from_currency", "to_currency", "date")
    )
    return result
