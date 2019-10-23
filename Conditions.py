class Conditions:
    def __init__(self, weight_probability: float, random_probability: float,
                 max_weight: float, min_weight: float, weight_shift: float):
        self.weight_probability: float = weight_probability
        self.random_probability: float = random_probability
        self.max_weight: float = max_weight
        self.min_weight: float = min_weight
        self.weight_shift: float = weight_shift
