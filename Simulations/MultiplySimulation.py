import math
from typing import Tuple, List

import pygame

from Simulation import Simulation, SimulationState
import numpy


def number_to_digits(number, digit_count) -> List[float]:
    return [(number // (2.0) ** i) % 2.0 for i in range(digit_count)]


def digits_to_number(digits) -> int:
    return sum([(digits[i] * (2.0) ** i) for i in range(len(digits))])


class MultiplySimulation(Simulation):

    def __init__(self, batch_size: int = 1,
                 limit: int = 256, verbosity=0, screen=None, shape=None, digits=4):
        """
        A class for representing a simulation of xor
        :param batch_size: The number of agents the simulation can represent in at one time
        :param limit: The limit of the number of times the simulation can be run
        """
        super().__init__(1, 2, screen is not None and shape is not None, shape, screen, batch_size)
        self.verbosity = verbosity
        self.batch_size = batch_size
        self.score = numpy.array([0.0 for i in range(batch_size)])
        self.results = [0 for i in range(batch_size)]
        self.past = numpy.zeros((limit, batch_size, digits * 2))
        self.completed = [False for i in range(batch_size)]
        self.limit = limit
        self.digits = digits

    def get_data_size(self) -> int:
        """
        Get the size of the data the simulation passes to an outside agent
        :return: The length of the data array
        """
        return self.digits * 2 + 1

    def get_controls_size(self) -> int:
        """
        Get the size of the controls the simulation can receive
        :return: The length of the controls array
        """
        return self.digits * 2

    def apply_controls(self, controls: Tuple[float], batch_id: int = None):
        """
        Receives an array of values representing the controls
        Uses that array to apply controls and change the simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :param controls: A tuple of floats, representing the controls
        """
        if batch_id is None:
            self.results = [controls for i in range(self.batch_size)]
            self.completed = [True for i in range(self.batch_size)]

            binary = tuple(number_to_digits(self.time_count, self.digits * 2))
            n1 = digits_to_number(binary[:self.digits])
            n2 = digits_to_number(binary[self.digits:])
            inputs = number_to_digits(n1 * n2, self.digits * 2)

            self.score += [sum([1.0 - ((inputs[i] - result[i]) ** 2.0) for i in range(len(inputs))])
                           for result in self.results]

            self.next()
        else:
            self.results[batch_id] = controls
            self.completed[batch_id] = True

            binary = tuple(number_to_digits(self.time_count, self.digits * 2))
            n1 = digits_to_number(binary[:self.digits])
            n2 = digits_to_number(binary[self.digits:])
            inputs = number_to_digits(n1 * n2, self.digits * 2)

            self.score[batch_id] += sum(
                [1.0 - ((inputs[i] - self.results[batch_id][i]) ** 2.0) for i in range(len(inputs))])

            if all(self.completed):
                self.next()

    def apply_controls_batch(self, controls_batch: List[Tuple[float]]):
        """
        Receives a list of controls to apply to a batch of agents
        :param controls_batch: A list of tuples of floats, representing the controls of many agents
        """
        self.results = [control for control in controls_batch]
        self.completed = [True for i in range(self.batch_size)]

        binary = tuple(number_to_digits(self.time_count, self.digits * 2))
        n1 = digits_to_number(binary[:self.digits])
        n2 = digits_to_number(binary[self.digits:])
        inputs = number_to_digits(n1 * n2, self.digits * 2)

        self.score += [sum([1.0 - ((inputs[i] - result[i]) ** 2.0) for i in range(len(inputs))])
                       for result in self.results]
        # print(self.score)

        self.next()

    def get_data(self, batch_id: int = None) -> Tuple[float, ...]:
        """
        Gets a tuple of floats representing the data that the simulation provides to outside agents
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: a tuple of floats representing the data that the simulation provides to outside agents
        """
        return tuple(number_to_digits(self.time_count, self.digits * 2) + [1])

    def get_data_batch(self) -> List[Tuple[float, ...]]:
        """
        Gets the list of data tuples for all the agents
        :return: a list of tuples of floats representing the data that the simulation provides to a batch of agents
        """
        return [tuple(number_to_digits(self.time_count, self.digits * 2) + [1])] * self.batch_size

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
        self.past[self.time_count, :, :] = numpy.array(self.results)
        # print("\n".join(list(map(lambda row: " ".join(list(map(lambda cell: "%1.0f"%round(cell), row))), self.past[:self.time_count+1]))))
        # print()
        self.time_count += 1
        self.completed = [False for i in range(self.batch_size)]
        if self.screen and self.shape:
            self.draw_scores()

    def restart(self):
        if self.verbosity > 1:
            expected = numpy.array(
                list(map(lambda inputs: int(inputs[0] != inputs[1]), list(map(get_xor_args, list(range(self.limit)))))))
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
            print(" ".join(list(map(lambda val: "%1.4f" % (val), self.score / self.time_count))))
            print("BEST SCORE")
            print(max(list(map(lambda col: (numpy.sum(1.0 - numpy.square((col > 0.5) - expected)) /
                                            self.limit), self.past.transpose()))))
        self.past = numpy.zeros((self.limit, self.batch_size, self.digits * 2))
        self.time_count = 0
        self.score = numpy.array([0.0 for i in range(self.batch_size)])
