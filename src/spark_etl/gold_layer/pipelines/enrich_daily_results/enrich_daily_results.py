from pyspark.sql import functions as F

from src.spark_etl.gold_layer.tables import FactDailyResult
from src.spark_etl.silver_layer.tables.spark_tables import (
    InvestmentOptionBought,
    InvestmentOptionValueOvertime,
)
from src.spark_etl.utils import get_spark_session


def main():
    spark = get_spark_session()

    # Silver Tables
    io_bought = InvestmentOptionBought(spark)
    io_value_overtime = InvestmentOptionValueOvertime(spark)

    # Gold Tables
    fact_table = FactDailyResult(spark)

    # Steps:
    ## 1: Get Latest date for each symbol in fact table
    df_fact_daily = fact_table.get_dataframe()
    df_fact_daily = df_fact_daily.groupBy("symbol").agg(
        F.max("date").alias("latest_date"),
    )

    ## 2: Get IOs Bought sincs latest date
    df_io_bought = io_bought.get_dataframe()
    if not df_fact_daily.isEmpty():
        df_io_bought = df_io_bought.join(
            df_fact_daily,
            (df_io_bought.symbol == df_fact_daily.symbol)
            & (
                (df_io_bought.date > df_fact_daily.latest_date)
                | df_fact_daily.latest_date.isNull()
            ),
            "left",
        ).select(df_io_bought["*"])

    df_new_daily_results = df_io_bought.select(
        "symbol",
        F.col("date_bought").alias("date"),
    )
    df_new_daily_results.show()
    ## 3 Create new rows for facttable from latest date until yesterday for each symbol

    ### 3.1
    spark.stop()


if __name__ == "__main__":
    main()
