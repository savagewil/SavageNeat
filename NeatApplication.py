from __future__ import annotations

from typing import List

from Conditions import Conditions
from GenePool import GenePool
from Generation import Generation
from Genome import Genome
from Population import Population
from Simulation import Simulation


class NeatApplication:
    def __init__(self, conditions: Conditions, simualtion: Simulation, load_file=None):
        self.simualtion = simualtion
        self.conditions = conditions
        self.past: List[Generation] = []
        if load_file is None:
            gene_pool = GenePool(0, 0, {})
            genomes = self.start_genes(gene_pool)
            population = Population([])
            population.add_all_genomes(genomes)
            self.current_generation = Generation(0, population, gene_pool)

    def start_genes(self, gene_pool: GenePool) -> List[Genome]:
        pass
