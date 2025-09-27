"""Module for the base class for Silver Layer tables using the deltalake package."""

import hashlib
import logging
import os
import re
from abc import ABC, abstractmethod
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
from deltalake import DeltaTable, write_deltalake
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv()


class BaseTable(ABC):
    """Base class for Silver Layer tables using the deltalake package."""

    def __init__(
        self,
        medaillon_layer: str,
    ) -> None:
        """Initialize the BaseTable."""
        if medaillon_layer not in ["bronze", "silver", "gold"]:
            msg = "medaillon_layer must be one of 'bronze', 'silver', or 'gold'."
            raise ValueError(msg)
        self.medaillon_layer = medaillon_layer

        data_dir = os.getenv("DATA_DIR")
        if not data_dir:
            msg = "Environment variable 'DATA_DIR' is not set."
            raise ValueError(msg)

        self.silver_path = Path(data_dir) / self.medaillon_layer

        self.table_name = self._class_name_to_table_name()

        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        """Create the Delta table if it does not exist."""
        table_path = self.silver_path / self.table_name
        schema = self.return_defined_schema()
        schema = schema.append(pa.field("id", pa.string()))
        DeltaTable.create(
            table_path,
            schema=schema,
            mode="ignore",
        )

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
    def return_defined_schema(self) -> pa.Schema:
        """Abstract method to process data. Must be implemented by subclasses."""

    @abstractmethod
    def return_primary_keys_columns(self) -> list[str]:
        """Return the primary key columns for the table.

        This method should return a list of column names that are considered primary
        keys. This is used for creating a unique identifier for the table.
        """

    def _add_hash_id(self, table: pa.Table) -> pa.Table:
        """Create a unique identifier based on its primary keys columns."""
        primary_keys = self.return_primary_keys_columns()

        if not primary_keys:
            msg = "Primary keys columns are not defined."
            raise ValueError(msg)

        pk_cols = [table.column(col).cast(pa.string()) for col in primary_keys]
        if len(pk_cols) == 1:
            concat_array = pk_cols[0]  # No joining needed
        else:
            concat_array = pc.binary_join_element_wise(*pk_cols)

        hash_values = [
            hashlib.sha256(row.as_py().encode()).hexdigest() for row in concat_array
        ]

        id_array = pa.array(hash_values, type=pa.string())
        return table.append_column("id", id_array)

    def get_table(self) -> DeltaTable:
        """Return the DeltaTable for the specified table."""
        return DeltaTable(f"{self.silver_path}/{self.table_name}")

    def _merge_pyarrow_tables(
        self,
        old_table: pa.Table,
        new_data: pa.Table,
    ) -> pa.Table:
        """Merge two PyArrow tables."""
        new_ids = new_data["id"]
        mask = pc.is_in(old_table["id"], value_set=new_ids)
        filtered_existing = old_table.filter(pc.invert(mask))
        return pa.concat_tables([filtered_existing, new_data], promote=True)

    def _merge_data(self, input_df: pa.Table) -> None:
        """Merge the input DataFrame with the existing Delta table."""
        delta_table = self.get_table()
        existing_table = delta_table.to_pyarrow_table()
        input_table = self._add_hash_id(input_df)

        # Step 4: Concatenate new and non-overlapping existing data
        merged_table = self._merge_pyarrow_tables(existing_table, input_table)

        write_deltalake(
            table_or_uri=delta_table,
            data=merged_table,
            mode="overwrite",
        )

    def merge_from_dict(self, data: dict) -> None:
        """Merge data from a dictionary into the Delta table."""
        schema = self.return_defined_schema()
        input_table = pa.Table.from_pydict(data, schema=schema)
        self._merge_data(input_table)
