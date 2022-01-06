from GUI import GUI
from client import Client
from Algo import Algo

PORT = 6666
HOST = '127.0.0.1'

client = Client()
client.start_connection(HOST, PORT)
client.add_agent("{\"id\":0}")
client.start()
while client.is_running():
    gui = GUI(client)
    gui.draw()

