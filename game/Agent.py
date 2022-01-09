from src.Node import Location
from src.Node import Node
from src.GraphAlgo import GraphAlgo


# This class represents an agent
class Agent:

    def __init__(self, id, value, src, dest, speed, pos: tuple, graph: GraphAlgo):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos
        self.graph_algo = graph
        self.next_node = -1
        self.is_taken = False
        self.next_node_list = []  # [node :Node]
        self.next_pokemon = None

    def setNextNode(self, next_node):
        self.next_node = next_node

    def add_node(self, nodes):
        self.next_node_list.append(nodes)
