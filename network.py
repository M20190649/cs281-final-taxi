import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

class Node():
    def __init__(self, coord, node_id, network):
        """
        Construct a Node object given a tuple of coordinates and id

        Inputs
        ------
        coord: a tuple of (lat, long) coordinate
        node_id: an int specifying an id
        network: parent network
        """
        self.coord = coord
        self.node_id = node_id
        self.starts, self.ends = [], []
        self.network = network

    def __repr__(self):
        x, y = self.coord
        return '<Node {}: ({}, {})>'.format(self.node_id, x, y)


class Street():
    def __init__(self, start_node_id, end_node_id, street_id, twoway, network):
        """
        Construct a Street object from the start_node to the end_node

        Inputs
        ------
        start_node: the starting Node
        end_node: the end Node
        id: int street_id
        twoway: boolean, whether the street is twoway
        network: parent network
        """
        self.street_id = street_id
        self.start = start_node_id
        self.end = end_node_id
        self.twin = None
        self.twoway = twoway
        self.network = network
        if twoway:
            self.exist = 1
        else:
            self.exist = 0.5

    def set_existence(self, p):
        """
        Modify the probability of existence of Street
        """
        if self.twoway:
            raise AttributeError('Twoway streets must exist')
        else:
            self.exist = p

    def add_twin(self, twin_id):
        """
        Add twin_id to twin
        """
        if self.twoway:
            raise AttributeError('Twoway streets do not have twins')
        self.twin = twin_id

    def __repr__(self):
        return '<Street {}: twoway = {}; from {} to {}>'\
                .format(self.street_id, self.twoway,
                    self.network.nodes[self.start],
                    self.network.nodes[self.end])


class Network():
    def __init__(self, coords):
        """
        Construct a Network object given a list of coords

        Inputs
        ------
        coords: a list of coordinates representing Nodes
        """
        self.this_node_id = 0
        self.this_street_id = 0
        self.nodes = []
        self.streets = []

        for coord in coords:
            node = Node(coord, self.this_node_id, self)
            self.nodes.append(node)
            self.this_node_id += 1

    def __add_street_to_node(self, node_id, street_id, ends_street):
        """
        Add a Street object to the Node

        Inputs
        ------
        node_id: the id of the Node for which the street is added to
        street_id: the id of the Street to the added to the Node
        ends_street: boolean, if True, then the Street added leads to the Node,
            otherwise, the Street added initiates from the Node
        """
        if ends_street:
            self.nodes[node_id].ends.append(street_id)
        else:
            self.nodes[node_id].starts.append(street_id)

    def __add_single_street(self, start_node_id, end_node_id, twoway):
        """
        Add a Street object to the Network and related Nodes

        Inputs
        ------
        start_node_id: int, the id of the Node that starts the street
        end_node_id: int, the id of the Node that ends the street
        twoway: boolean, whether the street is a twoway street

        Returns
        ------
        street: Street object constructed
        """

        street_id = self.this_street_id
        street = Street(start_node_id, end_node_id, street_id, twoway, self)
        self.this_street_id += 1
        self.streets.append(street)
        self.__add_street_to_node(start_node_id, street_id, False)
        self.__add_street_to_node(end_node_id, street_id, True)
        return street

    def add_streets_from_nodes(self, node1_id, node2_id, twoway):
        """
        Add two Streets from two nodes

        Inputs
        ------
        node1_id, node2_id : ids for nodes
        twoway: boolean, whether the street connecting the nodes is twoway

        Returns
        -----
        s1, s2: Streets constructed
        """
        s1 = self.__add_single_street(node1_id, node2_id, twoway)
        s2 = self.__add_single_street(node2_id, node1_id, twoway)
        if not twoway:
            s1.add_twin(s2.street_id)
            s2.add_twin(s1.street_id)
        return s1, s2

    def get_node(self, lat, long):
        """
        Takes lat, long coordinates and returns the id of the closest node
        """
        dists = map(lambda node :
                    (node.coord[0] - lat) ** 2 + (node.coord[1] - long) ** 2,
                    self.nodes)
        return np.argmin(dists)

    def plot(self):
        for street in tqdm(self.streets):
            n1 = self.nodes[street.start]
            n2 = self.nodes[street.end]
            x1, y1 = n1.coord
            x2, y2 = n2.coord
            plt.plot([x1, x2], [y1, y2])




