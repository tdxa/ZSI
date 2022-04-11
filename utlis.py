import csv
import random
from type import List, RatedIndividual, Population, Matrix


def read_file(path: str, delimiter=" "):
    with open(path, newline="") as file:
        next(file)
        return [list(filter(None, row)) for row in csv.reader(file, delimiter=delimiter)]


def create_matrix(data: List[List[int]]) -> list[list[None]]:
    num_cities = sum(1 for _ in data)
    matrix = [[None] * num_cities for _ in range(num_cities)]
    for x in range(num_cities):
        for y in range(num_cities):
            try:
                matrix[x][y] = int(data[x][y])
            except IndexError:
                matrix[x][y] = int(data[y][x])
    return matrix


def generate_base_population(matrix: Matrix, n: int) -> Population:
    m = [n for n in range(len(matrix))]
    return [random.sample(m, len(m)) for _ in range(n)]


def print_winner(winner: RatedIndividual) -> None:
    print("-".join(str(point) for point in winner[0]) + " " + "".join(str(winner[1])))
