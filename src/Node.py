class Location:

    def __init__(self, x, y, z):
        self.location = (x, y, z)


class Node:

    def __init__(self, id: int, location):
        self.id = id
        self.weight = 0
        self.tag = 0
        self.location = location
        self.in_edges = {}  # {node's id : weight}
        self.out_edges = {}  # {node's id : weight}
        self.out_edges_size = 0
        self.in_edges_size = 0

    def setWeight(self, weight):
        """
        set the weight of the node
        :param weight:
        """
        self.weight = weight

    def setTag(self, tag):
        """
        set the node tag
        :param tag:
        """
        self.tag = tag

    def set_location(self, x, y, z):
        """
        set the node location
        :param x:
        :param y:
        :param z:
        """
        self.location = (x, y, z)

    def __repr__(self):
        return f"{self.id}: |edges out| {self.out_edges_size} |edges in| {self.in_edges_size}"
