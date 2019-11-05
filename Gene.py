from __future__ import annotations
import Conditions
import random
import StructureGene
import GenePool

from functions import surround_tag, remove_tag

class Gene:
    def __init__(self, weight: float, in_node: int, out_node: int, innovation_number: int,
                 enabled: bool = True, gene_pool: GenePool.GenePool = None):
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
        if gene_pool:
            self.innovation_number = gene_pool.get_innovation_number(self.to_structure_gene())

    def mutate(self, conditions: Conditions.Conditions) -> Gene:
        """
        Creates a mutated gene, with the same structure as the current.
        It same start and end, but has a mutated weight.
        The mutation can be a random shift, a complete randomization, or no mutation
        :param conditions: The Conditions objects which contains the parameters of the mutation
        :return: A new mutated gene with the same structure
        """
        if random.random() < conditions.gene_weight_probability:
            if random.random() < conditions.gene_random_probability:
                return Gene(random.random() * (conditions.gene_max_weight - conditions.gene_min_weight) + conditions.gene_min_weight,
                            self.in_node, self.out_node, self.innovation_number, self.enabled)
            else:
                return Gene(min(conditions.gene_max_weight,
                                max(conditions.gene_min_weight,
                                    (self.weight +
                                     random.random() *
                                     2 * conditions.gene_weight_shift
                                     - conditions.gene_weight_shift))),
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
            raise TypeError("Less than is not supported between %s and %s" % (str(type(self)), str(type(other))))

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
            raise TypeError("Less than or equal is not supported between %s and %s" % (str(type(self)), str(type(other))))

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
            raise TypeError("Greater than is not supported between %s and %s" % (str(type(self)), str(type(other))))

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
            raise TypeError("Greater than or equal is not supported between %s and %s" % (str(type(self)), str(type(other))))

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
        return StructureGene.StructureGene(self.in_node, self.out_node)

    def __str__(self) -> str:

        save_string = ""
        save_string += surround_tag("weight", str(self.weight))
        save_string += surround_tag("in_node", str(self.in_node))
        save_string += surround_tag("out_node", str(self.out_node))
        save_string += surround_tag("innovation_number", str(self.innovation_number))
        save_string += surround_tag("enabled", str(self.enabled))

        return save_string

    @staticmethod
    def load(string) -> Gene:
        weight_str, string = remove_tag("weight", string)
        in_node_str, string = remove_tag("in_node", string)
        out_node_str, string = remove_tag("out_node", string)
        innovation_number_str, string = remove_tag("innovation_number", string)
        enabled_str, string = remove_tag("enabled", string)

        weight = float(weight_str)
        in_node = int(in_node_str)
        out_node = int(out_node_str)
        innovation_number = int(innovation_number_str)
        enabled = bool(enabled_str)

        return Gene(weight,in_node, out_node, innovation_number, enabled)

