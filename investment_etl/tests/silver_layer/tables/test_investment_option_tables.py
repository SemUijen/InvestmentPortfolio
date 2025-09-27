import pytest
from unittest.mock import patch
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
from investment_etl.utils import DeltaLakeTable, SparkTable

@patch.object(DeltaLakeTable, "_create_table_if_not_exists", return_value=None)
@patch.object(SparkTable, "_create_table_if_not_exists", return_value=None)
class TestSparkvsDeltaLakeTables:
    def test_investment_options(self, deltalake_vs_spark_tables_test, spark_session):
            spark_table = InvestmentOptionSpark(spark=spark_session)
            delta_table = InvestmentOptionDeltaLake()

            deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)

    def test_investment_options_bought(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = InvestmentOptionBoughtSpark(spark=spark_session)
        delta_table = InvestmentOptionBoughtDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)

    def test_io_stock_exchange(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = IoStockExchangeSpark(spark=spark_session)
        delta_table = IoStockExchangeDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)

    def test_stock_exchange(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = StockExchangeSpark(spark=spark_session)
        delta_table = StockExchangeDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)

    def test_investment_option_value_overtime(self, deltalake_vs_spark_tables_test, spark_session):
        spark_table = InvestmentOptionValueOvertimeSpark(spark=spark_session)
        delta_table = InvestmentOptionValueOvertimeDeltaLake()

        deltalake_vs_spark_tables_test.run_all_tests(spark_table, delta_table)
