class Conditions:
    def __init__(self, weight_probability: float, random_probability: float,
                 disable_probability: float, node_probability: float, connection_probability: float,
                 asexual_probability: float, interspecies_reproduction_probability: float,

                 max_weight: float, min_weight: float, weight_shift: float,

                 weight_coefficient: float, disjoint_coefficient: float, excess_coefficient: float,

                 species_age_fertility_limit: int, species_threshold: float, keep_champion: bool):
        self.weight_probability: float = weight_probability
        self.random_probability: float = random_probability
        self.disable_probability: float = disable_probability
        self.node_probability: float = node_probability
        self.connection_probability: float = connection_probability
        self.asexual_probability: float = asexual_probability
        self.interspecies_reproduction_probability: float = interspecies_reproduction_probability

        self.max_weight: float = max_weight
        self.min_weight: float = min_weight

        self.weight_shift: float = weight_shift

        self.weight_coefficient: float = weight_coefficient
        self.disjoint_coefficient: float = disjoint_coefficient
        self.excess_coefficient: float = excess_coefficient

        self.species_age_fertility_limit: int = species_age_fertility_limit
        self.species_threshold: float = species_threshold
        self.keep_champion: bool = keep_champion
