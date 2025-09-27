"""Init file for silver layer tables module."""

# ruff: noqa: I001
from .spark_tables import (
    CurrencyExchangeRate as CurrencyExchangeRateSpark,
    InvestmentOption as InvestmentOptionSpark,
    InvestmentOptionBought as InvestmentOptionBoughtSpark,
    InvestmentOptionValueOvertime as InvestmentOptionValueOvertimeSpark,
    IoStockExchange as IoStockExchangeSpark,
    StockExchange as StockExchangeSpark,
)

from .deltalake_tables import (
    CurrencyExchangeRate as CurrencyExchangeRateDeltaLake,
    InvestmentOption as InvestmentOptionDeltaLake,
    InvestmentOptionBought as InvestmentOptionBoughtDeltaLake,
    InvestmentOptionValueOvertime as InvestmentOptionValueOvertimeDeltaLake,
    IoStockExchange as IoStockExchangeDeltaLake,
    StockExchange as StockExchangeDeltaLake,
)


__all__ = [
    "CurrencyExchangeRateDeltaLake",
    "CurrencyExchangeRateSpark",
    "InvestmentOptionBoughtDeltaLake",
    "InvestmentOptionBoughtSpark",
    "InvestmentOptionDeltaLake",
    "InvestmentOptionSpark",
    "InvestmentOptionValueOvertimeDeltaLake",
    "InvestmentOptionValueOvertimeSpark",
    "IoStockExchangeDeltaLake",
    "IoStockExchangeSpark",
    "StockExchangeDeltaLake",
    "StockExchangeSpark",
]
