"""Module contains class for Exchange Rate API requests."""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field

from src.stockprobe.alphavantage.url_generator import BaseAPIurl


class OutputSizeEnum(StrEnum):
    """Enum for output size."""

    COMPACT = "compact"
    FULL = "full"


class ExchangeSymbols(StrEnum):
    """Enum for exchange symbols."""

    EURO = "EUR"
    USD = "USD"


class ForeignExchangeRateURL(BaseAPIurl):
    """Base model for all API requests."""

    function: str = "FX_DAILY"
    from_symbol: ExchangeSymbols = Field(..., description="From EUR")
    to_symbol: ExchangeSymbols = Field(..., description="To currency")
    outputsize: OutputSizeEnum = Field(
        default=OutputSizeEnum.FULL,
        description="Size of the output data",
    )


test = ForeignExchangeRateURL(
    apikey="demo",
    from_symbol=ExchangeSymbols.USD,
    to_symbol=ExchangeSymbols.EURO,
).return_url()
print(test)
