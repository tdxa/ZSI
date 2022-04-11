from typing import List


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


def best_individual(population_with_rate):
    minimum = min(x[1] for index, x in enumerate(population_with_rate))
    minimum_index = \
        [index for index, value in enumerate(population_with_rate) for i, j in enumerate(value) if j == minimum][0]

    return population_with_rate[minimum_index]