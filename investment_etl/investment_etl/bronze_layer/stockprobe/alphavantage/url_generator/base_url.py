"""Module contains the base pydantic class  to interact with the alphavantage core stock API."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class DataType(StrEnum):
    """Enumeration for data types used in API responses."""

    JSON = "json"
    CSV = "csv"


class BaseAPIurl(BaseModel):
    """Base model for all API requests."""

    base_url: str = "https://www.alphavantage.co/query"

    apikey: str = Field(..., description="Your API key")
    datatype: DataType = Field(
        default=DataType.JSON,
        description="Response format (JSON or CSV)",
    )

    def _to_url_params(self) -> str:
        """Convert the model to URL parameters string."""
        exclude = {"base_url"}
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

    model_config = {
        "frozen": True,
        "extra": "forbid",
    }
