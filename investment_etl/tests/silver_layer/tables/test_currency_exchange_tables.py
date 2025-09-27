import pytest
from unittest.mock import patch
from investment_etl.silver_layer.tables import (
    CurrencyExchangeRateDeltaLake,
    CurrencyExchangeRateSpark,
)
from investment_etl.utils import DeltaLakeTable, SparkTable
@patch.object(DeltaLakeTable, "_create_table_if_not_exists", return_value=None)
@patch.object(SparkTable, "_create_table_if_not_exists", return_value=None)
class TestCurrencyExchangeTable:
    def test_similarity_between_deltalake_and_spark(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = CurrencyExchangeRateSpark(spark=spark_session)
        deltalake_table = CurrencyExchangeRateDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, deltalake_table)