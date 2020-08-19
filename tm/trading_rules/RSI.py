from typing import List

import pandas as pd
from ta import momentum

from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule


class RSI(TradingRule):
    # The days parameters needs 8 bits (= all integers in [0, 255]),
    # the buyIndicator and sellIndicator each 7 bits [0,128]
    num_bits: List[int] = [8, 7, 7]

    def __init__(self, stock_data_provider: StockDataProvider, days: int = 200, buyIndicator: int = 30, sellIndicator: int = 70):
        super().__init__(stock_data_provider)
        self.__days: int = days if days > 1 else 1
        self.__buyIndicator: int = buyIndicator if (buyIndicator >= 0 and buyIndicator <= 100) else 30
        self.__sellIndicator: int = sellIndicator if (sellIndicator >= 0 and sellIndicator <= 100) else 70

    def calculate(self) -> pd.Series:
        """
        Calculates the simple moving average
        :return: Series containing the simple moving average values for each closing price
        """
        return momentum.rsi(self._history['Close'])

        """
        Alternative:
        rsi_period = 14
        chg = self._history['Close'].diff(1)
        gain = chg.mask(chg < 0, 0)
        loss = chg.mask(chg > 0, 0)
        avg_gain = gain.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
        avg_loss = loss.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
        rs = abs(avg_gain / avg_loss)
        rsi = 100 - (100 / (1 + rs))
        """

    def buy_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be bought and false else
        :return: Series containing buy or not buy indicators
        """
        # Buy if the rsi is smaller than 30
        rsi = self.calculate()
        # A boolean vector
        buy_decisions = (rsi <= self.__buyIndicator)
        return pd.Series(data=buy_decisions, index=self._history.index)

    def sell_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be sold and false else
        :return: Series containing sell or not sell indicators
        """
        # Sell if the rsi is higher than 70
        rsi = self.calculate()
        # A boolean vector
        sell_decisions = (rsi >= self.__sellIndicator)
        return pd.Series(data=sell_decisions, index=self._history.index)
