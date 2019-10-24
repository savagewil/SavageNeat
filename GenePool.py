from __future__ import annotations
from typing import Dict

from Gene import Gene, StructureGene


class GenePool:
    def __init__(self, innovation_number: int, node_number: int, node_depths: Dict[int: int]):
        """
        The GenePool class keeps track of the next available innovation number, and node number
        It also tracks the new connection innovations and new nodes in the current generation
        :param innovation_number: The next available innovation number
        :param node_number: The next available node number
        :param node_depths: A dictionary for keeping track of the relative depth of nodes
        """
        self.innovation_number: int = innovation_number
        self.node_number: int = node_number
        self.connection_innovations: Dict[StructureGene, int] = {}
        self.node_innovations: Dict[Gene, int] = {}
        self.node_depths: Dict[int: int] = node_depths

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
            in_node_depth = self.node_depths[gene.in_node]
            out_node_depth = self.node_depths[gene.out_node]
            new_depth = (in_node_depth + out_node_depth) // 2
            self.node_depths[self.node_number - 1] = new_depth
            return self.node_number - 1

    def get_depth(self, node: int) -> int:
        """
        Gets the depth of the node in the network
        :param node: The node to get the depth of
        :return: The depth of the node
        """
        return self.node_depths[node]

    def next(self) -> GenePool:
        """
        Creates the GenePool for the next Generation
        Keeps the innovation number and node number, as well as the depths for the nodes
        Clears the innovation dictionaries
        :return: The next GenePool
        """
        return GenePool(self.innovation_number, self.node_number, self.node_depths.copy())
