from __future__ import annotations
from Conditions import Conditions
import random



class Gene:
    def __init__(self, weight: float, in_node: int, out_node: int, innovation_number: int, enabled: bool = True):
        self.weight: float = weight
        self.in_node: int = in_node
        self.out_node: int = out_node
        self.innovation_number: int = innovation_number
        self.enabled: bool = enabled

    def mutate(self, conditions: Conditions) -> Gene:
        if random.random() < conditions.weight_probability:
            if random.random() < conditions.random_probability:
                return Gene(random.random() * (conditions.max_weight - conditions.min_weight) + conditions.min_weight,
                            self.in_node, self.out_node, self.innovation_number, self.enabled)
            else:
                return Gene(min(conditions.max_weight,
                                max(conditions.min_weight,
                                    (self.weight +
                                     random.random() *
                                     2 * conditions.weight_shift
                                     - conditions.weight_shift))),
                            self.in_node, self.out_node, self.innovation_number, self.enabled)
        else:
            return self.copy()

    def copy(self) -> Gene:
        return Gene(self.weight, self.in_node, self.out_node, self.innovation_number, self.enabled)

    def connection_equals(self, other) -> bool:
        if isinstance(other, Gene):
            return self.in_node == other.in_node and self.out_node == other.out_node
        else:
            return False

    def __eq__(self, other) -> bool:
        if isinstance(other, Gene):
            return self.innovation_number == other.innovation_number
        else:
            return False

    def __lt__(self, other) -> bool:
        if isinstance(other, Gene):
            return self.innovation_number < other.innovation_number
        else:
            raise TypeError("Less than is not supported between Gene and %s"%(str(type(other))))

    def __le__(self, other) -> bool:
        if isinstance(other, Gene):
            return self.innovation_number <= other.innovation_number
        else:
            raise TypeError("Less than or equal is not supported between Gene and %s"%(str(type(other))))

    def __gt__(self, other) -> bool:
        if isinstance(other, Gene):
            return self.innovation_number > other.innovation_number
        else:
            raise TypeError("Greater than is not supported between Gene and %s"%(str(type(other))))

    def __ge__(self, other) -> bool:
        if isinstance(other, Gene):
            return self.innovation_number >= other.innovation_number
        else:
            raise TypeError("Greater than or equal is not supported between Gene and %s"%(str(type(other))))
