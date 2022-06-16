import random
import networkx as nx
import pickle
import os
import numpy as np


def load_pickle(filename):
    resource_dir = "data/"
    filepath = os.path.join(resource_dir, filename)
    with open(filepath, 'rb') as handle:
        return pickle.load(handle)


def _get_room_list(G):

    room_list = []
    for node, data in G.nodes(data=True):
        parent_room = data['parent_room']
        if parent_room not in room_list and parent_room != 'corridor':
            room_list.append(parent_room)

    return room_list


def _get_node_for_room(G, room_name):
    room_nodes = {node: data for node, data in G.nodes(data=True) if data['parent_room'] == room_name}
    room_node_list = list(room_nodes.keys())
    room_node_degrees = [G.degree(node) for node in room_node_list]
    min_index = np.argmin(room_node_degrees)

    return room_node_list[min_index]


def create_distance_matrix(G):

    room_list = _get_room_list(G)
    distance_matrix = np.empty([len(room_list), len(room_list)])
    for i, room_name_1 in enumerate(room_list):
        node_1 = _get_node_for_room(G, room_name_1)
        for j, room_name_2 in enumerate(room_list):
            node_2 = _get_node_for_room(G, room_name_2)
            distance_matrix[i][j] = shortest_path_length = nx.shortest_path_length(G, source=node_1, target=node_2, weight='weight')

    return distance_matrix, room_list


def create_mapping(room_list):

    assert len(room_list) <= 26, "Too many rooms for a simple mapping"

    map_dict = {}
    for idx, room in enumerate(room_list):
        start = ord('a')
        room_label = chr(start + idx)
        map_dict[room_label] = room

    return map_dict


def reverse_room_mapping(individual, map_dict):

    return [map_dict[letter] for letter in individual]



