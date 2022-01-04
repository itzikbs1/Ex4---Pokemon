import math
import sys

from Pokemon import Pokemon
from Agent import Agent
from src.GraphAlgo import GraphAlgo
from src.Node import Node
from src.Node import Location
from client import Client
import json

EPS = 0.001


def distance(pos1, pos2):
    return math.sqrt(((pos1.x - pos2.x) ** 2) + ((pos1.y - pos2.y) ** 2))


class Algo:

    def __init__(self, client):
        self.pokemons = self.get_pokemon_list()
        self.agents = self.get_agents_list()
        self.graphAlgo = GraphAlgo()
        self.client = client

    def get_pokemon_list(self):
        pokemon_list = []
        str_pok = self.client.get_pokemons()
        json_pok = json.loads(str_pok)
        for values in json_pok['Pokemons']:
            location = tuple(float(s) for s in values['pos'].strip("()").split(","))
            pokemon = Pokemon(values['value'], values['type'], location)
            pokemon_list.append(pokemon)

        pokemon_list.sort(key=lambda x: x.value, reverse=True)
        return pokemon_list

    def get_agents_list(self):
        agents_list = []
        str_agt = self.client.get_pokemons()
        json_agt = json.loads(str_agt)
        for values in json_agt['Agents']:
            location = tuple(float(s) for s in values['pos'].strip("()").split(","))
            agent = Agent(values['id'], values['value'], values['src'], values['dest'], values['speed'], location)
            agents_list.append(agent)

        return agents_list

    def next_node(self, agent: Agent):
        min_dis = sys.maxsize
        dest = -1
        val = 0
        node_list = agent.next_node_list
        for pokemon in self.pokemons:
            dest = self.get_dest_pok(pokemon)
            if len(node_list) == 0:
                current_dis, node_list = self.graphAlgo.shortest_path(agent.src, dest)
            else:
                current_dis, node_list = self.graphAlgo.shortest_path(agent.next_node_list[len(node_list) - 1], dest)
            if current_dis < min_dis:
                min_dis = current_dis
                val = pokemon.value
        agent.next_node_list.append(node_list)

        return "{agent id : " + agent.id + ",next_node_id" + dest + "}"

    def get_dest_pok(self, p):
        for i in self.graphAlgo.graph.nodes:
            for e in self.graphAlgo.graph.all_out_edges_of_node(i):
                src = self.graphAlgo.graph.nodes[i]
                dest = self.graphAlgo.graph.nodes[e.get(0)]
                dist = distance(src.location, dest.location)
                if distance(p.pos, dest.location) + distance(p.pos, src.location) < dist - EPS:
                    if p.type_ < 0 and dest.id < src.id:
                        return i.dest
                    elif p.type_ > 0 and dest.id > src.id:
                        return i.dest
                    else:
                        continue

        return -1

    def go_to(self, agents):
        for agent in agents:
            for i in agent.next_node_list:
                agent.setPos(self.graphAlgo.graph.nodes[i].location)
                agent.setNextNode(i)
        self.dict_of_agents()

    def add_agent(self):
        pass

    def is_caught(self, pokemons, agent):
        for pokemon in pokemons:
            if distance(agent.pos, pokemon.pos) < EPS:
                if pokemon.type_ < 0 and agent.dest < agent.src:
                    agent.value += pokemon.value
                    return True
                elif pokemon.type_ > 0 and agent.dest > agent.src:
                    agent.value += pokemon.value
                    return True
                else:
                    return False
        return False

    def dict_of_agents(self):
        agents = []
        for agent in self.agents:
            k = agent.id
            v = agent.value
            src = agent.src
            dest = agent.dest
            agent = {"id": k, "value": v.value, "src": src, "dest": dest}
            loc = str(v.pos)[1:-1]
            agent["pos"] = str(loc.replace(' ', ''))
            final_dict = {"Agent", agent}
            agents.append(final_dict)
        return agents
