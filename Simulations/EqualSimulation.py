from typing import Tuple, List

from Simulation import Simulation, SimulationState
import numpy


def get_args(number) -> Tuple[float, float, float, float, float]:
    return float(number % 2), \
           float((number // (2 ** 1)) % 2), \
           float((number // (2 ** 2)) % 2), \
           float((number // (2 ** 3)) % 2), 1.0


class EqualSimulation(Simulation):

    def __init__(self, batch_size: int = 1,
                 limit: int = 19):
        """
        A class for representing a simulation of xor
        :param batch_size: The number of agents the simulation can represent in at one time
        :param limit: The limit of the number of times the simulation can be run
        """
        super().__init__(1, 2, False, None, None, batch_size)
        self.batch_size = batch_size
        self.score = numpy.array([0.0 for i in range(batch_size)])
        self.results = [0 for i in range(batch_size)]
        self.completed = [False for i in range(batch_size)]
        self.limit = limit

    def get_data_size(self) -> int:
        """
        Get the size of the data the simulation passes to an outside agent
        :return: The length of the data array
        """
        return 5

    def get_controls_size(self) -> int:
        """
        Get the size of the controls the simulation can receive
        :return: The length of the controls array
        """
        return 4

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

            inputs = get_args(self.time_count)
            self.score += [1.0 - (sum([((inputs[j] - self.results[j]) ** 2.0)for j in range(len(inputs))])/4)  for i in range(self.batch_size)]

            self.next()
        else:
            self.results[batch_id] = controls[0]
            self.completed[batch_id] = True

            inputs = get_args(self.time_count)
            self.score[batch_id] += 1.0 - (sum([((inputs[j] - self.results[j]) ** 2.0)for j in range(len(inputs))])/4)

            if all(self.completed):
                self.next()

    def apply_controls_batch(self, controls_batch: List[Tuple[float]]):
        """
        Receives a list of controls to apply to a batch of agents
        :param controls_batch: A list of tuples of floats, representing the controls of many agents
        """
        self.results = [control[0] for control in controls_batch]
        self.completed = [True for i in range(self.batch_size)]

        inputs = get_args(self.time_count)
        self.score += [1.0 - (sum([((inputs[j] - self.results[j]) ** 2.0)for j in range(len(inputs))])/4) for result in self.results]
        # print(self.score)

        self.next()

    def get_data(self, batch_id: int = None) -> Tuple[float, float]:
        """
        Gets a tuple of floats representing the data that the simulation provides to outside agents
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: a tuple of floats representing the data that the simulation provides to outside agents
        """
        return get_args(self.time_count)

    def get_data_batch(self) -> List[Tuple[float, float]]:
        """
        Gets the list of data tuples for all the agents
        :return: a list of tuples of floats representing the data that the simulation provides to a batch of agents
        """
        return [get_args(self.time_count)] * self.batch_size

    def get_state(self, batch_id: int = None) -> SimulationState:
        """
        Returns the state of the current simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: The state of the current simulation
        """

        return SimulationState.FINISHED if self.time_count > self.limit else SimulationState.RUNNING

    def get_state_batch(self) -> List[SimulationState]:
        """
        Returns the state of every agent in the batch
        :return: A list of the states of the agents in the current simulation
        """
        return [SimulationState.FINISHED if self.time_count > self.limit else SimulationState.RUNNING] * self.batch_size

    def get_score(self, batch_id: int = None) -> float:
        """
        Gets a score from the current simulation
        :param batch_id: The ID of the agent if the simulation uses batches
        :return: The score
        """
        return self.score[batch_id] / self.time_count

    def get_score_batch(self) -> List[float]:
        """
        Gets a list of scores from the current simulation
        :return: The list of scores for all agents in the batch
        """
        return self.score.copy() / self.time_count

    def next(self):
        self.time_count += 1
        self.completed = [False for i in range(self.batch_size)]

    def restart(self):
        self.time_count = 0
        self.score = numpy.array([0.0 for i in range(self.batch_size)])
