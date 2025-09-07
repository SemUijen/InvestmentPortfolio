import os
from datetime import datetime

from dotenv import load_dotenv

from src.spark_etl.utils import get_spark_session

from .utils import InvestmentOptionBronzePipeline

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    spark = get_spark_session()

    if not (DATA_DIR := os.getenv("DATA_DIR")):
        raise ValueError("DATA_DIR environment variable is not set")

    bronze_source = InvestmentOptionBronzePipeline(f"{DATA_DIR}/bronze", spark)

    # Example usage
    today = datetime.now()
    bronze_source.run(today)
