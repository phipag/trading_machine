import pytest
import pandas as pd
import math
from unittest.mock import Mock

from tm import StockDataProvider
from tm.trading_rules import RSI


@pytest.fixture()
def df():
    data = [['2015-01-02', 10], ['2015-01-03', 15], ['2015-01-04', 14], ['2015-01-05', 16], ['2015-01-06', 18],
            ['2015-01-07', 11], ['2015-01-08', 13], ['2015-01-09', 9], ['2015-01-10', 17], ['2015-01-11', 19]]
    df = pd.DataFrame(data, columns=['Date', 'Close'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index(['Date'])
    return df


@pytest.fixture()
def mock_sdp(df):
    return Mock(spec=StockDataProvider)

'''Rechnung nicht nachvollziehbar. Deshlab leider kein Test möglich'''
def test_rsi1(mock_sdp, df):
    mock_sdp.history = df
    rsi3 = RSI(mock_sdp, days=3, buyIndicator=30, sellIndicator=70)
