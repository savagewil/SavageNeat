from __future__ import annotations

from Conditions import Conditions
from GenePool import GenePool
from Genome import Genome
from Population import Population
from Simulation import Simulation
from functions import surround_tag, remove_tag


class Generation:
    def __init__(self, generation: int, population: Population, gene_pool: GenePool):
        """
        The Generation class encapsulates a whole generation of the neat algorithm
        :param generation: The generation number
        :param population: The population of genomes
        :param gene_pool: The gene pool for the current generation, used when reproducing
        """
        self.generation = generation
        self.population = population
        self.gene_pool = gene_pool

    def next(self, conditions: Conditions) -> Generation:
        """
        Creates the next generation
        :return: The next generation
        """
        new_population = self.population.next(conditions, self.gene_pool)
        new_gene_pool = self.gene_pool.next()
        return Generation(self.generation + 1, new_population, new_gene_pool)

    def run(self, simulation: Simulation, conditions: Conditions, batched: bool = False, batch_size: int = None):
        """
        Runs a simulation on every member of the population
        :param batched: If false run sim separately on each genome, if true run them as groups
        :param batch_size: The size of the batches to run, if None, then the batch will be the size of all the genomes
        :param simulation: The simulation to run
        :param conditions: The conditions to use when running the simulation
        """
        self.population.run(simulation, conditions, batched, batch_size)

    def get_score(self) -> float:
        """
        Returns the highest score in the population
        :return: The highest score in the population
        """
        self.population.update_fitness()
        return self.population.max_fitness

    def get_best(self) -> Genome:
        """
        Returns the genome with the highest score in the population
        :return: The genome with the highest score in the population
        """
        genomes = self.population.get_genomes()
        return max(genomes)

    def __str__(self) -> str:
        save_string = ""
        save_string += surround_tag("generation_count", str(self.generation))
        save_string += surround_tag("population", str(self.population))
        save_string += surround_tag("gene_pool", str(self.gene_pool))
        return save_string

    @staticmethod
    def load(string) -> Generation:
        generation_count, string = remove_tag("generation_count", string)
        population_str, string = remove_tag("population", string)
        gene_pool_str, string = remove_tag("gene_pool", string)
        population = Population.load(population_str)
        gene_pool = GenePool.load(gene_pool_str)
        return Generation(int(generation_count), population, gene_pool)