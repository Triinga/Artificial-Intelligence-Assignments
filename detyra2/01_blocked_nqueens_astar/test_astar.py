"""Teste: python -m unittest test_astar -v"""

import itertools
import os
import unittest

from astar import HEURISTICS, INF, Context, astar
from board import Board, load_instance, random_board, verify

HERE = os.path.dirname(os.path.abspath(__file__))


def solvable_brute_force(board):
    return any(not verify(board, p) for p in itertools.permutations(range(board.n)))


class Tests(unittest.TestCase):
    def test_page_example(self):
        b = load_instance(os.path.join(HERE, "instances", "example_page.lp"))
        self.assertEqual((b.n, b.blocked), (4, {(0, 0), (1, 1), (3, 2)}))
        self.assertEqual(verify(b, (2, 0, 3, 1)), [])   # zgjidhja e dhënë në faqe
        for h in HEURISTICS:
            r = astar(b, h)
            self.assertEqual(r.status, "solved")
            self.assertEqual(verify(b, r.solution), [])

    def test_matches_brute_force(self):
        """Në 45 tabela të vogla A* (me çdo heuristikë) gjen zgjidhje ⇔ zgjidhja ekziston."""
        for n in (4, 5, 6):
            for seed in range(15):
                b = random_board(n, 0.25, seed)
                expected = solvable_brute_force(b)
                for h in HEURISTICS:
                    for tie in ("deep", "fifo"):
                        self.assertEqual(astar(b, h, tie).status == "solved", expected, (n, seed, h, tie))

    def test_admissible(self):
        """h1, h2, h4 ≤ h* në çdo gjendje të arritshme (h* llogaritet me forcë brutale)."""
        for seed in range(10):
            b = random_board(6, 0.2, seed)
            ctx, n = Context(b), b.n

            def h_star(cols):
                rest = [c for c in range(n) if c not in cols]
                ok = any(not verify(b, tuple(cols) + p) for p in itertools.permutations(rest))
                return n - len(cols) if ok else INF

            def walk(cols, cm, d1, d2):
                for name in ("h1", "h2", "h4"):
                    self.assertLessEqual(HEURISTICS[name](ctx, len(cols), cm, d1, d2), h_star(cols))
                g = len(cols)
                if g < n:
                    for c in range(n):
                        if ctx.safe(g, cm, d1, d2) >> c & 1:
                            walk(cols + (c,), cm | 1 << c, d1 | 1 << (c - g + n - 1), d2 | 1 << (g + c))

            walk((), 0, 0, 0)

    def test_unsat(self):
        b = Board(8, {(r, 3) for r in range(8)})          # një kolonë e bllokuar plotësisht
        r = astar(b, "h4")
        self.assertEqual((r.status, r.expanded), ("no_solution", 0))
        self.assertEqual(astar(load_instance(os.path.join(HERE, "instances", "unsat_n3.lp")), "h4").status,
                         "no_solution")


if __name__ == "__main__":
    unittest.main()
