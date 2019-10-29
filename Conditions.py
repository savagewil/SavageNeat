class Conditions:
    def __init__(self, gene_weight_probability: float, gene_random_probability: float,
                 genome_disable_probability: float, genome_node_probability: float, genome_connection_probability: float,
                 species_asexual_probability: float, species_interspecies_reproduction_probability: float,

                 gene_max_weight: float, gene_min_weight: float, gene_weight_shift: float,

                 genome_weight_coefficient: float, genome_disjoint_coefficient: float, genome_excess_coefficient: float,

                 species_age_fertility_limit: int, species_threshold: float, species_keep_champion: bool, species_niche_divide_min: int,

                 population_age_limit: int):
        self.gene_weight_probability: float = gene_weight_probability
        self.gene_random_probability: float = gene_random_probability
        self.genome_disable_probability: float = genome_disable_probability
        self.genome_node_probability: float = genome_node_probability
        self.genome_connection_probability: float = genome_connection_probability
        self.species_asexual_probability: float = species_asexual_probability
        self.species_interspecies_reproduction_probability: float = species_interspecies_reproduction_probability

        self.gene_max_weight: float = gene_max_weight
        self.gene_min_weight: float = gene_min_weight

        self.gene_weight_shift: float = gene_weight_shift

        self.genome_weight_coefficient: float = genome_weight_coefficient
        self.genome_disjoint_coefficient: float = genome_disjoint_coefficient
        self.genome_excess_coefficient: float = genome_excess_coefficient

        self.species_age_fertility_limit: int = species_age_fertility_limit
        self.species_threshold: float = species_threshold
        self.species_keep_champion: bool = species_keep_champion
        self.species_niche_divide_min: int = species_niche_divide_min

        self.population_age_limit: int = population_age_limit
