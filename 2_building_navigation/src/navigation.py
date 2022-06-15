import random
import networkx as nx
import pickle
import os


def load_pickle(filename):
    resource_dir = "data/"
    filepath = os.path.join(resource_dir, filename)
    with open(filepath, 'rb') as handle:
        return pickle.load(handle)


def select_two_random_nodes(G):

    node_1, data = random.sample(list(G.nodes.items()), 1)[0]
    node_1_room = data['parent_room']

    node_2, data_2 = random.sample(list(G.nodes.items()), 1)[0]
    node_2_room = data_2['parent_room']

    while node_2_room == node_1_room:
        node_2, data_2 = random.sample(list(G.nodes.items()), 1)[0]
        node_2_room = data_2['parent_room']

    return node_1, node_2


def find_shortest_path(G, node_1, node_2):

    shortest_path = nx.shortest_path(G, source=node_1, target=node_2, weight='weight')
    shortest_path_length = nx.shortest_path_length(G, source=node_1, target=node_2, weight='weight')

    return shortest_path, shortest_path_length
