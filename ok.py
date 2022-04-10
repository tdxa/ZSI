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
                print(matrix[individual[n]][individual[n + 1]])
                rates_uq.append(matrix[individual[n]][individual[n + 1]])
                n += 1
        except:
            rates_uq.append(matrix[individual[-1]][individual[0]])

        rates.append(sum(rates_uq))

    return [[population[i], rates[i]] for i in range(len(population))]


