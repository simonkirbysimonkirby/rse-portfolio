import random
import numpy as np
import operator

from ga_mappings import load_pickle, create_distance_matrix, create_mapping, reverse_room_mapping

from genetic_algorithm import create_initial_population, calculate_fitness, _create_next_generation

from tsp_visualisation import visualise_fitness


def main():
    rseed = 42
    random.seed(rseed)
    np.random.seed(rseed)

    building_G = load_pickle('final_building_network.pickle')
    distance_matrix, room_list = create_distance_matrix(building_G)
    map_dict = create_mapping(room_list)

    # Genetic algorithm inputs
    epochs = 2000
    population_size = 100
    elite_number = 25
    mutation_rate = 0.05

    # Number of rooms to visit on a round
    route_length = 20
    print(f"The nurse must visit the following rooms once: {room_list[:route_length]}")

    # Create and assess initial population
    population = create_initial_population(population_size, route_length, map_dict)
    _, min_idx, min_distance = calculate_fitness(population, distance_matrix)
    print(f"Shortest initial distance: {min_distance} m")
    min_distances = [min_distance]
    min_individuals = [population[min_idx]]

    # For each epoch, generate a new population and assess it

    for i in range(0, epochs):
        new_population = _create_next_generation(population, distance_matrix, elite_number, mutation_rate)
        _, min_idx, min_distance = calculate_fitness(population, distance_matrix)
        min_distances.append(min_distance)
        min_individuals.append(population[min_idx])
        population = new_population

    # Print best solution
    best_min_idx, best_min_val = min(enumerate(min_distances), key=operator.itemgetter(1))
    total_improvement = 100 * (min_distances[0] - best_min_val) / min_distances[0]
    print(f"Best solution found: {best_min_val:.2f} m, an improvement of {total_improvement:.2f} %")

    # Reverse the mapping and get a room sequence
    best_individual = min_individuals[best_min_idx]
    best_route = reverse_room_mapping(best_individual, map_dict)
    print(f"The best route found is: {best_route}")

    # Create output visualisation
    visualise_fitness(min_distances)


if __name__ == "__main__":
    main()
