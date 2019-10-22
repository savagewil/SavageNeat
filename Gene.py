
class Gene:
    def __init__(self, weight: float, in_node: int, out_node: int, innovation_number :int, enabled :bool = True):
        self.weight: float = weight
        self.in_node: int = in_node
        self.out_node: int = out_node
        self.innovation_number: int = innovation_number
        self.enabled: bool = enabled

    def mutate(self, ):