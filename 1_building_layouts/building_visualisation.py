import matplotlib.pyplot as plt
from descartes import PolygonPatch


def plot_doorways_and_rooms(polygon_dict, doorway_dict):

    polygon_patches, names, centroids = [], [], []

    for room_name, polygon in polygon_dict.items():
        patch = PolygonPatch(polygon.buffer(0), fc='white', linewidth=2)
        polygon_patches.append(patch)
        names.append(room_name)
        centroids.append(list(polygon.centroid.coords)[0])

    fig, ax = plt.subplots()
    fig.set_size_inches(18, 10)

    for idx, room_name in enumerate(names):
        ax.add_patch(polygon_patches[idx])
        centroid = centroids[idx]
        ax.text(centroid[0] - 1, centroid[1], room_name)

    for room_name, coords in doorway_dict.items():
        ax.plot([i[0] for i in coords],
                [i[1] for i in coords],
                linestyle='solid',
                linewidth=4,
                markersize=10,
                c='r')

    ax.autoscale_view()
    ax.axis('equal')
    plt.title("Building layout: rooms and doorways")
    plt.xlabel('x position, m')
    plt.ylabel('y position, m')
    plt.show()


def plot_building_skeletons(polygon_dict, skeleton_dict, doorway_dict):

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 10)

    for room_name, polygon in polygon_dict.items():
        patch = PolygonPatch(polygon.buffer(0), fc='none', linewidth=4, linestyle='solid')
        ax.add_patch(patch)

        skeleton = skeleton_dict[room_name]

        if room_name == 'corridor':
            color_style_string = 'r-'

        else:
            color_style_string = 'blue'

        for h in skeleton.halfedges:
            if h.is_bisector:
                p1 = h.vertex.point
                p2 = h.opposite.vertex.point
                ax.plot([p1.x(), p2.x()], [p1.y(), p2.y()], color_style_string, lw=2)

        if room_name != 'corridor':
            doorway_coords = doorway_dict[room_name]

            ax.plot([i[0] for i in doorway_coords],
                    [i[1] for i in doorway_coords],
                    linestyle='solid',
                    linewidth=8,
                    markersize=12,
                    c='white')

    ax.axis('equal')
    plt.title("Straight skeletons of each room in building")
    plt.show()