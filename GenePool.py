from typing import Dict
from Gene import Gene

class ConnectionInnovationDict(dict):


class GenePool:
    def __init__(self, innovation_number: int, node_number: int):
        """

        :param innovation_number:
        :param node_number:
        """
        self.innovation_number: int = innovation_number
        self.node_number: int = node_number
        self.connection_innovations: Dict[Gene, int] = {}
        self.node_innovations: Dict[Gene, int] = {}

    def get_innovation_number(self, gene: Gene):
        pass

    def get_node_number(self, gene: Gene):
        pass