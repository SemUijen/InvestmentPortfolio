import logging
from datetime import datetime
from pathlib import Path

import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql.functions import col, explode, split, to_date
from pyspark.sql.types import MapType, StringType, StructField, StructType

from src.spark_etl.silver_layer.tables.spark_tables import (
    InvestmentOptionValueOvertime,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class InvestmentOptionBronzePipeline:
    """Utility class for the bronze layer data."""

    def __init__(self, base_dir: str, spark: SparkSession):
        self.base_dir = base_dir
        self.spark = spark

    def _bronze_json_schema(self) -> StructType:
        return StructType(
            [
                StructField(
                    "Meta Data",
                    StructType(
                        [
                            StructField("1. Information", StringType(), True),
                            StructField("2. Symbol", StringType(), True),
                            StructField("3. Last Refreshed", StringType(), True),
                            StructField("4. Output Size", StringType(), True),
                            StructField("5. Time Zone", StringType(), True),
                        ],
                    ),
                    True,
                ),
                StructField(
                    "Time Series (Daily)",
                    MapType(
                        StringType(),  # Date as string
                        StructType(
                            [
                                StructField("1. open", StringType(), True),
                                StructField("2. high", StringType(), True),
                                StructField("3. low", StringType(), True),
                                StructField("4. close", StringType(), True),
                                StructField("5. volume", StringType(), True),
                            ],
                        ),
                    ),
                    True,
                ),
            ],
        )

    def _get_file_paths(self, today: datetime) -> list[str]:
        """Construct the file path for the bronze layer data.

        :param symbol_name: The name of the symbol.
        :param today: The date in 'YYYY-MM-DD' format.
        :return: The full file path as a string.
        """
        logger.info("Getting file paths for %s", today)
        file_paths = []
        year, month, day = (
            today.strftime("%Y"),
            today.strftime("%m"),
            today.strftime("%d"),
        )

        investment_directory = Path(self.base_dir) / "investment_options"
        # Get first-level folders in the investment_directory

        for f in investment_directory.iterdir():
            if f.is_dir():
                file_name = f"{year}-{month}-{day}_{f.name}.json"
                file_paths.append(
                    str(
                        investment_directory
                        / f.name
                        / f"year={today.year}"
                        / f"month={today.month}"
                        / f"day={today.day}"
                        / file_name,
                    ),
                )

        return file_paths

    def _load_investment_options(self, today: datetime) -> DataFrame:
        """Load investment options data for a specific date.

        :param today: The date in 'YYYY-MM-DD' format.
        :return: A Spark DataFrame containing the investment options data.
        """
        logger.info("Loading investment options data for %s", today)
        file_paths = self._get_file_paths(today)
        logger.info("File paths: %s", file_paths)
        if not file_paths:
            raise ValueError("No files found for the specified date.")

        return (
            self.spark.read.option("multiline", "true")
            .schema(self._bronze_json_schema())
            .json(file_paths)
        )

    def _extract_nested_json(self, df: DataFrame) -> DataFrame:
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

    def _fill_missing_weekends(self, df: DataFrame) -> DataFrame:
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

    def run(self, today: datetime):
        """Run the pipeline to load investment options data.

        :param today: The date in 'YYYY-MM-DD' format.
        :return: A Spark DataFrame containing the investment options data.
        """
        logger.info("Running InvestmentOptionBronzePipeline for %s", today)

        df = self._load_investment_options(today)
        if df.isEmpty():
            logger.warning("No data found for %s", today)
            return

        logger.info("Saving investment options data to silver layer")
        df = self._extract_nested_json(df)
        df = self._fill_missing_weekends(df)
        InvestmentOptionValueOvertime(spark=self.spark).merge_dataframe(
            df,
        )
        logger.info("Investment options data saved to silver layer")
