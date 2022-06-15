import networkx as nx


def _convert_segment_to_tuples(segment):
    p1, p2 = segment.point(0), segment.point(1)
    coordinate_tuple_1 = (round(float(p1.x()), 3), round(float(p1.y()), 3))
    coordinate_tuple_2 = (round(float(p2.x()), 3), round(float(p2.y()), 3))

    return coordinate_tuple_1, coordinate_tuple_2


def _create_network_nodes(room_name, segment_list):
    """Get nodes with no repeats"""
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
    """Create edges from segments"""
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
    """Create graph for single room from segment dict."""
    room_node_coord_dict, room_node_label_dict = _create_network_nodes(room_name, segment_list)
    edge_list = _create_network_edges(segment_list, room_node_label_dict)

    parent_room_attrs = {node: {'parent_room': room_name} for node in room_node_coord_dict.keys()}
    map_room_attrs = {node: {'room': 'placeholder_room'} for node in room_node_coord_dict.keys()}
    node_tag_attrs = {node: {'node_tag': 'placeholder_node_tag'} for node in room_node_coord_dict.keys()}
    coords_attrs = {node: {'coords': coordinate_tuple} for node, coordinate_tuple in room_node_coord_dict.items()}
    category_attrs = {node: {'category': 'placeholder_category'} for node in room_node_coord_dict.keys()}
    active_attrs = {node: {'active': 'active'} for node in room_node_coord_dict.keys()}

    G = nx.Graph()

    for idx, edge in enumerate(edge_list):
        G.add_edge(edge[0], edge[1], weight=1)

    nx.set_node_attributes(G, parent_room_attrs)
    nx.set_node_attributes(G, map_room_attrs)
    nx.set_node_attributes(G, node_tag_attrs)
    nx.set_node_attributes(G, coords_attrs)
    nx.set_node_attributes(G, category_attrs)
    nx.set_node_attributes(G, active_attrs)

    return G


def _create_room_network_list(updated_room_segment_dict):
    """Create graph of whole clinic. Lets create the whole clinic graph (with connecting lines) and then simplify"""
    clinic_graph_list = []
    for room_name, segment_list in updated_room_segment_dict.items():
        G = _create_single_room_network(room_name, segment_list)
        clinic_graph_list.append(G)

    return clinic_graph_list


def _find_connecting_nodes(connecting_segment_dict):
    """Create connecting node dict"""
    connecting_node_dict = {}
    for room_name, segment_list in connecting_segment_dict.items():
        coordinate_tuple_1, coordinate_tuple_2 = _convert_segment_to_tuples(segment_list[0])
        connecting_node_dict[room_name] = [coordinate_tuple_1, coordinate_tuple_2]

    return connecting_node_dict


def create_building_network(updated_room_segment_dict, connecting_segment_dict):
    """Merge clinic graph, add edges from connecting dict. Weird type issue, so converting to strings here."""
    clinic_graph_list = _create_room_network_list(updated_room_segment_dict)
    G = nx.compose_all(clinic_graph_list)
    connecting_node_dict = _find_connecting_nodes(connecting_segment_dict)

    for room_name, node_list in connecting_node_dict.items():
        node_1_coords, node_2_coords = node_list[0], node_list[1]
        connecting_node_1 = [node_key for node_key, data in G.nodes(data=True) if data['coords'] == node_1_coords][0]
        connecting_node_2 = [node_key for node_key, data in G.nodes(data=True) if data['coords'] == node_2_coords][0]
        G.add_edge(connecting_node_1, connecting_node_2, weight=1)

    return G