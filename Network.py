import NeatLinearNet
import Simulation


class Network:
    def __init__(self, weight_matrix, enabled_matrix, input_size, output_size, middle_size, cache_size=0):
        """

        :param weight_matrix:
        :param enabled_matrix:
        :param input_size:
        :param output_size:
        :param middle_size:
        :param cache_size:
        """
        self.neural_net: NeatLinearNet = NeatLinearNet.NeatLinearNet(input_size, output_size, middle_size,
                                                                     weight_matrix,
                                                                     enabled_matrix)
        self.cache_size = cache_size
        self.cache = {}

    def run(self, input_values: tuple[float]) -> tuple[float]:
        """

        :param input_values:
        :return:
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

        :param simulation:
        :return:
        """
        while simulation.get_state() != Simulation.SimulationState.FINISHED:
            input_data = simulation.get_data()
            processed_data = self.run(input_data)
            simulation.apply_input(processed_data)
        return simulation.get_score()
