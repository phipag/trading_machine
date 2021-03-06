from abc import ABC, abstractmethod
from typing import List

import pandas as pd

from tm import StockDataProvider


class TradingRule(ABC):
    num_bits: List[int]

    # TODO: Refactor because only StockDataProvider().history['Close'] is used by all trading rules
    def __init__(self, stock_data_provider: StockDataProvider):
        self._history: pd.DataFrame = stock_data_provider.history

    @property
    def history(self):
        return self._history

    @property
    @abstractmethod
    def num_bits(self):
        """
        A list of integers where the size of the list represents the number of parameters of the trading rule and
        each value the required number of bits in a bit encoded vector
        :return: List[int]
        """
        return self.num_bits

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def buy_signals(self):
        pass

    @abstractmethod
    def sell_signals(self):
        pass
