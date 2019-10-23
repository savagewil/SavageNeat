class Conditions:
    def __init__(self, weight_probability: float, random_probability: float,
                 max_weight: float, min_weight: float, weight_shift: float,
                 weight_coefficient: float, disjoint_coefficient: float, excess_coefficient: float):
        self.weight_probability: float = weight_probability
        self.random_probability: float = random_probability
        self.max_weight: float = max_weight
        self.min_weight: float = min_weight
        self.weight_shift: float = weight_shift
        self.weight_coefficient = weight_coefficient
        self.disjoint_coefficient = disjoint_coefficient
        self.excess_coefficient = excess_coefficient

