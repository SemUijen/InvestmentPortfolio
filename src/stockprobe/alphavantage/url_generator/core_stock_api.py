"""Module contains class for generating URLs for Alpha Vantage CoreStockAPI."""

from enum import StrEnum

from pydantic import Field

from .base_url import BaseAPIurl


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
