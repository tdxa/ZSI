import random


def pmx_get_child(parent_1, parent_2, start_crossover, stop_crossover, m):
    child = [None] * m

    # Copy slice between crossover points
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


def pmx_v2(data):
    individual_1, individual_2 = data
    m = len(individual_1)
    # crossover_points = sorted(random.sample(random.randint(0,m), 2))
    start_crossover = random.randint(0, m - (m // 2))
    stop_crossover = start_crossover + (m // 2)
    print("DATA", data)
    print("POINTS", [start_crossover, stop_crossover])
    s = pmx_get_child(individual_1, individual_2, start_crossover, stop_crossover, m)
    f = pmx_get_child(individual_2, individual_1, start_crossover, stop_crossover, m)

    print("CHILD 1:", s)
    print("CHILD 2:", f)


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
