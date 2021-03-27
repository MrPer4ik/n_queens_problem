from genetic_algorithm import GeneticAlgorithm
from time import time

N_TESTS = 100
N_QUEENS = 5
GENERATION_SIZE = 200
MUTATION_PROB = 1


if __name__ == '__main__':
    test_times = []
    for _ in range(N_TESTS):
        start_time = time()
        solver = GeneticAlgorithm(n_queens=N_QUEENS, generation_size=GENERATION_SIZE, mutation_prob=MUTATION_PROB)
        _, _ = solver.run()
        test_times.append(time() - start_time)
    print(f'Elapsed average time {sum(test_times) / len(test_times)} sec. {N_TESTS} tests were run.')
