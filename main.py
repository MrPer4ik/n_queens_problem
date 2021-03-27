from genetic_algorithm import GeneticAlgorithm
from local_search import MinConflictNQueensSolver
from matplotlib import pyplot as plt


if __name__ == '__main__':
    n, alg = None, None

    try:
        n = int(input('Enter n queen (n > 3): '))
    except ValueError:
        print('Please input an integer.\n')
    while not isinstance(n, int) or n < 4:
        try:
            n = int(input('Enter n queen (n > 3): '))
        except ValueError:
            print('Please input an integer.\n')

    try:
        alg = int(input('Enter number for algorithm (1 - local search, 2 - genetic algorithm): '))
    except ValueError:
        print('Please input 1 or 2.\n')
    while alg not in [1, 2]:
        try:
            alg = int(input('Enter number for algorithm (1 - local search, 2 - genetic algorithm): '))
        except ValueError:
            print('Please input 1 or 2.\n')

    if alg == 1:
        min_conflict = MinConflictNQueensSolver(n=n)
        board, res, step = min_conflict.run()
        print(f'Result: {res}. Found in {step} step.')
        char_list = map(list, board)
        for line in char_list:
            print(" ".join(line))
    else:
        genetic_algorithm = GeneticAlgorithm(n_queens=n, max_generations=100000,
                                             generation_size=200, mutation_prob=0.05)
        generation, res = genetic_algorithm.run()
        print(f'Result: {res}. Found in {generation} generation.')
        plt.plot(list(range(generation)), genetic_algorithm.mean_fitness_per_generation)
        plt.xlabel('Generation')
        plt.ylabel('Fitness Function')
        genetic_algorithm.print_result(res.genes)
        plt.show()
