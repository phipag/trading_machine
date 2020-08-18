from typing import List

import pandas as pd

from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule


class MACD(TradingRule):
    # The lowerEMA, higherEMA,signalEMA parameters each need 8 bits (= all integers in [0, 255])
    num_bits: List[int] = [24]

    def __init__(self, stock_data_provider: StockDataProvider, lowerEMA: int = 12, higherEMA: int = 26, signalEMA: int = 9):
        super().__init__(stock_data_provider)
        self.__lowerEMA: int = lowerEMA
        self.__higherEMA: int = higherEMA
        self.__signalEMA: int = signalEMA

    def calculate(self) -> pd.Series:
        """
        Not Implemented
        """

    def get_macd(self) -> pd.Series:
        """
        Construct a Series containing the MACD line
        :return: Series containing the MACD value
        """
        ema12 = self._history['Close'].ewm(span=self.__lowerEMA, adjust=False).mean()
        ema26 = self._history['Close'].ewm(span=self.__higherEMA, adjust=False).mean()
        macd = ema12 - ema26
        return pd.Series(data=macd, index=self._history.index)

    def get_signal(self) -> pd.Series:
        """
        Construct a Series containing the signal line
        :return: Series containing the signal value
        """
        macd = self.get_macd()
        signal = macd.ewm(span=self.__signalEMA, adjust=False).mean()
        return pd.Series(data=signal, index=self._history.index)

    def buy_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be bought and false else
        :return: Series containing buy or not buy indicators
        """
        # Buy if the MACD crosses the signal from below
        ema12 = self._history['Close'].ewm(span=self.__lowerEMA, adjust=False).mean()
        ema26 = self._history['Close'].ewm(span=self.__higherEMA, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=self.__signalEMA, adjust=False).mean()

        # A boolean vector
        buy_decisions = (macd.shift(1) < signal.shift(1)) & (macd >= signal)
        return pd.Series(data=buy_decisions, index=self._history.index)

    def sell_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be sold and false else
        :return: Series containing sell or not sell indicators
        """
        # Sell if the MACD crosses the signal from below
        ema12 = self._history['Close'].ewm(span=self.__lowerEMA, adjust=False).mean()
        ema26 = self._history['Close'].ewm(span=self.__higherEMA, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=self.__signalEMA, adjust=False).mean()
        # A boolean vector
        sell_decisions = (macd.shift(1) > signal.shift(1)) & (macd <= signal)
        return pd.Series(data=sell_decisions, index=self._history.index)
