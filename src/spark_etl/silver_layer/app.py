import os
from datetime import datetime

from delta import configure_spark_with_delta_pip
from dotenv import load_dotenv
from pyspark.sql import SparkSession

from .utils import InvestmentOptionBronzePipeline

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    builder = (
        SparkSession.builder.appName("MyApp")
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension",
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    if not (DATA_DIR := os.getenv("DATA_DIR")):
        raise ValueError("DATA_DIR environment variable is not set")

    bronze_source = InvestmentOptionBronzePipeline(f"{DATA_DIR}/bronze", spark)

    # Example usage
    today = datetime.now()
    bronze_source.run(today)
