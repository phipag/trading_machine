from typing import List

import numpy as np
import pandas as pd

from tm import StockDataProvider
from tm.backtesting.MonteCarloSimulation import MonteCarloSimulation


class GeometricBrownianMotion(MonteCarloSimulation):
    def __init__(self, data: StockDataProvider):
        self.__closing_prices: pd.Series = data.history['Close']

    def __fit_geometric_brownian_motion(self, time_steps: int) -> pd.Series:
        log_returns = self.__get_log_returns()
        mean = log_returns.mean()
        variance = log_returns.var()
        standard_deviation = log_returns.std()

        drift = mean - 0.5 * variance
        gbm_multipliers: np.ndarray = np.exp(drift + standard_deviation * np.random.standard_normal(time_steps))

        start_price = self.__closing_prices.iloc[-1]
        gbm_stock_prices = np.zeros(time_steps)
        gbm_stock_prices[0] = start_price

        for i in range(1, time_steps):
            gbm_stock_prices[i] = gbm_stock_prices[i - 1] * gbm_multipliers[i]

        return pd.Series(gbm_stock_prices, index=pd.date_range(self.__closing_prices.index[-1], periods=time_steps, freq='D'))

    def simulate(self, num_simulations: int, time_steps: int) -> pd.DataFrame:
        simulations: List[pd.Series] = []
        for i in range(num_simulations):
            simulations.append(self.__fit_geometric_brownian_motion(time_steps))
        return pd.concat(simulations, axis=1)

    def __get_log_returns(self) -> pd.Series:
        return np.log(1 + self.__closing_prices.pct_change())
