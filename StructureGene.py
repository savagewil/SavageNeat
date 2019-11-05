from __future__ import annotations

import Gene

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
            raise TypeError("Less than is not supported between %s and %s" % (str(type(self)), str(type(other))))

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
            raise TypeError("Less than or equal is not supported between %s and %s" % (str(type(self)), str(type(other))))

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
            raise TypeError("Greater than is not supported between %s and %s" % (str(type(self)), str(type(other))))

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
            raise TypeError("Greater than or equal is not supported between %s and %s" % (str(type(self)), str(type(other))))

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

    def __str__(self) -> str:

        save_string = ""
        save_string += surround_tag("in_node", str(self.in_node))
        save_string += surround_tag("out_node", str(self.out_node))

        return save_string

    @staticmethod
    def load(string) -> StructureGene:
        in_node_str, string = remove_tag("in_node", string)
        out_node_str, string = remove_tag("out_node", string)

        in_node = int(in_node_str)
        out_node = int(out_node_str)

        return StructureGene(in_node, out_node)


