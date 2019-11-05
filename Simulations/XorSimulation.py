from typing import Tuple, List

import pygame

from Simulation import Simulation


class XorSimulation(Simulation):

    def __init__(self, visuals: bool = False,
                 shape: Tuple[int, int, int, int] = None, screen: pygame.Surface = None, batch_size: int = 1):
        """
        A class for representing a simulation
        :param controls_size: The length of the controls the simulation will use
        :param data_size: The length of the data the simulation passes to outside agents
        :param visuals: A boolean to control whether the simulation is displayed or not
        :param shape: The area to display the Simulation on a surface, [x, y, width, height
        :param screen: A pygame surface where the Simulation will be displayed
        :param batch_size: The number of agents the simulation can represent in at one time
        """
        super().__init__(1, 2, visuals, shape, screen, batch_size)
        self.score = [0.0 for i in range(batch_size)]
        self.results = [0 for i in range(batch_size)]
        self.completed = [False for i in range(batch_size)]


    def get_data_size(self) -> int:
        """
        Get the size of the data the simulation passes to an outside agent
        :return: The length of the data array
        """
        return 2

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
            self.score = [0.0 for i in range(batch_size)]
            self.results = [controls[0] for i in range(batch_size)]
            self.completed = [True for i in range(batch_size)]
            self.next()
        else:


            self.results[batch_id] = controls[0]
            self.completed[batch_id] = True
            self.score[batch_id] =

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

    def next(self):
