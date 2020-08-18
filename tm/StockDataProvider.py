import pandas as pd
import yfinance as yf


class StockDataProvider:
    def __init__(self, ticker_name: str, period='max', start=None, end=None):
        if not ticker_name:
            raise ValueError('Please provider a ticker name.')

        ticker: yf.Ticker = yf.Ticker(ticker_name)
        try:
            self.__history: pd.DataFrame = ticker.history(period=period, start=start, end=end)
            self.__actions: pd.DataFrame = ticker.actions
            self.__dividends: pd.Series = ticker.dividends
            self.__splits: pd.Series = ticker.splits
            self.__info: pd.DataFrame = ticker.info
        except TypeError:
            raise ValueError('The provided ticker name "' + ticker_name + '" cannot be found.')

    @property
    def history(self):
        return self.__history

    @property
    def actions(self):
        return self.__actions

    @property
    def dividends(self):
        return self.__dividends

    @property
    def splits(self):
        return self.__splits

    @property
    def info(self):
        return self.__info
