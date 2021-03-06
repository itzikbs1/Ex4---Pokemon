import json

from game.Agent import Agent
from unittest import TestCase
from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph
from src.Node import Node


class TestAgent(TestCase):
    graph = DiGraph()
    graphAlgo = GraphAlgo()
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

    agent = Agent(0, 0, 3, 4, 1, (2, 1, 2), graphAlgo)

    def test_set_src(self):
        self.assertEqual(self.agent.src, 3)

    def test_set_dest(self):
        self.assertEqual(self.agent.dest, 4)

    def test_set_pos(self):
        self.assertEqual(self.agent.pos, (2, 1, 2))

    def test_set_id(self):
        self.assertEqual(self.agent.id, 0)

    def test_set_value(self):
        self.assertEqual(self.agent.value, 0)

    def test_set_speed(self):
        self.assertEqual(self.agent.speed, 4)

    def test_set_speed(self):
        self.assertEqual(self.agent.graph_algo, self.graphAlgo)
