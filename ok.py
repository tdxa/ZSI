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


def selection_tournament(data):
    tournament = [random.sample(data, 3) for _ in range(5)]
    ratings = []

    for i in range(len(tournament)):
        ratings.append([c[1] for c in tournament[i]])

    winners_indexes = [c.index(min(c)) for c in ratings]

    new_population = []
    for i in range(len(tournament)):
        new_population.append(tournament[i][winners_indexes[i]])

    return new_population


def selection_roulette(data):
    new_rating = reverse_individual_rating(data)
    sum_rating = sum(new_rating)
    probabilities = [p / sum_rating for p in new_rating]
    new_pop = random.choices(data, probabilities, k=4)

    return new_pop


def genetic_algorithm(file, epochs):
    pass


mat = create_matrix(read_file(f))
pop = generate_base_population(mat, 5)
pop_rat = rate(mat, pop)
# print(mat)
# print(pop)
# print(pop_rat)

selection_roulette(pop_rat)
selection_tournament(pop_rat)
