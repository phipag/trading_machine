import pytest
import pandas as pd
import math
from unittest.mock import Mock

from tm import StockDataProvider
from tm.trading_rules import STO



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


def test_sto1(mock_sdp, df):
    mock_sdp.history = df
    sto3 = STO(mock_sdp, days=3)
    assert math.isnan(sto3.calculate().iloc[0])
    assert sto3.calculate().iloc[1] == 100
    assert sto3.calculate().iloc[2] == 80
    assert sto3.calculate().iloc[3] == 100
    assert sto3.calculate().iloc[4] == 100
    assert sto3.calculate().iloc[5] == 12.5
    assert sto3.calculate().iloc[6] == 37.5
    assert sto3.calculate().iloc[7] == 0
    assert round(sto3.calculate().iloc[8], 4) == 88.8889
    assert sto3.calculate().iloc[9] == 100


def test_sto2(mock_sdp, df):
    mock_sdp.history = df
    sto3 = STO(mock_sdp, days=3)
    assert math.isnan(sto3.get_dLine().iloc[0])
    assert math.isnan(sto3.get_dLine().iloc[1])
    assert math.isnan(sto3.get_dLine().iloc[2])
    assert round(sto3.get_dLine().iloc[3], 4) == 93.3333
    assert round(sto3.get_dLine().iloc[4], 4) == 93.3333
    assert round(sto3.get_dLine().iloc[5], 4) == 70.8333
    assert sto3.get_dLine().iloc[6] == 50
    assert round(sto3.get_dLine().iloc[7], 4) == 16.6667
    assert round(sto3.get_dLine().iloc[8], 4) == 42.1296
    assert round(sto3.get_dLine().iloc[9], 4) == 62.9630


def test_sto3(mock_sdp, df):
    mock_sdp.history = df
    sto3 = STO(mock_sdp, days=3)
    assert sto3.buy_signals().iloc[0] == False
    assert sto3.buy_signals().iloc[1] == False
    assert sto3.buy_signals().iloc[2] == False
    assert sto3.buy_signals().iloc[3] == False
    assert sto3.buy_signals().iloc[4] == False
    assert sto3.buy_signals().iloc[5] == False
    assert sto3.buy_signals().iloc[6] == False
    assert sto3.buy_signals().iloc[7] == False
    assert sto3.buy_signals().iloc[8] == True
    assert sto3.buy_signals().iloc[9] == False


def test_sto4(mock_sdp, df):
    mock_sdp.history = df
    sto3 = STO(mock_sdp, days=3)
    assert sto3.sell_signals().iloc[0] == False
    assert sto3.sell_signals().iloc[1] == False
    assert sto3.sell_signals().iloc[2] == False
    assert sto3.sell_signals().iloc[3] == False
    assert sto3.sell_signals().iloc[4] == False
    assert sto3.sell_signals().iloc[5] == True
    assert sto3.sell_signals().iloc[6] == False
    assert sto3.sell_signals().iloc[7] == False
    assert sto3.sell_signals().iloc[8] == False
    assert sto3.sell_signals().iloc[9] == False


def test_sto5(mock_sdp, df):
    mock_sdp.history = df
    sto6 = STO(mock_sdp, days=6)
    assert math.isnan(sto6.calculate().iloc[0])
    assert sto6.calculate().iloc[1] == 100
    assert sto6.calculate().iloc[2] == 80
    assert sto6.calculate().iloc[3] == 100
    assert sto6.calculate().iloc[4] == 100
    assert sto6.calculate().iloc[5] == 12.5
    assert sto6.calculate().iloc[6] == 37.5
    assert sto6.calculate().iloc[7] == 0
    assert round(sto6.calculate().iloc[8], 4) == 88.8889
    assert sto6.calculate().iloc[9] == 100


def test_sto6(mock_sdp, df):
    mock_sdp.history = df
    sto6 = STO(mock_sdp, days=6)
    assert math.isnan(sto6.get_dLine().iloc[0])
    assert math.isnan(sto6.get_dLine().iloc[1])
    assert math.isnan(sto6.get_dLine().iloc[2])
    assert math.isnan(sto6.get_dLine().iloc[3])
    assert math.isnan(sto6.get_dLine().iloc[4])
    assert math.isnan(sto6.get_dLine().iloc[5])
    assert round(sto6.get_dLine().iloc[6], 4) == 71.6667
    assert sto6.get_dLine().iloc[7] == 55
    assert round(sto6.get_dLine().iloc[8], 4) == 56.4815
    assert round(sto6.get_dLine().iloc[9], 4) == 56.4815


def test_sto7(mock_sdp, df):
    mock_sdp.history = df
    sto6 = STO(mock_sdp, days=6)
    assert sto6.buy_signals().iloc[0] == False
    assert sto6.buy_signals().iloc[1] == False
    assert sto6.buy_signals().iloc[2] == False
    assert sto6.buy_signals().iloc[3] == False
    assert sto6.buy_signals().iloc[4] == False
    assert sto6.buy_signals().iloc[5] == False
    assert sto6.buy_signals().iloc[6] == False
    assert sto6.buy_signals().iloc[7] == False
    assert sto6.buy_signals().iloc[8] == True
    assert sto6.buy_signals().iloc[9] == False


def test_sto8(mock_sdp, df):
    mock_sdp.history = df
    sto6 = STO(mock_sdp, days=6)
    assert sto6.sell_signals().iloc[0] == False
    assert sto6.sell_signals().iloc[1] == False
    assert sto6.sell_signals().iloc[2] == False
    assert sto6.sell_signals().iloc[3] == False
    assert sto6.sell_signals().iloc[4] == False
    assert sto6.sell_signals().iloc[5] == False
    assert sto6.sell_signals().iloc[6] == False
    assert sto6.sell_signals().iloc[7] == False
    assert sto6.sell_signals().iloc[8] == False
    assert sto6.sell_signals().iloc[9] == False