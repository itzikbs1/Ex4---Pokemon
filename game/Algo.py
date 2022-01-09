import math
import sys

from game.Pokemon import Pokemon
from game.Agent import Agent
from src.GraphAlgo import GraphAlgo

import json

EPS1 = 0.001
EPS = EPS1 * EPS1


def distance(pos1, pos2):
    """
    This function calcs the distance between two points and returns is
    :param pos1: first point
    :param pos2: second point
    :return: The distance
    """
    return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))


class Algo:
    """
    This class implements the algorithm to find best route from agent to pokemon
    """
#
    def __init__(self, client):
        self.client = client
        self.pokemons = []
        self.agents = []
        self.graphAlgo = GraphAlgo()
        self.agents_list = {}  # {id agent: path,.....}
        self.agents_list_pok = {}  # {id agent: pok,.....}
        self.counter_nodes = {}  # {agent id, counter to num of node to pok}
        self.size_path = {}  # {agent.id, size path}

    def init_list_agents(self):
        for ag in self.agents:
            self.agents_list[ag.id] = []

    def init_pok_list_agents(self):
        for ag in self.agents:
            self.agents_list_pok[ag.id] = []

    def init_counter_nodes(self):
        for ag in self.agents:
            self.counter_nodes[ag.id] = 0

    def init_size_path(self):
        for ag in self.agents:
            self.size_path[ag.id] = 0

    def free_pok(self, agent, pokemon):
        for poki in self.agents_list_pok.values():
            if poki is not None:
                for p in poki:
                    if p is not None:
                        if p.value == pokemon.value and p.type_ == pokemon.type_:
                            if p.pos[0] == pokemon.pos[0] and p.pos[1] == pokemon.pos[1]:
                                return False
        return True

    def get_pokemon_list(self):
        """
        This function gets a string formatted as json reprsenting a list of pokemons
        and turns it to a list of pokemons
        :return: The pokemons list
        """
        pokemons = []
        pokemon_json = self.client.get_pokemons()
        text_file = open("pok.json", "w")  # load to a text file
        text_file.write(pokemon_json)
        text_file.close()
        with open("pok.json", "r") as fin:  # loads the file to a json file
            content = json.load(fin)
        with open("pok.json", "w") as fout:  # dumps it to a json
            json.dump(content, fout, indent=1)
        with open("pok.json") as f:  # load from the json and get all the values
            json_pok = json.load(f)
        for values in json_pok['Pokemons']:
            location = tuple(float(s) for s in values['Pokemon']['pos'].strip("()").split(","))
            pok = Pokemon(values['Pokemon']['value'], values['Pokemon']['type'], location)
            pokemons.append(pok)
        self.pokemons = pokemons
        return self.pokemons

    def get_agents_list(self):
        """
        This function gets a string formatted as json reprsenting a list of agents
        and turns it to a list of agnets
        :return: The agents list
        """
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

    def get_graph(self):
        """
        This function gets a json string representing a graph and loads it to a graph object.
        :return:
        """
        graph_string = self.client.get_graph()
        text_file = open("graph_string.txt", "w")
        text_file.write(graph_string)
        text_file.close()
        with open("graph_string.txt", "r") as fin:
            content = json.load(fin)
        with open("graph_string.txt", "w") as fout:
            json.dump(content, fout, indent=1)
        self.graphAlgo.load_from_json("graph_string.txt")  # use the load from json algorithm from GraphAlgo class
        return self.graphAlgo

    def get_info(self):
        """
        Gets info from the server
        :return: The insfo representing amount of agents and moves
        """
        game_info_str = self.client.get_info()
        y = json.loads(game_info_str)
        return [y["GameServer"]["agents"], y["GameServer"]["moves"]]

    def next_node(self, agent: Agent):
        """
        Thi function finds the best set of nodes for an agent to get fastest to the closest pokemon.
        It uses shortest_path algorithm which is used in GraphAlgo class. This algorithm uses dijkstra algorithm to find
        shrtest path from node a to node b and it returns the weight of the path and the actual path.
        :param agent:
        :return:
        """
        min_dis = sys.maxsize  # set min distance to max size
        node_list_final = []
        pok = None
        for pokemon in self.pokemons:  # iterate over all pokemons
            if self.free_pok(agent, pokemon):
                if len(self.agents_list_pok[agent.id]) == 0:
                    self.pokemon_edge(pokemon)  # update the edge the pokemon is on

                    if len(self.agents_list[agent.id]) == 0:  # if the list is empty
                        current_dis, node_list = self.graphAlgo.shortest_path(agent.src, pokemon.src)  # calc best path
                        t1 = distance(agent.pos, self.graphAlgo.graph.nodes[agent.src].location)
                        t2 = distance(pokemon.pos, self.graphAlgo.graph.nodes[pokemon.src].location)
                        current_dis += self.graphAlgo.graph.nodes[pokemon.src].out_edges[pokemon.dest] + (
                                t2 - t1)  # add dest
                        node_list.append(pokemon.dest)  # add to node list

                    else:  # if the list is not empty do the same
                        current_dis, node_list = self.graphAlgo.shortest_path(self.agents_list[agent.id][-1],
                                                                              pokemon.src)
                        t1 = distance(agent.pos, self.graphAlgo.graph.nodes[agent.src].location)
                        t2 = distance(pokemon.pos, self.graphAlgo.graph.nodes[pokemon.src].location)
                        until_dis = self.graphAlgo.shortest_path_dist(self.agents_list[agent.id][0],
                                                                      self.agents_list[agent.id][-1])
                        current_dis += self.graphAlgo.graph.nodes[pokemon.src].out_edges[pokemon.dest] + (
                                t2 - 2 * t1) + until_dis
                        node_list.append(pokemon.dest)
                    if current_dis < min_dis:  # check for minimum distance path
                        min_dis = current_dis
                        node_list_final = node_list
                        pok = pokemon

        if len(node_list_final) > 0:
            poki = Pokemon(pok.value, pok.type_, pok.pos)
            self.agents_list_pok[agent.id].append(poki)
            node_list_final.pop(0)  # pop the first value because its the source of the agent
            self.agents_list[agent.id].extend(node_list_final)  # add to it's list
            self.size_path[agent.id] = len(node_list_final)

    def go_to(self, agent):
        """
        This function sets the next node for the agent to go to
        :param agent: Current agent
        """
        if len(self.agents_list[agent.id]) > 0 and agent.dest == -1:
            temp = self.agents_list[agent.id][0]  # get first element from list
            agent.src = temp  # set is as the new agent src
            del self.agents_list[agent.id][0]  # remove it
            self.counter_nodes[agent.id] += 1
            self.client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(temp) + '}')  # set next node
            if self.counter_nodes[agent.id] == self.size_path[agent.id]:
                self.counter_nodes[agent.id] = 0
                self.agents_list_pok[agent.id] = []

    def get_dest_pok(self, p, src, dest):
        """
        This function finds the edge the pokemon is on. It's src and dest nodes
        :param p: pokemon
        :param src: src node
        :param dest: dest node
        :return: true if on this edge, false if not
        """
        dist = distance(src.location, dest.location)
        if p.type_ < 0 and dest.id > src.id:
            return False
        elif p.type_ > 0 and dest.id < src.id:
            return False
        else:
            return distance(p.pos, dest.location) + distance(p.pos, src.location) - EPS < dist

    def pokemon_edge(self, p):
        """
        This function sets the pokemon src and dest to the edge its located on.
        :param p: the pokemon
        """
        for i in self.graphAlgo.graph.nodes:  # iterate over each node
            for e in self.graphAlgo.graph.all_out_edges_of_node(i).keys():  # get all edges going out from the node
                src = self.graphAlgo.graph.nodes[i]
                dest = self.graphAlgo.graph.nodes[e]
                if self.get_dest_pok(p, src, dest):  # if its on the edge update src and dest
                    p.src = src.id
                    p.dest = dest.id

    def choose_agent(self):
        """
        This function applies the whole algorithm and moves the agents
        :return:
        """
        for agent in self.agents:
            self.next_node(agent)
            self.go_to(agent)

        self.client.move()
