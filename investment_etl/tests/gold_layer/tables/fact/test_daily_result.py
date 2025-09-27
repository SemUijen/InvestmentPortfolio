import pytest
from investment_etl.gold_layer.tables.fact import FactDailyResultDeltaLake, FactDailyResultSpark

class TestFactDailyResultTables:
    def test_similarity_between_deltalake_and_spark(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = FactDailyResultSpark(spark=spark_session)
        deltalake_table = FactDailyResultDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, deltalake_table)