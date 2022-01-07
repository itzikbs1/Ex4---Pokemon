import math
import sys

from Pokemon import Pokemon
from Agent import Agent
from src.GraphAlgo import GraphAlgo
from src.Node import Node
from src.Node import Location
from client import Client
import json

EPS1 = 0.001
EPS = EPS1 * EPS1


def distance(pos1, pos2):
    return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))


class Algo:

    def __init__(self, client):
        self.client = client
        self.pokemons = []
        self.agents = []

        # {id agent: pokemon,.....}
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

    def get_agent_info(self):
        game_info_str = self.client.get_info()
        y = json.loads(game_info_str)
        return y["GameServer"]["agents"]

    def next_node(self, agent: Agent):
        min_dis = sys.maxsize
        node_list_final = []
        for pokemon in self.pokemons:
            if not pokemon.is_taken:
                self.pokemon_edge(pokemon)

                if len(agent.next_node_list) == 0:
                    current_dis, node_list = self.graphAlgo.shortest_path(agent.src, pokemon.src)
                    t1 = distance(agent.pos, self.graphAlgo.graph.nodes[agent.src].location)
                    t2 = distance(pokemon.pos, self.graphAlgo.graph.nodes[pokemon.src].location)
                    current_dis += self.graphAlgo.graph.nodes[pokemon.src].out_edges[pokemon.dest] + (t2 - t1)
                    node_list.append(pokemon.dest)


                else:
                    current_dis, node_list = self.graphAlgo.shortest_path(agent.next_node_list[-1], pokemon.src)
                    t1 = distance(agent.pos, self.graphAlgo.graph.nodes[agent.src].location)
                    t2 = distance(pokemon.pos, self.graphAlgo.graph.nodes[pokemon.src].location)
                    current_dis += self.graphAlgo.graph.nodes[pokemon.src].out_edges[pokemon.dest] + (t2 - t1)
                    node_list.append(pokemon.dest)
                if current_dis < min_dis:
                    min_dis = current_dis
                    node_list_final = node_list
                    agent.next_pokemon = pokemon
                    agent.is_taken = True
                    pokemon.is_taken = True
                    # print(node_list)
                    # print(current_dis)
            # print(self.characters[agent.id].pos)
        if len(node_list_final) > 0:
            node_list_final.pop(0)
            agent.next_node_list.extend(node_list_final)

    def go_to(self, agent):
        if len(agent.next_node_list) > 0 and agent.dest == -1:
            temp = agent.next_node_list[0]
            agent.src = temp
            del agent.next_node_list[0]
            self.client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(temp) + '}')
            self.is_caught(agent.next_pokemon, agent)
            # self.client.move()

    def get_dest_pok(self, p, src, dest):
        dist = distance(src.location, dest.location)
        if p.type_ < 0 and dest.id > src.id:
            return False
        elif p.type_ > 0 and dest.id < src.id:
            return False
        else:
            return distance(p.pos, dest.location) + distance(p.pos, src.location) - EPS < dist

    def pokemon_edge(self, p):
        for i in self.graphAlgo.graph.nodes:
            for e in self.graphAlgo.graph.all_out_edges_of_node(i).keys():
                src = self.graphAlgo.graph.nodes[i]
                dest = self.graphAlgo.graph.nodes[e]
                if self.get_dest_pok(p, src, dest):
                    p.src = src.id
                    p.dest = dest.id

    def dist_ag_to_pok(self, agent, pokemon):
        t1 = distance(agent.pos, self.graphAlgo.graph.nodes[agent.src].location)
        t2 = distance(pokemon.pos, self.graphAlgo.graph.nodes[pokemon.src].location)
        return self.graphAlgo.shortest_path_dist(agent.src, pokemon.src) + (t2 - t1)

    def is_caught(self, pokemon, agent):
        if distance(agent.pos, pokemon.pos) < EPS:
            if pokemon.type_ < 0 and agent.dest < agent.src:
                agent.value += pokemon.value
                agent.next_pokemon = None
                # pokemon.is_taken = False
                # self.pokemons.remove(pokemon)
            elif pokemon.type_ > 0 and agent.dest > agent.src:
                agent.value += pokemon.value
                agent.next_pokemon = None
                # pokemon.is_taken = False
                # self.pokemons.remove(pokemon)
            else:
                return

    def choose_agent(self):
        for agent in self.agents:
            if agent.next_pokemon is None and not agent.is_taken:
                print(agent.next_pokemon)
                self.next_node(agent)
                self.go_to(agent)
                print(agent.is_taken)
                print(agent.next_pokemon, agent.id)
        self.client.move()

    # def dict_of_agents(self):
    #     agents = []
    #     for agent in self.agents:
    #         k = agent.id
    #         v = agent.value
    #         src = agent.src
    #         dest = agent.dest
    #         agent = {"id": k, "value": v.value, "src": src, "dest": dest}
    #         loc = str(v.pos)[1:-1]
    #         agent["pos"] = str(loc.replace(' ', ''))
    #         final_dict = {"Agent", agent}
    #         agents.append(final_dict)
    #     return agents
