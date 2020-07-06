import pandas as pd
import yfinance as yf


class StockDataProvider:
    __history: pd.DataFrame
    __actions: pd.DataFrame
    __dividends: pd.Series
    __splits: pd.Series
    __info: pd.DataFrame

    def __init__(self, ticker_name: str, period='max', start=None, end=None):
        if not ticker_name:
            raise ValueError('Please provider a ticker name.')

        ticker: yf.Ticker = yf.Ticker(ticker_name)
        try:
            self.__history = ticker.history(period=period, start=start, end=end)
            self.__actions = ticker.actions
            self.__dividends = ticker.dividends
            self.__splits = ticker.splits
            self.__info = ticker.info
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
