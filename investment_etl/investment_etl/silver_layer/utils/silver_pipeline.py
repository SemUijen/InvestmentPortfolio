import logging
import time
from collections.abc import Callable
from datetime import datetime
from functools import wraps

from pyspark.sql import SparkSession

from investment_etl.utils import BaseTable

from .bronze_source import BronzeSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SilverPipeline:
    """Utility class for the bronze layer data."""

    def __init__(
        self,
        bronze_source: BronzeSource,
        spark: SparkSession,
        silver_table: BaseTable,
    ):
        self.bronze_source = bronze_source
        self.spark = spark
        self.silver_table = silver_table
        self.transform_functions: list[Callable] = []

    def add_transform_function(self, func: Callable) -> None:
        """Add a transformation function to the pipeline."""

        def timing_wrapper(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable:
                start_time = time.perf_counter()
                logger.info("Starting transformation: %s", func.__name__)
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start_time
                logger.info(
                    "Finished transformation: %s in %.2f seconds",
                    func.__name__,
                    elapsed,
                )
                return result

            return wrapper

        wrapped_func = timing_wrapper(func)
        self.transform_functions.append(wrapped_func)

    def run(self, today: datetime) -> None:
        """Run the ETL process for the bronze to silver layer."""
        logger.info("Running Silver Pipeline for %s", today)

        df_bronze = self.bronze_source._load_data(today)
        if df_bronze.isEmpty():
            logger.warning("No data found for %s", today)
            return

        logger.info("Saving investment options data to silver layer")
        for transform in self.transform_functions:
            df_bronze = transform(df_bronze)

        self.silver_table.merge_dataframe(
            df_bronze,
        )
        logger.info("Data saved to silver table %s", self.silver_table.table_name)
