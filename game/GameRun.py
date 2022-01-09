import sys
from GUI import GUI
from client import Client
from Algo import Algo
import subprocess

# This class is responsible on running the client and the gui. Basically the whole program.
# It sets the client, num of agents and the gui and while the client is running, the gui is drawing
if __name__ == "__main__":
    PORT = 6666
    HOST = '127.0.0.1'
    client = Client()
    algo = Algo(client)
    gui = GUI(client)
    client.start_connection(HOST, PORT)
    num_of_agents = algo.get_info()[0]
    for i in range(num_of_agents):
        client.add_agent("{\"id\":" + str(i) + "}")
    client.start()
    while client.is_running():
        gui.draw()
