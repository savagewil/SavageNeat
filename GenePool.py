from typing import Dict
from Gene import Gene, StructureGene
f

class ConnectionInnovationDict(dict):


class GenePool:
    def __init__(self, innovation_number: int, node_number: int):
        """

        :param innovation_number:
        :param node_number:
        """
        self.innovation_number: int = innovation_number
        self.node_number: int = node_number
        self.connection_innovations: Dict[StructureGene, int] = {}
        self.node_innovations: Dict[Gene, int] = {}

    def get_innovation_number(self, gene: StructureGene):
        """
        Gets the innovation number associated with a Structure Gene
        if the innovation is already discovered in the current generation
        the same number is used
        :param gene: A structure gene which needs the innovation number
        :return: An innovation number connected to the structure gene
        """
        if gene in self.connection_innovations:
            return self.connection_innovations[gene]
        else:
            self.connection_innovations[gene] = self.innovation_number
            self.innovation_number += 1
            return self.innovation_number - 1


    def get_node_number(self, gene: Gene):
        """
        Gets the node number associated with a Gene
        if the innovation is already discovered in the current generation
        the same number is used
        :param gene: A gene which is splitting to create the node
        :return: A node number created by splitting the gene
        """
        if gene in self.node_innovations:
            return self.node_innovations[gene]
        else:
            self.node_innovations[gene] = self.node_number
            self.node_number += 1
            return self.node_number - 1