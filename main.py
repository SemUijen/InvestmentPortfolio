import os

import requests
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
    daily_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IWDA.AMS&apikey={api_key}"
    data = get_api_data(daily_url)
    if data:
        print(data)

    search_symbol_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=IWDA&apikey={api_key}"
