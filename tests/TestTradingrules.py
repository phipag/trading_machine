import unittest
import math
from tm import StockDataProvider
from tm.trading_rules import SimpleMovingAverage
from tm.trading_rules import ExponentialMovingAverage


class TestTradingrules(unittest.TestCase):

    def test_sma(self):
        sma3 = SimpleMovingAverage(StockDataProvider(ticker_name='MSFT', start="2015-01-02", end="2015-01-16"), days=3)
        self.assertTrue(math.isnan(sma3.calculate().iloc[0]))
        self.assertTrue(math.isnan(sma3.calculate().iloc[1]))
        self.assertAlmostEqual(sma3.calculate().iloc[2], 41.29, places=6)
        self.assertAlmostEqual(sma3.calculate().iloc[3], 41.133333, places=6)
        self.assertAlmostEqual(sma3.calculate().iloc[4], 41.51, places=6)
        self.assertAlmostEqual(sma3.calculate().iloc[5], 41.966667, places=6)
        self.assertAlmostEqual(sma3.calculate().iloc[6], 42.076667, places=6)
        self.assertAlmostEqual(sma3.calculate().iloc[7], 41.71, places=6)
        self.assertAlmostEqual(sma3.calculate().iloc[8], 41.343333, places=6)
        self.assertAlmostEqual(sma3.calculate().iloc[9], 41.01, places=6)

        self.assertEqual(sma3.buy_signals().iloc[0], False)
        self.assertEqual(sma3.buy_signals().iloc[1], False)
        self.assertEqual(sma3.buy_signals().iloc[2], False)
        self.assertEqual(sma3.buy_signals().iloc[3], True)
        self.assertEqual(sma3.buy_signals().iloc[4], True)
        self.assertEqual(sma3.buy_signals().iloc[5], False)
        self.assertEqual(sma3.buy_signals().iloc[6], False)
        self.assertEqual(sma3.buy_signals().iloc[7], False)
        self.assertEqual(sma3.buy_signals().iloc[8], False)
        self.assertEqual(sma3.buy_signals().iloc[9], False)

        self.assertEqual(sma3.sell_signals().iloc[0], False)
        self.assertEqual(sma3.sell_signals().iloc[1], False)
        self.assertEqual(sma3.sell_signals().iloc[2], True)
        self.assertEqual(sma3.sell_signals().iloc[3], False)
        self.assertEqual(sma3.sell_signals().iloc[4], False)
        self.assertEqual(sma3.sell_signals().iloc[5], False)
        self.assertEqual(sma3.sell_signals().iloc[6], True)
        self.assertEqual(sma3.sell_signals().iloc[7], False)
        self.assertEqual(sma3.sell_signals().iloc[8], True)
        self.assertEqual(sma3.sell_signals().iloc[9], True)

        sma8 = SimpleMovingAverage(StockDataProvider(ticker_name='MSFT', start="2015-01-02", end="2015-01-16"), days=8)
        self.assertTrue(math.isnan(sma8.calculate().iloc[0]))
        self.assertTrue(math.isnan(sma8.calculate().iloc[1]))
        self.assertTrue(math.isnan(sma8.calculate().iloc[2]))
        self.assertTrue(math.isnan(sma8.calculate().iloc[3]))
        self.assertTrue(math.isnan(sma8.calculate().iloc[4]))
        self.assertTrue(math.isnan(sma8.calculate().iloc[5]))
        self.assertTrue(math.isnan(sma8.calculate().iloc[6]))
        self.assertAlmostEqual(sma8.calculate().iloc[7], 41.59625, places=6)
        self.assertAlmostEqual(sma8.calculate().iloc[8], 41.50625, places=6)
        self.assertAlmostEqual(sma8.calculate().iloc[9], 41.4125, places=6)

        self.assertEqual(sma8.buy_signals().iloc[0], False)
        self.assertEqual(sma8.buy_signals().iloc[1], False)
        self.assertEqual(sma8.buy_signals().iloc[2], False)
        self.assertEqual(sma8.buy_signals().iloc[3], False)
        self.assertEqual(sma8.buy_signals().iloc[4], False)
        self.assertEqual(sma8.buy_signals().iloc[5], False)
        self.assertEqual(sma8.buy_signals().iloc[6], False)
        self.assertEqual(sma8.buy_signals().iloc[7], False)
        self.assertEqual(sma8.buy_signals().iloc[8], False)
        self.assertEqual(sma8.buy_signals().iloc[9], False)

        self.assertEqual(sma8.sell_signals().iloc[0], False)
        self.assertEqual(sma8.sell_signals().iloc[1], False)
        self.assertEqual(sma8.sell_signals().iloc[2], False)
        self.assertEqual(sma8.sell_signals().iloc[3], False)
        self.assertEqual(sma8.sell_signals().iloc[4], False)
        self.assertEqual(sma8.sell_signals().iloc[5], False)
        self.assertEqual(sma8.sell_signals().iloc[6], False)
        self.assertEqual(sma8.sell_signals().iloc[7], True)
        self.assertEqual(sma8.sell_signals().iloc[8], False)
        self.assertEqual(sma8.sell_signals().iloc[9], False)

if __name__ == '__main__':
    unittest.main()
