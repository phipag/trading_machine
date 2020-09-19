from typing import List

import pandas as pd

from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule


class BollingerBaender(TradingRule):
    # The days parameters needs 6 bits (= all integers in [0, 63])
    # The multiplier parameters needs 3 bits (= all integers in [0, 7])
    num_bits: List[int] = [6, 3]

    def __init__(self, stock_data_provider: StockDataProvider, days: int = 20, multiplier: int = 2):
        super().__init__(stock_data_provider)
        self.__days: int = days if days > 1 else 1
        self.__multiplier: int = multiplier

    def calculate(self) -> pd.Series:
        """
        Calculates the Chandelier exit
        :return: Series containing the Chandelier exit values for each closing price
        """
        sma = self._history['Close'].rolling(window=self.__days).mean()
        std = self._history['Close'].rolling(window=self.__days).std()

        return sma - std * self.__multiplier

    def buy_signals(self) -> pd.Series:
        return False

    def sell_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be sold and false else
        :return: Series containing sell or not sell indicators
        """
        # The rule of the indicator is to close long positions when the price goes below the exit long
        bb = self.calculate()
        # A boolean vector
        sell_decisions = (self._history['Close'].shift(1) > bb) & (self._history['Close'] <= bb)
        return pd.Series(data=sell_decisions, index=self._history.index)
