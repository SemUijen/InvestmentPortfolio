"""Base class for Silver Layer tables in Spark ETL."""

import logging
import os
import re
from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable, DeltaTableBuilder
from dotenv import load_dotenv
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import md5
from pyspark.sql.types import StructType

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class BaseTable(ABC):
    """Base class for Silver Layer tables in Spark ETL."""

    def __init__(self, spark: SparkSession = None):

        self.spark = spark

        data_dir = os.getenv("DATA_DIR")
        if not data_dir:
            raise ValueError("Environment variable 'DATA_DIR' is not set.")

        self.silver_path = Path(data_dir) / "silver"

        self.table_name = self._class_name_to_table_name()

        self._create_table_if_not_exists()

    def _class_name_to_table_name(self) -> str:
        """Convert a CamelCase class name to snake_case.

        Args:
            class_name (str): The class name in CamelCase (e.g., "InvestmentOption")

        Returns:
            str: The name in snake_case (e.g., "investment_option")

        """
        # Insert underscore before uppercase letters that follow lowercase letters
        # This handles cases like "InvestmentOption" -> "Investment_Option"
        snake_case = re.sub("([a-z0-9])([A-Z])", r"\1_\2", self.__class__.__name__)

        # Convert to lowercase
        return snake_case.lower()

    @contextmanager
    def _create_spark_session(self) -> Generator[SparkSession]:
        """Create a Spark session with Delta support."""
        if self.spark:
            return self.spark

        builder = (
            SparkSession.builder.appName("MyApp")
            .config("spark.local.dir", os.getenv("DATA_DIR"))
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            )
        )

        spark = configure_spark_with_delta_pip(builder).getOrCreate()
        yield spark
        spark.stop()

    @abstractmethod
    def return_defined_schema(self) -> StructType:
        """Abstract method to process data. Must be implemented by subclasses."""

    @abstractmethod
    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the table.

        This method should return a list of column names that are considered primary
        keys. This is used for creating a unique identifier for the table.
        """

    def _add_hash_id(self, input_df: DataFrame) -> DataFrame:
        """Creates a unique identifier for the table based on its primary keys columns."""
        primary_keys = self.return_primary_keys_columns()

        return input_df.withColumn(
            "id",
            md5(
                *[input_df[col] for col in primary_keys],
            ),  # Create a hash based on primary key columns
        )

    def get_table(self) -> DeltaTable:
        """Return the DeltaTable for the specified table."""
        with self._create_spark_session() as spark:
            return DeltaTable.forPath(
                spark,
                f"{self.silver_path}/{self.table_name}",
            )

    def _return_delta_table_builder(self, spark: SparkSession) -> DeltaTableBuilder:
        """Return a DeltaTableBuilder for the specified table."""
        table_path = f"{self.silver_path}/{self.table_name}"
        builder = (
            DeltaTable.createIfNotExists(spark)
            .tableName(self.table_name)
            .addColumn("id", "string")
        )  # Add 'id' column for unique identifier
        for field in self.return_defined_schema():
            builder.addColumn(field.name, field.dataType.typeName())

        builder.location(table_path)
        return builder

    def _create_table_if_not_exists(self) -> None:
        """Creates the Delta table if it does not exist."""
        with self._create_spark_session() as spark:
            table_path = f"{self.silver_path}/{self.table_name}"
            if not DeltaTable.isDeltaTable(spark, table_path):

                builder = self._return_delta_table_builder(spark)
                builder.execute()
                logging.info("Table %s created at %s", self.table_name, table_path)
            else:
                logging.info(
                    "Table %s already exists at %s",
                    self.table_name,
                    table_path,
                )

    def merge_data(self, new_data: StructType) -> None:
        """Merge new data into the existing Delta table."""
        delta_table = self.get_table()
        delta_table.alias("existing").merge(
            new_data.alias("new"),
            "existing.id = new.id",  # Assuming 'id' is the primary key
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        logging.info("Data merged into table %s", self.table_name)
