import pandas as pd
import numpy as np

from typing import List
from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule

'''STochastic Oscillator'''


class STO(TradingRule):
    # The days_kline and days_dline parameters each need 8 bits (= all integers in [0, 127])
    num_bits: List[int] = [8,8]

    def __init__(self, stock_data_provider: StockDataProvider, days_kline: int = 14, days_dline: int = 3):
        super().__init__(stock_data_provider)
        self.__days_kline: int = days_kline if days_kline > 1 else 1
        self.__days_dline: int = days_dline if days_dline > 1 else 1
        lowestValue = self._history['Close'].iloc[0]
        highestValue = self._history['Close'].iloc[0]
        lowestArray = self._history['Close'].rolling(window=self.__days_kline).min()
        highestArray = self._history['Close'].rolling(window=self.__days_kline).max()
        for i in range(0, self.__days_kline):
            if self._history['Close'].iloc[i] < lowestValue:
                lowestValue = self._history['Close'].iloc[i]
            if self._history['Close'].iloc[i] > highestValue:
                highestValue = self._history['Close'].iloc[i]
            lowestArray[i] = lowestValue
            highestArray[i] = highestValue
        self._history['Lowest'] = lowestArray
        self._history['Highest'] = highestArray

    def calculate(self) -> pd.Series:
        """
        Calculates the stochastic oscillator
        :return: Series containing the rate of change values for each closing price
        """
        kLine = (self._history['Close'] - self._history['Lowest']) / (self._history['Highest'] - self._history['Lowest']) * 100
        return pd.Series(data=kLine, index=self._history.index)

    def get_dLine(self) -> pd.Series:
        """
        Calculates the %D Line
        :return: Series containing the rate of change values for each closing price
        """
        kLine = self.calculate()
        return kLine.rolling(window=self.__days_dline).mean()

    def buy_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be bought and false else
        :return: Series containing buy or not buy indicators
        """
        # Buy if the %K line crosses above the %D line
        kLine = self.calculate()
        dLine = self.get_dLine()
        # A boolean vector
        buy_decisions = (kLine.shift(1) < dLine.shift(1)) & (kLine >= dLine)
        return pd.Series(data=buy_decisions, index=self._history.index)

    def sell_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be sold and false else
        :return: Series containing sell or not sell indicators
        """
        # Sell when the %K line crosses below the %D line
        kLine = self.calculate()
        dLine = self.get_dLine()
        # A boolean vector
        sell_decisions = (kLine.shift(1) > dLine.shift(1)) & (kLine <= dLine)
        return pd.Series(data=sell_decisions, index=self._history.index)
