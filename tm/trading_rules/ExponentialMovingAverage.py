from typing import List

import pandas as pd

from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule


class ExponentialMovingAverage(TradingRule):
    # The days parameter needs 8 bits (= all integers in [0, 255])
    num_bits: List[int] = [8]
    __days: int

    def __init__(self, stock_data_provider: StockDataProvider, days: int = 200):
        super().__init__(stock_data_provider)
        self.__days = days if days > 1 else 1

    def calculate(self) -> pd.Series:
        """
        Calculates the exponential moving average
        :return: Series containing the exponential moving average values for each closing price
        """
        return self._history['Close'].ewm(span=self.__days, adjust=False).mean()

    def buy_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be bought and false else
        :return: Series containing buy or not buy indicators
        """
        # Buy if the stock price crosses the SMA from below
        ema = self.calculate()
        # A boolean vector
        buy_decisions = (self._history['Close'].shift(1) < ema) & (self._history['Close'] >= ema)
        return pd.Series(data=buy_decisions, index=self._history.index)

    def sell_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be sold and false else
        :return: Series containing sell or not sell indicators
        """
        # Sell if the stock price crosses the SMA from below
        ema = self.calculate()
        # A boolean vector
        sell_decisions = (self._history['Close'].shift(1) > ema) & (self._history['Close'] <= ema)
        return pd.Series(data=sell_decisions, index=self._history.index)
