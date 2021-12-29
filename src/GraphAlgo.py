import heapq
import json
import random
import sys
from typing import List

import matplotlib
from matplotlib import pyplot as plt

matplotlib.matplotlib_fname()
from GraphAlgoInterface import GraphAlgoInterface
from Node import Node
from DiGraph import DiGraph
from GraphInterface import GraphInterface
from queue import PriorityQueue


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph: DiGraph = None):
        """
        Initialize the graph with a DiGraph
        :param graph: the graph all the algorithms will run on
        """
        if graph is None:
            graph = DiGraph()
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the DiGraph refers to this class
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:

        """
        This function loads a graph from a json file.
        :param file_name:  The path to the json file
        :return: True if the loading was successful, False o.w.
        """
        try:
            g = DiGraph()
            with open(file_name) as f:
                data = json.load(f)
            # iterate over the Nodes list
            for node in data['Nodes']:
                if len(node) == 1:  # if there is no position to the node we randomize it
                    loc = (random.uniform(0, 100), random.uniform(0, 100), 0)
                    node['pos'] = loc
                    g.add_node(node['id'], node['pos'])  # add the node to the graph
                else:
                    location = tuple(float(s) for s in node['pos'].strip("()").split(","))  # get the location
                    g.add_node(node['id'], location)  # add the node to the graph
            # iterate over the Edges list
            for edge in data['Edges']:
                g.add_edge(edge['src'], edge['dest'], edge['w'])  # add the edge to the graph
            self.graph = g
            return True
        except IOError as e:
            return False

    def save_to_json(self, file_name: str) -> bool:
        """
        This function saves the graph in JSON format to a file
        :param file_name: The path to the out file
        :return: True if the save was successful, False o.w.
        """
        try:
            with open(file_name, 'w') as file:
                dict1 = {"Edges": self.dict_of_edge(), "Nodes": self.dict_of_node()}  # create a dictionary
                # representing the whole graph using the help methods
                g = dict1
                json.dump(g, file, ensure_ascii=False, indent=4)  # turn it into a json
        except IOError as e:
            return False
        return True

    def dict_of_node(self):
        """
        This function creates a Nodes list and appends dictionaries representing the nodes
        :return: The Nodes list
        """
        Nodes = []
        for k, v in self.graph.get_all_v().items():
            node = {}
            temp_location = str(v.location)[1:-1]
            node["pos"] = str(temp_location.replace(' ', ''))
            node["id"] = k
            Nodes.append(node)
        return Nodes

    def dict_of_edge(self):
        """
        This function creates an Edges list and appends dictionaries representing the edges
        :return:
        """
        Edges = []
        for k1 in self.graph.nodes.keys():
            for k2, v in self.graph.all_out_edges_of_node(k1).items():
                edges = {"src": k1, "w": v, "dest": k2}
                Edges.append(edges)
        return Edges

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        This function computes the shortest path from node id1 to node id2
        :param id1: source node's id
        :param id2: destination node's id
        :return: The path as integer list and the weight of the path
        """
        path_list = self.path(id1, id2)
        dist = self.graph.nodes[id2].weight
        if dist == sys.maxsize:
            return float('inf'), path_list
        return dist, path_list

    def dikjstra(self, src: Node):
        """
        The dijkstra algorithm computes the shortest path between a node to every other node in the graph. We set a
        PriorityQueue which contains the weights of the nodes and the nodes themselves. The weight of the node is the
        weight of the edge going in the node plus the path to the node. We iterate over the edges, check if a node
        hasn't been visited yet and compute the path between the current node to it. Then compare to the latest and
        update.
        :param src: the source node
        """
        self.set_tag()  # set all tags i.e parents to -1
        self.set_weight()  # set all the weights to max value
        visited = []  # set a visited list
        pq = PriorityQueue()  # set the pq
        self.graph.nodes[src.id].setWeight(0)  # the weight from the node to itself is 0
        pq.put(PrioritizedItem(src.weight, src))
        while len(
                visited) is not self.graph.nodes_size and pq.qsize() > 0:  # check while we didnt visit each node or removed all the nodes from the queue
            t = pq.get()
            r = t.get_id()
            curr_node = self.graph.nodes[r]  # set the neighbor. At first it is the node src
            if curr_node not in visited:
                visited.append(curr_node)
                self.adj(curr_node, pq, visited)  # check all of it's  neighbors

    def adj(self, node, pq, visited):
        """
        This function computes the path from a node to all of it's neighbors
        :param node: source node
        :param pq: the pq
        :param visited: visited list
        """
        current_dis = -1
        new_dis = -1
        e = self.graph.nodes[node.id].out_edges
        for nd in e:  # iterate over all adjacent nodes
            node_dest = self.graph.nodes[nd]  # neighbor node

            if node_dest not in visited:
                current_dis = self.graph.nodes[node.id].out_edges[nd]
                new_dis = current_dis + node.weight  # calculate new dis

                if new_dis < node_dest.weight:  # if it's lower update it as the new lowest cost path
                    node_dest.setWeight(new_dis)
                    node_dest.setTag(node.id)

                pq.put(PrioritizedItem(node_dest.weight, node_dest))  # add to pq

    def path(self, src: int, dest: int):
        """
        This function computes the shortest path between source node to destination node - as an ordered list of
        nodes. This function will use the shortest_path_dist method to get all the parent nodes to each node that
        computes the shortest path using the tags. It will add the parents to a list and return it.
        :param src: source node's id
        :param dest: destination node's id
        :return:
        """
        path_list = []
        self.shortest_path_dist(src, dest)  # after this is done all the tags are set to the best weight route nodes
        parent = dest
        while parent is not src:  # we go back from dest to src and add each parent to the list
            path_list.append(self.graph.nodes[parent].id)  # add to the path list
            parent = self.graph.nodes[dest].tag  # update the parent
            if parent == -1:
                return []
            dest = self.graph.nodes[parent].id

        path_list.append(self.graph.nodes[src].id)
        path_list.reverse()  # reverse the list
        return path_list

    def shortest_path_dist(self, src: int, dest: int):
        """
        This function computes the weight of the shortest path
        :param src: src node's id
        :param dest: destination node's id
        :return: the wegith of the shortest path
        """
        self.set_tag()
        self.dikjstra(self.graph.nodes[src])
        return self.graph.nodes[dest].weight

    def set_tag(self):
        """
        Sets all the tags of the nodes to -1. The tags represent the parent of the node
        """
        for i in self.graph.nodes:
            self.graph.nodes[i].setTag(-1)

    def set_weight(self):
        """
        Sets all the weights to max value
        """
        for i in self.graph.nodes:
            self.graph.nodes[i].setWeight(sys.maxsize)

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
         check if the cities list contained in the graph
        calculate path using dijkstra from node in the list to another one after im found
         the shortest(weight) removing him from the list and calculate again from
        the end of the path and adding the the new path(weight) to the list
        and the weight to variable min_list_temp
        doing this for all the nodes in the cities list
        if we found better path(lower weight) im changing the list
        :param node_lst: list of nodes we need to visit
        :return: the weight of the path and all the nodes we visited
        """
        current_path = []
        cities_list = []
        min_list = sys.maxsize
        cities_temp_list = []
        min_temp = 0
        for i in range(len(node_lst)):
            break_loop = False
            first_time = False
            cities_temp_list.clear()
            cities_temp = node_lst.copy()
            min_temp = 0
            curr_node_index = i
            location = i
            while len(cities_temp) > 1:
                key = cities_temp[location]
                cities_temp.remove(key)
                self.dikjstra(self.graph.nodes[key])
                min_value = sys.maxsize
                for j in range(len(cities_temp)):
                    if min_value > self.graph.nodes[cities_temp[j]].weight:
                        min_value = self.graph.nodes[cities_temp[j]].weight
                        curr_node_index = cities_temp[j]
                        location = j
                if min_value == sys.maxsize:
                    break_loop = True
                    break
                min_temp += min_value
                current_path = self.shortest_path_tsp(key, curr_node_index)
                if first_time:
                    current_path.pop(0)
                first_time = True
                cities_temp_list.extend(current_path)
            if min_list > min_temp and not break_loop:
                cities_list.clear()
                cities_list = cities_temp_list.copy()
                min_list = min_temp
        return cities_list, min_list

    def shortest_path_tsp(self, src, dest):
        """
        This function computes shortest path from src node to dest node
        :param src: src node's id
        :param dest: destination node's id
        :return: the shortest path
        """
        path_list = []
        parent = dest
        while parent is not src:
            path_list.append(self.graph.nodes[parent].id)
            parent = self.graph.nodes[dest].tag
            dest = self.graph.nodes[parent].id

        path_list.append(self.graph.nodes[src].id)
        path_list.reverse()
        return path_list

    def centerPoint(self) -> (int, float):
        """
        his function finds the NodeData which minimizes the max distance to all the other nodes. The algorithm to
        finding the center is to compute all the minimal distances from each node to any other node using dijkstra.
        Then we will take the maximum distance of all the minimals. The node which refers to this distance is the
        center distance.
        :return: the node's center id and the min-maximum distance
        """
        max_value = sys.maxsize  # set the min max distance to max value
        key = -1
        for i in self.graph.nodes:  # iterate over the all the nodes in the graph
            node = self.graph.nodes[i]
            self.dikjstra(node)  # check all the minimal distances
            temp = self.get_max()  # get the maximum distance out of the minmal
            if temp == sys.maxsize:
                return -1, float('inf')
            if temp < max_value:  # check for the lowest and update it
                max_value = temp
                key = node.id

        return key, max_value

    def get_max(self):
        """
        This function takes the maximum weight from a list of weights representing the distances to each node.
        :return: the max value out of the minimal
        """
        max_value = -sys.maxsize - 1
        for i in self.graph.nodes:
            node_w = self.graph.nodes[i].weight
            if node_w > max_value:
                max_value = node_w
        return max_value

    def plot_graph(self) -> None:
        """
        Draws the graph using matplotlib library.
        """
        for n in self.graph.nodes.values():  # iterate over all the nodes
            if n.location is None:  # if there is no location we randomize it
                x_src = random.uniform(0, 100)
                y_src = random.uniform(0, 100)
                n.set_location(x_src, y_src, 0)
                plt.plot(x_src, y_src, markersize=20, marker='.', color='blue')  # draws the nodes
                plt.text(x_src, y_src, str(n.id), color='red', fontsize=10)  # draws each node id
                plt.xlabel("x")
            else:
                x_src = n.location[0]
                y_src = n.location[1]
                plt.plot(x_src, y_src, color='blue', marker='.', markersize=20)
                plt.text(x_src, y_src, str(n.id), color='red', fontsize=10)
                plt.xlabel("x")
            for k, w in self.graph.all_out_edges_of_node(n.id).items():  # iterate over edges going out
                node_dest = self.graph.nodes[k]
                if node_dest.location is None:
                    x_dest = random.uniform(0, 100)
                    y_dest = random.uniform(0, 100)
                    z_dest = random.uniform(0, 100)
                    node_dest.location = (x_dest, y_dest, z_dest)
                plt.annotate("", xy=(n.location[0], n.location[1]),
                             xytext=(node_dest.location[0], node_dest.location[1]),
                             arrowprops=dict(arrowstyle="<-"))  # drawing the edges

                plt.ylabel("y")
                plt.title("my graph")

        plt.show()

        return


"""
This class represents a object we add to the priority queue in dijkstra
"""


class PrioritizedItem:
    def __init__(self, weight, node):
        self.weight = weight
        self.node = node

    def __lt__(self, other):
        """
        Set the compare function in the priority queue
        :param other: other node's weight
        :return: the smaller weight
        """
        return self.weight < other.weight

    def get_id(self):
        return self.node.id
