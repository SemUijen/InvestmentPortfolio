"""Module contains class for generating URLs for Alpha Vantage CoreStockAPI."""

from __future__ import annotations

from pydantic import Field

from .base_url import BaseAPIurl


class TimeSeriesDailyURL(BaseAPIurl):
    """Model for intraday time series request."""

    function: str = "TIME_SERIES_DAILY"
    outputsize: str | None = Field("compact", description="Size of the output data")
