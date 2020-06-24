import pandas as pd
from ta import momentum
from tm import StockDataProvider
from tm.trading_rules.TradingRule import TradingRule


class RSI(TradingRule):
    __days: int

    def __init__(self, stock_data_provider: StockDataProvider, days: int = 200):
        super().__init__(stock_data_provider)
        self.__days = days

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
        buy_decisions = (rsi <= 30)
        return pd.Series(data=buy_decisions, index=self._history.index)

    def sell_signals(self) -> pd.Series:
        """
        Construct a Series containing True if the stock should be sold and false else
        :return: Series containing sell or not sell indicators
        """
        # Sell if the rsi is higher than 70
        rsi = self.calculate()
        # A boolean vector
        sell_decisions = (rsi >= 70)
        return pd.Series(data=sell_decisions, index=self._history.index)
