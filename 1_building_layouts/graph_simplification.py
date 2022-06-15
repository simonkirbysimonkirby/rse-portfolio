import networkx as nx

from visualisation import plot_clinic_network


def trim_graph(G):
    """Trim nodes on graph (order < 2)"""
    L = G.copy()
    leaves = set()
    for node, degree in L.degree():
        if degree < 2:
            leaves.add(node)
    L.remove_nodes_from(leaves)

    return L, len(leaves)


def euclidean_distance(coord_tuple_1, coord_tuple_2):
    """Euclidean distance between two points"""
    x1, y1 = coord_tuple_1
    x2, y2 = coord_tuple_2
    return round(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5, 4)


def remove_close_order_1_nodes(G, threshold):
    """Check order 1 nodes, and remove them if they are too close to another node"""
    L = G.copy()
    short_distance_leaves = set()
    for node, degree in L.degree():
        node_coord_tuple = L.nodes[node]['coords']
        if degree < 2:
            neighbor_nodes = L.neighbors(node)
            for neighbour in neighbor_nodes:
                neighbour_coord_tuple = L.nodes[neighbour]['coords']
                euc_distance = euclidean_distance(node_coord_tuple, neighbour_coord_tuple)
                if euc_distance < threshold:
                    short_distance_leaves.add(node)

    L.remove_nodes_from(short_distance_leaves)
    number_nodes_removed = len(short_distance_leaves)

    return L, number_nodes_removed


def find_single_close_node_pair(G, distance_threshold):
    """Find a single node pair that is close """
    contract_pair = None
    for node, data in G.nodes(data=True):
        node_coord_tuple = G.nodes[node]['coords']
        neighbor_node_list = list(G.neighbors(node))
        for neighbor_node in neighbor_node_list:
            neighbour_coord_tuple = G.nodes[neighbor_node]['coords']
            euc_distance = euclidean_distance(node_coord_tuple, neighbour_coord_tuple)
            if euc_distance < distance_threshold:
                contract_pair = tuple([node, neighbor_node])

    return contract_pair


def contract_network_nodes(G, node_1, node_2):
    """Function to merge nodes a single time"""
    return nx.contracted_nodes(G, node_1, node_2, self_loops=False)


def remove_contract_attribute(G):
    """Function to delete contraction attributes from the graph"""
    attribute_name = 'contraction'
    for node, data in G.nodes(data=True):
        if attribute_name in data.keys():
            del G.nodes[node][attribute_name]

    return G


def contract_graph(G, threshold):
    """Identify close nodes in the clinic graph, and then contract them, returning a new graph"""
    L = G.copy()
    count = 0
    contract_pair = find_single_close_node_pair(L, threshold)
    while contract_pair is not None:
        node_1, node_2 = contract_pair
        L = contract_network_nodes(L, node_1, node_2)
        count += 1
        contract_pair = find_single_close_node_pair(L, threshold)

    return remove_contract_attribute(L), count


def run_trim_sequence(G, polygon_dict, plot_bool):

    # Stage 1
    trimmed_G, nodes_removed = trim_graph(G)
    print(f"Stage 1 - remove order 1 nodes (with no distance criteria): {nodes_removed} nodes removed")
    if plot_bool:
        plot_clinic_network(trimmed_G, polygon_dict)

    # Stage 2
    number_nodes_removed = 1
    while number_nodes_removed > 0:
        trimmed_G, number_nodes_removed = remove_close_order_1_nodes(trimmed_G, threshold=1.5)
        print(f"Stage 2 - remove order 1 nodes that are close/under threshold distance: {number_nodes_removed} nodes removed")
        if plot_bool:
            plot_clinic_network(trimmed_G, polygon_dict)

    # Stage 3
    contracted_G, number_nodes_contracted = contract_graph(trimmed_G, threshold=0.5)
    print(f"Stage 3 - contract close node pairs in network: {number_nodes_contracted} node pairs contracted")

    if plot_bool:
        plot_clinic_network(contracted_G, polygon_dict)

    return contracted_G


def relabel_graph(G):
    """Relabel graph based on number of nodes in each room, and update node tag attribute"""
    parent_room_dict, mapping_dict, node_tag_dict = {}, {}, {}
    for node, data in G.nodes(data=True):
        parent_room = data['parent_room']
        if parent_room not in parent_room_dict:
            new_count = 1
            parent_room_dict[parent_room] = new_count
        else:
            current_count = parent_room_dict[parent_room]
            new_count = current_count + 1
            parent_room_dict[parent_room] = new_count

        old_label_split = node.split()[:-1]
        node_tag = f"n{new_count}"
        new_label_components = old_label_split + [node_tag]
        new_label = " ".join(new_label_components)
        mapping_dict[node] = new_label
        node_tag_dict[new_label] = {'node_tag': node_tag}

    nx.relabel_nodes(G, mapping_dict, copy=False)
    nx.set_node_attributes(G, node_tag_dict)

    return G