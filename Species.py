from __future__ import annotations

import random
from typing import List

from Conditions import Conditions
from Genome import Genome


class Species:
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

    def next(self) -> Species:
        """
        Gets the species for the next generation
        :return: The same species, with no genes, a representative from the current generation and the age increased
        """
        new_representative = random.choice(self.genomes)
        new_age = self.age + 1
        return Species(new_representative, [], new_age, self.max_fitness)

    def reproduce(self, count: int, genomes: List[Genome], conditions: Conditions) -> List[Genome]:
        """
        Creates a new list of genomes
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

        for i in range(count - (1 if conditions.keep_champion else 0)):
            if random.random() < conditions.asexual_probability:
                selected_genome = species_genomes[i % len(species_genomes)]
                new_genome = selected_genome.breed(selected_genome)
            elif random.random() < conditions.interspecies_reproduction_probability:
                mother_genome = species_genomes[i % len(species_genomes)]
                father_genome = random.choice(genomes)
                new_genome = mother_genome.breed(father_genome)
            else:
                mother_genome = species_genomes[i % len(species_genomes)]
                father_genome = random.choice(species_genomes)
                new_genome = mother_genome.breed(father_genome)
            new_genomes.append(new_genome)
        if conditions.keep_champion:
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
