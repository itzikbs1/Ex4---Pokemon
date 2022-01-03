from types import SimpleNamespace
from game.client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

# init pygame
from src.GraphAlgo import GraphAlgo

WIDTH, HEIGHT = 1080, 720

pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)
RADIUS = 15


class GUI:

    def __init__(self, client: Client):
        self.pokemons = []
        self.agents = []
        self.graph = GraphAlgo()
        self.client = client

    def get_pokemons(self):
        pokemons_json = self.client.get_pokemons()
        self.pokemons = json.loads(pokemons_json, object_hook=lambda d: SimpleNamespace(**d))
        self.pokemons = [p.Pokemon for p in self.pokemons]
        for p in self.pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=self.my_scale(
                float(x), x=True), y=self.my_scale(float(y), y=True))
        return self.pokemons

    def get_agents(self):
        agents = json.loads(self.client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
        self.agents = [agent.Agent for agent in agents]
        for a in self.agents:
            x, y, _ = a.pos.split(',')
            a.pos = SimpleNamespace(x=self.my_scale(
                float(x), x=True), y=self.my_scale(float(y), y=True))
        return self.agents

    def get_graph(self):
        graph_string = self.client.get_graph()
        graph_json = json.dumps(graph_string)
        self.graph.load_from_json(graph_json)
        return self.graph

    def get_min_max(self):
        for n in self.get_graph().graph.nodes.values():
            x, y, _ = n.pos.split(',')
            n.pos = SimpleNamespace(x=float(x), y=float(y))

        # get data proportions
        min_x = min(list(self.get_graph().graph.nodes.values()), key=lambda n: n.pos.x).pos.x
        min_y = min(list(self.get_graph().graph.nodes.values()), key=lambda n: n.pos.y).pos.y
        max_x = max(list(self.get_graph().graph.nodes.values()), key=lambda n: n.pos.x).pos.x
        max_y = max(list(self.get_graph().graph.nodes.values()), key=lambda n: n.pos.y).pos.y

        return min_x, min_y, max_x, max_y

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        min_x, min_y, max_x, max_y = self.get_min_max()
        if x:
            return self.scale(data, 50, screen.get_width() - 50, min_x, max_x)
        if y:
            return self.scale(data, 50, screen.get_height() - 50, min_y, max_y)

    """
    The code below should be improved significantly:
    The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
    """

    # # check events
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #         exit(0)

    # refresh surface
    # screen.fill(Color(0, 0, 0))

    def draw_nodes(self):
        for n in self.get_graph().graph.nodes.values():
            x = self.my_scale(n.location[0], x=True)
            y = self.my_scale(n.location[1], y=True)

            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(screen, int(x), int(y),
                                  RADIUS, Color(64, 80, 174))
            gfxdraw.aacircle(screen, int(x), int(y),
                             RADIUS, Color(255, 255, 255))

            # draw the node id
            id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)

    def draw_edges(self):
        for i in self.get_graph().graph.nodes:
            for e in self.get_graph().graph.all_out_edges_of_node(i):
                # find the edge nodes
                src = next(n for n in self.graph.graph.nodes.values() if n.id == i)
                dest = next(n for n in self.get_graph().graph.nodes.values() if n.id == e.get(0))

                # scaled positions
                src_x = self.my_scale(src.pos.x, x=True)
                src_y = self.my_scale(src.pos.y, y=True)
                dest_x = self.my_scale(dest.pos.x, x=True)
                dest_y = self.my_scale(dest.pos.y, y=True)

                # draw the line
                pygame.draw.line(screen, Color(61, 72, 126),
                                 (src_x, src_y), (dest_x, dest_y))

    def draw_agents(self):
        for agent in self.get_agents():
            pygame.draw.circle(screen, Color(122, 61, 23),
                               (int(agent.pos.x), int(agent.pos.y)), 10)
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked
        # in the same way).

    def draw_pokemons(self):
        for p in self.get_pokemons():
            if p.type > 0:
                pygame.draw.circle(screen, Color(0, 0, 255), (int(p.pos.x), int(p.pos.y)), 10)
            else:
                pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    def same_edge(self, p1, p2):
        for i in self.get_graph().graph.nodes:
            for e in self.get_graph().graph.all_out_edges_of_node(i):
                src = self.graph.graph.nodes[i]
                dest = self.graph.graph.nodes[e.get(0)]
                m = (src.location(1) - dest.location(1)) / (src.location(0) - dest.location(0))
                if p1.pos.y - src.location(1) == m * (p1.pos.x - src.location(0)) and p2.pos.y - src.location(
                        1) == m * (p2.pos.x - src.location(0)):
                    if p1.type != p2.type:
                        return False
                    else:
                        return True

        return False

        # update screen changes
        # display.update()
        #
        # refresh rate
        # clock.tick(60)
