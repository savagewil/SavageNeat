from __future__ import annotations

from typing import List

from Conditions import Conditions
from Genome import Genome
from Simulation import Simulation, SimulationState
from Specie import Specie


class Population:
    def __init__(self, species: List[Specie], age: int = 0, max_fitness: float = None):
        """
        Population is a class which represents all of the genomes in the generation
        All of these genomes are collected into species
        :param species: The species in the population
        """
        self.species: List[Specie] = species
        self.age: int = age
        self.max_fitness: float = max_fitness

    def next(self, conditions: Conditions) -> Population:
        """
        Produces the population of the next generation
        Makes the species reproduce, then adds the new genomes are created to the species
        :param conditions: The conditions used to produce the next population
        :return: The new population for the next generation
        """
        if self.age > conditions.population_age_limit:
            return self.next_stagnant(conditions)
        else:
            new_species = []
            genomes = self.get_genomes()
            fit_species = list(filter(lambda specie: species.fertile(conditions), self.species))
            total_fitness = sum(list(map(lambda specie:specie.niche_fitness, fit_species)))
            for species in fit_species:


            new_population = Population([], self.age + 1, self.max_fitness)
            return new_population

    def add_genome(self, genome: Genome, conditions: Conditions):
        """
        Adds a genome to the first matching species
        :param genome: The genome to add into the population
        :param conditions: The conditions to use when comparing the genome to the species
        """
        added = True
        for specie in self.species:
            if specie.add(genome, conditions):
                added = True
                break
        if not added:
            specie = Specie(genome, [genome])
            self.add(specie)

    def add(self, species: Specie):
        """
        Adds a new species to the population
        :param species: The species to add
        """
        self.species.append(species)

    def run(self, simulation: Simulation, conditions:Conditions, batched: bool = False, batch_size: int = None):
        """
        Runs a simulation on every member of the population
        :param batched: If false run sim separately on each genome, if true run them as groups
        :param batch_size: The size of the batches to run, if None, then the batch will be the size of all the genomes
        :param simulation: The simulation to run
        """
        if batched:
            genomes = self.get_genomes()
            batches = []
            if batch_size:
                assert batch_size == simulation.batch_size
                for batch_start in range(0, len(genomes), batch_size):
                    batches.append(genomes[batch_start:min(batch_start + batch_size, len(genomes) + 1)])
            else:
                assert len(genomes) == simulation.batch_size
                batches.append(genomes)

            for batch in batches:
                while any([state != SimulationState.FINISHED for state in simulation.get_state_batch()]):
                    data = simulation.get_data_batch()
                    controls = []
                    for i in range(simulation.batch_size):
                        if i < len(batch):
                            control = batch[i].network.run(data[i])
                            assert len(control) == simulation.get_controls_size()
                            controls.append(control)
                        else:
                            controls.append([0.0]*simulation.get_controls_size())

                    simulation.apply_controls_batch(controls)
                scores = simulation.get_score_batch()
                for i in range(len(batch)):
                    batch[i].set_fitness(scores[i])

            for specie in self.species:
                specie.update_fitness(conditions)

        else:
            for specie in self.species:
                specie.run(simulation, conditions)


    def next_stagnant(self, conditions: Conditions) -> Population:
        """
        Produces the next populations if the whole population is stagnant
        :param conditions: The conditions to use when reproducing
        :return: The next population
        """
        pass

    def add_all_genomes(self, genomes: List[Genome], conditions: Conditions):
        """
        Adds all genomes from a list to the first appropriate species
        :param genomes: A list of genomes to add to the population
        :param conditions: The conditions to use when reproducing
        """
        for genome in genomes:
            self.add_genome(genome, conditions)

    def get_fertile_genomes(self, conditions: Conditions) -> List[Genome]:
        """
        Gets all of the genomes which are in a fertile species
        :return: A list of at genomes in a fertile species
        """
        fertile_species = list(filter(lambda specie: specie.fertile(conditions), self.species))
        list_genomes = list(map(lambda species: species.genomes, fertile_species))
        genomes = [genome for genomes in list_genomes for genome in genomes]
        return genomes

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
        empty_species = list(filter(lambda specie: specie.genomes is [], self.species))
        for specie in empty_species:
            self.species.remove(specie)
        return empty_species

    def update_fitness(self):
        """
        Updates the max fitness of the population
        """
        max_fitness = max(list(map(lambda specie: specie.max_fitness, self.species)))

        if max_fitness > self.max_fitness:
            self.max_fitness = max_fitness
            self.age = 0
