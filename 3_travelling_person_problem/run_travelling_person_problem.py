from ga_mappings import load_pickle, create_distance_matrix, create_mapping

from genetic_algorithm import create_population, _make_route, _calculate_individual_fitness


def main():
    building_G = load_pickle('final_building_network.pickle')

    distance_matrix, room_list = create_distance_matrix(building_G)
    map_dict = create_mapping(room_list)

    # GA stuff

    route = _make_route(map_dict, 5)

    fitness = _calculate_individual_fitness(route, distance_matrix)

    print(fitness)

    #population = create_population(100, 5, map_dict)
    #print(fitness)


if __name__ == "__main__":
    main()