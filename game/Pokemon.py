from src.Node import Location
from src.Node import Node
from src.GraphAlgo import GraphAlgo
import json


# This class represents a pokemon
class Pokemon:

    def __init__(self, value, type_, pos: tuple):
        self.value = value
        self.type_ = type_
        self.pos = pos
        self.src = 0
        self.dest = 0
        self.is_taken = False
