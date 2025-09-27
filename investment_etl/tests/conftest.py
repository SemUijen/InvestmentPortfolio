import pytest
import time
from pyspark.sql import SparkSession
from investment_etl.utils.spark_session import get_spark_session
from investment_etl.utils.base_tables import SparkTable, DeltaLakeTable
import logging

from tests.test_utils.spark_vs_delta_tables_test import DeltaLakeVsSparkTablesTest

@pytest.fixture(scope="session")
def spark_session():
    """Create a Spark session for testing."""
    # Suppress py4j logging before creating session
    logging.getLogger("py4j").setLevel(logging.ERROR)
    logging.getLogger("py4j.java_gateway").setLevel(logging.ERROR)

    spark = get_spark_session()
    spark.sparkContext.setLogLevel("ERROR")
    yield spark
    spark.stop()


@pytest.fixture(scope="session")
def deltalake_vs_spark_tables_test() -> DeltaLakeVsSparkTablesTest:
    return DeltaLakeVsSparkTablesTest()