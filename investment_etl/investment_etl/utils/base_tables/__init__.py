"""Initialization for base table utilities."""

from .deltalake_tables import BaseTable as DeltaLakeTable
from .spark_tables import BaseTable as SparkTable

__all__ = ["DeltaLakeTable", "SparkTable"]
