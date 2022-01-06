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
    return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))


class Algo:

    def __init__(self, client):
        self.client = client
        self.pokemons = []
        self.agents = []
        self.characters = {}  # {id agent: pokemon,.....}
        self.graphAlgo = GraphAlgo()

    def get_pokemon_list(self):
        pokemons = []
        pokemon_json = self.client.get_pokemons()
        text_file = open("pok.json", "w")
        text_file.write(pokemon_json)
        text_file.close()
        with open("pok.json", "r") as fin:
            content = json.load(fin)
        with open("pok.json", "w") as fout:
            json.dump(content, fout, indent=1)
        with open("pok.json") as f:
            json_pok = json.load(f)
        for values in json_pok['Pokemons']:
            location = tuple(float(s) for s in values['Pokemon']['pos'].strip("()").split(","))
            pok = Pokemon(values['Pokemon']['value'], values['Pokemon']['type'], location)
            pokemons.append(pok)
        self.pokemons = pokemons
        return self.pokemons

    def get_agents_list(self):
        self.agents = []
        str_agt = self.client.get_agents()
        text_file = open("str_agt.json", "w")
        text_file.write(str_agt)
        text_file.close()
        with open("str_agt.json", "r") as fin:
            content = json.load(fin)
        with open("str_agt.json", "w") as fout:
            json.dump(content, fout, indent=1)
        with open("str_agt.json") as f:
            json_agt = json.load(f)
        for values in json_agt['Agents']:
            location = tuple(float(s) for s in values['Agent']['pos'].strip("()").split(","))
            agent = Agent(values['Agent']['id'], values['Agent']['value'], values['Agent']['src'],
                          values['Agent']['dest'],
                          values['Agent']['speed'], location, self.graphAlgo)
            self.agents.append(agent)

        return self.agents

    def next_node(self, agent: Agent):
        min_dis = sys.maxsize
        node_list = []
        for pokemon in self.pokemons:
            self.get_dest_pok(pokemon)

            if len(agent.next_node_list) == 0:
                current_dis, node_list = self.graphAlgo.shortest_path(agent.src, pokemon.src)
                current_dis += self.graphAlgo.graph.nodes[pokemon.src].out_edges[pokemon.dest]
                node_list.append(pokemon.dest)
            else:
                current_dis, node_list = self.graphAlgo.shortest_path(agent.next_node_list[-1], pokemon.src)
                current_dis += self.graphAlgo.graph.nodes[pokemon.src].out_edges[pokemon.dest]
            if current_dis < min_dis:
                min_dis = current_dis
                node_list.append(pokemon.dest)
                self.characters[agent.id] = pokemon
        node_list.pop(0)
        agent.next_node_list.extend(node_list)

    def get_dest_pok(self, p):
        for i in self.graphAlgo.graph.nodes:
            for e in self.graphAlgo.graph.all_out_edges_of_node(i).keys():
                src = self.graphAlgo.graph.nodes[i]
                dest = self.graphAlgo.graph.nodes[e]
                dist = distance(src.location, dest.location)
                if distance(p.pos, dest.location) + distance(p.pos, src.location) - EPS < dist:
                    if p.type_ < 0 and dest.id < src.id:
                        p.src = src.id
                        p.dest = dest.id
                    elif p.type_ > 0 and dest.id > src.id:
                        p.src = src.id
                        p.dest = dest.id
                    else:
                        continue

        return -1

    def go_to(self, agent):
        if len(agent.next_node_list) > 0 and agent.dest == -1:
            print(agent.pos)
            # print(agent.next_node_list)
            temp = agent.next_node_list[0]
            agent.src = temp
            del agent.next_node_list[0]
            # agent.setPos(self.graphAlgo.graph.nodes[temp].location)
            self.client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(temp) + '}')
            self.is_caught(self.pokemons, agent)
            # self.client.move()
            print(agent.pos)

    def add_agent(self):
        pass

    def is_caught(self, pokemons, agent):
        for pokemon in pokemons:
            if distance(agent.pos, pokemon.pos) < EPS:
                if pokemon.type_ < 0 and agent.dest < agent.src:
                    agent.value += pokemon.value
                    self.characters.pop(agent.id, None)
                    self.pokemons.remove(pokemon)
                elif pokemon.type_ > 0 and agent.dest > agent.src:
                    agent.value += pokemon.value
                    self.characters.pop(agent.id, None)
                    self.pokemons.remove(pokemon)
                else:
                    return

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
