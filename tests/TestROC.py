import pytest
import pandas as pd
import math
from unittest.mock import Mock

from tm import StockDataProvider
from tm.trading_rules import ROC


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


def test_roc1(mock_sdp, df):
    mock_sdp.history = df
    roc3 = ROC(mock_sdp, days=3)
    assert math.isnan(roc3.calculate().iloc[0])
    assert math.isnan(roc3.calculate().iloc[1])
    assert math.isnan(roc3.calculate().iloc[2])
    assert roc3.calculate().iloc[3] == 60
    assert roc3.calculate().iloc[4] == 20
    assert round(roc3.calculate().iloc[5], 4) == -21.4286
    assert roc3.calculate().iloc[6] == -18.75
    assert roc3.calculate().iloc[7] == -50
    assert round(roc3.calculate().iloc[8], 4) == 54.5455
    assert round(roc3.calculate().iloc[9], 4) == 46.1538


def test_roc2(mock_sdp, df):
    mock_sdp.history = df
    roc3 = ROC(mock_sdp, days=3)
    assert roc3.buy_signals().iloc[0] == False
    assert roc3.buy_signals().iloc[1] == False
    assert roc3.buy_signals().iloc[2] == False
    assert roc3.buy_signals().iloc[3] == False
    assert roc3.buy_signals().iloc[4] == False
    assert roc3.buy_signals().iloc[5] == False
    assert roc3.buy_signals().iloc[6] == False
    assert roc3.buy_signals().iloc[7] == False
    assert roc3.buy_signals().iloc[8] == True
    assert roc3.buy_signals().iloc[9] == False


def test_roc3(mock_sdp, df):
    mock_sdp.history = df
    roc3 = ROC(mock_sdp, days=3)
    assert roc3.sell_signals().iloc[0] == False
    assert roc3.sell_signals().iloc[1] == False
    assert roc3.sell_signals().iloc[2] == False
    assert roc3.sell_signals().iloc[3] == False
    assert roc3.sell_signals().iloc[4] == False
    assert roc3.sell_signals().iloc[5] == True
    assert roc3.sell_signals().iloc[6] == False
    assert roc3.sell_signals().iloc[7] == False
    assert roc3.sell_signals().iloc[8] == False
    assert roc3.sell_signals().iloc[9] == False


def test_roc4(mock_sdp, df):
    mock_sdp.history = df
    roc7 = ROC(mock_sdp, days=7)
    assert math.isnan(roc7.calculate().iloc[0])
    assert math.isnan(roc7.calculate().iloc[1])
    assert math.isnan(roc7.calculate().iloc[2])
    assert math.isnan(roc7.calculate().iloc[3])
    assert math.isnan(roc7.calculate().iloc[4])
    assert math.isnan(roc7.calculate().iloc[5])
    assert math.isnan(roc7.calculate().iloc[6])
    assert roc7.calculate().iloc[7] == -10
    assert round(roc7.calculate().iloc[8], 4) == 13.3333
    assert round(roc7.calculate().iloc[9], 4) == 35.7143


def test_roc5(mock_sdp, df):
    mock_sdp.history = df
    roc7 = ROC(mock_sdp, days=7)
    assert roc7.buy_signals().iloc[0] == False
    assert roc7.buy_signals().iloc[1] == False
    assert roc7.buy_signals().iloc[2] == False
    assert roc7.buy_signals().iloc[3] == False
    assert roc7.buy_signals().iloc[4] == False
    assert roc7.buy_signals().iloc[5] == False
    assert roc7.buy_signals().iloc[6] == False
    assert roc7.buy_signals().iloc[7] == False
    assert roc7.buy_signals().iloc[8] == True
    assert roc7.buy_signals().iloc[9] == False


def test_roc6(mock_sdp, df):
    mock_sdp.history = df
    roc7 = ROC(mock_sdp, days=7)
    assert roc7.sell_signals().iloc[0] == False
    assert roc7.sell_signals().iloc[1] == False
    assert roc7.sell_signals().iloc[2] == False
    assert roc7.sell_signals().iloc[3] == False
    assert roc7.sell_signals().iloc[4] == False
    assert roc7.sell_signals().iloc[5] == False
    assert roc7.sell_signals().iloc[6] == False
    assert roc7.sell_signals().iloc[7] == False
    assert roc7.sell_signals().iloc[8] == False
    assert roc7.sell_signals().iloc[9] == False