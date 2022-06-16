import random
import numpy as np
import operator

from ga_mappings import reverse_room_mapping

from tsp_visualisation import visualise_fitness


class GeneticAlgorithm:

    def __init__(self, route_length, epochs, population_size, elite_number, mutation_rate, map_dict):

        self.epochs = epochs
        self.population_size = population_size
        self.elite_number = elite_number
        self.mutation_rate = mutation_rate
        self.min_distances = []
        self.min_individuals = []
        self.population = [self._create_route(route_length, map_dict) for _ in range(0, self.population_size)]

    def _create_route(self, route_length, map_dict):
        possible_rooms = list(map_dict.keys())
        route_rooms = possible_rooms[:route_length]
        route = random.sample(route_rooms, route_length - 1)
        route.append(route[0])

        return route

    def _calculate_individual_fitness(self, individual, distance_matrix):
        total_distance = 0
        for idx, label in enumerate(individual[:-1]):
            matrix_index_i = ord(label) - ord('a')
            matrix_index_j = ord(individual[idx + 1]) - ord('a')
            total_distance += distance_matrix[matrix_index_i][matrix_index_j]

        return 1 / total_distance

    def _calculate_fitness(self, distance_matrix):

        population_fitness = {}
        for idx, individual in enumerate(self.population):
            fitness = self._calculate_individual_fitness(individual, distance_matrix)
            population_fitness[idx] = fitness

        sorted_population_fitness = dict(sorted(population_fitness.items(), key=lambda item: item[1], reverse=True))
        min_idx = list(sorted_population_fitness.keys())[0]
        min_distance = round(1 / sorted_population_fitness[min_idx], 2)

        return sorted_population_fitness, min_idx, min_distance

    def _probability_selection(self, sorted_population_fitness):

        probabilities = {idx: fitness / sum(sorted_population_fitness.values()) for idx, fitness in sorted_population_fitness.items()}
        sorted_individual_idxs = list(sorted_population_fitness.keys())

        selection_idxs = []
        for i in range(0, self.elite_number):
            elite_id = sorted_individual_idxs[i]
            selection_idxs.append(elite_id)

        remaining_required = len(sorted_individual_idxs) - self.elite_number
        tournament_selection = list(np.random.choice(sorted_individual_idxs, size=remaining_required, p=list(probabilities.values()), replace=True))
        selection_idxs += tournament_selection
        candidate_individuals = [self.population[idx] for idx in selection_idxs]

        return candidate_individuals

    def _order_crossover(self, parent_1, parent_2):
        """Order crossover proposed by Davis"""

        trimmed_parent_1, trimmed_parent_2 = parent_1[:-1], parent_2[:-1]
        cross_a, cross_b = np.random.randint(0, len(trimmed_parent_1), size=2)
        min_cross = min(cross_a, cross_b)
        max_cross = max(cross_a, cross_b)
        remains_idx = [idx for idx, _ in enumerate(trimmed_parent_1) if idx not in range(min_cross, max_cross)]
        sub_chromosome = trimmed_parent_1[min_cross:max_cross]

        # Fill the remains indices with the remains from parent 2
        parent_2_remains = [gene for gene in trimmed_parent_2 if gene not in sub_chromosome]
        for idx, remains_idx in enumerate(remains_idx):
            parent_2_gene = parent_2_remains[idx]
            if remains_idx < min_cross:
                sub_chromosome.insert(min_cross-1, parent_2_gene)
            else:
                sub_chromosome.insert(max_cross+1, parent_2_gene)

        sub_chromosome.append(sub_chromosome[0])

        return sub_chromosome

    def _create_new_population(self, selected_individuals):

        children = []
        pool_size = len(selected_individuals) - self.elite_number
        shuffled_selected_ids = random.sample(selected_individuals, len(selected_individuals))

        # Carry elites forward
        children += selected_individuals[:self.elite_number]

        # Create the rest of the children using crossover
        for i in range(0, pool_size-self.elite_number):
            parent_1, parent_2 = shuffled_selected_ids[i], shuffled_selected_ids[len(selected_individuals) - i - 1]
            child = self._order_crossover(parent_1, parent_2)
            children.append(child)

        return children

    def _mutate_individual(self, individual):

        for _ in individual:
            if random.random() < self.mutation_rate:
                idx_1, idx_2 = np.random.randint(1, len(individual)-1, size=2)
                gene_1, gene_2 = individual[idx_1], individual[idx_2]
                individual[idx_1], individual[idx_2] = gene_2, gene_1

        return individual

    def _mutate_population(self, new_population):

        population_with_mutation = []
        for idx, individual in enumerate(new_population):
            if idx > self.elite_number / 2:
                mutated_individual = self._mutate_individual(individual)
                population_with_mutation.append(mutated_individual)
            else:
                population_with_mutation.append(individual)

        return population_with_mutation

    def _create_next_generation(self, distance_matrix):

        sorted_population_fitness, _, _ = self._calculate_fitness(distance_matrix)
        new_candidates = self._probability_selection(sorted_population_fitness)
        new_population = self._create_new_population(new_candidates)
        self.population = self._mutate_population(new_population)

    def _save_variables(self, min_idx, min_distance):

        self.min_distances.append(min_distance)
        self.min_individuals.append(self.population[min_idx])

    def run(self, distance_matrix):

        _, min_idx, min_distance = self._calculate_fitness(distance_matrix)
        self._save_variables(min_idx, min_distance)

        # For each epoch, generate a new population and assess it
        for _ in range(0, self.epochs):
            self._create_next_generation(distance_matrix)
            _, min_idx, min_distance = self._calculate_fitness(distance_matrix)
            self._save_variables(min_idx, min_distance)

    def process_outputs(self, map_dict):
        best_min_idx, best_min_val = min(enumerate(self.min_distances), key=operator.itemgetter(1))
        total_improvement = 100 * (self.min_distances[0] - best_min_val) / self.min_distances[0]
        best_individual = self.min_individuals[best_min_idx]
        best_route = reverse_room_mapping(best_individual, map_dict)

        # Create output visualisation
        visualise_fitness(self.min_distances)

        # Print some info to console
        print(f"Shortest initial distance: {self.min_distances[0]} m")
        print(f"Best solution found: {best_min_val:.2f} m, an improvement of {total_improvement:.2f} %")
        print(f"The best route found is: {best_route}")
