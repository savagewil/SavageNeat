from __future__ import annotations

import random
from typing import List, Tuple
from Gene import Gene
from NeatErrors import NetworkFullError
from Network import Network
from GenePool import GenePool
from Conditions import Conditions
import numpy as np


def process_genes(genes: List[Gene], input_size: int, output_size: int, gene_pool: GenePool) \
        -> Tuple[np.array, np.array, int, List[int]]:
    """

    :param genes:
    :param input_size:
    :param output_size:
    :param gene_pool:
    :return:
    """
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
    nodes_with_depth = list(map(lambda node: (gene_pool.get_depth(node), node), nodes))
    nodes.sort()
    nodes_with_depth.sort()
    node_indices = {}
    for i in range(len(nodes_with_depth)):
        node_indices[nodes_with_depth[i][1]] = i

    middle_size = len(middles)
    enabled_matrix = np.zeros((input_size + middle_size, middle_size + output_size), dtype=bool)
    weight_matrix = np.zeros((input_size + middle_size, middle_size + output_size))

    for gene in genes:
        if gene.enabled:
            start = node_indices[gene.in_node]
            end = node_indices[gene.out_node] - input_size
            enabled_matrix[start][end] = True
            weight_matrix[start][end] = gene.weight
    return weight_matrix, enabled_matrix, middle_size, list(middles)


class Genome:
    def __init__(self, genes: List[Gene], input_size: int, output_size: int):
        """

        :param genes:
        :param input_size:
        :param output_size:
        """
        self.genes: List[Gene] = genes  # its is assumed that the genes will be in sorted order
        weight_matrix, enabled_matrix, middle_size, middles = process_genes(self.genes, input_size, output_size)

        self.network: Network = Network(weight_matrix, enabled_matrix, input_size, output_size, middle_size)
        self.raw_fitness: float = 0
        self.start_nodes: List[int] = list(range(input_size))
        self.middle_nodes: List[int] = middles
        self.end_nodes: List[int] = list(range(-output_size, 0))

    def add_node(self, gene_pool: GenePool) -> Genome:
        """

        :param gene_pool:
        :return:
        """
        splitting_gene: Gene = random.choice(self.genes)
        new_node = gene_pool.get_node_number(splitting_gene)

        in_gene = Gene(splitting_gene.weight, splitting_gene.in_node, new_node, 0, gene_pool=gene_pool)
        out_gene = Gene(1.0, new_node, splitting_gene.out_node, 0, gene_pool=gene_pool)

        new_genes = []

        for gene in self.genes:
            if gene == splitting_gene:
                disabled_gene = gene.copy()
                disabled_gene.enabled = False
                new_genes.append(disabled_gene)
            else:
                new_genes.append(gene.copy())

        new_genes.append(in_gene)
        new_genes.append(out_gene)

        return Genome(new_genes)

    def add_connection(self, gene_pool: GenePool, conditions: Conditions) -> Genome:
        """

        :param gene_pool:
        :param conditions:
        :return:
        """
        endings = []
        starts = self.start_nodes + self.middle_nodes
        start_node = None
        while (not endings) and starts:
            start_node = random.choice(self.start_nodes + self.middle_nodes)
            starts.remove(start_node)

            endings = list(filter(lambda end_node: gene_pool.get_depth(end_node) > gene_pool.get_depth(start_node),
                                  self.middle_nodes + self.start_nodes))

            used_genes = (filter(lambda gene: gene.in_node == start_node, self.genes))
            for gene in used_genes:
                if gene.out_node in endings:
                    endings.remove(gene.out_node)
        if endings:
            end_node = random.choice(endings)
            new_gene = Gene(random.random() * (conditions.max_weight - conditions.min_weight) + conditions.min_weight,
                            start_node, end_node, 0, gene_pool=gene_pool)
            new_genes = list(map(Gene.copy, self.genes))
            new_genes.append(new_gene)
            return Genome(new_genes)
        else:
            raise NetworkFullError("add connection")

    def compare(self, other: Genome, conditions: Conditions) -> float:
        """

        :param other:
        :param conditions:
        :return:
        """
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
        """

        :param other:
        :return:
        """
        pass

    def copy(self):
        """

        :return:
        """
        return Genome(list(map(Gene.copy, self.genes)))