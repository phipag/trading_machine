from typing import List

import pandas as pd

from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule


class ChandelierExit(TradingRule):
    # The days parameters needs 6 bits (= all integers in [0, 63])
    # The multiplier parameters needs 3 bits (= all integers in [0, 7])
    num_bits: List[int] = [6, 3]

    def __init__(self, stock_data_provider: StockDataProvider, days: int = 22, multiplier: int = 3):
        super().__init__(stock_data_provider)
        self.__days: int = days if days > 1 else 1
        self.__multiplier: int = multiplier

    def calculate(self) -> pd.Series:
        """
        Calculates the Chandelier exit
        :return: Series containing the Chandelier exit values for each closing price
        """
        highest_value = self._history['Close'].rolling(window=self.__days).max()
        # TODO: optimization possible with Current ATR = ((Prior ATR x 13) + Current TR) / 14
        data = self._history.copy()
        data['tr0'] = abs(self._history['High'] - self._history['Low'])
        data['tr1'] = abs(self._history['High'] - self._history['Close'].shift())
        data['tr2'] = abs(self._history['Low'] - self._history['Close'].shift())
        tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
        atr = tr.ewm(alpha=1 / self.__days, min_periods=self.__days, adjust=False).mean()
        return highest_value - atr * self.__multiplier

    def buy_signals(self) -> pd.Series:
        return pd.Series(data=False, index=self._history.index)

    def sell_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be sold and false else
        :return: Series containing sell or not sell indicators
        """
        # The rule of the indicator is to close long positions when the price goes below the exit long
        ce = self.calculate()
        # A boolean vector
        sell_decisions = (self._history['Close'].shift(1) > ce) & (self._history['Close'] <= ce)
        return pd.Series(data=sell_decisions, index=self._history.index)
