from typing import List, Optional

import numpy as np
import pandas as pd
from deap.tools import HallOfFame

from tm import StockDataProvider
from tm.backtesting.MonteCarloSimulation import MonteCarloSimulation
from tm.backtesting.utils import mock_stock_data_provider_closing_prices
from tm.optimizers import StrategyPerformanceEvaluator, map_chromosome_to_trading_rule_parameters, filter_for_active_rules
from tm.trading_rules import TradingRule


class MonteCarloCrossValidation:
    """
    A class used to run cross-validation on a given set of trading rules
    """

    def __init__(self, hof: HallOfFame, monte_carlo_simulator: MonteCarloSimulation, trading_rules: List[TradingRule]):
        """
        Initializes the class with the hall of fame and a simulator
        :param hof: DEAP HallOfFame class containing the best n trading rule combinations found by the genetic algorithm
        :param monte_carlo_simulator: A monte carlo simulator used to artificially generate stock prices for backtesting
        :param trading_rules: List of trading rule classes which have been used by the optimizer to calculate the hall of fame
        """
        self.__hof = hof
        if len(hof) < 1:
            raise ValueError('Please make sure that the hall of fame contains at least one individual.')
        self.__monte_carlo_simulator = monte_carlo_simulator
        self.__trading_rules = trading_rules
        # Contains the best individual of the hall of fame after cross validation
        self.__best_individual: Optional[List[int]] = None

    @property
    def best_individual(self):
        if self.__best_individual is None:
            raise UserWarning('Cannot get the best individual before running the algorithm. Please make sure to call the \'run\' method calling this property.')
        return self.__best_individual

    def run(self, num_iterations: int, time_steps: int) -> List[int]:
        """
        Runs all trading rules in the hall of fame against the artificial stock prices
        :param num_iterations: The number of stock prices to simulate by the simulator
        :param time_steps: The number of stock days to simulate for each simulation
        :return: The trading rule combination with the best average profit as chromosome (bitvector)
        """
        best_rule_index, max_mean_net_profit = 0, float('-inf')
        simulations_df = self.__monte_carlo_simulator.simulate(num_iterations, time_steps)

        for index, individual in enumerate(self.__hof):
            # Collect net_profits on each monte carlo simulation to calculate the mean later
            net_profits: np.ndarray = np.array([])

            for col in simulations_df.columns:
                closing_prices: pd.Series = simulations_df[col]
                # The simulations are no real stock data, therefore the StockDataProvider has to be mocked because it is
                # required by the TradingRule class
                data_provider: StockDataProvider = mock_stock_data_provider_closing_prices(closing_prices)

                # Creates instances for all given TradingRule subclasses and filter for active rules only
                rule_instances = list(map(lambda Rule, params: Rule(data_provider, *params), self.__trading_rules, map_chromosome_to_trading_rule_parameters(individual, self.__trading_rules)))
                active_rule_instances = filter_for_active_rules(individual, rule_instances)

                # Uses the StrategyPerformanceEvaluator to calculate the net profit
                evaluator = StrategyPerformanceEvaluator(active_rule_instances)
                net_profit = evaluator.calculate_net_profit()
                net_profits = np.append(net_profits, net_profit)

            mean_net_profit = np.mean(net_profits)
            if mean_net_profit > max_mean_net_profit:
                best_rule_index, max_mean_net_profit = index, mean_net_profit

        self.__best_individual = self.__hof[best_rule_index]
        print('Best individual:', self.__best_individual)
        print('Best average net profit:', max_mean_net_profit)
        return self.__best_individual
