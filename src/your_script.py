import json
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Get data paths from environment variables
bronze_data_path = os.getenv("BRONZE_DATA_PATH")
silver_data_path = os.getenv("SILVER_DATA_PATH")
gold_data_path = os.getenv("GOLD_DATA_PATH")

logger.info("Bronze data path: %s", bronze_data_path)
logger.info("Silver data path: %s", silver_data_path)
logger.info("Gold data path: %s", gold_data_path)

# Sample JSON data
json_data = """
[
    {"id": 1, "name": "Alice", "investment": 1000},
    {"id": 2, "name": "Bob", "investment": 1500},
    {"id": 3, "name": "Charlie", "investment": 2000}
]
"""
# Parse the JSON data
data = json.loads(json_data)

# Ensure the bronze data path exists
try:
    os.makedirs(bronze_data_path, exist_ok=True)
    logger.info("Created directory: %s", bronze_data_path)
except Exception as e:
    logger.error("Failed to create directory: %s", bronze_data_path)
    logger.error(e)

    # Write the data to a JSON file in the bronze data path
file_path = f"{bronze_data_path}/data.json"
with open(file_path, "w") as f:
    json.dump(data, f, indent=4)
logger.info("Data successfully written to %s", file_path)

# Read the data from the JSON file using spark
from pyspark.sql import SparkSession

# Initialize Spark session
spark = (
    SparkSession.builder.appName("InvestmentPortfolio")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .getOrCreate()
)
# Read the JSON data into a Spark DataFrame
df = spark.createDataFrame(data)
print(df)
# Show the DataFrame content
df.show()

# Write the DataFrame to a Delta table in the silver data path
spark.sql(
    "CREATE DATABASE IF NOT EXISTS InvestmentPortfolioSilver LOCATION '/InvestmentPortfolioData/silver'",
)

df.write.format("delta").mode("overwrite").saveAsTable(
    "InvestmentPortfolioSilver.DATA_test",
)

logger.info("Data successfully written to Delta format at %s", silver_data_path)
