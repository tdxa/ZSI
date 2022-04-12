from type import Matrix, Population, RatedPopulation, RatedIndividual


def fitness(cost_array: list, solution: list) -> int:
    mark = sum([cost_array[solution[index]][solution[index + 1]] for index in
                range(len(solution) - 1)])
    return mark + cost_array[solution[-1]][solution[0]]


def rate(matrix: Matrix, population: Population) -> RatedPopulation:
    # rates = []
    # for individual in population:
    #     current = []
    #     try:
    #         for n, _ in enumerate(individual):
    #             current.append(matrix[individual[n - 1]][individual[n]])
    #     except:
    #         current.append(matrix[individual[-1]][individual[0]])
    #
    #     rates.append(sum(current))
    #
    # return [[population[i], rates[i]] for i in range(len(population))]
    marks = [fitness(matrix, individual) for individual in population]

    return [[population[i], marks[i]] for i in range(len(population))]


def best_individual(population_with_rate: RatedPopulation) -> RatedIndividual:
    minimum = min([x[1] for index, x in enumerate(population_with_rate)])
    minimum_index = \
        [index for index, value in enumerate(population_with_rate) for i, j in enumerate(value) if j == minimum][0]

    return population_with_rate[minimum_index]
