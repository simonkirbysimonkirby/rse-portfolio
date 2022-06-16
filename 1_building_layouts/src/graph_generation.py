import networkx as nx


def _convert_segment_to_tuples(segment):
    """Converts a line segment to a pair of coordinate tuples, with some rounding.

    Args:
        segment (line segment object): line segment defined by two points

    Returns:
        coordinate_tuple_1 (tuple): x, y coordinate tuple pair
        coordinate_tuple_2 (tuple): x, y coordinate tuple pair
    """

    p1, p2 = segment.point(0), segment.point(1)
    coordinate_tuple_1 = (round(float(p1.x()), 3), round(float(p1.y()), 3))
    coordinate_tuple_2 = (round(float(p2.x()), 3), round(float(p2.y()), 3))

    return coordinate_tuple_1, coordinate_tuple_2


def _create_network_nodes(room_name, segment_list):
    """Creates a set of nodes, keeping track of the counts, for a single room line segment list. Checks for no repeat
    nodes.

    Args:
        room_name (str): room name
        segment_list (list): contains line segments for the room_name

    Returns:
        room_node_coord_dict (dict): dictionary of node coordinates
        room_node_label_dict (dict): dictionary containing node labels
    """

    room_node_coord_dict, room_node_label_dict = {}, {}
    node_count = 0

    for segment in segment_list:
        coordinate_tuple_1, coordinate_tuple_2 = _convert_segment_to_tuples(segment)
        for coordinate_tuple in [coordinate_tuple_1, coordinate_tuple_2]:
            if coordinate_tuple not in list(room_node_coord_dict.values()):
                node_label = f"{room_name} n{node_count + 1}"
                room_node_coord_dict[node_label] = coordinate_tuple
                room_node_label_dict[coordinate_tuple] = node_label
                node_count += 1

    return room_node_coord_dict, room_node_label_dict


def _create_network_edges(segment_list, room_node_label_dict):
    """Creates network edges from a segment list.

    Args:
        segment_list (list): contains line segments for the room_name
        room_node_label_dict: (dict) dictionary containing node labels

    Returns:
        edge_list (list): list of edges, defined by tuple of two nodes (i.e. e = (u, v))
    """

    edge_list = []
    for segment in segment_list:
        coordinate_tuple_1, coordinate_tuple_2 = _convert_segment_to_tuples(segment)
        node_1, node_2 = room_node_label_dict[coordinate_tuple_1], room_node_label_dict[coordinate_tuple_2]
        if node_1 == node_2:  # Never create a self loop
            continue
        else:
            edge = (node_1, node_2)
            edge_list.append(edge)

    return edge_list


def _create_single_room_network(room_name, segment_list):
    """Creates a single room network of nodes and edges based on a list of line segments for that room. Some attributes
    are set, and not used in this portfolio project. However, we will use the coordinates, node tag, and parent room
    attributes later.

    Args:
        room_name (str): name of room
        segment_list (list): contains line segments for the room_name

    Returns:
        G (networkx graph object): graph object for single room
    """

    room_node_coord_dict, room_node_label_dict = _create_network_nodes(room_name, segment_list)
    edge_list = _create_network_edges(segment_list, room_node_label_dict)

    parent_room_attrs = {node: {'parent_room': room_name} for node in room_node_coord_dict.keys()}
    map_room_attrs = {node: {'room': 'placeholder_room'} for node in room_node_coord_dict.keys()}
    node_tag_attrs = {node: {'node_tag': 'placeholder_node_tag'} for node in room_node_coord_dict.keys()}
    coords_attrs = {node: {'coords': coordinate_tuple} for node, coordinate_tuple in room_node_coord_dict.items()}

    G = nx.Graph()

    for idx, edge in enumerate(edge_list):
        G.add_edge(edge[0], edge[1], weight=1)

    nx.set_node_attributes(G, parent_room_attrs)
    nx.set_node_attributes(G, map_room_attrs)
    nx.set_node_attributes(G, node_tag_attrs)
    nx.set_node_attributes(G, coords_attrs)

    return G


def _create_room_network_list(updated_room_segment_dict):
    """Creates a list of networkx graphs for each room in the building, based on the new, cut segments for each room

    Args:
        updated_room_segment_dict (dict): contains updated room segments for each room

    Returns:
        clinic_graph_list (networkx graph object): list of graphs for each room
    """

    clinic_graph_list = []
    for room_name, segment_list in updated_room_segment_dict.items():
        G = _create_single_room_network(room_name, segment_list)
        clinic_graph_list.append(G)

    return clinic_graph_list


def _find_connecting_nodes(connecting_segment_dict):
    """Creates a dictionary containing the coordinates of the connecting segments.

    Args:
        connecting_segment_dict (dict): contains the connecting line segments used to cut the straight skeletons

    Returns:
        connecting_node_dict (dict): dictionary containing the coordinates of the connecting segments
    """
    connecting_node_dict = {}
    for room_name, segment_list in connecting_segment_dict.items():
        coordinate_tuple_1, coordinate_tuple_2 = _convert_segment_to_tuples(segment_list[0])
        connecting_node_dict[room_name] = [coordinate_tuple_1, coordinate_tuple_2]

    return connecting_node_dict


def create_building_network(updated_room_segment_dict, connecting_segment_dict):
    """Completes the building network by merging each sub-graph for each room together, and then adding edges between
    the connecting node pairs. A complex, but fully connected network is returned.

    Args:
        updated_room_segment_dict (dict): contains updated/cut room segments
        connecting_segment_dict (dict): contains the connecting line segments used to cut the straight skeletons

    Returns:
        G (networkx graph object): fully connecting graph of building
    """

    clinic_graph_list = _create_room_network_list(updated_room_segment_dict)
    G = nx.compose_all(clinic_graph_list)
    connecting_node_dict = _find_connecting_nodes(connecting_segment_dict)

    for room_name, node_list in connecting_node_dict.items():
        node_1_coords, node_2_coords = node_list[0], node_list[1]
        connecting_node_1 = [node_key for node_key, data in G.nodes(data=True) if data['coords'] == node_1_coords][0]
        connecting_node_2 = [node_key for node_key, data in G.nodes(data=True) if data['coords'] == node_2_coords][0]
        G.add_edge(connecting_node_1, connecting_node_2, weight=1)

    return G
