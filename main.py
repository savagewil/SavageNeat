from NeatApplication import NeatApplication
from Conditions import Conditions
if __name__ == '__main__':
    conditions = Conditions(
        gene_weight_probability=,
        gene_random_probability=,
        genome_disable_probability=,
        genome_node_probability=,
        genome_connection_probability=,
        species_asexual_probability=,
        species_interspecies_reproduction_probability=,
        gene_max_weight=,
        gene_min_weight=,
        gene_weight_shift=,
        genome_weight_coefficient=,
        genome_disjoint_coefficient=,
        genome_excess_coefficient=,
        species_age_fertility_limit=,
        species_threshold=,
        species_keep_champion=,
        species_niche_divide_min=,
        population_age_limit=,
        population_size=,
        app_start_node_depth=,
        app_end_node_depth=)

    app = NeatApplication(conditions,)