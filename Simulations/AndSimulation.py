import math
from typing import Tuple, List

import pygame

from Simulation import Simulation, SimulationState
import numpy


def get_xor_args(number) -> Tuple[float, float, float]:
    return float(number % 2.0), float((number // (2.0 ** 1.0)) % 2.0), 1.0

def and_func(num1, num2):
    return int(num1 == 1 and num2 == 1)

class AndSimulation(Simulation):

    def __init__(self, batch_size: int = 1,
                 limit: int = 4, screen=None, shape=None):
        """
        A class for representing a simulation of xor
        :param batch_size: The number of agents the simulation can represent in at one time
        :param limit: The limit of the number of times the simulation can be run
        """
        super().__init__(1, 2, screen is not None and shape is not None, shape, screen, batch_size)
        self.batch_size = batch_size
        self.score = numpy.array([0.0 for i in range(batch_size)])
        self.results = [0 for i in range(batch_size)]
        self.past = numpy.zeros((limit, batch_size))
        self.completed = [False for i in range(batch_size)]
        self.limit = limit

    def get_data_size(self) -> int:
        """
        Get the size of the data the simulation passes to an outside agent
        :return: The length of the data array
        """
        return 3

    def get_controls_size(self) -> int:
        """
        Get the size of the controls the simulation can receive
        :return: The length of the controls array
        """
        return 1

    def apply_controls(self, controls: Tuple[float], batch_id: int = None):
        """
        Receives an array of values representing the controls
        Uses that array to apply controls and change the simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :param controls: A tuple of floats, representing the controls
        """
        if batch_id is None:
            self.results = [controls[0] for i in range(self.batch_size)]
            self.completed = [True for i in range(self.batch_size)]

            inputs = get_xor_args(self.time_count)
            self.score += [1.0 - ((and_func(inputs[0], inputs[1]) - self.results[i]) ** 2.0) for i in
                           range(self.batch_size)]

            self.next()
        else:
            self.results[batch_id] = controls[0]
            self.completed[batch_id] = True

            inputs = get_xor_args(self.time_count)
            self.score[batch_id] += 1.0 - ((and_func(inputs[0], inputs[1]) - self.results[batch_id]) ** 2.0)

            if all(self.completed):
                self.next()

    def apply_controls_batch(self, controls_batch: List[Tuple[float]]):
        """
        Receives a list of controls to apply to a batch of agents
        :param controls_batch: A list of tuples of floats, representing the controls of many agents
        """
        self.results = [control[0] for control in controls_batch]
        self.completed = [True for i in range(self.batch_size)]

        inputs = get_xor_args(self.time_count)
        self.score += [1.0 - ((and_func(inputs[0], inputs[1]) - result) ** 2.0) for result in self.results]
        # print(self.score)

        self.next()

    def get_data(self, batch_id: int = None) -> Tuple[float, float, float]:
        """
        Gets a tuple of floats representing the data that the simulation provides to outside agents
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: a tuple of floats representing the data that the simulation provides to outside agents
        """
        return get_xor_args(self.time_count)

    def get_data_batch(self) -> List[Tuple[float, float, float]]:
        """
        Gets the list of data tuples for all the agents
        :return: a list of tuples of floats representing the data that the simulation provides to a batch of agents
        """
        return [get_xor_args(self.time_count)] * self.batch_size

    def get_state(self, batch_id: int = None) -> SimulationState:
        """
        Returns the state of the current simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: The state of the current simulation
        """

        return SimulationState.RUNNING if self.time_count < self.limit else SimulationState.FINISHED

    def get_state_batch(self) -> List[SimulationState]:
        """
        Returns the state of every agent in the batch
        :return: A list of the states of the agents in the current simulation
        """
        return [SimulationState.RUNNING if self.time_count < self.limit else SimulationState.FINISHED] * self.batch_size

    def get_score(self, batch_id: int = None) -> float:
        """
        Gets a score from the current simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: The score
        """
        return self.score[batch_id] / (self.time_count)

    def get_score_batch(self) -> List[float]:
        """
        Gets a list of scores from the current simulation
        :return: The list of scores for all agents in the batch
        """
        return self.score.copy() / (self.time_count)

    def next(self):
        # print("\n".join(list(map(lambda row: " ".join(list(map(lambda cell: "%1.0f"%round(cell), row))), self.past[:self.time_count+1]))))
        # print()
        self.past[self.time_count, :] = self.results
        # print("\n".join(list(map(lambda row: " ".join(list(map(lambda cell: "%1.0f"%round(cell), row))), self.past[:self.time_count+1]))))
        # print()
        self.time_count += 1
        self.completed = [False for i in range(self.batch_size)]
        if self.screen and self.shape:
            self.draw_scores()

    def restart(self):
        expected = numpy.array(
            list(map(lambda inputs: int(inputs[0] == 1 and inputs[1] == 1), list(map(get_xor_args, list(range(self.limit)))))))
        # print(expected)
        print("PAST")
        print("\n".join(list(map(lambda row: " ".join(list(map(lambda cell: "%1.4f" % cell, row))), self.past))))
        print("REAL SCORE")
        print(" ".join(list(
            map(lambda col: "%1.4f" % (numpy.sum(1.0 - numpy.square(col - expected)) / self.limit),
                self.past.transpose()))))
        print("ROUNDED SCORE")
        print(" ".join(list(map(lambda col: "%1.4f" % (numpy.sum(1.0 - numpy.square(numpy.round(col) - expected)) /
                                                       self.limit), self.past.transpose()))))
        print("SCORE")
        print(" ".join(list(map(lambda val: "%1.4f" % (val), self.score / (self.time_count)))))
        print("BEST SCORE")
        print(max(list(map(lambda col: (numpy.sum(1.0 - numpy.square((col > 0.5) - expected)) /
                                        self.limit), self.past.transpose()))))
        self.past = numpy.zeros((self.limit, self.batch_size))
        self.time_count = 0
        self.score = numpy.array([0.0 for i in range(self.batch_size)])