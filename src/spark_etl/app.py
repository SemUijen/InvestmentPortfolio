"""Run full medaillon pipeline."""

from src.spark_etl.bronze_layer import app as bronze_pipelines
from src.spark_etl.gold_layer import app as gold_pipelines
from src.spark_etl.silver_layer import app as silver_pipelines


def main():
    """Run full medaillon pipeline."""
    bronze_pipelines.main()
    silver_pipelines.main()
    gold_pipelines.main()
