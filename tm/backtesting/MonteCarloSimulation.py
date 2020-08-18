from abc import ABC, abstractmethod


class MonteCarloSimulation(ABC):
    @abstractmethod
    def simulate(self, num_iterations: int, time_steps: int):
        pass
