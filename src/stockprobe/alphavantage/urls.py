# this module is used to define the urls for the alphavantage SDK

from abc import ABC


class AlphavantageUrls(ABC):
    base_url = "https://www.alphavantage.co/query?"
