import pickle
import os


def load_pickle(filename):
    resource_dir = "../data/"
    filepath = os.path.join(resource_dir, filename)
    with open(filepath, 'rb') as handle:
        return pickle.load(handle)


if __name__ == "__main__":
    polygon_dict = load_pickle("room_polygons.pickle")

