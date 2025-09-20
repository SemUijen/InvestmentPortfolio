import logging

import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import col, explode, split, to_date

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
        col("Meta Data.`2. Symbol`").alias("symbol"),
        col("Time Series (Daily)"),
    )
    df = df.select(
        col("symbol"),
        explode(col("Time Series (Daily)")).alias("date", "values"),
    )
    logger.info("Cleaning symbol and converting date to date format")
    df = df.withColumn("symbol", split(col("symbol"), "\\.")[0])
    df = df.withColumn("date", to_date(col("date"), "yyyy-MM-dd"))
    # # Expand nested structure
    logger.info("Selecting and value renaming columns")
    df = df.select(
        col("symbol"),
        col("date"),
        col("values.`1. open`").alias("open"),
        col("values.`2. high`").alias("high"),
        col("values.`3. low`").alias("low"),
        col("values.`4. close`").alias("close"),
        col("values.`5. volume`").alias("volume"),
    )

    return df


def fill_missing_weekends(df: DataFrame) -> DataFrame:
    """Fill missing weekend dates in the DataFrame."""
    logger.info("Filling missing weekend dates in DataFrame")
    # Identify the first date with non-null 'close' value for each symbol
    first_dates = (
        df.filter(col("close").isNotNull())
        .groupBy("symbol")
        .agg(F.min("date").alias("first_date"))
    )

    # Generate complete date series per symbol
    complete_series = first_dates.select(
        col("symbol"),
        explode(
            F.sequence(
                col("first_date"),
                F.current_date(),
                F.expr("interval 1 day"),
            ),
        ).alias("date"),
    )

    # Join and fill missing values
    window_spec = Window.partitionBy("symbol").orderBy("date")

    result = (
        complete_series.join(df, ["symbol", "date"], "left")
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
        .withColumn(
            "volume_filled",
            F.when(F.dayofweek(col("date")).isin([1, 7]), F.lit(0)).otherwise(
                F.coalesce(col("volume"), F.lit(0)),
            ),
        )
        .select(
            "symbol",
            "date",
            col("open_filled").alias("open"),
            col("high_filled").alias("high"),
            col("low_filled").alias("low"),
            col("close_filled").alias("close"),
            col("volume_filled").alias("volume"),
        )
        .orderBy("symbol", "date")
    )

    return result
