from src.Node import Location
from src.Node import Node
from src.GraphAlgo import GraphAlgo
import json


class Agent:

    def __init__(self, id, value, src, dest, speed, pos: tuple, graph : GraphAlgo):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos
        self.graph_algo = graph
        self.next_node = -1
        self.next_node_list = []  # [node :Node]

    def setSrc(self, src):
        self.src = src

    def setDest(self, dest):
        self.dest = dest

    def setPos(self, pos):
        self.pos = pos

    def setNextNode(self, next_node):
        self.next_node = next_node

    def save_agent(self):
        json_str = {"Agents": self.dict_of_agents()}
        s = json.dumps(json_str, indent=4)
        return s

    def add_node(self, nodes: list):
        self.next_node_list.append(nodes)

    def dict_of_agents(self):
        agents = []
        k = self.id
        v = self.value
        src = self.src
        dest = self.dest
        agent = {"id": k, "value": v.value, "src": src, "dest": dest}
        loc = str(v.pos)[1:-1]
        agent["pos"] = str(loc.replace(' ', ''))
        final_dict = {"Agent", agent}
        agents.append(final_dict)
        return agents

    def next_edge(self):
        pass


