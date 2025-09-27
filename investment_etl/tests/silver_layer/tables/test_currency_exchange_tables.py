import pytest

from investment_etl.silver_layer.tables import (
    CurrencyExchangeRateDeltaLake,
    CurrencyExchangeRateSpark,
)

class TestCurrencyExchangeTable:
    def test_similarity_between_deltalake_and_spark(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = CurrencyExchangeRateSpark(spark=spark_session)
        deltalake_table = CurrencyExchangeRateDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, deltalake_table)