import pytest
from unittest.mock import patch
from investment_etl.gold_layer.tables.fact import FactDailyResultDeltaLake, FactDailyResultSpark
from investment_etl.utils import DeltaLakeTable, SparkTable

@patch.object(DeltaLakeTable, "_create_table_if_not_exists", return_value=None)
@patch.object(SparkTable, "_create_table_if_not_exists", return_value=None)
class TestFactDailyResultTables:
    def test_similarity_between_deltalake_and_spark(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = FactDailyResultSpark(spark=spark_session)
        deltalake_table = FactDailyResultDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, deltalake_table)