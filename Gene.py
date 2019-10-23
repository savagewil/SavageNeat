from __future__ import annotations
from Conditions import Conditions
import random


class Gene:
    def __init__(self, weight: float, in_node: int, out_node: int, innovation_number: int, enabled: bool = True):
        """
        The gene class represents a connection gene, a connection between two nodes in a Network
        :param weight: The weight is the strength of the connection
        :param in_node: The in node is the node the connection starts at
        :param out_node: The out node the node the connection ends at
        :param innovation_number: The innovation number is a number used to track gene's history
        :param enabled: The enabled bit is used to identify if a connection is active
        """
        self.weight: float = weight
        self.in_node: int = in_node
        self.out_node: int = out_node
        self.innovation_number: int = innovation_number
        self.enabled: bool = enabled

    def mutate(self, conditions: Conditions) -> Gene:
        """
        Creates a mutated gene, with the same structure as the current.
        It same start and end, but has a mutated weight.
        The mutation can be a random shift, a complete randomization, or no mutation
        :param conditions: The Conditions objects which contains the parameters of the mutation
        :return: A new mutated gene with the same structure
        """
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
        """
        Returns a new gene which is a copy of the current gene
        :return: A new copy of the current gene
        """
        return Gene(self.weight, self.in_node, self.out_node, self.innovation_number, self.enabled)

    def __eq__(self, other: Gene) -> bool:
        """
        Checks if two genes should be considered equal
        Checks if two nodes have the same innovation number
        Returns false if the other object is not a Gene
        :param other: An object which should represent a Gene
        :return: True if the other is a Gene with the same innovation number, False otherwise
        """
        if isinstance(other, Gene):
            return self.innovation_number == other.innovation_number
        else:
            return False

    def __lt__(self, other: Gene) -> bool:
        """
        Checks if the current gene is less than another gene
        Looks to see if the current gene's innovation number is less than the innovation number of another node
        Throws a type error if the other object is not a Gene
        :param other: An object which should represent a Gene
        :return: True if the current innovation number is less than the other innovation number, False otherwise
        """
        if isinstance(other, Gene):
            return self.innovation_number < other.innovation_number
        else:
            raise TypeError("Less than is not supported between Gene and %s" % (str(type(other))))

    def __le__(self, other: Gene) -> bool:
        """
        Checks if the current gene is less than or equal to another gene
        Looks to see if the current gene's innovation number is
        less than or equal to the innovation number of another node
        Throws a type error if the other object is not a Gene
        :param other: An object which should represent a Gene
        :return: True if the current innovation number is
        less than or equal to the other innovation number, False otherwise
        """
        if isinstance(other, Gene):
            return self.innovation_number <= other.innovation_number
        else:
            raise TypeError("Less than or equal is not supported between Gene and %s" % (str(type(other))))

    def __gt__(self, other: Gene) -> bool:
        """
        Checks if the current gene is greater than another gene
        Looks to see if the current gene's innovation number is greater than the innovation number of another node
        Throws a type error if the other object is not a Gene
        :param other: An object which should represent a Gene
        :return: True if the current innovation number is greater than the other innovation number, False otherwise
        """
        if isinstance(other, Gene):
            return self.innovation_number > other.innovation_number
        else:
            raise TypeError("Greater than is not supported between Gene and %s" % (str(type(other))))

    def __ge__(self, other: Gene) -> bool:
        """
        Checks if the current gene is greater than or equal to another gene
        Looks to see if the current gene's innovation number is
        greater than or equal to the innovation number of another node
        Throws a type error if the other object is not a Gene
        :param other: An object which should represent a Gene
        :return: True if the current innovation number is
        greater than or equal to the other innovation number, False otherwise
        """
        if isinstance(other, Gene):
            return self.innovation_number >= other.innovation_number
        else:
            raise TypeError("Greater than or equal is not supported between Gene and %s" % (str(type(other))))

    def __hash__(self):
        """
        Return a hash that is unique when the gene has a unique innovation number
        :return: a unique hash
        """
        return self.innovation_number

    def to_structure_gene(self):
        """
        Creates a structure gene from the structure of the current gene
        :return: A StructureGene representing the structure of the gene
        """
        return StructureGene(self.in_node, self.out_node)


