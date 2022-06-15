import pickle
import os
import skgeom as sg
import numpy as np

from visualisation import _plot_building_skeletons, _plot_building_line_segments


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


def _create_single_room_skeletons(room_polygon):
    """Function to create a straight skeleton of a single room from its polygon. Requires a bit of wrangling to convert
    between polygon types, ensure which rings are selected, etc. More information on straight skeletons can be found
    here: https://en.wikipedia.org/wiki/Straight_skeleton.

    Args:
        room_polygon (Shapely polygon): a Shapely polygon constructed from the room coordinates

    Returns:
        sg.skeleton.create_interior_straight_skeleton(final_poly) (skgeom skeleton object): the straight skeleton
    """

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


def _create_clinic_skeletons(polygon_dict):
    """Creates a straight skeleton for each room polygon, and stores them in a dictionary.

    Args:
        polygon_dict (dict): dictionary of all polygons for rooms in building

    Returns:
        dict (str: skgeom straight skeleton object): dictionary containing all straight skeletons for building
    """

    return {room_name: _create_single_room_skeletons(polygon) for room_name, polygon in polygon_dict.items()}


def _create_skeleton_line_dict(skeleton_dict):
    """Converts every straight skeleton object for each room into a manageable set of line segments.

    Args:
        skeleton_dict (dict): dictionary of all straight skeletons for each room in the building

    Returns:
        room_segment_dict (str: list): dictionary of line segments for each room
    """

    room_segment_dict = {}
    for room_name, skeleton in skeleton_dict.items():
        room_segments = []
        for h in skeleton.halfedges:
            if h.is_bisector:
                p1 = h.vertex.point
                p2 = h.opposite.vertex.point
                segment = sg.Segment2(p1, p2)
                room_segments.append(segment)

        room_segments = room_segments[1::2]
        room_segment_dict[room_name] = room_segments

    return room_segment_dict


def _create_intersection_segment(doorway_coords):
    """Creates perpendicular intersection segment, by projecting a line through a vector orthogonal to the doorway.
    This will be used to find the intersection points with the straight skeletons. We will project along this line in
    the positive and negative directions respectively.

    Args:
        doorway_coords (tuple): coordinates of a doorway (we will create intersection segments at 90 degrees to this)

    Returns:
        intersection_segment (skgeom line segment): intersection line segment
        skgeom_doorway_midpoint (skgeom point): midpoint of doorway
    """

    doorway_p1 = sg.Point2(doorway_coords[0][0], doorway_coords[0][1])
    doorway_p2 = sg.Point2(doorway_coords[1][0], doorway_coords[1][1])

    doorway_midpoint = 0.5 * (doorway_coords[0][0] + doorway_coords[1][0]), 0.5 * (doorway_coords[0][1] + doorway_coords[1][1])
    skgeom_doorway_midpoint = sg.Point2(doorway_midpoint[0], doorway_midpoint[1])

    # Create perpendicular ray through midpoint

    intersection_vector_half_length = 20
    doorway_vector = sg.Vector2(doorway_p1, doorway_p2)
    perp_doorway_vector_positive = intersection_vector_half_length * doorway_vector.perpendicular(sg.Sign.POSITIVE)
    perp_doorway_vector_negative = intersection_vector_half_length * doorway_vector.perpendicular(sg.Sign.NEGATIVE)

    positive_endpoint = skgeom_doorway_midpoint + perp_doorway_vector_positive
    negative_endpoint = skgeom_doorway_midpoint + perp_doorway_vector_negative

    intersection_segment = sg.Segment2(positive_endpoint, negative_endpoint)

    return intersection_segment, skgeom_doorway_midpoint


