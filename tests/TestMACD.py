import pytest
import pandas as pd
import math
from unittest.mock import Mock

from tm import StockDataProvider
from tm.trading_rules import MACD



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


def test_macd1(mock_sdp, df):
    mock_sdp.history = df
    macd352 = MACD(mock_sdp, lowerEMA=3, higherEMA=7, signalEMA=2)
    assert macd352.get_macd().iloc[0] == 0
    assert macd352.get_macd().iloc[1] == 1.25
    assert macd352.get_macd().iloc[2] == 1.3125
    assert macd352.get_macd().iloc[3] == 1.671875
    assert macd352.get_macd().iloc[4] == 2.09765625
    assert round(macd352.get_macd().iloc[5], 7) == 0.2451172
    assert round(macd352.get_macd().iloc[6], 7) == 0.0197754
    assert round(macd352.get_macd().iloc[7], 7) == -1.0671997
    assert round(macd352.get_macd().iloc[8], 7) == 0.6585846
    assert round(macd352.get_macd().iloc[9], 7) == 1.7234306


def test_macd2(mock_sdp, df):
    mock_sdp.history = df
    macd352 = MACD(mock_sdp, lowerEMA=3, higherEMA=7, signalEMA=2)
    assert macd352.get_signal().iloc[0] == 0
    assert round(macd352.get_signal().iloc[1], 4) == 0.8333
    assert round(macd352.get_signal().iloc[2], 4) == 1.1528
    assert round(macd352.get_signal().iloc[3], 4) == 1.4988
    assert round(macd352.get_signal().iloc[4], 4) == 1.8981
    assert round(macd352.get_signal().iloc[5], 4) == 0.7961
    assert round(macd352.get_signal().iloc[6], 4) == 0.2785
    assert round(macd352.get_signal().iloc[7], 4) == -0.6186
    assert round(macd352.get_signal().iloc[8], 4) == 0.2329
    assert round(macd352.get_signal().iloc[9], 4) == 1.2266


def test_macd3(mock_sdp, df):
    mock_sdp.history = df
    macd352 = MACD(mock_sdp, lowerEMA=3, higherEMA=7, signalEMA=2)
    assert macd352.buy_signals().iloc[0] == False
    assert macd352.buy_signals().iloc[1] == False
    assert macd352.buy_signals().iloc[2] == False
    assert macd352.buy_signals().iloc[3] == False
    assert macd352.buy_signals().iloc[4] == False
    assert macd352.buy_signals().iloc[5] == False
    assert macd352.buy_signals().iloc[6] == False
    assert macd352.buy_signals().iloc[7] == False
    assert macd352.buy_signals().iloc[8] == True
    assert macd352.buy_signals().iloc[9] == False


def test_macd4(mock_sdp, df):
    mock_sdp.history = df
    macd352 = MACD(mock_sdp, lowerEMA=3, higherEMA=7, signalEMA=2)
    assert macd352.sell_signals().iloc[0] == False
    assert macd352.sell_signals().iloc[1] == False
    assert macd352.sell_signals().iloc[2] == False
    assert macd352.sell_signals().iloc[3] == False
    assert macd352.sell_signals().iloc[4] == False
    assert macd352.sell_signals().iloc[5] == True
    assert macd352.sell_signals().iloc[6] == False
    assert macd352.sell_signals().iloc[7] == False
    assert macd352.sell_signals().iloc[8] == False
    assert macd352.sell_signals().iloc[9] == False


def test_macd5(mock_sdp, df):
    mock_sdp.history = df
    macd352 = MACD(mock_sdp, lowerEMA=3, higherEMA=7, signalEMA=1)
    assert macd352.get_signal().iloc[0] == 0
    assert macd352.get_signal().iloc[1] == 1.25
    assert macd352.get_signal().iloc[2] == 1.3125
    assert macd352.get_signal().iloc[3] == 1.671875
    assert macd352.get_signal().iloc[4] == 2.09765625
    assert round(macd352.get_signal().iloc[5], 7) == 0.2451172
    assert round(macd352.get_signal().iloc[6], 7) == 0.0197754
    assert round(macd352.get_signal().iloc[7], 7) == -1.0671997
    assert round(macd352.get_signal().iloc[8], 7) == 0.6585846
    assert round(macd352.get_signal().iloc[9], 7) == 1.7234306


def test_macd6(mock_sdp, df):
    mock_sdp.history = df
    macd352 = MACD(mock_sdp, lowerEMA=3, higherEMA=7, signalEMA=5)
    assert macd352.get_macd().iloc[0] == 0
    assert macd352.get_macd().iloc[1] == 1.25
    assert macd352.get_macd().iloc[2] == 1.3125
    assert macd352.get_macd().iloc[3] == 1.671875
    assert macd352.get_macd().iloc[4] == 2.09765625
    assert round(macd352.get_macd().iloc[5], 7) == 0.2451172
    assert round(macd352.get_macd().iloc[6], 7) == 0.0197754
    assert round(macd352.get_macd().iloc[7], 7) == -1.0671997
    assert round(macd352.get_macd().iloc[8], 7) == 0.6585846
    assert round(macd352.get_macd().iloc[9], 7) == 1.7234306


def test_macd6(mock_sdp, df):
    mock_sdp.history = df
    macd352 = MACD(mock_sdp, lowerEMA=5, higherEMA=4, signalEMA=-1)
    assert macd352.get_macd().iloc[0] == 0
    assert macd352.get_macd().iloc[1] == 0.5
    assert round(macd352.get_macd().iloc[2], 2) == 0.45
    assert round(macd352.get_macd().iloc[3], 3) == 0.545
    assert round(macd352.get_macd().iloc[4], 4) == 0.6645
    assert round(macd352.get_macd().iloc[5], 4) == -0.1326
    assert round(macd352.get_macd().iloc[6], 4) == -0.1452
    assert round(macd352.get_macd().iloc[7], 4) == -0.5199
    assert round(macd352.get_macd().iloc[8], 4) == 0.2717
    assert round(macd352.get_macd().iloc[9], 4) == 0.6548