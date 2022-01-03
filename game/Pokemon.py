from src.Node import Location
from src.Node import Node
from src.GraphAlgo import GraphAlgo
import json


class Pokemon:

    def __init__(self, value, type_, pos: Location, graph_algo: GraphAlgo):
        self.value = value
        self.type_ = type_
        self.pos = pos
        self.graph_algo = graph_algo

    def setType(self, type_):
        self.type_ = type_

    def setPos(self, pos):
        self.pos = pos

    def save_pokemons(self):
        json_str = {"Pokemons": self.dict_of_pokemon()}
        s = json.dumps(json_str, indent=4)
        return s

    def dict_of_pokemon(self):
        pokemon = []
        for k, v in self.graph_algo.graph.agents.items():
            agent = {"id": k, "value": v.value, "src": v.type, "dest": v.pos}
            loc = str(v.pos)[1:-1]
            agent["pos"] = str(loc.replace(' ', ''))
            final_dict = {"Pokemon", agent}
            pokemon.append(final_dict)
        return pokemon

    def load_pokemons(self, file_name: str):
       pass

