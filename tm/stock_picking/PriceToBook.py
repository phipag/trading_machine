import pandas as pd

from tm import StockDataProvider

from tm.stock_picking.StockPicker import StockPicker


class PriceToBook(StockPicker):

    def __init__(self, stock_data_provider: StockDataProvider):
        super().__init__(stock_data_provider)

    @property
    def calculate(self) -> pd.Series:
        return self._info['priceToBook']
