import random
import networkx as nx
import pickle
import os


def load_pickle(filename):
    """Loads a pickled input file found in the input data folder.

    Args:
        filename (string): filename of pickled input file

    Returns:
        pickle.load(handle) (dict): the un-pickled file
    """
    resource_dir = "data/"
    filepath = os.path.join(resource_dir, filename)
    with open(filepath, 'rb') as handle:
        return pickle.load(handle)


def select_two_random_nodes(G):
    """Selects two random nodes from a graph, but ensures that they are from a different parent room.

    Args:
        G (networkx graph object): graph of building

    Returns:
        node_1 (str): node name of random node
        node_1 (str): node name of random node from a different parent room
    """

    node_1, data = random.sample(list(G.nodes.items()), 1)[0]
    node_1_room = data['parent_room']

    node_2, data_2 = random.sample(list(G.nodes.items()), 1)[0]
    node_2_room = data_2['parent_room']

    while node_2_room == node_1_room:
        node_2, data_2 = random.sample(list(G.nodes.items()), 1)[0]
        node_2_room = data_2['parent_room']

    return node_1, node_2


def find_shortest_path(G, node_1, node_2):
    """Finds the shortest path between two given nodes in a graph. Distance is used as a heuristic, but we have
    set the Euclidean distance between nodes to the edge weight for ease.

    Args:
        G (networkx graph object): graph of building
        node_1 (str): node name of random node
        node_1 (str): node name of random node from a different parent room

    Returns:
        shortest_path (list): list of nodes on shortest path
        shortest_path_length (float): distance travelled along shortest path
    """

    shortest_path = nx.shortest_path(G, source=node_1, target=node_2, weight='weight')
    shortest_path_length = nx.shortest_path_length(G, source=node_1, target=node_2, weight='weight')

    return shortest_path, shortest_path_length
