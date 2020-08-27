import pytest
import pandas as pd
import math
from mock import Mock

from tm import StockDataProvider
from tm.trading_rules import SimpleMovingAverage
from tm.trading_rules import ExponentialMovingAverage

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


def test_sma1(mock_sdp, df):
    mock_sdp.history = df
    sma3 = SimpleMovingAverage(mock_sdp, days=3)
    assert math.isnan(sma3.calculate().iloc[0])
    assert math.isnan(sma3.calculate().iloc[1])
    assert sma3.calculate().iloc[2] == 13
    assert sma3.calculate().iloc[3] == 15
    assert sma3.calculate().iloc[4] == 16
    assert sma3.calculate().iloc[5] == 15
    assert sma3.calculate().iloc[6] == 14
    assert sma3.calculate().iloc[7] == 11
    assert sma3.calculate().iloc[8] == 13
    assert sma3.calculate().iloc[9] == 15


def test_sma2(mock_sdp, df):
    mock_sdp.history = df
    sma8 = SimpleMovingAverage(mock_sdp, days=8)
    assert math.isnan(sma8.calculate().iloc[0])
    assert math.isnan(sma8.calculate().iloc[1])
    assert math.isnan(sma8.calculate().iloc[2])
    assert math.isnan(sma8.calculate().iloc[3])
    assert math.isnan(sma8.calculate().iloc[4])
    assert math.isnan(sma8.calculate().iloc[5])
    assert math.isnan(sma8.calculate().iloc[6])
    assert sma8.calculate().iloc[7] == 13.25
    assert sma8.calculate().iloc[8] == 14.125
    assert sma8.calculate().iloc[9] == 14.625


def test_sma3(mock_sdp, df):
    mock_sdp.history = df
    sma3 = SimpleMovingAverage(mock_sdp, days=3)
    assert sma3.buy_signals().iloc[0] == False
    assert sma3.buy_signals().iloc[1] == False
    assert sma3.buy_signals().iloc[2] == False
    assert sma3.buy_signals().iloc[3] == True
    assert sma3.buy_signals().iloc[4] == False
    assert sma3.buy_signals().iloc[5] == False
    assert sma3.buy_signals().iloc[6] == False
    assert sma3.buy_signals().iloc[7] == False
    assert sma3.buy_signals().iloc[8] == True
    assert sma3.buy_signals().iloc[9] == False


def test_sma4(mock_sdp, df):
    mock_sdp.history = df
    sma3 = SimpleMovingAverage(mock_sdp, days=3)
    assert sma3.sell_signals().iloc[0] == False
    assert sma3.sell_signals().iloc[1] == False
    assert sma3.sell_signals().iloc[2] == False
    assert sma3.sell_signals().iloc[3] == False
    assert sma3.sell_signals().iloc[4] == False
    assert sma3.sell_signals().iloc[5] == True
    assert sma3.sell_signals().iloc[6] == False
    assert sma3.sell_signals().iloc[7] == True
    assert sma3.sell_signals().iloc[8] == False
    assert sma3.sell_signals().iloc[9] == False


def test_ema1(mock_sdp, df):
    mock_sdp.history = df
    ema0 = ExponentialMovingAverage(mock_sdp, weight=0)
    assert ema0.calculate().iloc[0] == 10
    assert ema0.calculate().iloc[1] == 15
    assert ema0.calculate().iloc[2] == 14
    assert ema0.calculate().iloc[3] == 16
    assert ema0.calculate().iloc[4] == 18
    assert ema0.calculate().iloc[5] == 11
    assert ema0.calculate().iloc[6] == 13
    assert ema0.calculate().iloc[7] == 9
    assert ema0.calculate().iloc[8] == 17
    assert ema0.calculate().iloc[9] == 19

def test_ema2(mock_sdp, df):
    mock_sdp.history = df
    ema10 = ExponentialMovingAverage(mock_sdp, weight=10)
    assert ema10.calculate().iloc[0] == 10
    assert ema10.calculate().iloc[1] == 12.5
    assert ema10.calculate().iloc[2] == 13.25
    assert ema10.calculate().iloc[3] == 14.625
    assert ema10.calculate().iloc[4] == 16.3125
    assert ema10.calculate().iloc[5] == 13.65625
    assert ema10.calculate().iloc[6] == 13.328125
    assert ema10.calculate().iloc[7] == 11.1640625
    assert ema10.calculate().iloc[8] == 14.08203125
    assert ema10.calculate().iloc[9] == 16.541015625


def test_ema3(mock_sdp, df):
    mock_sdp.history = df
    ema10 = ExponentialMovingAverage(mock_sdp, weight=10)
    assert ema10.buy_signals().iloc[0] == False
    assert ema10.buy_signals().iloc[1] == True
    assert ema10.buy_signals().iloc[2] == False
    assert ema10.buy_signals().iloc[3] == True
    assert ema10.buy_signals().iloc[4] == True
    assert ema10.buy_signals().iloc[5] == False
    assert ema10.buy_signals().iloc[6] == False
    assert ema10.buy_signals().iloc[7] == False
    assert ema10.buy_signals().iloc[8] == True
    assert ema10.buy_signals().iloc[9] == False


def test_ema4(mock_sdp, df):
    mock_sdp.history = df
    ema10 = ExponentialMovingAverage(mock_sdp, weight=10)
    assert ema10.sell_signals().iloc[0] == False
    assert ema10.sell_signals().iloc[1] == False
    assert ema10.sell_signals().iloc[2] == False
    assert ema10.sell_signals().iloc[3] == False
    assert ema10.sell_signals().iloc[4] == False
    assert ema10.sell_signals().iloc[5] == True
    assert ema10.sell_signals().iloc[6] == False
    assert ema10.sell_signals().iloc[7] == True
    assert ema10.sell_signals().iloc[8] == False
    assert ema10.sell_signals().iloc[9] == False
