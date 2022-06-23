import random
import numpy as np

from ga_mappings import load_pickle, create_distance_matrix, create_mapping

from genetic_algorithm import GeneticAlgorithm


def main():
    rseed = 40
    random.seed(rseed)
    np.random.seed(rseed)

    # Load data
    building_G = load_pickle('final_building_network.pickle')
    distance_matrix, room_list = create_distance_matrix(building_G)
    map_dict = create_mapping(room_list)

    # Define problem: how many rooms must be visited?
    route_length = 22
    print(f"The nurse must visit the following rooms once: {room_list[:route_length]}")

    # Random population?
    random_bool = True

    # Set up genetic algorithm parameters and run
    epochs = 2000
    population_size = 200
    elite_number = 25
    mutation_rate = 0.8

    genetic_algorithm = GeneticAlgorithm(route_length,
                                         epochs,
                                         population_size,
                                         elite_number,
                                         mutation_rate,
                                         map_dict)

    genetic_algorithm.run(distance_matrix, route_length, map_dict, random_bool)
    genetic_algorithm.process_outputs(map_dict)


if __name__ == "__main__":
    main()
