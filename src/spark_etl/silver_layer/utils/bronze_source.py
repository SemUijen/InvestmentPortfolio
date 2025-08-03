from datetime import datetime
from pathlib import Path

from pyspark.sql import SparkSession


class BronzeSource:
    """Utility class for the bronze layer data."""

    def __init__(self, base_dir: str, spark: SparkSession):
        self.base_dir = base_dir
        self.spark = spark

    def _get_file_paths(self, today: datetime) -> list[Path]:
        """Construct the file path for the bronze layer data.

        :param symbol_name: The name of the symbol.
        :param today: The date in 'YYYY-MM-DD' format.
        :return: The full file path as a string.
        """
        file_paths = []
        year, month, day = (
            today.strftime("%Y"),
            today.strftime("%m"),
            today.strftime("%d"),
        )

        investment_directory = Path(self.base_dir) / "investment_options"
        # Get first-level folders in the investment_directory

        for f in investment_directory.iterdir():
            if f.is_dir():
                file_name = f"{year}-{month}-{day}-{f.name}.json"
                file_paths.append(
                    investment_directory
                    / f.name
                    / f"year={today.year}"
                    / f"month={today.month}"
                    / f"day={today.day}"
                    / file_name,
                )

        return file_paths
