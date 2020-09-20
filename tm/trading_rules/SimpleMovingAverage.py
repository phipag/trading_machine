from typing import List
import pandas as pd
from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule


class SimpleMovingAverage(TradingRule):
    # The days parameters needs 8 bits (= all integers in [0, 127])
    num_bits: List[int] = [8]

    def __init__(self, stock_data_provider: StockDataProvider, days: int = 200):
        super().__init__(stock_data_provider)
        self.__days: int = days if days > 1 else 1

    def calculate(self) -> pd.Series:
        """
        Calculates the simple moving average
        :return: Series containing the simple moving average values for each closing price
        """
        return self._history['Close'].rolling(window=self.__days).mean()

    def buy_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be bought and false else
        :return: Series containing buy or not buy indicators
        """
        # Buy if the stock price crosses the SMA from below
        sma = self.calculate()
        # A boolean vector
        buy_decisions = (self._history['Close'].shift(1) < sma) & (self._history['Close'] >= sma)
        return pd.Series(data=buy_decisions, index=self._history.index)

    def sell_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be sold and false else
        :return: Series containing sell or not sell indicators
        """
        # Sell if the stock price crosses the SMA from above
        sma = self.calculate()
        # A boolean vector
        sell_decisions = (self._history['Close'].shift(1) > sma) & (self._history['Close'] <= sma)
        return pd.Series(data=sell_decisions, index=self._history.index)
