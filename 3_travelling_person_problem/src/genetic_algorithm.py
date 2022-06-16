import random
import numpy as np
import matplotlib.pyplot as plt


def _make_route(map_dict, route_length):

    possible_rooms = list(map_dict.keys())
    route_rooms = possible_rooms[:route_length]
    route = random.sample(route_rooms, route_length-1)
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


def plot_pop_fitness(sorted_population_fitness, elite_number):

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 10)
    for idx, fitness in enumerate(list(sorted_population_fitness.values())):
        if idx < elite_number:
            ax.scatter([np.random.random()], fitness, c='r')
        else:
            ax.scatter([np.random.random()], fitness, c='b')
    plt.show()


def calculate_fitness(population, distance_matrix):

    population_fitness = {}
    for idx, individual in enumerate(population):
        fitness = _calculate_individual_fitness(individual, distance_matrix)
        population_fitness[idx] = fitness

    sorted_population_fitness = dict(sorted(population_fitness.items(), key=lambda item: item[1], reverse=True))

    min_idx = list(sorted_population_fitness.keys())[0]
    min_distance = round(1 / sorted_population_fitness[min_idx], 2)

    return sorted_population_fitness, min_idx, min_distance





def _probability_selection(sorted_population_fitness, elite_number):
    #plot_pop_fitness(sorted_population_fitness, elite_number)

    probabilities = {idx: fitness / sum(sorted_population_fitness.values()) for idx, fitness in sorted_population_fitness.items()}
    sorted_individual_idxs = list(sorted_population_fitness.keys())

    selection_idxs = []
    for i in range(0, elite_number):
        elite_id = sorted_individual_idxs[i]
        selection_idxs.append(elite_id)

    remaining_required = len(sorted_individual_idxs) - elite_number
    tournament_selection = list(np.random.choice(sorted_individual_idxs, size=remaining_required, p=list(probabilities.values()), replace=True))

    selection_idxs += tournament_selection

    return selection_idxs


def _get_selected_individuals(population, selection_idxs):

    return [population[idx] for idx in selection_idxs]


def _ox1_crossover(parent_1, parent_2):

    trimmed_parent_1, trimmed_parent_2 = parent_1[:-1], parent_2[:-1]
    cross_a, cross_b = np.random.randint(0, len(trimmed_parent_1), size=2)

    min_cross = min(cross_a, cross_b)
    max_cross = max(cross_a, cross_b)
    remains_idx = [idx for idx, _ in enumerate(trimmed_parent_1) if idx not in range(min_cross, max_cross)]

    # print(f"Parent 1: {parent_1}")
    # print(f"Parent 2: {parent_2}")
    # print(f"Trimmed parent 1: {trimmed_parent_1}")
    # print(f"Trimmed parent 2: {trimmed_parent_2}")
    # print(f"Min cross: {min_cross}")
    # print(f"Max cross: {max_cross}")
    # print(f"Remains: {remains_idx}")

    sub_chromosome = trimmed_parent_1[min_cross:max_cross]
    # print(f"Sub chromo: {sub_chromosome}")

    # Fill the remains indices with the remains from parent 2
    parent_2_remains = [gene for gene in trimmed_parent_2 if gene not in sub_chromosome]
    for idx, remains_idx in enumerate(remains_idx):
        parent_2_gene = parent_2_remains[idx]
        if remains_idx < min_cross:
            sub_chromosome.insert(min_cross-1, parent_2_gene)
        else:
            sub_chromosome.insert(max_cross+1, parent_2_gene)

    sub_chromosome.append(sub_chromosome[0])

    # print(f"Parent 2 remains: {parent_2_remains}")
    # print(f"Final chromo: {sub_chromosome}")

    return sub_chromosome


def create_new_population(selected_individuals, elite_number):

    children = []
    pool_size = len(selected_individuals) - elite_number
    shuffled_selected_ids = random.sample(selected_individuals, len(selected_individuals))

    # Carry elites forward

    children += selected_individuals[:elite_number]

    # Create the rest of the children using crossover
    for i in range(0, pool_size-elite_number):
        parent_1, parent_2 = shuffled_selected_ids[i], shuffled_selected_ids[len(selected_individuals) - i - 1]
        child = _ox1_crossover(parent_1, parent_2)
        children.append(child)

    return children


def _mutate_individual(individual, mutation_rate):

    for _ in individual:
        if random.random() < mutation_rate:
            idx_1, idx_2 = np.random.randint(1, len(individual)-1, size=2)
            gene_1, gene_2 = individual[idx_1], individual[idx_2]
            individual[idx_1], individual[idx_2] = gene_2, gene_1

    return individual


def _mutate_population(population, elite_number, mutation_rate):

    population_with_mutation = []
    for idx, individual in enumerate(population):
        if idx > elite_number / 2:
            mutated_individual = _mutate_individual(individual, mutation_rate)
            population_with_mutation.append(mutated_individual)
        else:
            population_with_mutation.append(individual)

    return population_with_mutation


def count_same_ids(population, new_mutated_population):

    count = 0
    for i in population:
        if i in new_mutated_population:
            count += 1

    print(f"{count} made it to the new population")


def _create_next_generation(population, distance_matrix, elite_number, mutation_rate):

    sorted_population_fitness, _, _ = calculate_fitness(population, distance_matrix)

    selection_idxs = _probability_selection(sorted_population_fitness, elite_number)
    new_candidates = _get_selected_individuals(population, selection_idxs)
    new_population = create_new_population(new_candidates, elite_number)
    new_mutated_population = _mutate_population(new_population, elite_number, mutation_rate)

    #if population[min_idx] in new_mutated_population:
        #print(True)

    # count_same_ids(population, new_mutated_population)

    return new_mutated_population







