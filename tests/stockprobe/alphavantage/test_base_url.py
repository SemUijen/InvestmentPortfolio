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
    )


def test_to_url_params(valid_base_api_url: BaseAPIurl) -> None:
    """Test the _to_url_params method."""
    expected = "apikey=testapikey&datatype=json"
    assert valid_base_api_url._to_url_params() == expected


def test_return_url(valid_base_api_url: BaseAPIurl) -> None:
    """Test the return_url method."""
    expected = (
        "https://www.alphavantage.co/query?apikey=testapikey&datatype=json"
    )
    assert valid_base_api_url.return_url() == expected



def test_extra_field_forbidden() -> None:
    """Test that the model raises an error when an extra field is provided."""
    with pytest.raises(
        ValidationError,
        match="Extra inputs are not permitted",
    ):
        BaseAPIurl(
            apikey="testapikey",
            datatype=DataType.JSON,
            extra_field="extra",  # This should not be allowed
            # The BaseAPIurl model does not accept an 'extra_field'
        )


def test_type_validations() -> None:
    """Test that the model raises an error when an invalid type is provided."""
    with pytest.raises(
        ValidationError,
        match="Input should be 'json' or 'csv'",
    ):
        BaseAPIurl(
            apikey="testapikey",
            datatype="invalid",  # This should be DataType.JSON or DataType.CSV
        )
