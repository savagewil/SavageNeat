from NeatApplication import NeatApplication
from Conditions import Conditions
from Simulations.AddSimulation import AddSimulation
from Simulations.AndSimulation import AndSimulation
from Simulations.EqualSimulation import EqualSimulation
from Simulations.MultiplySimulation import MultiplySimulation
from Simulations.OrSimulation import OrSimulation
from Simulations.XorSimulation import XorSimulation
import pygame

# SCREEN_SHAPE = (1600, 800)

SCREEN_SHAPE = None
if __name__ == '__main__':
    screen = None
    shape = None
    if SCREEN_SHAPE:
        pygame.init()
        pygame.key.set_repeat(50, 10)
        screen = pygame.display.set_mode(SCREEN_SHAPE)

        shape = (0, 0, SCREEN_SHAPE[0], SCREEN_SHAPE[1])

    Population = 400
    conditions = Conditions(
        gene_weight_probability=0.8,
        gene_random_probability=0.1,
        genome_disable_probability=0.75,
        genome_node_probability=0.03,
        genome_connection_probability=0.05,
        species_asexual_probability=0.25,
        species_interspecies_reproduction_probability=0.001,
        species_keep_ratio=.5,
        gene_max_weight=2.0,
        gene_min_weight=-2.0,
        gene_weight_shift=.001,
        genome_weight_coefficient=0.4,
        genome_disjoint_coefficient=1.0,
        genome_excess_coefficient=1.0,
        genome_min_divide=20,
        species_age_fertility_limit=1000,
        species_threshold=3.0,
        species_keep_champion=True,
        species_champion_limit=5,
        species_niche_divide_min=0,
        population_age_limit=1000,
        population_size=Population,
        app_start_node_depth=0,
        app_end_node_depth=100)

    sim = XorSimulation(batch_size=Population, screen=screen, shape=shape, verbosity=0)
    app = NeatApplication(conditions, sim, screen=screen)
    app.main(time=500, batched=True, batch_size=Population, verbosity=1, shape=shape)
