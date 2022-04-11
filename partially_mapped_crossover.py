import random


def pmx_get_child(parent_1, parent_2, start_crossover, stop_crossover):
    child = [None] * len(parent_1)

    # Copy points between crossover start & stop from parent_1
    child[start_crossover:stop_crossover] = parent_1[start_crossover:stop_crossover]

    for index, point in enumerate(parent_2[start_crossover:stop_crossover]):
        index += start_crossover
        if point not in child:
            while child[index] is not None:
                index = parent_2.index(parent_1[index])
            child[index] = point

    for index, point in enumerate(child):
        if point is None:
            child[index] = parent_1[index]

    return child


def pmx_v2(data, chance_crossing: float):
    individual_1, individual_2 = data
    m = len(individual_1)

    start_crossover = random.randint(0, m - (m // 2))
    stop_crossover = start_crossover + (m // 2)

    if random.random() >= chance_crossing:
        return pmx_get_child(individual_1, individual_2, start_crossover, stop_crossover), pmx_get_child(individual_2,
                                                                                                         individual_1,
                                                                                                         start_crossover,
                                                                                                         stop_crossover)
    else:
        return data


# not working good
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
