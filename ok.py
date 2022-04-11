import csv
import random
from typing import List

f = './data/test.txt'


def read_file(path, delimiter=" "):
    with open(path, newline="") as file:
        next(file)
        return [row for row in csv.reader(file, delimiter=delimiter)]


def create_matrix(data):
    num_cities = sum(1 for _ in data)
    matrix = [[None] * num_cities for _ in range(num_cities)]
    for x in range(num_cities):
        for y in range(num_cities):
            try:
                matrix[x][y] = int(data[x][y])
            except IndexError:
                matrix[x][y] = int(data[y][x])
    return matrix


def generate_base_population(matrix: List[List[int]], n: int) -> List[List[int]]:
    m = [n for n in range(len(matrix))]
    return [random.sample(m, len(m)) for _ in range(n)]


def rate(matrix: List[List[int]], population: List[List[int]]):
    rates = []
    for individual in population:
        n = 0
        rates_uq = []
        try:
            for _ in individual:
                rates_uq.append(matrix[individual[n]][individual[n + 1]])
                n += 1
        except:
            rates_uq.append(matrix[individual[-1]][individual[0]])

        rates.append(sum(rates_uq))

    return [[population[i], rates[i]] for i in range(len(population))]


def best_rate(population_with_rate):
    return min(x[1] for x in population_with_rate)

def reverse_individual_rating(data):
    max_rate = max([x[1] for x in data])
    return [max_rate + 1 - x[1] for x in data]


def selection_tournament(data, k, n):
    tournament = [random.sample(data, k) for _ in range(n)]
    ratings = []

    for i in range(n):
        ratings.append([individual[1] for individual in tournament[i]])

    winners_indexes = [rate.index(min(rate)) for rate in ratings]

    new_population = []
    for i in range(n):
        new_population.append(tournament[i][winners_indexes[i]])

    return new_population


def selection_roulette(data, k):
    new_rating = reverse_individual_rating(data)
    sum_rating = sum(new_rating)
    probabilities = [p / sum_rating for p in new_rating]
    new_pop = random.choices(data, probabilities, k=k)

    return new_pop


def pmx(data):
    individual_1, individual_2 = data
    m = len(individual_1)

    # Choose crossover points
    crossover_points = sorted(random.sample(range(m), 2))

    result_1, result_2 = [0] * m, [0] * m

    for i in range(m):
        result_1[individual_1[i]] = i
        result_2[individual_2[i]] = i

    for i in range(crossover_points[0], crossover_points[1]):
        # Keep track of the selected values
        temp_1 = individual_1[i]
        temp_2 = individual_2[i]
        # Swap the matched value
        individual_1[i], individual_1[result_1[temp_2]] = temp_2, temp_1
        individual_2[i], individual_2[result_2[temp_1]] = temp_1, temp_2
        # Position bookkeeping
        result_1[temp_1], result_1[temp_2] = result_1[temp_2], result_1[temp_1]
        result_2[temp_1], result_2[temp_2] = result_2[temp_2], result_2[temp_1]

    return [result_1, result_2]


def swap_mutation(population, chance_swap_mutation):
    for point in population:
        for index, gen in enumerate(point):
            if random.random() > chance_swap_mutation:
                mutation_point = random.randrange(5)
                point[index], point[mutation_point] = point[mutation_point], point[index]
    return population


best_ratings = []


def genetic_algorithm(file, n, epochs):
    t = 0
    matrix = create_matrix(read_file(file))
    population = generate_base_population(matrix, n)
    population_with_rate = rate(matrix, population)
    print(matrix)
    print("-------------------")
    print(population)
    print("-------------------")
    print(population_with_rate)

    while t < epochs:
        print(f"Current iteration: {t + 1}")
        print("   Selection...")
        population_selection = selection_roulette(population_with_rate, 8)
        print("  ", population_selection)
        print("   Crossing...")
        prepare = [population_selection[i][0] for i in range(len(population_selection))]
        pairs_individuals = [prepare[i:i + 2] for i in range(0, len(population_selection), 2)]
        population_crossing = []
        for pair in pairs_individuals:
            population_crossing += pmx(pair)
        print(population_crossing)

        print("   Mutation...")
        population_mutation = swap_mutation(population_crossing, chance_swap_mutation)
        print(population_mutation)
        print("   Rating...")
        population_rating = rate(matrix, population_mutation)
        print(population_rating)
        print(f"Iteration rate: {best_rate(population_rating)}   ||   Current best rate:")
        t += 1


n = 6
chance_pmx_crossing = 0.65
chance_swap_mutation = 0.70

# mat = create_matrix(read_file(f))
# pop = generate_base_population(mat, n)
# pop_rat = rate(mat, pop)
# print(mat)
# print(pop)
# print("pop ratings   ", pop_rat)

# rou = selection_tournament(pop_rat, 3, n)
# print("tournament    ", rou)
# selection_roulette(pop_rat, 3)
# x = rou[0][0], rou[1][0]
# print("******    ", x)
# print("points", crossover_points)
# pmx(x, n, crossover_points)
# after_cross = pmx(x)
# print("PMX           ", after_cross)
#
# sw = swap_mutation(after_cross, chance_swap_mutation)
# print("swap          ",sw)
# print("**********")
# af = rate(mat, sw)
# print(af)

# best_rate(pop_rat)
genetic_algorithm(f, n, 100)
