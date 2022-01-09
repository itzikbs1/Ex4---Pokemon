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

