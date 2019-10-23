from __future__ import annotations

import random
from typing import List, Tuple
from Gene import Gene
from Network import Network
from GenePool import GenePool
from Conditions import Conditions
import numpy as np


def genes_to_matrices_and_dim(genes: List[Gene], input_size: int, output_size: int) -> Tuple[np.array, np.array, int]:
    nodes = set()
    middles = set()
    for connection_gene in genes:
        nodes.add(connection_gene.in_node)
        nodes.add(connection_gene.out_node)

        if connection_gene.in_node >= input_size:
            middles.add(connection_gene[1])

        if connection_gene.out_node > 0:
            middles.add(connection_gene[2])

    list(map(nodes.add, range(input_size)))
    list(map(nodes.add, range(-output_size, 0)))
    nodes = list(nodes)
    nodes.sort()

    middle_size = len(middles)
    enabled_matrix = np.zeros((input_size + middle_size, middle_size + output_size), dtype=bool)
    weight_matrix = np.zeros((input_size + middle_size, middle_size + output_size))

    for gene in genes:
        if gene.enabled:
            start = nodes.index(gene.in_node) - output_size
            end = gene.out_node if gene.out_node < 0 else nodes.index(gene.out_node) - (input_size + output_size)
            enabled_matrix[start][end] = True
            weight_matrix[start][end] = gene.weight
    return weight_matrix, enabled_matrix, middle_size


class Genome:
    def __init__(self, genes: List[Gene], input_size: int, output_size: int):
        self.genes: List[Gene] = genes  # its is assumed that the genes will be in sorted order
        weight_matrix, enabled_matrix, middle_size = genes_to_matrices_and_dim(self.genes, input_size, output_size)

        self.network: Network = Network(weight_matrix, enabled_matrix, input_size, output_size, middle_size)
        self.raw_fitness = 0

    def add_node(self, gene_pool: GenePool) -> Genome:
        spliting_gene = random.choice(self.genes)
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
