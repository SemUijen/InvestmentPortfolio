# This module contains the base pydal class that is used to interact with the alphavantage API
import logging
from enum import StrEnum
from typing import Optional

import requests
from pydantic import BaseModel, Field, model_validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DataType(StrEnum):
    JSON = "json"
    CSV = "csv"


class BaseAPIurl(BaseModel):
    """Base model for all API requests"""

    base_url: str = "https://www.alphavantage.co/query"
    apikey: str = Field(..., description="Your API key")
    datatype: DataType = Field(
        DataType.JSON, description="Response format (JSON or CSV)"
    )
    symbol: Optional[str] = Field(..., description="Stock symbol")
    symbols: Optional[list[str]] = Field([], description="Stock symbols")
    validate_symbol: bool = Field(
        True, description="Check if the symbol exists in the API database"
    )

    def _to_url_params(self) -> str:
        """Convert the model to URL parameters string."""
        params = []
        for field_name, field_value in self.model_dump(exclude_none=True).items():
            params.append(f"{field_name}={field_value}")
        return "&".join(params)

    def return_url(self) -> str:
        """Return the URL for the request"""
        return f"{self.base_url}?{self._to_url_params()}"

    @model_validator(mode="after")
    def check_symbol_exists(self):
        """Check if the symbol exists in the API database"""
        if not self.validate_symbol:
            return self

        logger.info(f"Checking if symbol {self.symbol} exists")
        response = requests.get(
            f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={self.symbol}&apikey={self.apikey}"
        )
        if response.status_code != 200:
            raise ValueError(f"An error occurred: {response.text}")
        data = response.json()
        logger.info(f"Symbol search response: {data}")
        if data.get("bestMatches", [{}])[0].get("9. matchScore", 0) != "1.0000":
            raise ValueError(
                f"Symbol {self.symbol} not found did you mean: {data.get("bestMatches", "No matches found")}"
            )
        return self

    class Config:
        frozen = True
        forbid_extra = True
