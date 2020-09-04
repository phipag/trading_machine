import pytest
from unittest.mock import Mock
from unittest.mock import patch
from tm.optimizers import StrategyPerformanceEvaluator
from tm import StockDataProvider
import pandas as pd

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
def mock_ema(df):
    mock_sdp = Mock(spec=StockDataProvider)
    mock_sdp.history = df
    ema = ExponentialMovingAverage(mock_sdp)
    return ema


@pytest.fixture()
def mock_sma(df):
    mock_sdp = Mock(spec=StockDataProvider)
    mock_sdp.history = df
    sma = SimpleMovingAverage(mock_sdp)
    return sma


def test_net_profit1(mock_sma, monkeypatch):
    # neither buy nor sell signals
    def mock_buy_signals(self):
        return list([False, False, False, False, False, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'buy_signals', mock_buy_signals)

    def mock_sell_signals(self):
        return list([False, False, False, False, False, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'sell_signals', mock_sell_signals)

    evaluator = StrategyPerformanceEvaluator([mock_sma])
    assert evaluator.calculate_net_profit() == 0


def test_net_profit2(mock_sma, monkeypatch):
    # no buy signal
    def mock_buy_signals(self):
        return list([False, False, False, False, False, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'buy_signals', mock_buy_signals)

    def mock_sell_signals(self):
        return list([True, False, False, False, False, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'sell_signals', mock_sell_signals)

    evaluator = StrategyPerformanceEvaluator([mock_sma])
    assert evaluator.calculate_net_profit() == 0


def test_net_profit3(mock_sma, monkeypatch):
    # simple one buy and sell
    def mock_buy_signals(self):
        return list([True, False, False, False, False, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'buy_signals', mock_buy_signals)

    def mock_sell_signals(self):
        return list([False, False, False, False, True, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'sell_signals', mock_sell_signals)

    evaluator = StrategyPerformanceEvaluator([mock_sma])
    assert evaluator.calculate_net_profit() == 7.93


def test_net_profit4(mock_sma, monkeypatch):
    # no sell signals -> added in the end
    def mock_buy_signals(self):
        return list([True, False, False, False, False, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'buy_signals', mock_buy_signals)

    def mock_sell_signals(self):
        return list([False, False, False, False, False, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'sell_signals', mock_sell_signals)

    evaluator = StrategyPerformanceEvaluator([mock_sma])
    assert evaluator.calculate_net_profit() == 8.9275


def test_net_profit5(mock_sma, monkeypatch):
    # no sell signals -> added in the end + consecutive buy signals
    def mock_buy_signals(self):
        return list([True, False, False, False, True, False, False, True, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'buy_signals', mock_buy_signals)

    def mock_sell_signals(self):
        return list([False, False, False, False, False, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'sell_signals', mock_sell_signals)

    evaluator = StrategyPerformanceEvaluator([mock_sma])
    assert evaluator.calculate_net_profit() == 8.9275


def test_net_profit6(mock_sma, monkeypatch):
    # several buy and sell signals
    def mock_buy_signals(self):
        return list([True, False, False, True, False, False, True, False, True, False])

    monkeypatch.setattr(SimpleMovingAverage, 'buy_signals', mock_buy_signals)

    def mock_sell_signals(self):
        return list([False, True, False, False, False, True, False, True, False, True])

    monkeypatch.setattr(SimpleMovingAverage, 'sell_signals', mock_sell_signals)

    evaluator = StrategyPerformanceEvaluator([mock_sma])
    assert evaluator.calculate_net_profit() == -2.275


def test_net_profit7(mock_sma, monkeypatch):
    # first sell signal
    def mock_buy_signals(self):
        return list([False, False, False, False, True, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'buy_signals', mock_buy_signals)

    def mock_sell_signals(self):
        return list([True, False, False, False, False, False, False, True, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'sell_signals', mock_sell_signals)

    evaluator = StrategyPerformanceEvaluator([mock_sma])
    assert evaluator.calculate_net_profit() == -9.0675


def test_net_profit8(mock_sma, monkeypatch):
    # consecutive buys and sells
    def mock_buy_signals(self):
        return list([True, True, True, True, False, True, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'buy_signals', mock_buy_signals)

    def mock_sell_signals(self):
        return list([False, False, False, False, True, False, False, True, True, False])

    monkeypatch.setattr(SimpleMovingAverage, 'sell_signals', mock_sell_signals)

    evaluator = StrategyPerformanceEvaluator([mock_sma])
    assert evaluator.calculate_net_profit() == 5.88


def test_net_profit9(mock_sma, monkeypatch):
    # simultanous buy and sell
    def mock_buy_signals(self):
        return list([True, False, False, True, False, False, False, False, False, False])

    monkeypatch.setattr(SimpleMovingAverage, 'buy_signals', mock_buy_signals)

    def mock_sell_signals(self):
        return list([False, False, False, True, False, False, False, False, True, False])

    monkeypatch.setattr(SimpleMovingAverage, 'sell_signals', mock_sell_signals)

    evaluator = StrategyPerformanceEvaluator([mock_sma])
    assert evaluator.calculate_net_profit() == 6.9325
