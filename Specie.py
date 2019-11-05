from __future__ import annotations

import random
from typing import List

from Conditions import Conditions
from GenePool import GenePool
from Genome import Genome
from Simulation import Simulation
from functions import surround_tag, remove_tag


class Specie:
    def __init__(self, representative: Genome, genomes: List[Genome] = None, age: int = 0, max_fitness: float = None):
        """
        The Species class represents a collection of Genomes which are all genetically similar to each other
        :param representative: A genome that represents the whole species
        :param genomes: The genomes that make up the species
        :param age: The age of the species since the fitness improved
        :param max_fitness: The maximum fitness the species has achieved
        """
        self.representative = representative
        self.genomes = genomes if genomes else []
        self.age = age
        self.max_fitness = max_fitness
        self.niche_fitness = 0

    def fertile(self, conditions: Conditions) -> bool:
        """
        Function for figuring out if a species can still reproduce
        :param conditions: The conditions to use to check
        :return: True if the species is young enough to reproduce
        """
        return self.age < conditions.species_age_fertility_limit

    def compare(self, genome: Genome, conditions: Conditions) -> float:
        """
        Compares a genome to the representative genome for the species
        :param genome: The Genome to compare to the species
        :param conditions: The conditions to use to compare
        :return: A value representing how similar the genome is to the species
        """
        return self.representative.compare(genome, conditions)

    def add(self, genome: Genome, conditions: Conditions) -> bool:
        """
        Adds a genome to the species if it is within the species threshold
        :param genome: The genome to add
        :param conditions: The conditions to use to add the species to the genome, has the species threshold
        :return: True is the genome gets added False otherwise
        """
        if self.compare(genome, conditions) < conditions.species_threshold:
            self.genomes.append(genome)
            return True
        return False

    def next(self) -> Specie:
        """
        Gets the species for the next generation
        :return: The same species, with no genes, a representative from the current generation and the age increased
        """
        new_representative = random.choice(self.genomes)
        new_age = self.age + 1
        return Specie(new_representative, [], new_age, self.max_fitness)

    def reproduce(self, count: int, genomes: List[Genome], conditions: Conditions, gene_pool: GenePool) -> List[Genome]:
        """
        Creates a new list of genomes
        :param gene_pool: The gene pool used when breeding new genomes
        :param count: The number of genomes to produce
        :param genomes: The genomes from the population
        :param conditions: The conditions to use to reproduce
        :return: a list of new genomes
        """
        if len(self.genomes) > count:
            self.genomes.sort()
            species_genomes = self.genomes[:count]
        else:
            species_genomes = self.genomes

        new_genomes = []

        for i in range(count - (1 if conditions.species_keep_champion and
                                     conditions.species_champion_limit < len(self.genomes) else 0)):
            if random.random() < conditions.species_asexual_probability:
                selected_genome = species_genomes[i % len(species_genomes)]
                new_genome = selected_genome.breed(selected_genome, gene_pool, conditions)
            elif random.random() < conditions.species_interspecies_reproduction_probability:
                mother_genome = species_genomes[i % len(species_genomes)]
                father_genome = random.choice(genomes)
                new_genome = mother_genome.breed(father_genome, gene_pool, conditions)
            else:
                mother_genome = species_genomes[i % len(species_genomes)]
                father_genome = random.choice(species_genomes)
                new_genome = mother_genome.breed(father_genome, gene_pool, conditions)
            new_genomes.append(new_genome)
        if conditions.species_keep_champion and conditions.species_champion_limit < len(self.genomes):
            new_genomes.append(species_genomes[0])

        return new_genomes

    def trim(self, count: int):
        """
        Trims the genome to a certain size
        :param count: The number of genomes to reduce the size to
        """
        self.genomes.sort(reverse=True)
        self.genomes = self.genomes[:min(len(self.genomes), count)]

    def get_genomes(self, count: int):
        """
        Returns a list of genomes of the size of the genome or smaller
        :param count: The number of genomes to return
        """
        self.genomes.sort(reverse=True)
        return self.genomes[:min(len(self.genomes), count)]

    def run(self, simulation: Simulation, conditions: Conditions, first_batch_id=0):
        """
        Runs a simulation on every genome in the species
        :param first_batch_id: The first batch id in the species
        :param simulation: The simulation to run
        :param conditions: The conditions to use when updating the fitness of the species
        :return:
        """
        for i in range(len(self.genomes)):
            self.genomes[i].run(simulation, batch_id=i + first_batch_id)
        self.update_fitness(conditions)

    def update_fitness(self, conditions: Conditions):
        """
        Updates the max fitness and niche fitness of the species
        :param conditions: The conditions to use to to get the niche fitness, uses niche_divide_min
        """
        niche_sum = 0
        max_fitness = 0
        for genome in self.genomes:
            niche_sum += genome.raw_fitness
            max_fitness = max(max_fitness, genome.raw_fitness)
        if max_fitness > self.max_fitness:
            self.max_fitness = max_fitness
            self.age = 0
        if conditions.species_niche_divide_min < len(self.genomes):
            self.niche_fitness = niche_sum / len(self.genomes)
        else:
            self.niche_fitness = niche_sum

    def __str__(self) -> str:

        self.representative = representative
        self.genomes = genomes if genomes else []
        self.age = age
        self.max_fitness = max_fitness
        self.niche_fitness = 0

        save_string = ""
        save_string += surround_tag("representative", str(self.representative))
        save_string += surround_tag("age", str(self.age))
        save_string += surround_tag("niche_fitness", str(self.niche_fitness))
        save_string += surround_tag("max_fitness", str(self.max_fitness))
        genomes_string = ""
        for genome in self.genomes:
            genomes_string += surround_tag("genome", str(genome))
        save_string += surround_tag("genomes", genomes_string)
        return save_string

    @staticmethod
    def load(string) -> Specie:
        representative_str, string = remove_tag("representative", string)
        age_str, string = remove_tag("age", string)
        niche_fitness_str, string = remove_tag("niche_fitness", string)
        max_fitness_str, string = remove_tag("max_fitness", string)
        genomes_str, string = remove_tag("genomes", string)

        representative = Genome.load(representative_str)
        age = int(age_str)
        niche_fitness = float(niche_fitness_str)
        max_fitness = float(max_fitness_str)

        genomes = []
        while genomes_str:
            genome_str, genomes_str = remove_tag("genome", genomes_str)
            genome = Genome.load(genome_str)
            genomes.append(genome)
        specie = Specie(representative, genomes, age, max_fitness)
        specie.niche_fitness = niche_fitness

        return specie
