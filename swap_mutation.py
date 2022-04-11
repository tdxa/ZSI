import random


def swap_mutation(population, chance_swap_mutation):
    for point in population:
        for index, gen in enumerate(point):
            if random.random() > chance_swap_mutation:
                mutation_point = random.randrange(5)
                point[index], point[mutation_point] = point[mutation_point], point[index]
    return population
