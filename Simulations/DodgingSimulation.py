import math
import random
from abc import abstractmethod
from typing import List, Type, Callable, Tuple
import Net
import numpy
import pygame
import enum

from Simulation import Simulation, SimulationState


class DodgingSimulation(Simulation):

    def __init__(self,
                 width: int,
                 depth: int,
                 shape: Tuple[int, int, int, int] = None,
                 screen: pygame.Surface = None,
                 batch_size: int = 1,
                 verbosity: int = 0,
                 obstacles=1,
                 delay=0):
        """
        A class for representing a simulation
        :param shape: The area to display the Simulation on a surface, [x, y, width, height
        :param screen: A pygame surface where the Simulation will be displayed
        :param batch_size: The number of agents the simulation can represent in at one time
        :param verbosity: How "verbal" the simulation should be
        """
        super().__init__(2,
                         (width * 2 - 1) * depth,
                         visuals=shape is not None,
                         shape=shape,
                         screen=screen,
                         batch_size=batch_size,
                         verbosity=verbosity)
        assert width % 2 == 1
        self.width = width
        self.depth = depth
        self.obstacles = obstacles
        self.delay = delay
        self.grid = numpy.zeros((self.width, self.depth))
        self.living = numpy.array([True] * self.batch_size)
        self.scores = numpy.array([0] * self.batch_size)
        self.locations = numpy.array([self.width // 2] * self.batch_size)
        self.moved = numpy.array([False] * self.batch_size)

    def restart(self):
        """
        Restarts the simulation
        If the simulation changes over time,
        this function should return it to the original state.
        """
        self.time_count = 0
        self.grid = numpy.zeros((self.width, self.depth))
        self.living = numpy.array([True] * self.batch_size)
        self.scores = numpy.array([0] * self.batch_size)
        self.locations = numpy.array([self.width // 2] * self.batch_size)
        self.moved = numpy.array([False] * self.batch_size)

    def get_data_size(self) -> int:
        """
        Get the size of the data the simulation passes to an outside agent
        :return: The length of the data array
        """
        return self.data_size

    def get_controls_size(self) -> int:
        """
        Get the size of the controls the simulation can receive
        :return: The length of the controls array
        """
        return self.controls_size

    def apply_controls(self, controls: Tuple[float, ...], batch_id: int = None):
        """
        Receives an array of values representing the controls
        Uses that array to apply controls and change the simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :param controls: A tuple of floats, representing the controls
        """
        if (controls[0] >= 0.5 and controls[1] >= 0.5) or (controls[0] < 0.5 and controls[1] < 0.5):
            if batch_id and self.living[batch_id] and not self.moved[batch_id]:
                self.moved[batch_id] = True
            elif not batch_id:
                self.moved[:] = True

        elif controls[0] >= 0.5:
            if batch_id and self.living[batch_id] and not self.moved[batch_id]:
                self.locations[batch_id] -= 1
                self.moved[batch_id] = True
            elif not batch_id:
                self.locations = self.locations - 1 * self.living * ~self.moved
                self.moved[:] = True
        elif controls[1] >= 0.5:
            if batch_id and self.living[batch_id]:
                self.locations[batch_id] += 1
                self.moved[batch_id] = True
            elif not batch_id:
                self.locations = self.locations + 1 * self.living * ~self.moved
                self.moved[:] = True
        self.next()

    def apply_controls_batch(self, controls_batch: List[Tuple[float]]):
        """
        Receives a list of controls to apply to a batch of agents
        :param controls_batch: A list of tuples of floats, representing the controls of many agents
        """
        left_controls = numpy.array([control[0] for control in controls_batch]) >= 0.5
        right_controls = numpy.array([control[1] for control in controls_batch]) >= 0.5
        # print(right_controls)
        # print(left_controls)

        self.locations = self.locations + (~self.moved) * self.living * (
                right_controls.astype(int) - left_controls.astype(int))
        self.moved = self.moved | self.living & True
        self.next()

    def get_data(self, batch_id: int = None) -> Tuple[float]:
        """
        Gets a tuple of floats representing the data that the simulation provides to outside agents
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: a tuple of floats representing the data that the simulation provides to outside agents
        """
        if batch_id is not None:
            view = numpy.ones(((self.width * 2 - 1), self.depth))
            shift = self.locations[batch_id] - self.width // 2
            view[self.width // 2 + shift: (3 * self.width) // 2 + shift, :] = \
                self.grid[max(0, -self.locations[batch_id]):
                          min(self.width, self.width * 2 - self.locations[batch_id] - 1)]
            return tuple(view.flatten())

        else:
            print(max(0, -self.locations[0]),
                  min(self.width, self.width * 2 - self.locations[0]),
                  -self.locations[0],
                  self.width * 2 - self.locations[0] - 1)
            view = numpy.ones(((self.width * 2 - 1), self.depth))
            shift = self.locations[0] - self.width // 2
            view[self.width // 2 + shift: (3 * self.width) // 2 + shift, :] = \
                self.grid[max(0, -self.locations[0]):
                          min(self.width, self.width * 2 - self.locations[0] - 1)]
            return tuple(view.flatten())

    def get_data_batch(self) -> List[Tuple[float]]:
        """
        Gets the list of data tuples for all the agents
        :return: a list of tuples of floats representing the data that the simulation provides to a batch of agents
        """
        views = [numpy.ones(((self.width * 2 - 1), self.depth)) for i in range(self.batch_size)]
        shifts = self.locations - (self.width // 2)
        # print(self.locations)
        # print(shifts)
        for i in range(self.batch_size):
            # print("--%d--"%i)
            # print(max(self.width//2 + shifts[i], 0), min((3 * self.width)//2 + shifts[i], self.width * 2 - 1))
            # print(max(0, -self.locations[i]), min(self.width, self.width * 2 - self.locations[i] - 1))
            # print(-self.locations[i], self.width * 2 - self.locations[i] - 1)

            views[i][max(self.width // 2 + shifts[i], 0): min((3 * self.width) // 2 + shifts[i], self.width * 2 - 1),
            :] = \
                self.grid[max(0, -self.locations[i]):
                          min(self.width, self.width * 2 - self.locations[i] - 1)]
        return [tuple(view.flatten()) for view in views]

    def get_state(self, batch_id: int = None) -> SimulationState:
        """
        Returns the state of the current simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: The state of the current simulation
        """
        if batch_id:
            return SimulationState.RUNNING if self.living[batch_id] else SimulationState.FINISHED
        else:
            return SimulationState.RUNNING if any(self.living) else SimulationState.FINISHED

    def get_state_batch(self) -> List[SimulationState]:
        """
        Returns the state of every agent in the batch
        :return: A list of the states of the agents in the current simulation
        """
        return [SimulationState.RUNNING if live else SimulationState.FINISHED for live in self.living]

    def get_score(self, batch_id: int = None) -> float:
        """
        Gets a score from the current simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: The score
        """
        return self.scores[batch_id] if batch_id else self.scores[0]

    def get_score_batch(self) -> List[float]:
        """
        Gets a list of scores from the current simulation
        :return: The list of scores for all agents in the batch
        """
        return self.scores.copy()

    def next(self):
        """
        Moves to the next step in the simulation
        """
        if not any(self.moved != self.living):
            self.time_count += 1
            self.grid[:, :-1] = self.grid[:, 1:]
            self.grid[:, -1] = numpy.zeros((self.width,))
            self.grid[random.sample(list(range(self.width)), self.obstacles), -1] = 1

            locations = self.locations * (self.locations >= 0) * (self.locations < self.width)

            print(self)

            self.living = self.living & \
                          (1 != self.grid[:, 0][locations]) & \
                          (self.locations >= 0) & \
                          (self.locations < self.width)
            self.scores += self.living

            self.moved = numpy.array([False] * self.batch_size)

    def __str__(self):
        pygame.time.delay(self.delay)
        string = "=" * self.depth + "\n"
        for w in range(self.width):
            for d in range(self.depth):
                if self.grid[w][d] == 1 and d == 0 and any((self.locations == w) & self.living):
                    string += "X"
                elif self.grid[w][d] == 1:
                    string += "0"
                elif d == 0 and any((self.locations == w) & self.living):
                    string += ">"
                else:
                    string += " "
            string += "\n"

        string += "=" * self.depth + "\n"
        return string


if __name__ == '__main__':
    sim = DodgingSimulation(9, 5, obstacles=4, batch_size=1)
    while sim.get_state() == SimulationState.RUNNING:
        print(sim)
        print("Scores:", sim.get_score_batch())
        IN = input("left(1) or right(0)")
        left = float(int(IN == '1'))
        right = float(int(IN == '0'))
        sim.apply_controls((left, right))
        print(numpy.reshape(sim.get_data(), (sim.width * 2 - 1, sim.depth)))
        sim.next()
