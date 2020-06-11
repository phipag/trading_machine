from abc import ABC, abstractmethod

import pandas as pd

from tm import StockDataProvider


class TradingRule(ABC):
    _history: pd.DataFrame

    def __init__(self, stock_data_provider: StockDataProvider):
        self._history = stock_data_provider.history

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def buy_signals(self):
        pass

    @abstractmethod
    def sell_signals(self):
        pass
