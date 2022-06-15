import random
import networkx as nx

def select_two_random_nodes(G):

    node_1, data = random.sample(list(G.nodes.items()), 1)[0]
    node_1_room = data['parent_room']

    node_2, data_2 = random.sample(list(G.nodes.items()), 1)[0]
    node_2_room = data_2['parent_room']

    while node_2_room == node_1_room:
        node_2, data_2 = random.sample(list(G.nodes.items()), 1)[0]
        node_2_room = data_2['parent_room']

    return node_1, node_2


def find_shortest_path_3d(G, node_1, node_2):

    return nx.shortest_path(G, source=node_1, target=node_2, weight='weight')
