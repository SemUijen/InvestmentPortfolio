import logging
from datetime import datetime
from pathlib import Path

import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql.functions import col, explode, split, to_date
from pyspark.sql.types import MapType, StringType, StructField, StructType


from src.spark_etl.utils import BaseTable
from src.spark_etl.silver_layer.tables.spark_tables import (
    InvestmentOptionValueOvertime,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class BronzeSource:
    """Utility class for the bronze layer data."""

    def __init__(self, base_dir: str, spark: SparkSession, schema: StructType, bronze_folder: str, spark_table: BaseTable):
        self.base_dir = base_dir
        self.spark = spark
        self.schema = schema
        self.bronze_folder = bronze_folder
        self.table = spark_table

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

        directory = Path(self.base_dir) / self.bronze_folder
        # Get first-level folders in the investment_directory

        for f in directory.iterdir():
            if f.is_dir():
                file_name = f"{year}-{month}-{day}_{f.name}.json"
                file_paths.append(
                    str(
                        directory
                        / f.name
                        / f"year={today.year}"
                        / f"month={today.month}"
                        / f"day={today.day}"
                        / file_name,
                    ),
                )

        return file_paths

    def _load_data(self, today: datetime) -> DataFrame:
        """Load investment options data for a specific date.

        :param today: The date in 'YYYY-MM-DD' format.
        :return: A Spark DataFrame containing the investment options data.
        """
        logger.info("Loading %s data for %s", self.bronze_folder, today)
        file_paths = self._get_file_paths(today)
        logger.info("File paths: %s", file_paths)
        if not file_paths:
            raise ValueError("No files found for the specified date.")

        return (
            self.spark.read.option("multiline", "true")
            .schema(self.schema)
            .json(file_paths)
        )

