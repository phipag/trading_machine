from typing import List
import pandas as pd
from ta import momentum
from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule


class ROC(TradingRule):
    # The days parameters needs 8 bits (= all integers in [0, 255])
    num_bits: List[int] = [8]
    __days: int

    def __init__(self, stock_data_provider: StockDataProvider, days: int = 12):
        super().__init__(stock_data_provider)
        self.__days = days

    def calculate(self) -> pd.Series:
        """
        Calculates the rate of change
        :return: Series containing the rate of change values for each closing price
        """
        return momentum.roc(self._history['Close'], self.__days)

    def buy_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be bought and false else
        :return: Series containing buy or not buy indicators
        """
        # Buy if the roc moves above the zero-line
        roc = self.calculate()
        # A boolean vector
        buy_decisions = (roc.shift(1) < 0) & (roc > 0)
        return pd.Series(data=buy_decisions, index=self._history.index)

    def sell_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be sold and false else
        :return: Series containing sell or not sell indicators
        """
        # Sell if the roc moves under the zero-line
        roc = self.calculate()
        # A boolean vector
        sell_decisions = (roc.shift(1) > 0) & (roc < 0)
        return pd.Series(data=sell_decisions, index=self._history.index)
