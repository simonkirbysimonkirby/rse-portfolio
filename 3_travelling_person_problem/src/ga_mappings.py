import random
import networkx as nx
import pickle
import os
import numpy as np


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


def _get_room_list(G):
    """Parses a building network object, and creates a list of rooms (excluding the corridor)

    Args:
        G (networkx graph object): final building network graph object, with data attached (created in
        app 1 in portfolio project)

    Returns:
        room_list (list): list of rooms in building that will be used in travelling person problem
    """

    room_list = []
    for node, data in G.nodes(data=True):
        parent_room = data['parent_room']
        if parent_room not in room_list and parent_room != 'corridor':
            room_list.append(parent_room)

    return room_list


def _get_node_for_room(G, room_name):
    """Selects the lowest degree node for a given room. This node will be the node that is travelled to
    in the travelling person problem. For most rooms this is degree 1, but some rooms are "through" rooms
    and do not have a degree 1 node. If there are multiple nodes of the same degree the first index is
    returned.

    Args:
        G (networkx graph object): final building network graph object, with data attached (created in
        app 1 in portfolio project)
        room_name (str): name of room to select a node for

    Returns:
        room node name (str): minimum node name of given room
    """

    room_nodes = {node: data for node, data in G.nodes(data=True) if data['parent_room'] == room_name}
    room_node_list = list(room_nodes.keys())
    room_node_degrees = [G.degree(node) for node in room_node_list]
    min_index = np.argmin(room_node_degrees)

    return room_node_list[min_index]


def create_distance_matrix(G):
    """Creates a distance matrix between every room in the clinic (given by room_list). This distance is
    calculated using the shortest path algorithm shown in app 2, using nx.shortest_path_length(). Consecutive
    room repeats are not possible, but zeros are entered on the diagonal.

    Args:
        G (networkx graph object): final building network graph object, with data attached (created in
        app 1 in portfolio project)

    Returns:
        distance_matrix (numpy ndarray): array populated between rooms at the i, j indexes in room_list
        room_list (list): list of rooms that can be travelled to in the building
    """

    room_list = _get_room_list(G)
    distance_matrix = np.empty([len(room_list), len(room_list)])
    for i, room_name_1 in enumerate(room_list):
        node_1 = _get_node_for_room(G, room_name_1)
        for j, room_name_2 in enumerate(room_list):
            node_2 = _get_node_for_room(G, room_name_2)
            distance_matrix[i][j] = shortest_path_length = nx.shortest_path_length(G, source=node_1, target=node_2, weight='weight')

    return distance_matrix, room_list


def create_mapping(room_list):
    """So that we can run/test/debug the genetic algorithm with simple alphabetical characters, we need
    to create a mapping dictionary. This dictionary holds a mapping of room name to alphabetical character.
    A simple assertion is made to check whether the number of rooms in the room_list is too great for a 26
    alphabetical character logic (this probably would not break as other non-alphabetical characters exist,
    but has not been tested).

    Args:
        room_list (list): list of rooms that can be travelled to in the building

    Returns:
        map dict (dict): dictionary of room_name: map character for each room in the building
    """

    assert len(room_list) <= 26, "Too many rooms for a simple mapping"

    map_dict = {}
    for idx, room in enumerate(room_list):
        start = ord('a')
        room_label = chr(start + idx)
        map_dict[room_label] = room

    return map_dict


def reverse_room_mapping(individual, map_dict):
    """Simple function to get the room name for a given alphabetical character in the mapping dict

    Args:
        individual (list): a single individual containing a list of alphabetical characters
        map_dict (dict): dictionary of room_name: map character for each room in the building

    Returns:
        list of rooms (list): a list/sequence of rooms that are visited
    """

    return [map_dict[letter] for letter in individual]



