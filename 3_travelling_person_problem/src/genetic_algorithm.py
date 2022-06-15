import random



def _make_route(map_dict, route_length):

    possible_rooms = list(map_dict.values())
    route = random.sample(possible_rooms, route_length-1)
    route.append(route[0])

    return route


def create_initial_population(population_size, route_length, map_dict):

    return [_make_route(map_dict, route_length) for _ in range(0, population_size)]


def _calculate_individual_fitness(individual, distance_matrix):

    total_distance = 0
    for idx, label in enumerate(individual[:-1]):
        matrix_index_i = ord(label) - ord('a')
        matrix_index_j = ord(individual[idx+1]) - ord('a')
        total_distance += distance_matrix[matrix_index_i][matrix_index_j]

    return 1 / total_distance


def calculate_fitness(population, distance_matrix):

    population_results = {}
    for idx, individual in enumerate(population):
        fitness = _calculate_individual_fitness(individual, distance_matrix)
        population_results[idx] = fitness


