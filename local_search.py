import random


class NQueensCSP:
    def __init__(self, variables, adj_list, domains):
        self.variables = variables
        self.adjList = adj_list
        self.domains = domains

    def n_conflicts(self, x1, x, assignment):
        """
        Return the number of conflicts x1 = x has with other variables
        Subclasses may implement this more efficiently
        """
        def conflict(x2):
            return self.conflicts(x1, x, x2, assignment[x2])
        return sum(conflict(x2) for x2 in self.adjList[x1] if x2 in assignment)

    def conflicted_vars(self, current):
        """ Return a list of variables in conflict in current assignment """
        return [var for var in self.variables
                if self.n_conflicts(var, current[var], current) > 0]

    @staticmethod
    def conflicts(row1, col1, row2, col2):
        return col1 == col2 or row1 + col1 == row2 + col2 or row1 - col1 == row2 - col2

    def min_conflicts_value(self, x, assignment):
        """ Return the value that will give var the least number of conflicts. """
        random.shuffle(self.domains[x])
        return min(self.domains[x], key=lambda e: self.n_conflicts(x, e, assignment))

    def min_conflicts(self, max_steps=1000000, verbose=False):
        """
        Solve a CSP by stochastic hill climbing on the number of conflicts.
        Generate a complete assignment for all variables (probably with conflicts)
        """
        assignment = {}
        for x in self.variables:
            val = self.min_conflicts_value(x, assignment)
            assignment[x] = val

        for i in range(max_steps):
            conflicted = self.conflicted_vars(assignment)
            if not conflicted:
                if verbose:
                    print("Success!")
                return i + 1, assignment
            x = random.choice(conflicted)
            val = self.min_conflicts_value(x, assignment)
            assignment[x] = val
            if verbose:
                print(f'\rProgress: {i+1} / {max_steps}')


class MinConflictNQueensSolver:
    def __init__(self, n=8, max_steps=1000000, verbose=False):
        self.n = n
        self.max_steps = max_steps
        self.verbose = verbose

    def make_board(self, result):
        board = []
        for i in range(self.n):
            line = ['x'] * self.n
            line[result[i]] = 'Q'
            board.append(str().join(line))
        return board

    def build_csp_problem(self):
        adj_list = {}
        for i in range(self.n):
            adj_list[i] = set([j for j in range(self.n) if j != i])
        domains = {}
        for i in range(self.n):
            domains[i] = list(range(self.n))
        return NQueensCSP(list(range(self.n)), adj_list, domains)

    def run(self):
        csp = self.build_csp_problem()
        step, result = csp.min_conflicts(self.max_steps, self.verbose)
        res = dict([(value, key) for key, value in result.items()])
        csp = [res[i] + 1 for i in range(self.n)]
        return self.make_board(result), csp, step
