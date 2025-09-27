import pytest

from investment_etl.silver_layer.tables import (
    InvestmentOptionSpark,
    InvestmentOptionDeltaLake,
    InvestmentOptionBoughtDeltaLake,
    InvestmentOptionBoughtSpark,
    IoStockExchangeDeltaLake,
    IoStockExchangeSpark,
    StockExchangeDeltaLake,
    StockExchangeSpark,
    InvestmentOptionValueOvertimeSpark,
    InvestmentOptionValueOvertimeDeltaLake,
)


class TestInvestmentOptionTable:
    def test_similarity_between_deltalake_and_spark(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = InvestmentOptionSpark(spark=spark_session)
        delta_table = InvestmentOptionDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)


class TestInvestmentOptionBoughtTable:
    def test_similarity_between_deltalake_and_spark(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = InvestmentOptionBoughtSpark(spark=spark_session)
        delta_table = InvestmentOptionBoughtDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)

class TestIoStockExchangeTable:
    def test_similarity_between_deltalake_and_spark(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = IoStockExchangeSpark(spark=spark_session)
        delta_table = IoStockExchangeDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)

class TestStockExchangeTable:
    def test_similarity_between_deltalake_and_spark(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = StockExchangeSpark(spark=spark_session)
        delta_table = StockExchangeDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)

class TestInvestmentOptionValueOvertimeTable:
    def test_similarity_between_deltalake_and_spark(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = InvestmentOptionValueOvertimeSpark(spark=spark_session)
        delta_table = InvestmentOptionValueOvertimeDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)
