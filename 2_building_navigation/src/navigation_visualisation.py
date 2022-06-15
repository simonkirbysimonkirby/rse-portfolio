import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from descartes import PolygonPatch
import networkx as nx

def visualise_shortest_path(G, polygon_dict, shortest_path, shortest_path_length):

    node_1, node_2 = shortest_path[0], shortest_path[-1]

    G_pos = {node_key: data['coords'] for node_key, data in G.nodes(data=True)}

    node_cmap = []
    for node in list(G.nodes()):
        if node == node_1:
            node_cmap.append('lightgreen')
        elif node == node_2:
            node_cmap.append('orangered')
        elif node in shortest_path:
            node_cmap.append('deepskyblue')
        else:
            node_cmap.append('white')

    options = {
        "font_size": 9,
        "node_size": 200,
        "node_color": node_cmap,
        "edgecolors": "black",
        "linewidths": 2,
        "width": 1.5,
        'edge_color': 'black',
    }

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 10)

    for name, polygon in polygon_dict.items():
        patch = PolygonPatch(polygon.buffer(0), fc='none', linewidth=1)
        ax.add_patch(patch)

    nx.draw(G, G_pos, **options, with_labels=False)

    handles, labels = ax.get_legend_handles_labels()
    ax.axis('equal')
    ax.margins(0.15)
    plt.title('Shortest path between two nodes in the building')

    extra_legend_entries = {
        'Start node': 'lightgreen',
        'End node': 'red',
        'Node on shortest path': 'deepskyblue',
        f"Distance travelled: {shortest_path_length:.2f} m": 'white',
    }

    for label, color in extra_legend_entries.items():
        patch = mpatches.Patch(color=color, label=label)
        handles.append(patch)

    plt.legend(handles=handles, frameon=False, ncol=3, labelspacing=1, loc="lower center")
    plt.show()