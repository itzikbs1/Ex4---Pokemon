from GUI import GUI
from client import Client
from Algo import Algo

PORT = 6666
HOST = '127.0.0.1'
client = Client()
algo = Algo(client)
client.start_connection(HOST, PORT)
num_of_agents = algo.get_agent_info()
# for i in range(num_of_agents):
#     client.add_agent("{\"id\":" + str(i) + "}")
client.add_agent("{\"id\":0}")
client.add_agent("{\"id\":1}")
client.add_agent("{\"id\":2}")
client.start()
while client.is_running():
    gui = GUI(client)
    gui.draw()
