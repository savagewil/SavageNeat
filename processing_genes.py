from typing import Tuple, List

import numpy as np

from Gene import Gene
from GenePool import GenePool


def process_genes(genes: List[Gene], input_size: int, output_size: int, gene_pool: GenePool) \
        -> Tuple[np.array, np.array, int, List[int]]:
    """
    Processes Genes to produce a weight Adjacency matrix and an Enabled matrix,
    as well as the nodes that are not input or output nodes
    :param genes: The Genes to convert
    :param input_size: The number of input nodes
    :param output_size: The number of output nodes
    :param gene_pool: The GenePool which has data on the depth of nodes, which creates the ordering
    :return: A Tuple containing, Weight Adjacency Matrix, Enabled Adjacency Matrix, Number of middle nodes,
        and the list of middle nodes
    """
    # print("PROCESSING In:", '\n\t'.join([str(gene) for gene in genes]))
    # print("PROCESSING In:", input_size, output_size)
    nodes = set()
    middles = set()
    for connection_gene in genes:
        nodes.add(connection_gene.in_node)
        nodes.add(connection_gene.out_node)

        if connection_gene.in_node > input_size:
            middles.add(connection_gene.in_node)

        if connection_gene.out_node > 0:
            middles.add(connection_gene.out_node)

    list(map(nodes.add, range(1, input_size + 1)))
    list(map(nodes.add, range(0, -output_size, -1)))
    # print("PROCESSING In:",
    #       list(map(nodes.add, range(1, input_size + 1))),
    #       list(map(nodes.add, range(0, -output_size, -1))))

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
    # print("PROCESSING OUT:", weight_matrix.shape, enabled_matrix.shape, middle_size, list(middles), middles)
    return weight_matrix, enabled_matrix, middle_size, list(middles)
