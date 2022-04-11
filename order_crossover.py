import random

from type import Population, Individual


def order_xover(parent_1: Individual, parent_2: Individual, start_crossover: int, stop_crossover: int):
    child = [None] * len(parent_1)

    # Copy a slice from first parent:
    child[start_crossover:stop_crossover] = parent_1[start_crossover:stop_crossover]

    # Fill using order from second parent:
    b_ind = stop_crossover
    c_ind = stop_crossover
    l = len(parent_1)
    while None in child:
        if parent_2[b_ind % l] not in child:
            child[c_ind % l] = parent_2[b_ind % l]
            c_ind += 1
        b_ind += 1
    return child


def order_xover_pair(data: Population, chance_crossing: float):
    parent_1, parent_2 = data
    half = len(parent_1) // 2
    start = random.randint(0, len(parent_1) - half)
    stop = start + half
    if random.random() >= chance_crossing:
        return order_xover(parent_1, parent_2, start, stop), order_xover(parent_2, parent_1, start, stop)
    else:
        return data
