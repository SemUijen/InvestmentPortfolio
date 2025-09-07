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
    fact_table_daily = FactDailyResult(spark)

    # Steps:
    ## 1: Get Latest date for each symbol in fact table
    df_fact_daily = fact_table_daily.get_dataframe()
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

    df_new_io_bought = df_io_bought.select(
        "symbol",
        F.col("date_bought").alias("date"),
        F.col("price").alias("price"),
        F.col("amount").alias("number_owned"),
        F.col("cost_of_buy"),
    )

    df_new_io_bought.show()
    ## 3 Create new rows for facttable from latest date until yesterday for each symbol

    df_io_value_overtime = io_value_overtime.get_dataframe()
    df_io_value_overtime.show()

    df_new_daily_results = (
        df_new_io_bought.select(
            F.col("symbol"),
            (F.col("price") * F.col("number_owned")).alias("total_investment"),
            F.col("number_owned"),
            F.col("cost_of_buy"),
            F.explode(
                F.sequence(
                    F.col("date"),
                    F.lit(F.current_date()),
                    F.expr("interval 1 day"),
                ),
            ).alias("date"),
        )
        .groupBy("date", "symbol")
        .agg(
            F.sum("total_investment").alias("total_investment"),
            F.sum("number_owned").alias("number_owned"),
            F.first("cost_of_buy").alias("cost_of_buy"),
        )
        .orderBy("date", "symbol")
    )
    df_new_daily_results.show()

    df_new_daily_results = (
        df_new_daily_results.join(
            df_io_value_overtime,
            (df_new_daily_results.symbol == df_io_value_overtime.symbol)
            & (df_new_daily_results.date == df_io_value_overtime.date),
            "left",
        )
        .drop(
            df_io_value_overtime["date"],
        )
        .select(
            df_new_daily_results["*"],
            F.date_format(F.col("date"), "yyyyddMM").cast("int").alias("date_id"),
            F.col("close").alias("value_single_io"),
            (F.col("total_investment") / F.col("number_owned")).alias("avg_buy_price"),
            (F.col("close") * F.col("number_owned")).alias("total_value"),
            (F.col("total_value") - F.col("total_investment")).alias(
                "product_profit",
            ),
            (F.lit(0)).alias(
                "currency_profit",
            ),  # Should be 0 for euros and currency eschange rates for others to the euro
            (
                F.col("product_profit")
                + F.col("currency_profit")
                - 2 * F.col("cost_of_buy")
            ).alias("total_profit"),
        )
    ).orderBy("date", "symbol")

    fact_table_daily.merge_dataframe(df_new_daily_results)

    fact_table_daily.get_dataframe().show()

    spark.stop()


if __name__ == "__main__":
    main()
