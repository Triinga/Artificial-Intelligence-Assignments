"""Teste: python -m unittest test_seating -v"""

import itertools
import os
import random
import unittest

from pysat.solvers import Solver

from encoding import Formula, SeatingEncoding, at_least_seqcounter, at_most_seqcounter, gender_bounds, verify_plan
from instance import Instance, generate, load_instance

HERE = os.path.dirname(os.path.abspath(__file__))


def small_instance(seed):
    """9 mysafirë, 3 tavolina × 3 vende, |burra - gra| <= 1."""
    rng = random.Random(seed)
    g = [f"M{i}" for i in range(1, 10)]
    pairs = list(itertools.combinations(g, 2))
    rng.shuffle(pairs)
    return Instance(g, {x: rng.choice("MF") for x in g}, pairs[:4], pairs[4:6], 3, 3, 1, f"small{seed}")


def brute_force(inst):
    for assign in itertools.product(range(inst.tables), repeat=inst.n):
        tables = [[g for g, t in zip(inst.guests, assign) if t == k] for k in range(inst.tables)]
        if not verify_plan(inst, tables):
            return True
    return False


def sat(clauses, assumptions=()):
    with Solver(name="cadical195", bootstrap_with=clauses) as s:
        return s.solve(assumptions=list(assumptions))


class Tests(unittest.TestCase):
    def test_seqcounter_exhaustive(self):
        """Për çdo n ≤ 7, k < n dhe çdo vlerësim të x: formula SAT ⇔ Σx ≤ k (dhe Σx ≥ k)."""
        for n in range(1, 8):
            for k in range(n):
                for at_most in (True, False):
                    f = Formula()
                    f.group("t")
                    xs = [f.new_var() for _ in range(n)]
                    (at_most_seqcounter if at_most else at_least_seqcounter)(f, xs, k)
                    for bits in itertools.product((0, 1), repeat=n):
                        want = sum(bits) <= k if at_most else sum(bits) >= k
                        self.assertEqual(sat(f.clauses, [x if b else -x for x, b in zip(xs, bits)]), want)

    def test_seqcounter_size(self):
        f = Formula()
        f.group("t")
        xs = [f.new_var() for _ in range(100)]
        at_most_seqcounter(f, xs, 10)
        self.assertEqual((f.nv - 100, len(f.clauses)), (99 * 10, 2 * 100 * 10 + 100 - 3 * 10 - 1))

    def test_gender_bounds(self):
        self.assertEqual(gender_bounds(10, 3), (4, 6))

    def test_against_brute_force(self):
        """25 instanca të vogla: SAT ⇔ brute force, me dhe pa thyerje simetrie."""
        results = []
        for seed in range(25):
            inst = small_instance(seed)
            expected = brute_force(inst)
            results.append(expected)
            for sym in (False, True):
                enc = SeatingEncoding(inst, symmetry=sym)
                with Solver(name="cadical195", bootstrap_with=enc.f.clauses) as s:
                    self.assertEqual(s.solve(), expected, (seed, sym))
                    if expected:
                        self.assertEqual(verify_plan(inst, enc.decode(s.get_model())), [])
        self.assertTrue(any(results) and not all(results))     # ka edhe SAT edhe UNSAT

    def test_repo_instances(self):
        for name, expected in (("sat_party", True), ("unsat_big_family", False), ("unsat_enemies", False)):
            inst = load_instance(os.path.join(HERE, "instances", name))
            self.assertEqual(sat(SeatingEncoding(inst).f.clauses), expected, name)

    def test_generator_is_sat(self):
        for seed in range(3):
            inst = generate(seed, n_conflicts=300, n_together=60)
            enc = SeatingEncoding(inst)
            with Solver(name="cadical195", bootstrap_with=enc.f.clauses) as s:
                self.assertTrue(s.solve())
                self.assertEqual(verify_plan(inst, enc.decode(s.get_model())), [])


if __name__ == "__main__":
    unittest.main()
