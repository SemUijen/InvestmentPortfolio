import pytest
import requests_mock
from pydantic import ValidationError

from src.stockprobe.alphavantage.url_generator.base_url import BaseAPIurl, DataType


@pytest.fixture
def valid_base_api_url() -> BaseAPIurl:
    """Provide a valid BaseAPIurl instance."""
    return BaseAPIurl(
        apikey="testapikey",
        datatype=DataType.JSON,
        symbol="AAPL",
    )


def test_to_url_params(valid_base_api_url: BaseAPIurl) -> None:
    """Test the _to_url_params method."""
    expected = "apikey=testapikey&datatype=json&symbol=AAPL"
    assert valid_base_api_url._to_url_params() == expected


def test_return_url(valid_base_api_url: BaseAPIurl) -> None:
    """Test the return_url method."""
    expected = (
        "https://www.alphavantage.co/query?apikey=testapikey&datatype=json&symbol=AAPL"
    )
    assert valid_base_api_url.return_url() == expected


def test_validate_symbol_success() -> None:
    """Test that the symbol validation is successful for a valid symbol."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=AAPL&apikey=demo",
            json={
                "bestMatches": [
                    {
                        "1. symbol": "AAPL",
                        "2. name": "Apple Inc.",
                        "9. matchScore": "1.0000",
                    },
                ],
            },
            status_code=200,
        )
        BaseAPIurl(symbol="AAPL", apikey="demo", validate_symbol=True)


def test_validate_symbol_no_matches_found() -> None:
    """Test that the symbol validation raises an error when no matches are found."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=INVALID&apikey=demo",
            json={"bestMatches": []},
            status_code=200,
        )

        with pytest.raises(
            ValidationError,
            match="Symbol INVALID not found and no close matches found",
        ):
            BaseAPIurl(symbol="INVALID", apikey="demo", validate_symbol=True)
