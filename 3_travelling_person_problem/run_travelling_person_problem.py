from ga_mappings import load_pickle, create_distance_matrix


def main():
    building_G = load_pickle('final_building_network.pickle')

    distance_matrix, room_list = create_distance_matrix(building_G)




if __name__ == "__main__":
    main()