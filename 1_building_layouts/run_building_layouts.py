from geometry_processing import load_pickle, create_line_segments_from_polygons
from visualisation import plot_doorways_and_rooms, plot_clinic_network
from graph_generation import create_building_network
from graph_simplification import run_trim_sequence, final_graph_processing, save_graph


def main():
    # Load data: polygons of rooms, and doorway coordinates/metadata
    polygon_dict = load_pickle("room_polygons.pickle")
    building_doorway_dict = load_pickle("building_doorways.pickle")
    doorway_location_dict = building_doorway_dict['doorway_location_dict']
    doorway_connection_dict = building_doorway_dict['doorway_info_dict']

    # Plot input data: doorways and polygons
    plot_doorways_and_rooms(polygon_dict, doorway_location_dict)

    # Create straight skeletons of room polygons and cut/connect them through doorways
    updated_room_segment_dict, connecting_segment_dict = create_line_segments_from_polygons(polygon_dict, doorway_location_dict, doorway_connection_dict, plot_bool=True)

    # Create network from line segments
    complex_G = create_building_network(updated_room_segment_dict, connecting_segment_dict)
    plot_clinic_network(complex_G, polygon_dict, True, 'output_4_complex')

    # Simplify network using a three-stage routine
    simplified_G = run_trim_sequence(complex_G, polygon_dict, plot_bool=True)

    # Relabel and set final edge weights of graph to Euclidean distances
    final_G = final_graph_processing(simplified_G)

    # Save final simplified and relabelled network
    save_graph(final_G, "output_7_final_building_network.pickle")


if __name__ == "__main__":
    main()
