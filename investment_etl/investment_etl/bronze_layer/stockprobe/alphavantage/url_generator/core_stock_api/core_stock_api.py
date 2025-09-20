"""Module contains class for generating URLs for Alpha Vantage CoreStockAPI."""

import logging
from enum import StrEnum

from pydantic import Field

from investment_etl.bronze_layer.stockprobe.alphavantage.url_generator import (
    BaseAPIurl,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class OutputSizeEnum(StrEnum):
    """Enum for output size."""

    COMPACT = "compact"
    FULL = "full"


class TimeSeriesDailyURL(BaseAPIurl):
    """Model for intraday time series request."""

    function: str = "TIME_SERIES_DAILY"
    outputsize: OutputSizeEnum = Field(
        default=OutputSizeEnum.COMPACT,
        description="Size of the output data",
    )

    symbol: str | None = Field(default=None, description="Stock symbol")

    def return_search_url(self) -> str:
        """Return the URL for the search request."""
        if not self.symbol:
            raise ValueError("Symbol must be provided for search URL")
        return f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={self.symbol}&apikey={self.apikey}"
