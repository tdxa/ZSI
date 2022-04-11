import random
from typing import List

from type import RatedPopulation


def reverse_individual_rating(data: RatedPopulation) -> List[int]:
    max_rate = max([x[1] for x in data])
    return [max_rate + 1 - x[1] for x in data]


def selection_tournament(data: RatedPopulation, k: int, n: int) -> RatedPopulation:
    tournament = [random.sample(data, k) for _ in range(n)]
    ratings = []

    for i in range(n):
        ratings.append([individual[1] for individual in tournament[i]])

    winners_indexes = [rate.index(min(rate)) for rate in ratings]

    new_population = []
    for i in range(n):
        new_population.append(tournament[i][winners_indexes[i]])

    return new_population


def selection_roulette(data: RatedPopulation, k: int) -> RatedPopulation:
    new_rating = reverse_individual_rating(data)
    sum_rating = sum(new_rating)
    probabilities = [p / sum_rating for p in new_rating]
    new_pop = random.choices(data, probabilities, k=k)
    return new_pop
