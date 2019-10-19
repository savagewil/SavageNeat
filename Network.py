import NeatLinearNet
import Simulation

class Network:
    def __init__(self, weight_matrix, enabled_matrix, input_size, output_size, middle_size):
        self.neural_net:NeatLinearNet = NeatLinearNet.NeatLinearNet(input_size, output_size, middle_size, weight_matrix,
                                                      enabled_matrix)

    def run(self, input: tuple[float]) -> tuple[float]:
        self.neural_net.set_in(input)
        out = self.neural_net.get_out()
        return out

    def execute(self, simulation:Simulation):
        simulation.run([self.neural_net])