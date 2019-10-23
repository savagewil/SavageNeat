from typing import Tuple
import numpy as np
from NeatLinearNet import NeatLinearNet
import Simulation


class Network:
    def __init__(self, weight_matrix: np.array, enabled_matrix: np.array, input_size: int, output_size: int,
                 middle_size: int, cache_size: int = 0, batch_id: int = None):

        """
        The Network represents a Neural Network
        Can have a cache to save answers
        :param weight_matrix: The matrix representing the weights of the neural network
        :param enabled_matrix: The matrix showing which connections exist in the neural network
        :param input_size: The number of input nodes to the network
        :param output_size: The number of output nodes from the network
        :param middle_size: The number of hidden nodes in the network
        :param cache_size: The size, in cache entries, of the cache for saving answers
        """
        self.neural_net: NeatLinearNet = NeatLinearNet(input_size, output_size, middle_size,
                                                       weight_matrix, enabled_matrix)
        self.cache_size: int = cache_size
        self.cache: dict = {}
        self.batch_id: int = batch_id

    def run(self, input_values: Tuple[float]) -> Tuple[float]:
        """
        Runs the neural network on an input and returns the output
        If the cache exists, it checks if the input is in the cache
        If using a cache, caches the output
        :param input_values: The values to use as input to the network
        :return: The values from the output layer of the neural network
        """
        if input_values in self.cache:
            out = self.cache[input_values]
            self.cache.pop(input_values)
            self.cache[input_values] = out
            return out
        else:
            self.neural_net.set_in(input_values)
            out = self.neural_net.get_out()
            if len(self.cache) >= self.cache_size > 0:
                self.cache.pop(list(self.cache.keys())[0])
                self.cache[input_values] = out
            elif len(self.cache) < self.cache_size:
                self.cache[input_values] = out
            return out

    def execute(self, simulation: Simulation):
        """
        Runs a simulation using the using the neural network as the agent
        :param simulation: The simulation to run, and get the score from
        :return: The score from the simulation
        """
        while simulation.get_state(batch_id=self.batch_id) != Simulation.SimulationState.FINISHED:
            input_data = simulation.get_data(batch_id=self.batch_id)
            processed_data = self.run(input_data)
            simulation.apply_controls(processed_data, batch_id=self.batch_id)
        return simulation.get_score()

    def set_batch_id(self, batch_id: int):
        """
        Sets the batch id of the network
        :param batch_id: The batch id to change the current batch id to
        """
        self.batch_id = batch_id
