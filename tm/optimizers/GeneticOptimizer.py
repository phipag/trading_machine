import random
from typing import List, Tuple, Union, Any

import numpy as np
from deap import base, tools, creator

from tm.trading_rules import TradingRule


# TODO: Replace use more numpy function e.g. to calculate mean and random probabilities
# noinspection PyUnresolvedReferences
class GeneticOptimizer:
    __trading_rules: List[TradingRule]
    __toolbox: base.Toolbox
    __individual_size: int

    @property
    def toolbox(self):
        return self.__toolbox

    def __init__(self, trading_rules: List[TradingRule]):
        self.__trading_rules = trading_rules

        # Create fitness maximization function and "Individual" Type with DEAP creator.
        creator.create('FitnessMax', base.Fitness, weights=(1.0,))
        creator.create('Individual', list, fitness=creator.FitnessMax)

        # Register all function to the DEAP toolbox.
        # Those specify the genetic components and will be called during the execution of the algorithm.
        self.__toolbox = base.Toolbox()
        # Creates a random bit the form of an integer, either 1 or 0.
        self.__toolbox.register('random_bit', np.random.randint, low=0, high=2)
        # Generator for chromosomes (individuals)
        self.__individual_size = self.__calculate_chromosome_length()
        self.__toolbox.register('individual', tools.initRepeat, creator.Individual, self.__toolbox.random_bit,
                                n=self.__individual_size)
        # Generates a population by calling the individual function on the toolbox.
        self.__toolbox.register('population', tools.initRepeat, list, self.__toolbox.individual)
        # Register the genetic operators
        self.__toolbox.register('evaluate', self.__evaluateFitness)
        self.__toolbox.register('mate', tools.cxTwoPoint)
        self.__toolbox.register('mutate', tools.mutFlipBit, indpb=0.05)
        self.__toolbox.register('select', tools.selTournament, tournsize=3)

    # TODO: Replace dummy evaluation by real net profit calculation
    def __evaluateFitness(self, individual) -> Tuple[Union[int, Any]]:
        return sum(individual),

    def __calculate_chromosome_length(self) -> int:
        """
        Calculates the bit encoded chromosome length by using TradingRule.num_bits
        :return: int
        """
        # Reserve one bit for each trading_rule representing a turn on/off binary variable
        total_length = len(self.__trading_rules)
        for rule in self.__trading_rules:
            total_length += sum(rule.num_bits)
        return total_length

    def run(self):
        population = self.__toolbox.population(n=300)
        # Evaluate the entire population
        fitnesses = list(map(self.__toolbox.evaluate, population))
        for individual, fitness in zip(population, fitnesses):
            individual.fitness.values = fitness
            print(individual, fitness, individual.fitness.values)

        # CXPB is the probability with which two individuals are crossed.
        # MUTPB is the probability for mutating an individual.
        CXPB, MUTPB = 0.5, 0.2

        # Extracting all the fitnesses
        fitnesses = [individual.fitness.values[0] for individual in population]

        # Begin the evolution
        # Variable keeping track of the number of generations
        g = 0
        while max(fitnesses) < self.__individual_size and g < 1000:
            # A new generation
            g = g + 1
            print("-- Generation %i --" % g)
            # Select the next generation individuals
            offspring = self.__toolbox.select(population, len(population))
            # Clone the selected individuals
            offspring = list(map(self.__toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    self.__toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            for mutant in offspring:
                if random.random() < MUTPB:
                    self.__toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [individual for individual in offspring if not individual.fitness.valid]
            fitnesses = map(self.__toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            # Replace the population with the offspring
            population[:] = offspring

            # Gather all the fitnesses in one list and print the stats
            fitnesses = [individual.fitness.values[0] for individual in population]

            length = len(population)
            mean = sum(fitnesses) / length
            sum2 = sum(x * x for x in fitnesses)
            std = abs(sum2 / length - mean ** 2) ** 0.5

            print("  Min %s" % min(fitnesses))
            print("  Max %s" % max(fitnesses))
            print("  Avg %s" % mean)
            print("  Std %s" % std)
