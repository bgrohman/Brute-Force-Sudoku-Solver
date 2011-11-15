import math
from datetime import datetime

class Sudoku(object):

    def __init__(self):
        self.n = 0
        self.b = 0
        self.puzzle = []
        self.num_guesses = 0
        self.known_indices = []

    def load_puzzle(self, puzzle_string):
        self.puzzle = []
        self.known_indices = []
        rows = [row for row in puzzle_string.split("\n") if row]
        self.n = len(rows)
        self.b = int(math.sqrt(self.n))
        for row_index, row in enumerate(rows):
            for col_index, c in enumerate(row):
                if c.isdigit():
                    self.puzzle.append(int(c))
                    if int(c) != 0:
                        self.known_indices.append((row_index * self.n) + col_index)

    def load_puzzle_from_file(self, path):
        with open(path, 'r') as f:
            self.load_puzzle(f.read())

    def to_string(self, pretty=True):
        return "".join(['\n' + str(c) if i % self.n == 0 else str(c) for i, c in enumerate(self.puzzle)])

    def __repl__(self):
        return self.to_string(pretty=False)

    def __str__(self):
        return self.to_string()

    def solve(self):
        start_time = datetime.now()
        self.num_guesses = 0
        r = self.solve_from(0, 1)
        while r is not None:
            r = self.solve_from(r[0], r[1])
        return datetime.now() - start_time

    def solve_from(self, index, starting_guess):
        if index < 0 or index > len(self.puzzle):
            raise Exception("Invalid puzzle index %s after %s guesses" % (index, self.num_guesses))

        last_valid_guess_index = None
        found_valid_guess = False
        for i in xrange(index, len(self.puzzle)):
            if i not in self.known_indices:
                found_valid_guess = False
                for guess in xrange(starting_guess, self.n + 1):
                    self.num_guesses += 1
                    if self.valid(i, guess):
                        found_valid_guess = True
                        last_valid_guess_index = i
                        self.puzzle[i] = guess
                        break

                starting_guess = 1
                if not found_valid_guess:
                    break
        
        if not found_valid_guess:
            new_index = last_valid_guess_index if last_valid_guess_index is not None else index - 1
            new_starting_guess = self.puzzle[new_index] + 1
            self.reset_puzzle_at(new_index)

            while new_starting_guess > self.n or new_index in self.known_indices:
                new_index -= 1
                new_starting_guess = self.puzzle[new_index] + 1
                self.reset_puzzle_at(new_index)
            
            return (new_index, new_starting_guess)
        else:
            return None

    def reset_puzzle_at(self, index):
        for i in xrange(index, len(self.puzzle)):
            if i not in self.known_indices:
                self.puzzle[i] = 0

    def valid_for_row(self, index, guess):
        row_index = int(math.floor(index / self.n))
        start = self.n * row_index
        finish = start + self.n
        for c_index in xrange(start, finish):
            if c_index != index and self.puzzle[c_index] == guess:
                return False
        return True

    def valid_for_column(self, index, guess):
        col_index = index % self.n
        for r in xrange(0, self.n):
            r_index = col_index + (self.n * r)
            if r_index != index and self.puzzle[r_index] == guess:
                return False
        return True

    def valid_for_block(self, index, guess):
        row_index = int(math.floor(index / self.n))
        col_index = index % self.n

        block_row = int(math.floor(row_index / self.b))
        block_col = int(math.floor(col_index / self.b))

        row_start = block_row * self.b
        row_end = row_start + self.b - 1
        col_start = block_col * self.b
        col_end = col_start + self.b - 1

        for r in xrange(row_start, row_end + 1):
            for c in xrange(col_start, col_end + 1):
                i = c + (r * self.n)
                if self.puzzle[i] == guess:
                    return False

        return True

    def valid(self, index, guess):
        return self.valid_for_row(index, guess) and self.valid_for_column(index, guess) and self.valid_for_block(index, guess)


if __name__ == "__main__":
    import sys

    s = Sudoku()
    s.load_puzzle_from_file(sys.argv[1])

    print "\nPuzzle:\n%s" % (s)

    time = s.solve()
    print "\nSolution:\n%s" % (s)
    print "\nNumber of guesses: %s" % (s.num_guesses)
    print "Total time: %s" % (time) 