class StructureGene:
    def __init__(self, in_node: int, out_node: int):
        """
        A structure node is an abstraction of a gene used to compare the structure of the gene
        :param in_node: The in node is the node the connection starts at
        :param out_node: The out node the node the connection ends at
        """
        self.in_node: int = in_node
        self.out_node: int = out_node

    def __eq__(self, other: StructureGene) -> bool:
        """
        Checks to see if the structure of the gene is the same
        can be used when finding the innovation number
        :param other: Another object, should be a Gene
        :return: True if the other is a Gene with the same structure (in and out nodes), False otherwise
        """
        if isinstance(other, StructureGene):
            return self.in_node == other.in_node and self.out_node == other.out_node
        else:
            return False

    def __lt__(self, other: StructureGene) -> bool:
        """
        Checks if the current gene is less than another gene
        Looks to see if the current gene's in_node is less than the other genes's in node,
        or the in nodes are equal, and the current gene's out node is less than the other's out node
        :param other: An object which should represent a Gene
        :return: True if the structure of the gene is less than the structure of the other, False otherwise
        """
        if isinstance(other, StructureGene):
            return self.in_node < other.in_node or (self.in_node == other.in_node and self.out_node < other.out_node)
        else:
            raise TypeError("Less than is not supported between StructureGene and %s" % (str(type(other))))

    def __le__(self, other: StructureGene) -> bool:
        """
        Checks if the current gene is less than or equal to another gene
        Looks to see if the current gene's in_node is less than the other genes's in node,
        or the in nodes are equal, and the current gene's out node is less than or equal to the other's out node
        :param other: An object which should represent a Gene
        :return: True if the structure of the gene is less than or equal to the structure of the other, False otherwise
        """
        if isinstance(other, StructureGene):
            return self.in_node < other.in_node or (self.in_node == other.in_node and self.out_node <= other.out_node)
        else:
            raise TypeError("Less than or equal is not supported between StructureGene and %s" % (str(type(other))))

    def __gt__(self, other: StructureGene) -> bool:
        """
        Checks if the current gene is greater than another gene
        Looks to see if the current gene's in_node is greater than the other genes's in node,
        or the in nodes are equal, and the current gene's out node is greater than the other's out node
        :param other: An object which should represent a Gene
        :return: True if the structure of the gene is greater than the structure of the other, False otherwise
        """
        if isinstance(other, StructureGene):
            return self.in_node > other.in_node or (self.in_node == other.in_node and self.out_node > other.out_node)
        else:
            raise TypeError("Greater than is not supported between StructureGene and %s" % (str(type(other))))

    def __ge__(self, other: StructureGene) -> bool:
        """
        Checks if the current gene is greater than or equal to another gene
        Looks to see if the current gene's in_node is greater than the other genes's in node,
        or the in nodes are equal, and the current gene's out node is greater than or equal to the other's out node
        :param other: An object which should represent a Gene
        :return: True if the structure of the gene is greater than or equal to the structure of the other, False otherwise
        """
        if isinstance(other, StructureGene):
            return self.in_node > other.in_node or (self.in_node == other.in_node and self.out_node >= other.out_node)
        else:
            raise TypeError("Greater than or equal is not supported between StructureGene and %s" % (str(type(other))))

    def __hash__(self):
        """
        Uses the structure to produce a hash that is unique for each structure
        :return: a hash that is unique for each structure
        """
        hash_agg = 0
        shift = 1
        in_node = self.in_node
        out_node = self.out_node
        while in_node > 0 or out_node > 0:
            hash_agg += shift * (in_node % 10) + shift * 10 * (out_node % 10)
            in_node = in_node // 10
            out_node = out_node // 10
            shift *= 100
        return hash_agg
