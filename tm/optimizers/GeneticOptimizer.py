import random
from functools import reduce
from typing import List, Tuple, Union, Any

import numpy as np
from deap import base, tools, creator, algorithms

from tm import StockDataProvider
from tm.optimizers.StrategyPerformanceEvaluator import StrategyPerformanceEvaluator
from tm.optimizers.utils import map_chromosome_to_trading_rule_parameters, filter_for_active_rules
from tm.trading_rules import TradingRule


# noinspection PyUnresolvedReferences
class GeneticOptimizer:
    def __init__(self, stock_data_provider: StockDataProvider, trading_rules: List[TradingRule], random_seed=1337):
        self.__trading_rules: List[TradingRule] = trading_rules
        self.__stock_data_provider: StockDataProvider = stock_data_provider

        if random_seed is not None:
            np.random.seed(random_seed)
            random.seed(random_seed)

        # Create fitness maximization function and "Individual" Type with DEAP creator.
        creator.create('FitnessMax', base.Fitness, weights=(1.0,))
        creator.create('Individual', list, fitness=creator.FitnessMax)

        # Register all functions to the DEAP toolbox.
        # Those specify the genetic components and will be called during the execution of the algorithm.
        self.__toolbox: base.Toolbox = base.Toolbox()
        # Creates a random bit in the form of an integer, either 1 or 0.
        self.__toolbox.register('random_bit', np.random.randint, low=0, high=2)
        # Generator for chromosomes (individuals)
        self.__individual_size: int = self.__calculate_chromosome_length()
        self.__toolbox.register('individual', tools.initRepeat, creator.Individual, self.__toolbox.random_bit, n=self.__individual_size)
        # Generates a population by calling the individual function on the toolbox.
        self.__toolbox.register('population', tools.initRepeat, list, self.__toolbox.individual)
        # Register the genetic operators
        self.__toolbox.register('evaluate', self.__evaluateFitness)
        self.__toolbox.register('mate', tools.cxTwoPoint)
        self.__toolbox.register('mutate', tools.mutFlipBit, indpb=0.05)
        self.__toolbox.register('select', tools.selTournament, tournsize=3)

    @property
    def toolbox(self):
        return self.__toolbox

    # noinspection PyPep8Naming
    def __evaluateFitness(self, individual: List[int]) -> Tuple[Union[int, Any]]:
        rule_instances = list(map(lambda Rule, params: Rule(self.__stock_data_provider, *params), self.__trading_rules, map_chromosome_to_trading_rule_parameters(individual, self.__trading_rules)))
        active_rule_instances = filter_for_active_rules(individual, rule_instances)
        if len(active_rule_instances) == 0:
            return (0,)
        evaluator = StrategyPerformanceEvaluator(active_rule_instances)
        net_profit, last_sell_signal = evaluator.calculate_net_profit()
        return net_profit,

    def __calculate_chromosome_length(self) -> int:
        """
        Calculates the bit encoded chromosome length by using TradingRule.num_bits
        :return: int
        """
        # Reserve one bit for each trading rule representing a turn on/off binary variable
        num_on_off_bits = len(self.__trading_rules)
        total_length = reduce(lambda accumulator, rule: accumulator + sum(rule.num_bits), self.__trading_rules, num_on_off_bits)
        return total_length

    def run(self, pop_size: int = 300, ngen: int = 15, cxpb: float = 0.5, mutpb: float = 0.2, hof_size: int = 5) -> tools.HallOfFame:
        if not 0 <= cxpb <= 1 or not 0 <= mutpb <= 1:
            raise ValueError('"cxpb" and "mutpb" parameters must be probabilities in the interval [0, 1].')
        population = self.__toolbox.population(n=pop_size)
        stats = tools.Statistics(lambda individual: individual.fitness.values)
        stats.register('min', np.min)
        stats.register('max', np.max)
        stats.register('mean', np.mean)
        stats.register('std', np.std)
        hof = tools.HallOfFame(hof_size)
        algorithms.eaSimple(population, self.__toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen, stats=stats, halloffame=hof)

        return hof
