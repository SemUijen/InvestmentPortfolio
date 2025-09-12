"""Pytest test cases for the BaseAPIurl class."""

import pytest

from src.stockprobe.alphavantage.url_generator.base_url import DataType
from src.stockprobe.alphavantage.url_generator.core_stock_api import TimeSeriesDailyURL


@pytest.fixture
def url_generator() -> TimeSeriesDailyURL:
    """Provide a valid BaseAPIurl instance."""
    return TimeSeriesDailyURL(
        apikey="testapikey",
        datatype=DataType.JSON,
        symbol="AAPL",
    )


def test_to_url_params(url_generator: TimeSeriesDailyURL) -> None:
    """Test the _to_url_params method."""
    expected = "apikey=testapikey&datatype=json&function=TIME_SERIES_DAILY&outputsize=compact&symbol=AAPL"
    assert url_generator._to_url_params() == expected

    expected = "https://www.alphavantage.co/query?apikey=testapikey&datatype=json&function=TIME_SERIES_DAILY&outputsize=compact&symbol=AAPL"
    assert url_generator.return_url() == expected
