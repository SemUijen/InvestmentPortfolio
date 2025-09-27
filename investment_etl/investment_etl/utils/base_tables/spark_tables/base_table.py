"""Base class for Silver Layer tables in Spark ETL."""

import logging
import os
import re
from abc import ABC, abstractmethod
from pathlib import Path

from delta.tables import DeltaTable, DeltaTableBuilder
from dotenv import load_dotenv
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import concat_ws, md5
from pyspark.sql.types import StructType

from investment_etl.utils.spark_session import get_spark_session

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class BaseTable(ABC):
    """Base class for Silver Layer tables using pyspark delta."""

    def __init__(self, medaillon_layer: str, spark: SparkSession | None = None) -> None:
        """Initialize the BaseTable."""
        if medaillon_layer not in ["bronze", "silver", "gold"]:
            msg = "medaillon_layer must be one of 'bronze', 'silver', or 'gold'."
            raise ValueError(msg)

        self.medaillon_layer = medaillon_layer
        if spark is None:
            msg = "Spark session not provided. Creating a new Spark session."
            logger.info(msg)
            spark = get_spark_session()

        self.spark = spark

        data_dir = os.getenv("DATA_DIR")
        if not data_dir:
            msg = "Environment variable 'DATA_DIR' is not set."
            raise ValueError(msg)

        self.silver_path = Path(data_dir) / self.medaillon_layer

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
        """Create a unique identifier based on its primary keys columns."""
        primary_keys = self.return_primary_keys_columns()

        return input_df.withColumn(
            "id",
            md5(concat_ws("||", *[input_df[col] for col in primary_keys])),
        )

    def get_table(self) -> DeltaTable:
        """Return the DeltaTable for the specified table."""
        return DeltaTable.forPath(
            self.spark,
            f"{self.silver_path}/{self.table_name}",
        )

    def get_dataframe(self) -> DataFrame:
        """Return the DataFrame for the specified table."""
        return self.get_table().toDF()

    def _return_delta_table_builder(self) -> DeltaTableBuilder:
        """Return a DeltaTableBuilder for the specified table."""
        table_path = f"{self.silver_path}/{self.table_name}"
        builder = (
            DeltaTable.createIfNotExists(self.spark)
            .tableName(self.table_name)
            .addColumn("id", "string")
        )  # Add 'id' column for unique identifier
        for field in self.return_defined_schema():
            if field.dataType.typeName() == "decimal":
                if hasattr(field.dataType, "precision") and hasattr(
                    field.dataType,
                    "scale",
                ):
                    builder.addColumn(
                        field.name,
                        f"decimal({field.dataType.precision},{field.dataType.scale})",
                    )
                else:
                    msg = (
                        f"Decimal field {field.name} must have "
                        "precision and scale defined."
                    )
                    raise ValueError(msg)
            else:
                builder.addColumn(field.name, field.dataType.typeName())

        builder.location(table_path)
        return builder

    def _create_table_if_not_exists(self) -> None:
        """Create the Delta table if it does not exist."""
        table_path = f"{self.silver_path}/{self.table_name}"
        if not DeltaTable.isDeltaTable(self.spark, table_path):
            builder = self._return_delta_table_builder()
            builder.execute()
            logger.info("Table %s created at %s", self.table_name, table_path)
        else:
            logger.info(
                "Table %s already exists at %s",
                self.table_name,
                table_path,
            )

    def _merge(self, new_data: DataFrame) -> None:
        """Merge new data into the existing Delta table."""
        delta_table = self.get_table()
        logger.info("Merging data into table %s", self.table_name)
        delta_table.alias("existing").merge(
            new_data.alias("new"),
            "existing.id = new.id",  # Assuming 'id' is the primary key
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        logger.info("Data merged into table %s", self.table_name)

    def merge_dataframe(self, new_data: DataFrame) -> None:
        """Merge new data into the existing Delta table."""
        if not isinstance(new_data, DataFrame):
            msg = "new_data must be a Spark DataFrame."
            raise TypeError(msg)

        new_data = self._add_hash_id(new_data)
        self._merge(new_data)

    def merge_dict_data(self, new_data: dict) -> None:
        """Merge new data from a dictionary into the existing Delta table."""
        if not isinstance(new_data, dict):
            msg = "new_data must be a dictionary."
            raise TypeError(msg)

        logger.info("Creating DataFrame from new data.")
        new_df = self.spark.createDataFrame(
            [new_data],
            schema=self.return_defined_schema(),
        )
        logger.info("Adding hash ID to new DataFrame.")
        new_df = self._add_hash_id(new_df)
        logger.info("Merging new DataFrame into the table.")
        self._merge(new_df)