def _find_room_intersection_point(room_segment_list, intersection_segment, skgeom_doorway_midpoint):
    """Uses an intersection segment to find the intersection point with a specified room. At the intersection point,
    the room segments are cut, and an updated set of cut segments are created.

    The intersection segment might return multiple intersections with a set of room line segments. All points are
    recorded, and the closest one is selected as the connecting point. This cut point defines two new cut room segments
    and one end of an intersection segment. Untouched lines remain untouched. Care is taken to ensure that overlaps
    are not created.

    Args:
        room_segment_list (list): list of line segments for a single room
        intersection_segment (skgeom line segment): an arbitrarily long line segment orthogonal to a doorway
        skgeom_doorway_midpoint (skgeom point object): the midpoint of a doorway

    Returns:
        updated_room_segment_list (list): a new set of cut room segments, cut at the cut point, with no overlaps.
        cut_point (skgeom point object): point at which the intersection segment cuts the room line segment (min distance)
    """

    # Find the intersections between the intersection segment and the room geometry, storing everything

    untouched_room_segments, segments_with_intersections, segment_lengths, intersection_points = [], [], [], []

    for segment in room_segment_list:
        intersection_point = sg.intersection(segment, intersection_segment)
        if intersection_point:
            possible_intersection_segment = sg.Segment2(skgeom_doorway_midpoint, intersection_point)
            possible_intersection_length_squared = possible_intersection_segment.squared_length()
            segments_with_intersections.append(segment)
            segment_lengths.append(possible_intersection_length_squared)
            intersection_points.append(intersection_point)

        else:
            untouched_room_segments.append(segment)

    # Find the intersection segment with the smallest length squared. This is the point to cut at.
    cut_segments = []
    index_min = np.argmin(segment_lengths)
    for idx, segment in enumerate(segments_with_intersections):
        if idx == index_min:
            cut_point = intersection_points[idx]
            sub_segment_1 = sg.Segment2(segment.point(0), cut_point)
            sub_segment_2 = sg.Segment2(segment.point(1), cut_point)

            cut_segments.append(sub_segment_1)
            cut_segments.append(sub_segment_2)

        else:
            untouched_room_segments.append(segment)

    # Finally create the new room segment list
    updated_room_segment_list = untouched_room_segments + cut_segments

    return updated_room_segment_list, cut_point


def _find_doorway_intersections(room_segment_dict, doorway_dict, doorway_info_dict):
    """Runs the intersection process for each doorway, connecting the two rooms either side of each one. Creates the
    connecting segments, and stores these.

    Args:
        room_segment_dict (dict): dictionary of line segments for each room
        doorway_dict (dict): contains doorway coordinates (two points per doorway)
        doorway_info_dict (dict): contains doorway metadata, including the parent and connecting rooms for each doorway

    Returns:
        room_segment_dict (dict): updated room segment lists in a dictionary
        connecting_segment_dict (dict): dictionary of intersection segments trimmed on both sides at two cut points
    """

    connecting_segment_dict = {}
    for room_name, doorway_coords in doorway_dict.items():
        room_segment_list = room_segment_dict[room_name]
        intersection_segment, skgeom_doorway_midpoint = _create_intersection_segment(doorway_coords)

        # Find intersection with parent room
        updated_room_segment_list, doorway_connection_1 = _find_room_intersection_point(room_segment_list,
                                                                                       intersection_segment,
                                                                                       skgeom_doorway_midpoint)

        # Find intersections with other connecting room
        other_connecting_room = doorway_info_dict[room_name]
        connecting_room_segment_list = room_segment_dict[other_connecting_room]
        updated_connecting_room_segment_list, doorway_connection_2 = _find_room_intersection_point(connecting_room_segment_list,
                                                                                                  intersection_segment,
                                                                                                  skgeom_doorway_midpoint)

        # Create the connecting segment and store in a dict (so we can relate to the doorway info if required)
        connecting_segment = sg.Segment2(doorway_connection_1, doorway_connection_2)
        connecting_segment_dict[room_name] = [connecting_segment]

        # Update the segment lists
        room_segment_dict[room_name] = updated_room_segment_list
        room_segment_dict[other_connecting_room] = updated_connecting_room_segment_list

    return room_segment_dict, connecting_segment_dict


def create_line_segments_from_polygons(polygon_dict, doorway_location_dict, doorway_connection_dict, plot_bool):
    """Function that runs the whole geometry processing routine, and controls plotting/visualisations.

    Args:
        polygon_dict (dict): dictionary containing room polygons
        doorway_location_dict (dict): dictionary containing coordinate information of doorways
        doorway_connection_dict (dict): dictionary containing metadata about each doorway
        plot_bool (bool): if True, plots a visualisation of line segments

    Returns:
        room_segment_dict (dict): updated room segment lists in a dictionary
        connecting_segment_dict (dict): dictionary of intersection segments trimmed on both sides at two cut points
    """

    skeleton_dict = _create_clinic_skeletons(polygon_dict)
    if plot_bool:
        _plot_building_skeletons(polygon_dict, skeleton_dict, doorway_location_dict)

    room_segment_dict = _create_skeleton_line_dict(skeleton_dict)
    updated_room_segment_dict, connecting_segment_dict = _find_doorway_intersections(room_segment_dict,
                                                                                     doorway_location_dict,
                                                                                     doorway_connection_dict)

    if plot_bool:
        _plot_building_line_segments(updated_room_segment_dict,
                                     connecting_segment_dict,
                                     polygon_dict,
                                     doorway_location_dict)

    return updated_room_segment_dict, connecting_segment_dict
