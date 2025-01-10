from typing import Optional

from pydantic import Field

from .base_url import BaseAPIurl


class TimeSeriesDailyURL(BaseAPIurl):
    """Model for intraday time series request"""

    function: str = "TIME_SERIES_DAILY"
    outputsize: Optional[str] = Field("compact", description="Size of the output data")
