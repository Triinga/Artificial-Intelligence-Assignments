"""
Killer Sudoku me Google OR-Tools CP-SAT (Constraint Programming), për krahasim.

Modeli: x[i] ∈ {1..9} për 81 qelizat; AddAllDifferent për rreshtat, kolonat, kutitë dhe kafazet;
Σ x[i] = S për çdo kafaz; x[i] = d për shifrat e dhëna. Opsionalisht numërohen zgjidhjet (për të kontrolluar unicitetin).
"""

from __future__ import annotations

import time

from ortools.sat.python import cp_model

from killer import UNITS, Puzzle


def build_model(p: Puzzle):
    m = cp_model.CpModel()
    x = [m.NewIntVar(1, 9, f"x{i}") for i in range(81)]
    for unit in UNITS:
        m.AddAllDifferent([x[i] for i in unit])
    for cage in p.cages:
        m.AddAllDifferent([x[i] for i in cage.cells])
        m.Add(sum(x[i] for i in cage.cells) == cage.total)
    for i, d in enumerate(p.givens):
        if d:
            m.Add(x[i] == d)
    return m, x


class _Counter(cp_model.CpSolverSolutionCallback):
    def __init__(self, x, limit):
        super().__init__()
        self.x, self.limit, self.count, self.first = x, limit, 0, None

    def on_solution_callback(self):
        self.count += 1
        if self.first is None:
            self.first = [self.Value(v) for v in self.x]
        if self.count >= self.limit:
            self.StopSearch()


def solve_cpsat(p: Puzzle, time_limit: float = 60.0, count_limit: int = 0) -> dict:
    """count_limit = 0: vetëm një zgjidhje; count_limit = 2: kontrollon nëse zgjidhja është unike."""
    m, x = build_model(p)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_workers = 1 if count_limit else 8
    solver.parameters.random_seed = 2026
    t0 = time.perf_counter()
    if count_limit:
        solver.parameters.enumerate_all_solutions = True
        cb = _Counter(x, count_limit)
        status = solver.Solve(m, cb)
        grid, n_sol = cb.first, cb.count
    else:
        status = solver.Solve(m)
        grid = [solver.Value(v) for v in x] if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
        n_sol = None
    dt = time.perf_counter() - t0
    name = "solved" if grid else ("no_solution" if status == cp_model.INFEASIBLE else "timeout")
    return {"grid": grid, "status": name, "seconds": dt, "branches": solver.NumBranches(),
            "conflicts": solver.NumConflicts(), "solutions": n_sol}
