from abc import ABC, abstractmethod

import pandas as pd

from tm import StockDataProvider


class StockPicker(ABC):
    _info: pd.DataFrame

    def __init__(self, stock_data_provider: StockDataProvider):
        self._info = stock_data_provider.info

    def info(self):
        return self._info

    @abstractmethod
    def calculate(self):
        pass