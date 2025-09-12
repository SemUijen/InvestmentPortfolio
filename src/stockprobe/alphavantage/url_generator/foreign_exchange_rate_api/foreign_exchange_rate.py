"""Module contains class for Exchange Rate API requests."""

from __future__ import annotations

from pydantic import Field

from src.stockprobe.alphavantage.url_generator import BaseAPIurl


class ForeignExchangeRateAPI(BaseAPIurl):
    """Base model for all API requests."""

    from_currency: str = Field(..., description="From currency")
    to_currency: str = Field(..., description="To currency")
    function: str = "CURRENCY_EXCHANGE_RATE"


test_case = ForeignExchangeRateAPI(
    apikey="demo",
    from_currency="USD",
    to_currency="EUR",
)
print(test_case.return_url())
