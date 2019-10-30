from __future__ import annotations

import random
from typing import List

from Conditions import Conditions
from Gene import Gene
from GenePool import GenePool
from Generation import Generation
from Genome import Genome
from Population import Population
from Simulation import Simulation


class NeatApplication:
    def __init__(self, conditions: Conditions, simulation: Simulation, load_file=None):
        """
        The Neat Application runs the Neat algorithm on a simulation, using the given conditions
        :param conditions: The conditions to use when running the algorithm
        :param simulation: The simulation Neat will be running
        :param load_file: A file to load previous data from
        """
        self.simulation = simulation
        self.conditions = conditions
        self.past: List[Generation] = []
        if load_file is None:
            gene_pool = GenePool(0, simulation.get_data_size() + 1, {})
            genomes = self.start_genomes(gene_pool)
            population = Population([])
            population.add_all_genomes(genomes, conditions)
            self.current_generation = Generation(0, population, gene_pool.next())
        else:
            raise NotImplementedError("Saving is coming soon")

    def start_genomes(self, gene_pool: GenePool) -> List[Genome]:
        """
        Creates the starter genomes
        :param gene_pool: The gene pool to update with the starter genomes
        :return: A list of starter genomes
        """
        in_size = self.simulation.get_data_size()
        out_size = self.simulation.get_controls_size()

        starter_genomes = []

        starter_genes = []
        for in_ in range(1, in_size + 1):
            for out_ in range(0, -out_size, -1):
                gene = Gene(random.random() * (self.conditions.gene_max_weight - self.conditions.gene_min_weight) +
                            self.conditions.gene_min_weight, in_, out_, 0, gene_pool=gene_pool)
                starter_genes.append(gene)

        for i in range(self.conditions.population_size):
            new_genes = [gene.copy() for gene in starter_genes]
            for gene in new_genes:
                gene.weight = (random.random() * (self.conditions.gene_max_weight - self.conditions.gene_min_weight) +
                               self.conditions.gene_min_weight)
            starter_genomes.append(Genome(new_genes, in_size, out_size))

        return starter_genomes

    def run(self, batched=False, batch_size=None, verbosity=0):
        self.current_generation.run(self.simulation, self.conditions, batched, batch_size)
        if verbosity > 0:
            print(self.current_generation.get_score())
        next_gen = self.current_generation.next(self.conditions)
        self.past.insert(0, next_gen)
        self.current_generation = next_gen

    def save(self, file_path):
        pass

    def load(self, file_path):
        pass

    def main(self, time=None, batched=False, batch_size=None, verbosity=0):
        while time is None or time > 0:
            if time is not None:
                time -= 1
            self.run(verbosity=verbosity)