"""Main application for the Spark ETL process of the Bronze Layer."""

import asyncio
import logging
import os

from dotenv import load_dotenv

from src.stockprobe.alphavantage.url_generator import TimeSeriesDailyURL

from .utils import AsyncDataIngestor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    # Example URLs and symbol names
    load_dotenv()

    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        error_message = "No API key found. Please set the API_KEY environment variable."
        raise ValueError(error_message)

    symbols = ["AIAA.DEX", "IMAE.AMS", "IWDA.AMS", "NDIA.AMS", "QDVE.DEX", "VWCE.DEX"]
    urls_to_ingest = [
        (
            TimeSeriesDailyURL(
                apikey=api_key,
                symbol=symbol,
                validate_symbol=False,
            ).return_url(),
            symbol,
        )
        for symbol in symbols
    ]
    logger.info("URLs to ingest: %s", urls_to_ingest)

    data_dir = os.getenv("DATA_DIR", "")
    if not data_dir:
        raise ValueError("DATA_DIR environment variable is not set.")

    # Create ingestor
    ingestor = AsyncDataIngestor(
        to_ingest=urls_to_ingest,
        base_dir=rf"{data_dir}/bronze",
        semaphore=2,
    )

    # Run ingestion
    await ingestor.ingest_all()


if __name__ == "__main__":
    asyncio.run(main())
