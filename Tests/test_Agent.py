import math
from unittest import TestCase
from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph
from src.Node import Node
from game.Agent import Agent
from game.Pokemon import Pokemon
from game.client import Client
from game.Algo import Algo


class TestAlgo(TestCase):
    graph = DiGraph()
    graph.add_node(0, (1, 2, 3))
    graph.add_node(1, (1, 2, 3))
    graph.add_node(2, (1, 2, 3))
    graph.add_node(3, (1, 2, 3))
    graph.add_node(4, (1, 2, 3))
    graph.add_edge(0, 1, 1)
    graph.add_edge(3, 0, 3)
    graph.add_edge(0, 2, 2)
    graph.add_edge(1, 3, 4)
    graph.add_edge(2, 3, 5)
    graph.add_edge(4, 1, 3)
    graph.add_edge(3, 4, 2)
    graphAlgo = GraphAlgo(graph)

    PORT = 6666
    HOST = '127.0.0.1'
    client = Client()
    algo = Algo(client)
    client.start_connection(HOST, PORT)
    client.start()

    agent1 = Agent(0, 0, 9, 8, 5.0, (2, 1, 2), graphAlgo)
    agent2 = Agent(0, 0, 3, 4, 1.0, (35.19951426649707, 32.10554296228734, 0.0), graphAlgo)

    pokemon1 = Pokemon(5.0, -1, (35.197656770719604, 32.10191878639921))
    pokemon2 = Pokemon(8.0, -1, (35.206679711961414, 32.10571613186106))
    pokemon3 = Pokemon(13.0, -1, (35.212669424769075, 32.105340746955505))
    pokemon4 = Pokemon(5.0, -1, (35.21120742821597, 32.10240519983585))
    pokemon5 = Pokemon(9.0, -1, (35.2107064115802, 32.10181728154006))
    pokemon6 = Pokemon(12.0, -1, (35.20704629752213, 32.105471692111855))

    node_src = Node(0, (1, 2, 3))
    node_dest = Node(1, (3, 2, 1))
    pok = Pokemon(5.0, -1, (1, 1, 0.0))

    def distance(self, pos1, pos2):
        return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))

    def test_get_pokemon_list(self):
        list_pok = self.algo.get_pokemon_list()
        self.assertEqual(list_pok[0].value, self.pokemon1.value)

    def test_get_agents_list(self):
        num_of_agents = self.algo.get_info()[0]
        for i in range(num_of_agents):
            self.client.add_agent("{\"id\":" + str(i) + "}")
        self.algo.agents = self.algo.get_agents_list()
        self.assertEqual(self.algo.agents[0].value, self.agent1.value)

    def test_get_agent_info(self):
        num_of_agents = self.algo.get_info()[0]
        self.assertEqual(int(self.client.get_info()[-3]), int(num_of_agents))

    def test_next_node(self):
        num_of_agents = self.algo.get_info()[0]
        for i in range(num_of_agents):
            self.client.add_agent("{\"id\":" + str(i) + "}")
        self.algo.init_pok_list_agents()
        self.algo.init_list_agents()
        self.algo.init_size_path()
        self.algo.init_counter_nodes()
        self.algo.agents_list_pok[self.agent1.id] = self.pokemon1
        self.agent1.value += self.pokemon1.value
        self.assertEqual(self.agent1.value, self.pokemon1.value)

    def test_go_to(self):
        num_of_agents = self.algo.get_info()[0]
        for i in range(num_of_agents):
            self.client.add_agent("{\"id\":" + str(i) + "}")
        self.algo.init_pok_list_agents()
        self.algo.init_list_agents()
        self.algo.agents_list[self.agent2.id] = {0: 0}
        self.assertEqual(self.algo.go_to(self.agent2), None)

    def test_get_dest_pok(self):
        self.assertEqual(self.algo.get_dest_pok(self.pokemon1, self.node_src, self.node_dest), False)
        self.assertEqual(self.algo.get_dest_pok(self.pok, self.node_dest, self.node_src), False)

    def test_pokemon_edge(self):
        self.algo.pokemon_edge(self.pokemon1)
        self.assertEqual(self.pokemon1.src, 0)
        self.assertEqual(self.pokemon1.dest, 0)

    def test_free_pok(self):
        num_of_agents = self.algo.get_info()[0]
        for i in range(num_of_agents):
            self.client.add_agent("{\"id\":" + str(i) + "}")
        self.algo.init_pok_list_agents()
        self.algo.init_list_agents()
        pokemon1 = Pokemon(5.0, -1, (35.197656770719604, 32.10191878639921, 0.0))
        pokemon2 = Pokemon(5.0, -1, (35.097656770719604, 32.10191878639921, 0.0))
        agent3 = Agent(0, 2, 1, 4, 5.0, (2, 1, 2), self.graphAlgo)

    def test_choose_agent(self):
        num_of_agents = self.algo.get_info()[0]
        for i in range(num_of_agents):
            self.client.add_agent("{\"id\":" + str(i) + "}")
        self.algo.init_pok_list_agents()
        self.algo.init_list_agents()
        self.algo.agents_list_pok[self.agent1.id] = self.pokemon1
        self.assertEqual(self.algo.agents_list_pok[0].value, self.pokemon1.value)

    def test_distance(self):
        self.assertEqual(self.distance(self.pokemon1.pos, self.pokemon2.pos), 0.0097894484630018)

