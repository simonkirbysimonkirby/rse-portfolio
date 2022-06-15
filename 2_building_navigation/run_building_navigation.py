from navigation import load_pickle, select_two_random_nodes, find_shortest_path

from navigation_visualisation import visualise_shortest_path


def main():
    building_G = load_pickle('final_building_network.pickle')
    polygon_dict = load_pickle('room_polygons.pickle')

    node_1, node_2 = select_two_random_nodes(building_G)
    shortest_path, shortest_path_length = find_shortest_path(building_G, node_1, node_2)
    visualise_shortest_path(building_G, polygon_dict, shortest_path, shortest_path_length)


if __name__ == "__main__":
    main()