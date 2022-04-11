from order_crossover import order_xover_pair
from partially_mapped_crossover import pmx, pmx_v2
from rating import rate, best_individual
from selection import selection_tournament, selection_roulette
from swap_mutation import swap_mutation
from utlis import read_file, print_winner, create_matrix, generate_base_population

FILE = './data/berlin52.txt'

N = 200
K = 50
EPOCHS = 10000
CHANCE_CROSSING = 0.65
CHANCE_SWAP_MUTATION = 0.66
CHANGE_CROSSING_METHOD = (40 * EPOCHS) / 100


def genetic_algorithm(file: str, n: int, k: int, epochs: int, chance_swap_mutation: float, chance_crossing: float,
                      change_crossing_method: float):
    t = 0
    matrix = create_matrix(read_file(file))
    population = generate_base_population(matrix, n)
    population_with_rate = rate(matrix, population)
    winner = best_individual(population_with_rate)

    while t < epochs:
        print(f"Current iteration: {t + 1}")

        print("   Selection...")
        if (t / epochs) * 100 < (80 * epochs) / 100:
            population_selection = selection_tournament(population_with_rate, k, n)
        else:
            population_selection = selection_roulette(population_with_rate, k)

        print("   Crossing...")
        prepare = [population_selection[i][0] for i in range(len(population_selection))]
        pairs_individuals = [prepare[i:i + 2] for i in range(0, len(population_selection), 2)]
        population_crossing = []
        for pair in pairs_individuals:
            if (t / epochs) * 100 < change_crossing_method:
                population_crossing += order_xover_pair(pair, chance_crossing)
            else:
                population_crossing += pmx_v2(pair)
        print("   Mutation...")
        population_mutation = swap_mutation(population_crossing, chance_swap_mutation)

        print("   Rating...")
        population_rating = rate(matrix, population_mutation)
        best = best_individual(population_rating)

        winner = best if best[1] < winner[1] else winner
        population_with_rate = population_rating
        print(f"Iteration rate: {best[1]}   ||   Current best rate: {winner[1]}")
        t += 1

    print_winner(winner)


if __name__ == "__main__":
    genetic_algorithm(file=FILE, n=N, k=K, epochs=EPOCHS, chance_crossing=CHANCE_CROSSING,
                      chance_swap_mutation=CHANCE_SWAP_MUTATION, change_crossing_method=CHANGE_CROSSING_METHOD)
