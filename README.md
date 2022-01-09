# Ex4---Pokemon
### The goal of this project
The goal of this project is to score the most points in the least amount of moves in a specified time.
We get a client. This client has the information about the game such as the agents, represented a json formatted string, the pokemons, also represented a json formatted string and a graph which is represented the same. We also get game info such as the amount of agents, amount of moves overtime and so on.
Using this data we need to catch as many pokemons as possible with our agents. To do so we need to find the best next node for the agent to go to, then call choose_next_edge function given in the client with the best next node we found and finally call move function which activates all  choose_next_edge calls.
But how do we find the best node to go to? This is done in the Algo class

## The classes

**Agent** - This class represents an agent. It has the default parameters given from the client like id, value and so on. 

**Pokemon** - This class represents a pokemon. it has the default parameters given from the client like value, type and so on. Some additional parameters are src and dest which will determine the source node and the destination node of the edge the pokemon is on.

**Algo** - This class implements the algorithm used to find the best route to each pokemon. the algorithm uses previous graph implementation as described in Ex3. You can find the project here: [Ex3](https://github.com/EranK123/Ex3).
Now we can use any algorithms used in this project to help us find the best route to a certain pokemon. 
Given a client we construct  a graph, agents and pokemons to work on. The class will have parameters to help us evaluate the best pokemon for an agent to go to. This paramters include the agents list of nodes allocated to him, represented as a dict. The pokemons allocated to him, a dictionary of counters that represents how many nodes the agent has passed and a dictionary of the size pf each path for each agent. The algorithm iterates over all the pokemons. It will check if the pokemon is not already in the agent's list. The algorithm will find where the pokemon is located using distances from the pokemon to the source node and dest node of the edge he is on. Then using the GraphAlgo class we can use shortest_path algorithm to find the shortest path of the agent to the pokemon plus the weight of the path. We then extract the minimun path and add it to the agent's list of nodes. We also add the pokemon assiciated with the path. Also update the length of the path. In the go_to method we take the list we just found from the main algorithm and remove the first node. Then add it to clint's choose_next_edge method. This will determine how the agent will move. We delete the pokemon if we reached it.



**GUI** - This class draws the graph, agents and pokemons and visualizes  the process of agents catching pokemons. This class gets a client as it’s parameter and with the client's data gets all the parameters we need to construct the gui. The gui repeats it’s drawing process until the client is not running anymore. This process includes drawing the agents, pokemons, edges and nodes. Each iteration we get new data about pokemons and the client so the gui will always updates the drawing.
Some added features about the gui are the Exit button and Pause button. Both are using the button class to construct a button. As the name suggests, these buttons pause the game or exit the game. In addition there is a timer on the screen to measure the running time of each stage, the agents score and amount of moves.

**GameRun** - This class is resonsible of running the whole program. It sets a client and while the client is still running it calss the GUI class to generate the gui and visualzie the case.

### Running the project

To run the program the user first needs to download the project from the github page including the jar file. Then he needs open the terminal and  be in the same directory as the client class. Then type the following command: *java -jar Ex4_Server_v0.0.jar (case number)*. Where the case number ranges from 0 to 15. Press enter and then run the GameRun class to initiate the gui and the algorithm.
You can also download from the release section. Simply download the release zip and follow the above steps

### UMl Diagram


![ZLPHRzms37xthz1Z3d61hOy7P6YxOK60OWYs3diO1a6nT3ubikLAykMkm_xxI4gsP3i9UYydaI95ylj8-OCFmeMnCrKLT32A_Mo4zygpTt75Vj6YTQAh6jhzPgLYwXnKBr5rwyHm_BUwPfphNWVEhxmoXvffMJDZ6n6qxNUWzYhyfNHx34d_J1lGWEABQ9CqY3QA-6GR5UVwKd_RLVzLAOZFIJi7Wb515AiWpZMxrAmqJ07F](https://user-images.githubusercontent.com/93202645/148696293-efa986e9-8089-489a-be1c-13c3a201b557.png)






### Screen Recordings

**Case 4 Recording:**

https://user-images.githubusercontent.com/93202645/148656554-62dfac0b-2db0-48f7-a495-60293e79f352.mov

**Case 10 Recording:**


https://user-images.githubusercontent.com/93202645/148656812-7cd93034-6beb-497f-88b1-5d16a913bab2.mov






