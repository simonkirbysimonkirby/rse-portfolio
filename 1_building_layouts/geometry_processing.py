import pickle
import os
import skgeom as sg

from building_visualisation import plot_doorways_and_rooms


def load_pickle(filename):
    resource_dir = "../data/"
    filepath = os.path.join(resource_dir, filename)
    with open(filepath, 'rb') as handle:
        return pickle.load(handle)


def _create_single_room_skeletons(room_polygon):

    # Exterior outline
    exterior_x, exterior_y = room_polygon.exterior.coords.xy
    exterior_coords = list(zip(exterior_x, exterior_y))[:-1]

    # Interior ring
    interior_poly_list = []
    if len(room_polygon.interiors) > 0:
        for interior in room_polygon.interiors:
            interior_x, interior_y = interior.coords.xy
            interior_coords = list(zip(interior_x, interior_y))[:-1]
            interior_poly = sg.Polygon(interior_coords)
            interior_poly_list.append(interior_poly)

    exterior_poly = sg.Polygon(exterior_coords)

    # Create polygon with holes. Here, just one hole.
    if len(interior_poly_list) > 0:
        for interior_poly in interior_poly_list:
            final_poly = sg.PolygonWithHoles(exterior_poly, [interior_poly])
            break

    else:
        final_poly = exterior_poly

    return sg.skeleton.create_interior_straight_skeleton(final_poly)


def create_clinic_skeletons(polygon_dict):

    return {room_name: _create_single_room_skeletons(polygon) for room_name, polygon in polygon_dict.items()}



if __name__ == "__main__":
    polygon_dict = load_pickle("room_polygons.pickle")
    building_doorway_dict = load_pickle("building_doorways.pickle")

    doorway_location_dict = building_doorway_dict['doorway_location_dict']
    doorway_connection_dict = building_doorway_dict['doorway_info_dict']

    plot_doorways_and_rooms(polygon_dict, doorway_location_dict)

    skeleton_dict = create_clinic_skeletons(polygon_dict)



