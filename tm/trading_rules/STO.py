import pandas as pd
import numpy as np

from typing import List
from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule


class STO(TradingRule):
    num_bits: List[int] = [8]
    __days: int

    def __init__(self, stock_data_provider: StockDataProvider, days: int = 14):
        super().__init__(stock_data_provider)
        self.__days = days
        lowestArray = np.empty(self._history['Close'].size)
        highestArray = np.empty(self._history['Close'].size)
        lowestValue = self._history['Close'].iloc[0]
        highestValue = self._history['Close'].iloc[0]
        for i in range(0, self._history['Close'].size):
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
        return kLine.rolling(window=self.__days).mean()

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
