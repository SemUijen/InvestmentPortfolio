from email.mime import base
import os
from datetime import datetime

from dotenv import load_dotenv

from src.spark_etl.silver_layer.utils import silver_pipeline
from src.spark_etl.utils import get_spark_session

from .utils import BronzeSource, SilverPipeline
from .utils.transformations import (
    extract_stock_json, fill_stock_weekends,
    extract_currency_json, fill_currency_weekends,
)
from pyspark.sql.types import MapType, StringType, StructField, StructType
from src.spark_etl.silver_layer.tables.spark_tables import (InvestmentOptionValueOvertime, CurrencyExchangeRate)


INVESTMENT_OPTION_SCHEMA = StructType(
        [
            StructField(
                "Meta Data",
                StructType(
                    [
                        StructField("1. Information", StringType(), True),
                        StructField("2. Symbol", StringType(), True),
                        StructField("3. Last Refreshed", StringType(), True),
                        StructField("4. Output Size", StringType(), True),
                        StructField("5. Time Zone", StringType(), True),
                    ],
                ),
                True,
            ),
            StructField(
                "Time Series (Daily)",
                MapType(
                    StringType(),  # Date as string
                    StructType(
                        [
                            StructField("1. open", StringType(), True),
                            StructField("2. high", StringType(), True),
                            StructField("3. low", StringType(), True),
                            StructField("4. close", StringType(), True),
                            StructField("5. volume", StringType(), True),
                        ],
                    ),
                ),
                True,
            ),
        ],
    )

CURRENCY_EXCHANGE_SCHEMA = StructType(
        [
            StructField(
                "Meta Data",
                StructType(
                    [
                        StructField("1. Information", StringType(), True),
                        StructField("2. From Symbol", StringType(), True),
                        StructField("3. To Symbol", StringType(), True),
                        StructField("4. Last Refreshed", StringType(), True),
                        StructField("5. Output Size", StringType(), True),
                        StructField("6. Time Zone", StringType(), True),
                    ],
                ),
                True,
            ),
            StructField(
                "Time Series FX (Daily)",
                MapType(
                    StringType(),  # Date as string
                    StructType(
                        [
                            StructField("1. open", StringType(), True),
                            StructField("2. high", StringType(), True),
                            StructField("3. low", StringType(), True),
                            StructField("4. close", StringType(), True),
                            StructField("5. volume", StringType(), True),
                        ],
                    ),
                ),
                True,
            ),
        ],
    )

def main():
    """Run silver layer pipeline."""
    load_dotenv()  # Load environment variables from .env file
    spark = get_spark_session()

    if not (DATA_DIR := os.getenv("DATA_DIR")):
        raise ValueError("DATA_DIR environment variable is not set")

    bronze_source_investment_options = BronzeSource(
        base_dir=f"{DATA_DIR}/bronze",
        spark=spark,
        schema=INVESTMENT_OPTION_SCHEMA,
        bronze_folder="investment_options",
        spark_table=InvestmentOptionValueOvertime(spark=spark),
    )
    silver_pipeline_investment_options = SilverPipeline(
        bronze_source=bronze_source_investment_options,
        spark=spark,
        silver_table=InvestmentOptionValueOvertime(spark=spark),
    )
    silver_pipeline_investment_options.add_transform_function(extract_stock_json)
    silver_pipeline_investment_options.add_transform_function(fill_stock_weekends)

    bronze_source_currency_exchange = BronzeSource(
        base_dir=f"{DATA_DIR}/bronze",
        spark=spark,
        schema=CURRENCY_EXCHANGE_SCHEMA,
        bronze_folder="exchange_rate",
        spark_table=CurrencyExchangeRate(spark=spark),
    )
    silver_pipeline_currency_exchange = SilverPipeline(
        bronze_source=bronze_source_currency_exchange,
        spark=spark,
        silver_table=CurrencyExchangeRate(spark=spark),
    )
    silver_pipeline_currency_exchange.add_transform_function(extract_currency_json)
    silver_pipeline_currency_exchange.add_transform_function(fill_currency_weekends)


    # Example usage
    today = datetime.now()
    #silver_pipeline_investment_options.run(today)
    
    silver_pipeline_currency_exchange.run(today)

if __name__ == "__main__":
    main()
