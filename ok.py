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


def pmx(data, n, p):
    individual_1, individual_2 = data
    m = len(individual_1)

    # Choose crossover points
    # crossover_points = sorted(random.sample(range(m), 2))
    print(crossover_points)

    result_1, result_2 = [0] * m, [0] * m

    for i in range(m):
        result_1[individual_1[i]] = i
        result_2[individual_2[i]] = i

    for i in range(p[0], p[1]):
        # Keep track of the selected values
        temp_1 = individual_1[i]
        temp_2 = individual_2[i]
        # Swap the matched value
        individual_1[i], individual_1[result_1[temp_2]] = temp_2, temp_1
        individual_2[i], individual_2[result_2[temp_1]] = temp_1, temp_2
        # Position bookkeeping
        result_1[temp_1], result_1[temp_2] = result_1[temp_2], result_1[temp_1]
        result_2[temp_1], result_2[temp_2] = result_2[temp_2], result_2[temp_1]

    print("result   ", result_1, result_2)


def cxPartialyMatched(ind1, ind2, p):
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. This crossover expects
    :term:`sequence` individuals of indices, the result for any other type of
    individuals is unpredictable.
    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.
    Moreover, this crossover generates two children by matching
    pairs of values in a certain range of the two parents and swapping the values
    of those indexes. For more details see [Goldberg1985]_.
    This function uses the :func:`~random.randint` function from the python base
    :mod:`random` module.
    .. [Goldberg1985] Goldberg and Lingel, "Alleles, loci, and the traveling
       salesman problem", 1985.
    """
    size = min(len(ind1), len(ind2))
    p1, p2 = [0] * size, [0] * size

    # Initialize the position of each indices in the individuals
    for i in range(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i
    # # Choose crossover points
    # cxpoint1 = random.randint(0, size)
    # cxpoint2 = random.randint(0, size - 1)
    #
    # if cxpoint2 >= cxpoint1:
    #     cxpoint2 += 1
    # else:  # Swap the two cx points
    #     cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Apply crossover between cx points
    for i in range(p[0], p[1]):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return ind1, ind2


def swap_mutation(population, chance_swap_mutation):
    for point in population:
        for index, gen in enumerate(point):
            if random.random() > chance_swap_mutation:
                mutation_point = random.randrange(5)
                point[index], point[mutation_point] = point[mutation_point], point[index]
    return population


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
        print("   Crossing...")
        print("   Mutation...")
        print("   Rating...")
        t += 1


n = 6
chance_pmx_crossing = 0.65
chance_swap_mutation = 0.70

mat = create_matrix(read_file(f))
pop = generate_base_population(mat, n)
pop_rat = rate(mat, pop)
# print(mat)
# print(pop)
print("pop ratings   ", pop_rat)

rou = selection_tournament(pop_rat, 3, n)
print("tournament    ", rou)
# selection_roulette(pop_rat, 3)
crossover_points = sorted(random.sample(range(5), 2))
# x = rou[0][0], rou[1][0]
# print("******    ", x)
# print("points", crossover_points)
# pmx(x, n, crossover_points)
after_cross = cxPartialyMatched(rou[0][0], rou[1][0], crossover_points)
print("PMX           ", after_cross)
print("**********")
swap_mutation(cxPartialyMatched(rou[0][0], rou[1][0], crossover_points), chance_swap_mutation)
# genetic_algorithm(f, n, 100)
