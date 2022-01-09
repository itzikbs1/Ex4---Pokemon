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
Given a client we construct  a graph, agents and pokemons to work on.
 The algorithm will iterate over each pokemon. It will first find the edge the pokemon is on. This is done by checking the distance between the pokemon position to an edge source and the same for edge dest.  After we find where the pokemon is located, we call the shortest_path algorithm. This algorithm is using the dijkstra algorithm to find the shortest path from node a to node b and in addition returns the path. We call this method on the agent's current location and the source of the edge the pokemon is located on. Now we have the cost of the path and the actual path saved in a list. Because we calculated the path from agent pos to pokemon src we need to add the weight of the edge to get to pokemon dest. We then add the dest to the list.
Then we make comparisons between each path of each pokemon to find the best one. When we finally find it we add it to the agent list of nodes.
To fill choose_next_edge parameters we get the first node from agent’s list node. Make it as his source node and remove it from the list. We then call this node in choose_next_edge and the agent’s id. This iterates over and over until the client time runs out so we will always have another node to go to.

**GUI** - This class draws the graph, agents and pokemons and visualizes  the process of agents catching pokemons. This class gets a client as it’s parameter and with the client's data gets all the parameters we need to construct the gui. The gui repeats it’s drawing process until the client is not running anymore. This process includes drawing the agents, pokemons, edges and nodes. Each iteration we get new data about pokemons and the client so the gui will always updates the drawing.
Some added features about the gui are the Exit button and Pause button. Both are using the button class to construct a button. As the name suggests, these buttons pause the game or exit the game. In addition there is a timer on the screen to measure the running time of each stage, the agents score and amount of moves.

**GameRun** - This class is resonsible of running the whole program. It sets a client and while the client is still running it calss the GUI class to generate the gui and visualzie the case.

### Running the project

To run the program the user first needs to download the project from the github page including the jar file. Then he needs open the terminal and  be in the same directory as the client class. Then type the following command: *java -jar Ex4_Server_v0.0.jar (case number)*. Where the case number ranges from 0 to 15. Press enter and then run the GameRun class to initiate the gui and the algorithm.

### UMl Diagram








### Screen Recordings

**Case 4 Recording:**

https://user-images.githubusercontent.com/93202645/148656554-62dfac0b-2db0-48f7-a495-60293e79f352.mov

**Case 10 Recording:**


https://user-images.githubusercontent.com/93202645/148656812-7cd93034-6beb-497f-88b1-5d16a913bab2.mov






