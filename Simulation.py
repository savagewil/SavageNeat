import math
from abc import abstractmethod
from typing import List, Type, Callable, Tuple
import Net
import numpy
import pygame
import enum


class SimulationState(enum.Enum):
    """
    SimulationState is an Enumeration which represents the state a simulation is currently in
    """
    FINISHED = 0
    NOT_STARTED = 1
    RUNNING = 2


class Simulation:

    def __init__(self,
                 controls_size: int,
                 data_size: int,
                 visuals: bool = False,
                 shape: Tuple[int, int, int, int] = None,
                 screen: pygame.Surface = None,
                 batch_size: int = 1,
                 verbosity: int = 0):
        """
        A class for representing a simulation
        :param controls_size: The length of the controls the simulation will use
        :param data_size: The length of the data the simulation passes to outside agents
        :param visuals: A boolean to control whether the simulation is displayed or not
        :param shape: The area to display the Simulation on a surface, [x, y, width, height
        :param screen: A pygame surface where the Simulation will be displayed
        :param batch_size: The number of agents the simulation can represent in at one time
        :param verbosity: How "verbal" the simulation should be
        """
        self.verbosity = verbosity
        self.controls_size = controls_size
        self.data_size = data_size
        self.visuals = visuals
        self.shape = shape
        self.screen = screen
        self.time_count = 0
        self.batch_size = batch_size

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
    def apply_controls(self, controls: Tuple[float], batch_id: int = None):
        """
        Receives an array of values representing the controls
        Uses that array to apply controls and change the simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :param controls: A tuple of floats, representing the controls
        """
        pass

    @abstractmethod
    def apply_controls_batch(self, controls_batch: List[Tuple[float]]):
        """
        Receives a list of controls to apply to a batch of agents
        :param controls_batch: A list of tuples of floats, representing the controls of many agents
        """
        pass

    @abstractmethod
    def get_data(self, batch_id: int = None) -> Tuple[float]:
        """
        Gets a tuple of floats representing the data that the simulation provides to outside agents
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: a tuple of floats representing the data that the simulation provides to outside agents
        """
        pass

    @abstractmethod
    def get_data_batch(self) -> List[Tuple[float]]:
        """
        Gets the list of data tuples for all the agents
        :return: a list of tuples of floats representing the data that the simulation provides to a batch of agents
        """
        pass

    @abstractmethod
    def get_state(self, batch_id: int = None) -> SimulationState:
        """
        Returns the state of the current simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: The state of the current simulation
        """
        pass

    @abstractmethod
    def get_state_batch(self) -> List[SimulationState]:
        """
        Returns the state of every agent in the batch
        :return: A list of the states of the agents in the current simulation
        """
        pass

    @abstractmethod
    def get_score(self, batch_id: int = None) -> float:
        """
        Gets a score from the current simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: The score
        """
        pass

    @abstractmethod
    def get_score_batch(self) -> List[float]:
        """
        Gets a list of scores from the current simulation
        :return: The list of scores for all agents in the batch
        """
        pass


    def draw_scores(self, delay=100):
        height = math.ceil(math.sqrt(self.batch_size))
        width = math.floor(math.sqrt(self.batch_size))
        count = 0
        for score in self.get_score_batch():
            text = "%0.3f" % (score)
            font = pygame.font.Font(None, 32)
            design = font.render(text, True, (0, 0, 0))
            self.screen.fill((min(255, max(0, int(255 * (1.0 - score)))), min(255, max(0, int(255 * score))), 0),
                        rect=pygame.Rect(
                            int((self.shape[2] / width) * (count % width)) + self.shape[0] + int((self.shape[2] / width) / 2),
                            int((self.shape[3] / height) * (count // width)) + self.shape[1],
                            int((self.shape[2] / width) / 2), int((self.shape[3] / height))))

            self.screen.blit(design,
                        pygame.Rect(int((self.shape[2] / width) * (count % width)) + self.shape[0] + int((self.shape[2] / width) / 2),
                                    int((self.shape[3] / height) * (count // width)) + self.shape[1] + int(
                                        (self.shape[3] / height) / 2),
                                    int((self.shape[2] / width) / 2),
                                    int((self.shape[3] / height) / 2)))
            count += 1
        pygame.display.flip()
        pygame.time.delay(delay)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                raise InterruptedError
