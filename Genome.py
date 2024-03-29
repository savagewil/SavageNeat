from __future__ import annotations

import random
from typing import List, Tuple
from Gene import Gene
from NeatErrors import NetworkFullError
from Network import Network
from GenePool import GenePool
from Conditions import Conditions
from Simulation import Simulation
from functions import surround_tag, remove_tag

from processing_genes import process_genes


class Genome:
    def __init__(self, genes: List[Gene], input_size: int, output_size: int, gene_pool: GenePool):
        """
        The genome class is a collection of genes which represents a network
        :param genes: The genes of the genome
        :param input_size: The number of input nodes
        :param output_size: The number of output nodes
        """
        assert len(genes) > 0
        self.genes: List[Gene] = genes  # its is assumed that the genes will be in sorted order
        weight_matrix, enabled_matrix, middle_size, middles = process_genes(self.genes, input_size, output_size, gene_pool)
        # print("GENOME",weight_matrix.shape, enabled_matrix.shape)

        self.network: Network = Network(weight_matrix, enabled_matrix, input_size, output_size, middle_size)
        self.raw_fitness: float = 0
        self.input_size: int = input_size
        self.output_size: int = output_size
        self.start_nodes: List[int] = list(range(1, input_size + 1))
        self.middle_nodes: List[int] = middles
        self.end_nodes: List[int] = list(range(0, -output_size, -1))

    def add_node(self, gene_pool: GenePool, conditions: Conditions) -> Genome:
        """
        Creates a new genome. Splits a randomly selected connection into two connections which share a new node

        The connection which starts at the original connections in_node is the in connection
        The connection which ends at the original connections out_node is the out connection

        Of the new connections, the in connection will have a weight of one
        The out connection will have the original connections weight

        The original connection is disabled

        :param conditions: Added for the node count
        :param gene_pool: The GenePool which provides the innovation numbers for the new connections,
         and the node number for the new node
        :return: Returns a copy of the current genome, but with a connection split with a new node added
        """
        conditions.new_node_count += 1
        splitting_gene: Gene = random.choice(self.genes)
        new_node = gene_pool.get_node_number(splitting_gene)

        in_gene = Gene(1.0, splitting_gene.in_node, new_node, 0, gene_pool=gene_pool)
        out_gene = Gene(splitting_gene.weight, new_node, splitting_gene.out_node, 0, gene_pool=gene_pool)

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

        return Genome(new_genes,self.input_size,self.output_size, gene_pool)

    def add_connection(self, gene_pool: GenePool, conditions: Conditions) -> Genome:
        """
        Creates a new genome with a randomly generated connection
        :param gene_pool: The GenePool which provides the innovation number for the new connection
        :param conditions: The Conditions which control how the range for the weights of the new connection
        :return: Returns a copy of the current genome, but with a new connection
        """
        conditions.new_connection_count += 1
        endings = []
        starts = self.start_nodes + self.middle_nodes
        start_node = None
        while (not endings) and starts:
            start_node = random.choice(starts)
            starts.remove(start_node)

            endings = list(filter(lambda end_node: gene_pool.get_depth(end_node) > gene_pool.get_depth(start_node),
                                  self.middle_nodes + self.start_nodes))

            used_genes = (filter(lambda gene: gene.in_node == start_node, self.genes))
            for gene in used_genes:
                if gene.out_node in endings:
                    endings.remove(gene.out_node)
        if endings:
            end_node = random.choice(endings)
            new_gene = Gene(random.random() * (
                    conditions.gene_max_weight - conditions.gene_min_weight) + conditions.gene_min_weight,
                            start_node, end_node, 0, gene_pool=gene_pool)
            new_genes = list(map(Gene.copy, self.genes))
            new_genes.append(new_gene)
            return Genome(new_genes, self.input_size, self.output_size, gene_pool)
        else:
            conditions.new_connection_count -= 1
            # raise NetworkFullError("add connection")
            # print("""Network full""")
            return self

    def compare(self, other: Genome, conditions: Conditions) -> float:
        """
        Compares two genomes to find how similar they are
        :param other: The genome to compare the current genome to
        :param conditions: The Conditions to compare under, includes weight, disjoint and excess coefficients
        :return: A float measuring similarity of the genomes, 0.0 being the most similar
        """
        self_index = 0
        other_index = 0
        comparison = 0.0
        disjoint_coefficient = conditions.genome_disjoint_coefficient / (1 if conditions.genome_min_divide >= len(self.genes) else len(self.genes))
        excess_coefficient = conditions.genome_excess_coefficient / (1 if conditions.genome_min_divide >= len(self.genes) else len(self.genes))

        while len(self.genes) > self_index and len(other.genes) > other_index:
            if self.genes[self_index] == other.genes[other_index]:
                comparison += (abs(self.genes[self_index].innovation_number -
                                   other.genes[other_index].innovation_number) *
                               conditions.genome_weight_coefficient)
                self_index += 1
                other_index += 1
            elif self.genes[self_index] < other.genes[other_index]:
                comparison += disjoint_coefficient
                self_index += 1
            else:
                comparison += disjoint_coefficient
                other_index += 1
        comparison += (len(self.genes) - self_index + len(
            other.genes) - other_index) * excess_coefficient
        return comparison

    def breed(self, other: Genome, gene_pool: GenePool, conditions: Conditions) -> Genome:
        """
        Breeds two Genomes to create a third child genome
        :param other: A genome to breed with the current Genome
        :param gene_pool: The GenePool allows new mutations to be tracked allows retrieval of new innovation numbers
        :return: A new genome created by breeding the two given genomes
        :param conditions: The conditions the breeding is occuring in, controls the rate of being disabled
        """
        # print("BREEDING", self)
        self_index = 0
        other_index = 0
        new_genes = []
        while len(self.genes) > self_index and len(other.genes) > other_index:
            if self.genes[self_index] == other.genes[other_index]:
                new_gene = self.genes[self_index].copy()
                new_gene.weight = random.choice([self.genes[self_index].weight, other.genes[other_index].weight])
                new_gene.enabled = ((self.genes[self_index].enabled or other.genes[other_index].enabled) or
                                    random.random() > conditions.genome_disable_probability)
                new_genes.append(new_gene)
                # if not new_gene.enabled:
                #     print("DISABLED GENE both")
                #     print(new_gene)
                #     print(self.genes[self_index])
                #     print(other.genes[other_index])
                self_index += 1
                other_index += 1
            elif self.genes[self_index] < other.genes[other_index]:
                if self.raw_fitness >= other.raw_fitness:
                    new_gene = self.genes[self_index].copy()
                    new_gene.enabled = (self.genes[self_index].enabled or
                                        random.random() > conditions.genome_disable_probability)
                    new_genes.append(new_gene)
                    # if not new_gene.enabled:
                    #     print("DISABLED GENE self")
                    #     print(new_gene)
                    #     print(self.genes[self_index])
                self_index += 1
            else:
                if self.raw_fitness <= other.raw_fitness:
                    new_gene = other.genes[other_index].copy()
                    new_gene.enabled = (other.genes[other_index].enabled or
                                        random.random() > conditions.genome_disable_probability)
                    new_genes.append(new_gene)
                    # if not new_gene.enabled:
                    #     print("DISABLED GENE other")
                    #     print(new_gene)
                    #     print(other.genes[other_index])
                other_index += 1


        for i in range(len(new_genes)):
            new_genes[i] = new_genes[i].mutate(conditions)

        new_genome = Genome(new_genes, self.input_size, self.output_size,gene_pool)

        if random.random() < conditions.genome_connection_probability:
            new_genome = new_genome.add_connection(gene_pool, conditions)

        if random.random() < conditions.genome_node_probability:
            new_genome = new_genome.add_node(gene_pool, conditions)

        return new_genome

    def run(self, simulation: Simulation, batch_id=0):
        """
        Runs a simulation using the genome, then updates the score
        :param batch_id: The id while shows which agent it is in the batch
        :param simulation: The simulation to run
        """
        self.network.batch_id = batch_id
        self.raw_fitness = self.network.execute(simulation)

    def copy(self) -> Genome:
        """
        Makes a copy of the genome
        :return: a copy of the genome
        """
        return Genome(list(map(Gene.copy, self.genes)), self.input_size, self.output_size)

    def __eq__(self, other: Genome) -> bool:
        """
        Checks to see if the genomes have the same score
        :param other: Another object, should be a Genome
        :return: True if the other is a Genome with the same score, False otherwise
        """
        if isinstance(other, Genome):
            return self.raw_fitness == other.raw_fitness
        else:
            return False

    def __lt__(self, other: Genome) -> bool:
        """
        Checks to see if the score of the current genome is less than the score of the other
        :param other: An object which should represent a Genome
        :return: True if the score of the genome is less than the score of the other, False otherwise
        """
        if isinstance(other, Genome):
            return self.raw_fitness < other.raw_fitness
        else:
            raise TypeError("Less than is not supported between %s and %s" % (str(type(self)), str(type(other))))

    def __le__(self, other: Genome) -> bool:
        """
        Checks to see if the score of the current genome is less than or equal the score of the other
        :param other: An object which should represent a Genome
        :return: True if the score of the genome is less than or equal to the score of the other, False otherwise
        """
        if isinstance(other, Genome):
            return self.raw_fitness <= other.raw_fitness
        else:
            raise TypeError(
                "Less than or equal is not supported between %s and %s" % (str(type(self)), str(type(other))))

    def __gt__(self, other: Genome) -> bool:
        """
        Checks to see if the score of the current genome is greater than the score of the other
        :param other: An object which should represent a Genome
        :return: True if the score of the genome is greater than the score of the other, False otherwise
        """
        if isinstance(other, Genome):
            return self.raw_fitness > other.raw_fitness
        else:
            raise TypeError("Greater than is not supported between %s and %s" % (str(type(self)), str(type(other))))

    def __ge__(self, other: Genome) -> bool:
        """
        Checks to see if the score of the current genome is greater than or equal to the score of the other
        :param other: An object which should represent a Genome
        :return: True if the score of the genome is greater than or equal to the score of the other, False otherwise
        """
        if isinstance(other, Genome):
            return self.raw_fitness >= other.raw_fitness
        else:
            raise TypeError(
                "Greater than or equal is not supported between %s and %s" % (str(type(self)), str(type(other))))

    def set_fitness(self, raw_fitness: float):
        """
        Sets the score of the genome
        :param raw_fitness: The new genome score
        """
        self.raw_fitness = raw_fitness

    def __str__(self) -> str:

        save_string = ""
        save_string += surround_tag("input_size", str(self.input_size))
        save_string += surround_tag("output_size", str(self.output_size))
        save_string += surround_tag("raw_fitness", str(self.raw_fitness))
        genes_string = ""
        for gene in self.genes:
            genes_string += surround_tag("gene", str(gene))
        save_string += surround_tag("genes", genes_string)
        return save_string

    @staticmethod
    def load(string) -> Genome:
        input_size_str, string = remove_tag("input_size", string)
        output_size_str, string = remove_tag("output_size", string)
        raw_fitness_str, string = remove_tag("raw_fitness", string)
        genes_str, string = remove_tag("genes", string)

        input_size = int(input_size_str)
        output_size = int(output_size_str)
        raw_fitness = float(raw_fitness_str)
        genes = []
        while genes_str:
            gene_str, genes_str = remove_tag("gene", genes_str)
            gene = Gene.load(gene_str)
            genes.append(gene)
        genome = Genome(genes, input_size, output_size)
        genome.raw_fitness = raw_fitness
        return genome