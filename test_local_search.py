from local_search import MinConflictNQueensSolver
from time import time

N_TESTS = 50
N_QUEENS = 100


if __name__ == '__main__':
    test_times = []
    for _ in range(N_TESTS):
        start_time = time()
        solver = MinConflictNQueensSolver(N_QUEENS)
        _, _, _ = solver.run()
        test_times.append(time() - start_time)
    print(f'Elapsed average time {sum(test_times) / len(test_times)} sec. {N_TESTS} tests were run.')
