"""Teste: python -m unittest test_killer -v"""

import random
import unittest

from cpsat_solver import solve_cpsat
from csp_solver import COMBOS, solve_csp
from killer import Cage, Puzzle, validate, verify


def random_solved_grid(rng):
    """Rrjetë e saktë Sudoku: modeli bazë + ndërrime që ruajnë rregullat."""
    base = [[(3 * (r % 3) + r // 3 + c) % 9 + 1 for c in range(9)] for r in range(9)]
    digits = list(range(1, 10))
    rng.shuffle(digits)
    rows = [b * 3 + r for b in rng.sample(range(3), 3) for r in rng.sample(range(3), 3)]
    cols = [b * 3 + c for b in rng.sample(range(3), 3) for c in rng.sample(range(3), 3)]
    return [digits[base[r][c] - 1] for r in rows for c in cols]


def random_puzzle(seed, max_size=4):
    """Ndan rrjetën në kafaze të lidhura (pa shifra të përsëritura brenda kafazit)."""
    rng = random.Random(seed)
    grid = random_solved_grid(rng)
    free = set(range(81))
    cages = []
    while free:
        start = min(free)
        cells, digits = [start], {grid[start]}
        free.discard(start)
        target = rng.randint(1, max_size)
        while len(cells) < target:
            options = [n for c in cells for n in (c - 9, c + 9, c - 1 if c % 9 else -1, c + 1 if c % 9 < 8 else -1)
                       if n in free and grid[n] not in digits]
            if not options:
                break
            n = rng.choice(options)
            cells.append(n)
            digits.add(grid[n])
            free.discard(n)
        cages.append(Cage(sum(grid[c] for c in cells), cells))
    return Puzzle(f"rand{seed}", cages), grid


class Tests(unittest.TestCase):
    def test_combos(self):
        self.assertEqual(COMBOS[2][3], [0b110])                    # {1,2}
        self.assertEqual(len(COMBOS[9][45]), 1)
        self.assertEqual(COMBOS[2][17], [(1 << 8) | (1 << 9)])     # {8,9}

    def test_random_puzzles_both_solvers(self):
        for seed in range(15):
            p, _ = random_puzzle(seed)
            validate(p)
            for r in (solve_csp(p), solve_cpsat(p)):
                self.assertEqual(r["status"], "solved", seed)
                self.assertEqual(verify(p, r["grid"]), [])

    def test_unsat_detected(self):
        """Dy kafaze 1-qelizore në të njëjtin rresht me të njëjtën shifër -> pa zgjidhje."""
        p, grid = random_puzzle(1, max_size=1)                   # çdo qelizë = kafaz me 1 qelizë
        by_cell = {c.cells[0]: c for c in p.cages}
        by_cell[1].total = by_cell[0].total                      # A2 = A1
        self.assertEqual(solve_csp(p)["status"], "no_solution")
        self.assertEqual(solve_cpsat(p)["status"], "no_solution")

    def test_verify_detects_errors(self):
        p, grid = random_puzzle(3)
        bad = grid[:]
        bad[0], bad[1] = bad[1], bad[0]
        self.assertTrue(verify(p, bad))


if __name__ == "__main__":
    unittest.main()
