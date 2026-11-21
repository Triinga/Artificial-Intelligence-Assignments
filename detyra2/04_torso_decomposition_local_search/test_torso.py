"""Teste: python -m unittest test_torso -v"""

import itertools
import random
import unittest

from torso import (Graph, evaluate, front_from_widths, hypervolume, outdegrees, select_best_subset,
                   staircase_hv, suffix_widths)

README_EDGES = [(0, 1), (0, 2), (1, 6), (2, 8), (3, 8), (3, 9), (4, 5), (4, 6), (4, 7)]


def literal_outdegrees(g, perm):
    """Procedura zyrtare fjalë për fjalë: skano permutacionin, shto brinjët {v,w} mes fqinjëve dalës."""
    pos = {v: i for i, v in enumerate(perm)}
    adj = {v: set() for v in range(g.n)}
    for u, v in g.edges:
        adj[u].add(v)
        adj[v].add(u)
    for u in perm:
        out = [v for v in adj[u] if pos[v] > pos[u]]
        for v, w in itertools.combinations(out, 2):
            if w not in adj[v]:
                adj[v].add(w)
                adj[w].add(v)
    return [sum(1 for v in adj[u] if pos[v] > pos[u]) for u in perm]


def random_graph(n, p, rng):
    edges = [(i, i + 1) for i in range(n - 1)]          # i lidhur
    edges += [(u, v) for u in range(n) for v in range(u + 2, n) if rng.random() < p]
    return Graph(n, edges)


class Tests(unittest.TestCase):
    def test_readme_example(self):
        g = Graph(10, README_EDGES)
        self.assertEqual(evaluate(g, [0, 1, 2, 4, 5, 3, 6, 8, 9, 7, 6]), (4, 2))

    def test_fill_matches_literal_procedure(self):
        rng = random.Random(0)
        for _ in range(200):
            n = rng.randint(2, 25)
            g = random_graph(n, rng.choice([0.05, 0.15, 0.3]), rng)
            perm = list(range(n))
            rng.shuffle(perm)
            self.assertEqual(outdegrees(g, perm), literal_outdegrees(g, perm))

    def test_hypervolume_and_subset(self):
        w = [5, 5, 4, 4, 3, 2, 2, 1, 0, 0]
        pts = front_from_widths(w)
        self.assertEqual(pts, [(0, 5), (2, 4), (4, 3), (5, 2), (7, 1), (8, 0)])
        self.assertEqual(hypervolume(pts, 10), staircase_hv(w))
        # nën-bashkësia optimale me DP = maksimumi me forcë brutale
        for k in (1, 2, 3, 4):
            best = max(hypervolume(list(c), 10) for c in itertools.combinations(pts, k))
            self.assertEqual(hypervolume(select_best_subset(pts, 10, k), 10), best)

    def test_suffix_widths_monotone(self):
        g = random_graph(30, 0.2, random.Random(1))
        w = suffix_widths(outdegrees(g, list(range(30))))
        self.assertTrue(all(a >= b for a, b in zip(w, w[1:])))
        self.assertEqual(w[-1], 0)


if __name__ == "__main__":
    unittest.main()
