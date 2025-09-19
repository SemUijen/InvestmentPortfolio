"""Module contains class for Exchange Rate API requests."""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field

from investment_etl.bronze_layer.stockprobe.alphavantage.url_generator import BaseAPIurl


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
