from NeatApplication import NeatApplication
from Conditions import Conditions
from Simulations.EqualSimulation import EqualSimulation
from Simulations.XorSimulation import XorSimulation

if __name__ == '__main__':
    Population = 150
    conditions = Conditions(
        gene_weight_probability=0.8,
        gene_random_probability=0.1,
        genome_disable_probability=0.75,
        genome_node_probability=0.03,
        genome_connection_probability=0.05,
        species_asexual_probability=0.25,
        species_interspecies_reproduction_probability=0.001,
        gene_max_weight=1.0,
        gene_min_weight=-1.0,
        gene_weight_shift=.01,
        genome_weight_coefficient=0.4,
        genome_disjoint_coefficient=1.0,
        genome_excess_coefficient=1.0,
        genome_min_divide=20,
        species_age_fertility_limit=15,
        species_threshold=3.0,
        species_keep_champion=True,
        species_champion_limit=5,
        species_niche_divide_min=0,
        population_age_limit=20,
        population_size=Population,
        app_start_node_depth=0,
        app_end_node_depth=100)

    sim = XorSimulation(batch_size=Population)
    app = NeatApplication(conditions, sim)

    app.main(time=100, batched=True, batch_size=Population, verbosity=1)
