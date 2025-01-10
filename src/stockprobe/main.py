import os
from pprint import pprint

import requests
from alphavantage.url_generator.core_stock_api import TimeSeriesDailyURL
from dotenv import load_dotenv


def get_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the API returns JSON data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":

    load_dotenv()
    api_key = os.getenv("alphavantage_api_key")
    if not api_key:
        raise ValueError(
            "No API key found. Please set the API_KEY environment variable."
        )
    url_generator = TimeSeriesDailyURL(apikey=api_key, symbol="IWDA")
    daily_url = url_generator.return_url()
    data = get_api_data(daily_url)
    if data:
        pprint(data)
