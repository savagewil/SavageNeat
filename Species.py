from __future__ import annotations

import random
from typing import List

from Conditions import Conditions
from Genome import Genome


class Species:
    def __init__(self, representative: Genome, genomes: List[Genome] = [], age: int = 0, max_fitness: float = None):
        self.representative = representative
        self.genomes = genomes
        self.age = age
        self.max_fitness = max_fitness
        self.niche_fitness = 0

    def fertile(self, conditions: Conditions) -> bool:
        return self.age < conditions.species_age_fertility_limit

    def compare(self, genome: Genome, conditions: Conditions) -> float:
        return self.representative.compare(genome, conditions)

    def add(self, genome: Genome, conditions: Conditions) -> bool:
        if self.compare(genome, conditions) < conditions.species_threshold:
            self.genomes.append(genome)
        return False

    def next(self) -> Species:
        new_representative = random.choice(self.genomes)
        new_age = self.age + 1
        return Species(new_representative, [], new_age, self.max_fitness)

    def reproduce(self, count: int, genomes: List[Genome], conditions: Conditions) -> List[Genome]:
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
        self.genomes.sort(reverse=True)
        self.genomes = self.genomes[:count]
