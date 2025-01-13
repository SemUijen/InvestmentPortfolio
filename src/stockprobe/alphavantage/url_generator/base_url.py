"""Module contains the base pydantic class  to interact with the alphavantage API."""

from __future__ import annotations

import logging
from enum import StrEnum

import requests
from pydantic import BaseModel, Field, model_validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DataType(StrEnum):
    """Enumeration for data types used in API responses."""

    JSON = "json"
    CSV = "csv"


class BaseAPIurl(BaseModel):
    """Base model for all API requests."""

    base_url: str = "https://www.alphavantage.co/query"
    apikey: str = Field(..., description="Your API key")
    datatype: DataType = Field(
        DataType.JSON,
        description="Response format (JSON or CSV)",
    )
    symbol: str | None = Field(None, description="Stock symbol")
    symbols: list[str] | None = Field(None, description="Stock symbols")
    validate_symbol: bool = Field(
        default=True,
        description="Check if the symbol exists in the API database",
    )

    def _to_url_params(self) -> str:
        """Convert the model to URL parameters string."""
        exclude = ["base_url", "validate_symbol"]
        params = []
        for field_name, field_value in self.model_dump(
            exclude_none=True,
            exclude=exclude,
        ).items():

            params.append(f"{field_name}={field_value}")
        return "&".join(params)

    def return_url(self) -> str:
        """Return the URL for the request."""
        return f"{self.base_url}?{self._to_url_params()}"

    @model_validator(mode="after")
    def check_symbol_exists(self) -> BaseAPIurl:
        """Check if the symbol exists in the alphavantage database.

        This is necessary because the API does not return an error if the symbol
        does not exist.
        """
        if not self.validate_symbol:
            return self

        logger.info("Checking if symbol %s exists", self.symbol)
        response = requests.get(
            f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={self.symbol}&apikey={self.apikey}",
            timeout=10,  # Timeout is in seconds
        )
        if response.status_code != 200:
            msg = f"An error occurred: {response.text}"
            raise ValueError(msg)

        data = response.json()
        logger.info("Symbol search response: %s", data)
        if not data.get("bestMatches"):
            msg = f"Symbol {self.symbol} not found and no close matches found"
            raise ValueError(msg)
        if data.get("bestMatches")[0].get("9. matchScore", 0) != "1.0000":
            msg = f"Symbol {self.symbol} not found did you mean: {data.get('bestMatches')}"
            raise ValueError(msg)
        return self

    model_config = {
        "frozen": True,
        "extra": "forbid",
    }
