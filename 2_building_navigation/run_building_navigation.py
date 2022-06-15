from navigation import load_pickle, select_two_random_nodes, find_shortest_path

from navigation_visualisation import visualise_shortest_path


def main():
    # Load data: building graph and building polygons
    building_G = load_pickle('final_building_network.pickle')
    polygon_dict = load_pickle('room_polygons.pickle')

    # Select two nodes at random, from different rooms
    node_1, node_2 = select_two_random_nodes(building_G)

    # Find shortest path between them (using networkx) and visualise this
    shortest_path, shortest_path_length = find_shortest_path(building_G, node_1, node_2)
    visualise_shortest_path(building_G, polygon_dict, shortest_path, shortest_path_length)


if __name__ == "__main__":
    main()
