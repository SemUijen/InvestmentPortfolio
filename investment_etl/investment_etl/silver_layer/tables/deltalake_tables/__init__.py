"""Silver Deltalake Tables Module."""

from .currency_exchange_tables import CurrencyExchangeRate
from .investment_option_tables import (
    InvestmentOption,
    InvestmentOptionBought,
    InvestmentOptionValueOvertime,
    IoStockExchange,
    StockExchange,
)

__all__ = [
    "CurrencyExchangeRate",
    "InvestmentOption",
    "InvestmentOptionBought",
    "InvestmentOptionValueOvertime",
    "IoStockExchange",
    "StockExchange",
]
