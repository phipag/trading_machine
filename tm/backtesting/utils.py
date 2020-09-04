from unittest.mock import patch, PropertyMock, MagicMock

import pandas as pd


def mock_stock_data_provider_closing_prices(closing_prices: pd.Series) -> MagicMock:
    with patch('tm.StockDataProvider') as mock:
        instance = mock.return_value
        type(instance).history = PropertyMock(return_value=closing_prices.to_frame(name='Close'))
    return instance
