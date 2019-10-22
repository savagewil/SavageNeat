from abc import abstractmethod
from typing import List, Type, Callable
import Net
import numpy
import pygame
import enum


class SimulationState(enum):
    FINISHED = 0
    NOT_STARTED = 1
    RUNNING = 2


class Simulation:

    def __init__(self,
                 controls_size: int,
                 data_size: int,
                 visuals: bool = False):
        """
        A class for representing a simulation
        :param controls_size: The length of the controls the simulation will use
        :param data_size: The length of the data the simulation passes to outside agents
        :param visuals: A boolean to control whether the simulation is displayed or not
        """
        self.controls_size = controls_size
        self.data_size = data_size
        self.time_count = 0

    def restart(self):
        """
        Restarts the simulation
        If the simulation changes over time,
        this function should return it to the original state.
        """
        self.time_count = 0

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

    @abstractmethod
    def apply_controls(self, controls: tuple[float]):
        """
        Receives an array of values representing the controls
        Uses that array to apply controls and change the simulation
        :param controls: A tuple of floats, representing the controls
        """
        pass

    @abstractmethod
    def get_data(self) -> tuple[float]:
        """
        Gets a tuple of floats representing the data that the simulation provides to outside agents
        :return: a tuple of floats representing the data that the simulation provides to outside agents
        """
        pass

    @abstractmethod
    def get_state(self) -> SimulationState:
        """
        Returns the state of the current simulation
        :return: The state of the current simulation
        """
        pass

    @abstractmethod
    def get_score(self) -> float:
        """
        Gets a score from the current simulation
        :return: The score
        """
        pass
