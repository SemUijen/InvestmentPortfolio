"""Pytest test cases for the BaseAPIurl class."""

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
        validate_symbol=False,
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


def test_validate_symbol__matches_found() -> None:
    """Test that the symbol validation raises an error when no matches are found."""
    matches = [
        {
            "1. symbol": "AAPL1",
            "2. name": "Apple Inc.",
            "9. matchScore": "0.9000",
        },
        {
            "1. symbol": "AAPLLL",
            "2. name": "Apple Inc.",
            "9. matchScore": "0.8900",
        },
    ]

    with requests_mock.Mocker() as m:
        m.get(
            "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=INVALID&apikey=demo",
            json={"bestMatches": matches},
            status_code=200,
        )

        with pytest.raises(
            ValueError,
            match=r"Symbol INVALID not found did you mean: \[{'1. symbol': 'AAPL1', '2. name': 'Apple Inc.', '9. matchScore': '0.9000'}, {'1. symbol': 'AAPLLL', '2. name': 'Apple Inc.', '9. matchScore': '0.8900'}\]",
        ):
            BaseAPIurl(symbol="INVALID", apikey="demo", validate_symbol=True)


def test_not_validating_symbol() -> None:
    """Test that the symbol is not validated when validate_symbol is False."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=AAPL&apikey=demo",
            json={"bestMatches": []},
            status_code=200,
        )

        BaseAPIurl(symbol="AAPL", apikey="demo", validate_symbol=False)
        assert not m.called


def test_api_call_when_validate_symbol_true() -> None:
    """Test that an API call is made when validate_symbol is True."""
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
        assert m.called


def test_extra_field_forbidden() -> None:
    """Test that the model raises an error when an extra field is provided."""
    with pytest.raises(
        ValidationError,
        match="Extra inputs are not permitted",
    ):
        BaseAPIurl(
            apikey="testapikey",
            datatype=DataType.JSON,
            symbol="AAPL",
            validate_symbol=False,
            extra_field="extra",
        )


def test_type_validations() -> None:
    """Test that the model raises an error when an invalid type is provided."""
    with pytest.raises(
        ValidationError,
        match="Input should be 'json' or 'csv'",
    ):
        BaseAPIurl(
            apikey="testapikey",
            datatype="invalid",
            symbol="AAPL",
            validate_symbol=False,
        )
