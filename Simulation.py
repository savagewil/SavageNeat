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
                 input_size: int,
                 data_size: int):
        self.input_size = input_size
        self.data_size = data_size
        self.time_count = 0

    def restart(self):
        self.time_count = 0

    @abstractmethod
    def get_data_size(self):
        return self.data_size

    @abstractmethod
    def get_input_size(self):
        return self.input_size

    @abstractmethod
    def apply_input(self, input_values: tuple[float]):
        pass

    @abstractmethod
    def get_data(self) -> tuple[float]:
        pass

    @abstractmethod
    def get_state(self) -> int:
        pass

    @abstractmethod
    def get_score(self) -> SimulationState:
        pass
