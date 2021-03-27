import random


class Chromosome:
    def __init__(self, length: int = 8):
        self.length = length
        self.genes = [random.randint(1, length) for _ in range(length)]

    def __str__(self):
        return f'Chromosome = {self.genes} Fitness = {self.fitness(self.length * (self.length - 1) // 2)}'

    def mutate(self):
        position = random.randint(0, self.length - 1)
        value = random.randint(1, self.length)
        self.genes[position] = value

    def fitness(self, max_fitness: int = 28) -> int:
        horizontal_collisions = sum([self.genes.count(queen) - 1 for queen in self.genes]) / 2
        diagonal_collisions = 0

        left_diagonal = [0] * 2 * self.length
        right_diagonal = [0] * 2 * self.length
        for i in range(self.length):
            left_diagonal[i + self.genes[i] - 1] += 1
            right_diagonal[self.length - i + self.genes[i] - 2] += 1

        for i in range(2 * self.length - 1):
            counter = 0
            if left_diagonal[i] > 1:
                counter += left_diagonal[i] - 1
            if right_diagonal[i] > 1:
                counter += right_diagonal[i] - 1
            diagonal_collisions += counter / (self.length - abs(i - self.length + 1))

        return int(max_fitness - (horizontal_collisions + diagonal_collisions))

    def probability(self, max_fitness: int = 28) -> float:
        return self.fitness(max_fitness) / max_fitness


class GeneticAlgorithm:
    def __init__(self, n_queens: int = 8, max_generations: int = 100000,
                 generation_size: int = 300, mutation_prob: float = 0.03):
        self.n_queens = n_queens
        self.max_fitness = n_queens * (n_queens - 1) // 2
        self.max_generations = max_generations
        self.generation_size = generation_size
        self.mutation_probability = mutation_prob
        self.mean_fitness_per_generation = []
        self.population = [Chromosome(n_queens) for _ in range(generation_size)]

    def random_pick(self) -> Chromosome:
        probabilities = [chromosome.probability(self.max_fitness) for chromosome in self.population]
        population_with_probability = list(zip(self.population, probabilities))
        total = sum(probabilities)
        r = random.uniform(0, total)
        upto = 0
        for c, w in population_with_probability:
            if upto + w >= r:
                return c
            upto += w

    def reproduce(self, chr_x: Chromosome, chr_y: Chromosome) -> Chromosome:  # doing cross_over between two chromosomes
        c = random.randint(0, self.n_queens - 1)
        result = Chromosome(self.n_queens)
        result.genes = chr_x.genes[0:c] + chr_y.genes[c:self.n_queens]
        return result

    def produce_children(self):
        probabilities = [chromosome.probability(self.max_fitness) for chromosome in self.population]
        population_with_probability = list(zip(self.population, probabilities))
        population_with_probability.sort(key=lambda x: x[1], reverse=True)
        new_population = [chromosome for chromosome, _ in population_with_probability][:self.generation_size // 2]
        for i in range(self.generation_size - len(new_population)):
            chr_x = self.random_pick()
            chr_y = self.random_pick()
            child = self.reproduce(chr_x, chr_y)
            if random.random() <= self.mutation_probability:
                child.mutate()
            new_population.append(child)
            if child.fitness(self.max_fitness) == self.max_fitness:
                break
        self.population = new_population

    def run(self, verbose=False) -> (int, Chromosome):
        generation = 1
        population_fitness = [chromosome.fitness(self.max_fitness) for chromosome in self.population]

        while self.max_fitness not in population_fitness and generation < self.max_generations:
            if verbose:
                print(f"=== Generation {generation} ===")
                print(f"Maximum Fitness = {max(population_fitness)}")
                for chromosome in self.population:
                    print(chromosome)
            self.mean_fitness_per_generation.append(sum(population_fitness) / self.generation_size)
            self.produce_children()
            population_fitness = [chromosome.fitness(self.max_fitness) for chromosome in self.population]
            generation += 1
        self.mean_fitness_per_generation.append(sum(population_fitness) / len(population_fitness))
        return generation, self.population[population_fitness.index(max(population_fitness))]

    def print_result(self, result):
        board = [['x'] * self.n_queens for _ in range(self.n_queens)]

        for queen in result:
            board[queen - 1][result.index(queen)] = "Q"
        for row in board:
            print(" ".join(row))
