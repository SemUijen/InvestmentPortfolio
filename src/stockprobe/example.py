"""Executable script to fetch stock data from the Alpha Vantage API."""

from __future__ import annotations

import logging
import os

import requests
from dotenv import load_dotenv

from .alphavantage.url_generator import TimeSeriesDailyURL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_api_data(url: str) -> dict | None:
    """Fetch data from an API."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the API returns JSON data
    except requests.exceptions.RequestException as e:
        logging.exception("An error occurred", exc_info=e)
        return None


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        error_message = "No API key found. Please set the API_KEY environment variable."
        raise ValueError(error_message)
    url_generator = TimeSeriesDailyURL(
        apikey=api_key,
        symbol="IWDA.AMS",
    )
    daily_url = url_generator.return_url()
    print(daily_url)
