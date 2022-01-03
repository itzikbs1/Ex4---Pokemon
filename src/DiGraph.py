from GraphInterface import GraphInterface
from Node import Node


class DiGraph(GraphInterface):

    def __init__(self):
        """
        initialize the graph with nodes dictionary, amount of nodes in the graph, amount of edges and mode counter
        """
        self.nodes = {}  # {node's id: the Node object}
        self.nodes_size = 0
        self.edges_size = 0
        self.agents = {}
        self.pokemons = {}
        self.mc = 0

    def v_size(self) -> int:
        """
        :return: the amount of the nodes
        """
        if self.nodes_size < 0:
            raise NotImplementedError
        return self.nodes_size

    def e_size(self) -> int:
        """
        :return: the amount of edges in the graph
        """
        if self.edges_size < 0:
            raise NotImplementedError
        return self.edges_size

    def get_all_v(self) -> dict:
        """
        :return: the nodes of the graph as a dictionary
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        :param id1: the node's id
        :return: the edges going in the node with this id
        """
        return self.nodes.get(id1).in_edges

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        :param id1:  the node's id
        :return: the edges going out of the node with this id
        """
        return self.nodes[id1].out_edges

    def get_mc(self) -> int:
        """
        :return: the mode counter
        """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        This function adds a new edge to the graph
        :param id1: the source node's id
        :param id2: the destination node's id
        :param weight: the edge's weight
        :return: true id successful, false if not
        """
        if self.nodes.get(id1) is None or self.nodes.get(id2) is None:
            return False
        if id1 == id2:
            return False

        self.nodes.get(id1).out_edges[id2] = weight  # add to node's id1 out edges
        self.nodes.get(id2).in_edges[id1] = weight  # add to node's id2 in edges
        self.mc += 1
        self.edges_size += 1
        self.nodes.get(id1).out_edges_size += 1
        self.nodes.get(id2).in_edges_size += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        This function adds a new node to the graph
        :param node_id: the node's id we wish to add
        :param pos: the node's location
        :return: true id successful, false if not
        """
        n = Node(node_id, pos)  # create a new node
        self.nodes[node_id] = n  # add it to nodes dict
        self.mc += 1
        self.nodes_size += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        This function removes a node from the graph and all of the edges referred to the node
        :param node_id: the node id we wish to remove
        :return: true id successful, false if not
        """
        if node_id not in self.nodes:
            return False

        n = self.nodes[node_id]  # get the node
        list_for_remove_out = []  # make a list for removed out edges
        list_for_remove_in = []  # make a list for removed out edges
        for i in n.out_edges:
            list_for_remove_out.append(i)

        for j in list_for_remove_out:
            self.remove_edge(node_id, j)

        for i in n.in_edges:
            list_for_remove_in.append(i)

        for j in list_for_remove_in:
            self.remove_edge(j, node_id)

        del self.nodes[node_id]  # finally remove the node
        self.nodes_size -= 1
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        This function removes an edge from the graph
        :param node_id1: the source node's id
        :param node_id2: the destination node's id
        :return: true id successful, false if not
        """
        if node_id1 not in self.nodes or node_id2 not in self.nodes:
            return False

        if self.nodes.get(node_id1).out_edges[node_id2] is None or self.nodes.get(node_id2).in_edges[node_id1] is None:
            return False

        del self.nodes.get(node_id1).out_edges[node_id2]  # access out edges of the node with the source id and
        # remove it
        del self.nodes.get(node_id2).in_edges[node_id1]  # access in edges of the node with the destination id and
        # remove it
        self.mc += 1
        self.edges_size -= 1
        self.nodes.get(node_id1).out_edges_size -= 1
        self.nodes.get(node_id2).in_edges_size -= 1
        return True

    def __repr__(self):
        return f"Graph: |V| = {self.nodes_size}, |E| = {self.edges_size}"
