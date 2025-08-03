import os
from datetime import datetime

from dotenv import load_dotenv
from pyspark.sql import SparkSession

from .utils import InvestmentOptionBronzePipeline

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    spark = SparkSession.builder.appName("SilverLayerApp").getOrCreate()
    if not (DATA_DIR := os.getenv("DATA_DIR")):
        raise ValueError("DATA_DIR environment variable is not set")

    bronze_source = InvestmentOptionBronzePipeline(f"{DATA_DIR}/bronze", spark)

    # Example usage
    today = datetime.now()
    symbol_name = "example_symbol"
    df = bronze_source.run(today)

    df.show()  # Display the loaded DataFrame
