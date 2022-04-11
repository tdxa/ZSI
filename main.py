from order_crossover import order_xover_pair
from partially_mapped_crossover import pmx_v2, pmx
from rating import rate, best_individual
from selection import selection_tournament, selection_roulette
from swap_mutation import swap_mutation
from utlis import read_file, print_winner, create_matrix, generate_base_population

FILE = './data/berlin52.txt'

N = 70
EPOCHS = 10000
CHANCE_CROSSING = 0.85
CHANCE_SWAP_MUTATION = 0.66
CHANGE_CROSSING_METHOD = (70 * 100) / 100


def genetic_algorithm(file: str, n: int, epochs: int, chance_swap_mutation: float, chance_crossing: float,
                      change_crossing_method: float):
    t = 0
    matrix = create_matrix(read_file(file))
    population = generate_base_population(matrix, n)
    population_with_rate = rate(matrix, population)
    winner = best_individual(population_with_rate)

    while t < epochs:
        print(f"Current iteration: {t + 1}")

        print("   Selection...")
        if t < 10000:
            population_selection = selection_tournament(population_with_rate, 6, 6)
        else:
            population_selection = selection_roulette(population_with_rate, 50)

        print("   Crossing...")
        prepare = [population_selection[i][0] for i in range(len(population_selection))]
        pairs_individuals = [prepare[i:i + 2] for i in range(0, len(population_selection), 2)]
        population_crossing = []
        for pair in pairs_individuals:
            # population_crossing += pmx_v2(pair)
            # pmx_v2(pair)
            # print("PAIR", pair)
            if (t / 100)*100 < change_crossing_method:
                population_crossing += order_xover_pair(pair, chance_crossing)
            else:
                population_crossing += pmx(pair)
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
    # mat = create_matrix(read_file(f))
    # pop = generate_base_population(mat, n)
    # pop_rat = rate(mat, pop)
    # print(mat)
    # print(pop)
    # print("pop ratings   ", pop_rat)

    # rou = selection_tournament(pop_rat, 3, n)
    # print("tournament    ", rou)
    # selection_roulette(pop_rat, 3)
    # x = rou[0][0], rou[1][0]
    # print("******    ", x)
    # print("points", crossover_points)
    # pmx(x, n, crossover_points)
    # after_cross = pmx(x)
    # print("PMX           ", after_cross)
    #
    # sw = swap_mutation(after_cross, chance_swap_mutation)
    # print("swap          ",sw)
    # print("**********")
    # af = rate(mat, sw)
    # print(af)

    # best_individual(pop_rat)
    genetic_algorithm(file=FILE, n=N, epochs=EPOCHS, chance_crossing=CHANCE_CROSSING,
                      chance_swap_mutation=CHANCE_SWAP_MUTATION, change_crossing_method=CHANGE_CROSSING_METHOD)
