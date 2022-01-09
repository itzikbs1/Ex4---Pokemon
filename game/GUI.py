import sys
from types import SimpleNamespace
from client import Client
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
REFRESH = 20
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)
RADIUS = 15
exit_img = pygame.image.load("../Images/Exit.png").convert_alpha()
pause_img = pygame.image.load("../Images/pause.png").convert_alpha()
background = pygame.image.load("../Images/5183000.jpg")


# This class is the gui class. It will draw the graph, agents and pokemons accoordingly to client's info.

class GUI:

    def __init__(self, client: Client):
        self.client = client
        self.screen = screen
        self.pokemons = []
        self.agents = []
        self.graph = GraphAlgo()
        self.algo = Algo(client)

    def draw(self):
        """
        This function draws the graph, agents and pokemons at any given time. It's running while the Exit button is
        not pressed.
        """
        pygame.init()
        start_time = Time.time()  # get the start time so we start to measure it and display it to the screen
        self.graph = self.algo.get_graph()  # get the graph from the client
        self.agents = self.algo.get_agents_list()  # get initial agents list from client
        self.scale_agents()
        self.algo.graphAlgo = self.graph
        pygame.display.set_caption("Pokemon Game")
        running = True
        while running:
            self.agents = self.algo.get_agents_list()  # get updated agents list
            self.scale_agents()
            self.pokemons = self.algo.get_pokemon_list()  # get pokemons list from client
            self.algo.choose_agent()  # apply the algorithm
            self.scale_pokemons()
            pygame.display.update()
            clock.tick(REFRESH)
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))  # apply backround image
            elapsed_time = Time.time() - start_time  # get elapsed time
            if self.add_exit_button():
                running = False
                pygame.quit()
            if self.add_pasue_button():
                self.pause()
                start_time = Time.time() - elapsed_time
            # self.get_time(int(elapsed_time))  # display the time
            self.get_time()  # display the time
            self.get_score()  # display the score
            self.get_moves()  # display the moves
            self.draw_nodes()
            self.draw_edges()
            self.draw_agents()
            self.draw_pokemons()
            pygame.display.update()
            clock.tick(REFRESH)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

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

    def my_scale(self, data, x=False, y=False):
        """
        Scales the given object position to screen position
        """
        min_x, min_y, max_x, max_y = self.get_min_max()
        if x:
            return self.scale(data, 50, screen.get_width() - 50, min_x, max_x)
        if y:
            return self.scale(data, 50, screen.get_height() - 50, min_y, max_y)

    def draw_nodes(self):
        """
        This function draws the nodes
        """
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
        """
        This function draws the nodes
        """
        for i in self.graph.graph.nodes:
            for e in self.graph.graph.all_out_edges_of_node(i).keys():
                # find the edge nodes
                src = next(n for n in self.graph.graph.nodes.values() if n.id == i)
                dest = next(n for n in self.graph.graph.nodes.values() if n.id == e)

                # scaled positions
                src_x = self.my_scale(src.location[0], x=True)
                src_y = self.my_scale(src.location[1], y=True)
                dest_x = self.my_scale(dest.location[0], x=True)
                dest_y = self.my_scale(dest.location[1], y=True)

                # draw the line
                pygame.draw.line(screen, Color(61, 72, 126),
                                 (src_x, src_y), (dest_x, dest_y))

    def scale_agents(self):
        """
        This function iterates over each agent and scales it to screen position scale
        """
        for a in self.agents:
            x = a.pos[0]
            y = a.pos[1]
            a.pos = (self.my_scale(x, x=True), self.my_scale(y, y=True), 0)

    def scale_pokemons(self):
        """
        This function iterates over each pokemon and scales it to screen position scale
        """
        for a in self.pokemons:
            x = a.pos[0]
            y = a.pos[1]
            a.pos = (self.my_scale(x, x=True), self.my_scale(y, y=True), 0)

    def draw_agents(self):
        """
        This function draws the agents as circles
        """
        for agent in self.agents:
            t = (int(agent.pos[0]), int(agent.pos[1]))
            pygame.draw.circle(screen, Color(250, 10, 23),
                               t, 10)

    def draw_pokemons(self):
        """
        This function draws the pokemons as circles. If the pokemons type is 1 it will draw them is one color,
        else the other color.
        """
        for p in self.pokemons:
            if p.type_ == 1:
                pygame.draw.circle(screen, Color(0, 0, 255), (int(p.pos[0]), int(p.pos[1])), 10)
            else:
                pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos[0]), int(p.pos[1])), 10)

    def add_exit_button(self):
        """
        This function makes an exit button
        :return: True if pressed
        """
        exit_button = Button(0, 0, exit_img, 0.2)
        if exit_button.draw(screen):
            return True

    def add_pasue_button(self):
        """
        This function makes a pause button
        :return: True if pressed
        """
        pasue_button = Button(100, 0, pause_img, 0.1)
        if pasue_button.draw(screen):
            return True

    def pause(self):
        """
        Pauses the game and displays writing on it.
        """
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
        """
        This function displays a message on the screen
        :param msg: the message
        :param color: message color
        :param y_displace: location
        :return:
        """
        text_surf, text_rect = self.text_objects(msg, color)
        text_rect.center = (WIDTH / 2), (HEIGHT / 2) + y_displace
        screen.blit(text_surf, text_rect)

    def text_objects(self, msg, color):
        """
        This function gets the object in rectangular way and returns it
        :param msg:
        :param color:
        :return:
        """
        text_surf = FONT.render(msg, True, color)
        return text_surf, text_surf.get_rect()

    def get_score(self):
        """
        This function gets the score from the agent, displays and updates it.
        :return:
        """
        for agent in self.agents:
            score = FONT.render("Agents Score : " + str(agent.value), True, Color("Black"))
            screen.blit(score, (WIDTH - 300, 10))

    def get_time(self):
        """
        Gets the current time and displays it on screen
        """
        time = FONT.render("Game Time : " + str(self.client.time_to_end()), True, Color("Black"))
        screen.blit(time, (WIDTH - 500, 10))

    def get_moves(self):
        """
        Gets the moves from the client and updates on screen
        """
        moves = FONT.render("Moves Counter :" + str(self.algo.get_info()[1]), True, Color("Black"))
        screen.blit(moves, (WIDTH - 750, 10))
