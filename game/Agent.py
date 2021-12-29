from src.Node import Location
from src.Node import Node
from src.GraphAlgo import GraphAlgo
import json
#dad

class Agent:

    def __init__(self, id, value, src: Node, dest: Node, speed, pos: Location, graph_algo: GraphAlgo):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos
        self.graph_algo = graph_algo

    def setSrc(self, src):
        self.src = src

    def setDest(self, dest):
        self.dest = dest

    def setPos(self, pos):
        self.pos = pos

    def save_agents(self):
        json_str = {"Agents": self.dict_of_agents()}
        s = json.dumps(json_str, indent=4)
        return s

    def dict_of_agents(self):
        agents = []
        for k, v in self.graph_algo.graph.agents.items():
            agent = {"id": k, "value": v.value, "src": v.src, "dest": v.dest}
            loc = str(v.pos)[1:-1]
            agent["pos"] = str(loc.replace(' ', ''))
            final_dict = {"Agent", agent}
            agents.append(final_dict)
        return agents
