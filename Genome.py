from __future__ import annotations

from typing import List, Tuple
from Gene import Gene
from Network import Network
from GenePool import GenePool
from Conditions import Conditions
import numpy as np


def make_adjacencys(genes: List[Gene], input_size: int, output_size: int) -> Tuple[np.array, np.array]:
    return np.array([]), np.array([])


def get_middle_size(genes: List[Gene], input_size: int, output_size: int) -> int:
    return 0


class Genome:
    def __init__(self, genes: List[Gene], input_size: int, output_size: int):
        self.genes: List[Gene] = genes  # its is assumed that the genes will be in sorted order
        weight_matrix, enabled_matrix = make_adjacencys(self.genes, input_size, output_size)
        middle_size = get_middle_size(self.genes)
        self.network: Network = Network(weight_matrix, enabled_matrix, input_size, output_size, middle_size)
        self.raw_fitness = 0

    def add_node(self, gene_pool: GenePool) -> Genome:
        pass

    def add_connection(self, gene_pool: GenePool) -> Genome:
        pass

    def compare(self, other: Genome, conditions: Conditions) -> float:
        self_index = 0
        other_index = 0
        comparison = 0.0

        while len(self.genes) > self_index and len(other.genes) > other_index:
            if self.genes[self_index] == other.genes[other_index]:
                comparison += (abs(self.genes[self_index].innovation_number -
                                   other.genes[other_index].innovation_number) *
                               conditions.weight_coefficient)
                self_index += 1
                other_index += 1
            elif self.genes[self_index] < other.genes[other_index]:
                comparison += conditions.disjoint_coefficient
                self_index += 1
            else:
                comparison += conditions.disjoint_coefficient
                other_index += 1
        comparison += (len(self.genes) - self_index + len(other.genes) - other_index) * conditions.excess_coefficient
        return comparison

    def breed(self, other: Genome) -> Genome:
        pass
