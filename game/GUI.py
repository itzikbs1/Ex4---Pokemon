import sys
from types import SimpleNamespace
from game.client import Client
import json
from pygame import gfxdraw
import pygame
import time as Time
from Button import Button
from pygame import *
from src.GraphAlgo import GraphAlgo
from Algo import Algo

WIDTH, HEIGHT = 1080, 720
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
REFRESH = 60
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)
RADIUS = 15
exit_img = pygame.image.load("../Images/Exit.png").convert_alpha()
pause_img = pygame.image.load("../Images/pause.png").convert_alpha()
background = pygame.image.load("../Images/5183000.jpg")


class GUI:

    def __init__(self, client: Client):
        self.client = client
        self.screen = screen
        self.pokemons = []
        self.agents = []
        self.graph = GraphAlgo()
        self.algo = Algo(client)

    def draw(self):
        # algo = Algo(self.client)
        pygame.init()
        start_time = Time.time()
        self.graph = self.get_graph()
        self.agents = self.algo.get_agents_list()
        self.scale_agents()
        self.algo.graphAlgo = self.graph
        pygame.display.set_caption("Pokemon Game")
        running = True
        while running:
            self.agents = self.algo.get_agents_list()
            self.scale_agents()
            self.pokemons = self.algo.get_pokemon_list()
            # is_minus = False
            for agent in self.agents:
                self.algo.next_node(agent)
                self.algo.go_to(agent)
                # if agent.dest == -1:
                #     is_minus = True
                # self.scale_agents()
                print(agent.pos)
                ttl = self.client.time_to_end()
            self.client.move()
            self.scale_pokemons()
            pygame.display.update()
            clock.tick(REFRESH)
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            elapsed_time = Time.time() - start_time
            if self.add_exit_button():
                running = False
                pygame.quit()
            if self.add_pasue_button():
                self.pause()
                start_time = Time.time() - elapsed_time
            self.get_time(int(elapsed_time))
            self.get_score()
            self.draw_nodes()
            self.draw_edges()
            self.draw_agents()
            self.draw_pokemons()
            pygame.display.update()
            clock.tick(REFRESH)

            # for agent in self.agents:
            #     if agent.dest == -1:
            #         next_node = (agent.src - 1) % self.graph.graph.nodes_size
            #         print(next_node)
            #         self.client.choose_next_edge(
            #             '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            #         ttl = self.client.time_to_end()
            #         print(ttl, self.client.get_info())
            #
            # self.client.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

    def get_pokemons(self):
        pokemons = json.loads(self.client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        self.pokemons = [p.Pokemon for p in pokemons]
        for p in self.pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=self.my_scale(
                float(x), x=True), y=self.my_scale(float(y), y=True))
        return self.pokemons

    def get_agents(self):
        agents = json.loads(self.client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
        self.agents = [agent.Agent for agent in agents]

    def get_graph(self):
        graph_string = self.client.get_graph()
        text_file = open("graph_string.txt", "w")
        text_file.write(graph_string)
        text_file.close()
        with open("graph_string.txt", "r") as fin:
            content = json.load(fin)
        with open("graph_string.txt", "w") as fout:
            json.dump(content, fout, indent=1)
        self.graph.load_from_json("graph_string.txt")
        return self.graph

    def get_min_max(self):

        # get data proportions
        min_x = min(list(self.graph.graph.nodes.values()), key=lambda n: n.location[0]).location[0]
        min_y = min(list(self.graph.graph.nodes.values()), key=lambda n: n.location[1]).location[1]
        max_x = max(list(self.graph.graph.nodes.values()), key=lambda n: n.location[0]).location[0]
        max_y = max(list(self.graph.graph.nodes.values()), key=lambda n: n.location[1]).location[1]

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

    def draw_nodes(self):
        for n in self.graph.graph.nodes.values():
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
        for i in self.graph.graph.nodes:
            for e in self.graph.graph.all_out_edges_of_node(i).keys():
                # find the edge nodes
                src = next(n for n in self.graph.graph.nodes.values() if n.id == i)
                dest = next(n for n in self.get_graph().graph.nodes.values() if n.id == e)

                # scaled positions
                src_x = self.my_scale(src.location[0], x=True)
                src_y = self.my_scale(src.location[1], y=True)
                dest_x = self.my_scale(dest.location[0], x=True)
                dest_y = self.my_scale(dest.location[1], y=True)

                # draw the line
                pygame.draw.line(screen, Color(61, 72, 126),
                                 (src_x, src_y), (dest_x, dest_y))

    def scale_agents(self):
        for a in self.agents:
            x = a.pos[0]
            y = a.pos[1]
            a.pos = (self.my_scale(x, x=True), self.my_scale(y, y=True), 0)

    def scale_pokemons(self):
        for a in self.pokemons:
            x = a.pos[0]
            y = a.pos[1]
            a.pos = (self.my_scale(x, x=True), self.my_scale(y, y=True), 0)

    def draw_agents(self):
        for agent in self.agents:
            print(agent.pos)
            t = (int(agent.pos[0]), int(agent.pos[1]))
            print(t)
            pygame.draw.circle(screen, Color(250, 10, 23),
                               t, 10)
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked
        # in the same way).

    def draw_pokemons(self):
        for p in self.pokemons:
            if p.type_ > 0:
                pygame.draw.circle(screen, Color(0, 0, 255), (int(p.pos[0]), int(p.pos[1])), 10)
            else:
                pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos[0]), int(p.pos[1])), 10)

    # def same_edge(self, p1, p2):
    #     for i in self.get_graph().graph.nodes:
    #         for e in self.get_graph().graph.all_out_edges_of_node(i):
    #             src = self.get_graph().graph.nodes[i]
    #             dest = self.get_graph().graph.nodes[e.get(0)]
    #             m = (src.location(1) - dest.location(1)) / (src.location(0) - dest.location(0))
    #             if p1.pos.y - src.location(1) == m * (p1.pos.x - src.location(0)) and p2.pos.y - src.location(
    #                     1) == m * (p2.pos.x - src.location(0)):
    #                 if p1.type != p2.type:
    #                     return False
    #                 else:
    #                     return True
    #
    #     return False

    def quit(self, mark):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                mark = False
            return mark

    def add_exit_button(self):
        exit_button = Button(0, 0, exit_img, 0.2)
        if exit_button.draw(screen):
            return True

    def add_pasue_button(self):
        pasue_button = Button(100, 0, pause_img, 0.1)
        if pasue_button.draw(screen):
            return True

    def pause(self):
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        pause = False
            screen.fill("White")
            self.message_to_screen("Paused", "Black", -100)
            self.message_to_screen("Press C to continue", "Black", 25)
            pygame.display.update()
            clock.tick(REFRESH)

    def message_to_screen(self, msg, color, y_displace=0):
        text_surf, text_rect = self.text_objects(msg, color)
        text_rect.center = (WIDTH / 2), (HEIGHT / 2) + y_displace
        screen.blit(text_surf, text_rect)

    def text_objects(self, msg, color):
        text_surf = FONT.render(msg, True, color)
        return text_surf, text_surf.get_rect()

    def get_score(self):
        for agent in self.agents:
            score = FONT.render("Agents Score : " + str(agent.value), True, Color("Black"))
            screen.blit(score, (WIDTH - 200, 10))

    def get_time(self, current_time):
        time = FONT.render("Game Time : " + str(current_time), True, Color("Black"))
        screen.blit(time, (WIDTH - 500, 10))
