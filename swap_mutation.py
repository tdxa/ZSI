import random

from type import Population


def swap_mutation(population: Population, chance_swap_mutation: float) -> Population:
    for point in population:
        for index, gen in enumerate(point):
            if random.random() >= chance_swap_mutation:
                mutation_point = random.randrange(5)
                point[index], point[mutation_point] = point[mutation_point], point[index]
    return population
