from __future__ import annotations

from typing import List

from Conditions import Conditions
from Genome import Genome
from Simulation import Simulation
from Specie import Specie


class Population:
    def __init__(self, species: List[Specie]):
        """
        Population is a class which represents all of the genomes in the generation
        All of these genomes are collected into species
        :param species: The species in the population
        """
        self.species: List[Specie] = species

    def next(self, conditions: Conditions) -> Population:
        """
        Produces the population of the next generation
        Makes the species reproduce, then adds the new genomes are created to the species
        :param conditions: The conditions used to produce the next population
        :return: The new population for the next generation
        """
        pass

    def add_genome(self, genome: Genome, conditions: Conditions):
        """
        Adds a genome to the first matching species
        :param genome: The genome to add into the population
        :param conditions: The conditions to use when comparing the genome to the species
        """
        pass

    def add(self, species: Species):
        """
        Adds a new species to the population
        :param species: The species to add
        """
        pass

    def run(self, simulation: Simulation, batched: bool = False, batch_size: int = None):
        """
        Runs a simulation on every member of the population
        :param batched: If false run sim separately on each genome, if true run them as groups
        :param batch_size: The size of the batches to run, if None, then the batch will be the size of all the genomes
        :param simulation: The simulation to run
        """
        pass

    def next_stagnant(self, conditions: Conditions) -> Population:
        """
        Produces the next populations if the whole population is stagnant
        :param conditions: The conditions to use when reproducing
        :return: The next population
        """
        pass

    def add_all_genomes(self, genomes: [Genome], conditions: Conditions):
        """
        Adds all genomes from a list to the first appropriate species
        :param genomes: A list of genomes to add to the population
        :param conditions: The conditions to use when reproducing
        """
        pass

    def get_fertile_genomes(self) -> List[Genome]:
        """
        Gets all of the genomes which are in a fertile species
        :return: A list of at genomes in a fertile species
        """
        pass

    def get_genomes(self) -> List[Genome]:
        """
        Gets all of the genomes in the population
        :return: A list of all the genomes in the population
        """
        list_genomes = list(map(lambda species: species.genomes, self.species))
        genomes = [genome for genomes in list_genomes for genome in genomes]
        return genomes

    def clear_empty_species(self) -> List[Specie]:
        """
        Removes every empty species
        :return: A list of the removed species
        """
        pass
