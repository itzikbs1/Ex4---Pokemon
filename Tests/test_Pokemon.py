from game.Pokemon import Pokemon
from unittest import TestCase
from src.GraphAlgo import GraphAlgo
from src.Node import Node


class test_Pokemon(TestCase):
    pokemon = Pokemon(12, 1, (12, 35, 42))

    def test_set_type(self):
        self.assertEqual(self.pokemon.type_, 1)

    def test_set_pos(self):
        self.assertEqual(self.pokemon.pos, (12, 35, 42))
