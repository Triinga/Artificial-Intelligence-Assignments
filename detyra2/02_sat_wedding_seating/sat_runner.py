"""
Ekzekutimi i një SAT solver-i (PySAT) me limit kohe.

Disa solver-a (p.sh. CaDiCaL) nuk e mbështesin `interrupt()`, prandaj kur jepet limit kohe
zgjidhja bëhet në një proces të veçantë që ndërpritet nëse e kalon limitin. Koha matet brenda
procesit (vetëm `solve()`), pra nuk përfshin nisjen e procesit.
"""

from __future__ import annotations

import multiprocessing as mp
import time


def _solve(clauses, solver_name):
    from pysat.solvers import Solver

    with Solver(name=solver_name, bootstrap_with=clauses) as s:
        t0 = time.perf_counter()
        sat = s.solve()
        dt = time.perf_counter() - t0
        return {"status": "SAT" if sat else "UNSAT", "model": s.get_model() if sat else None,
                "seconds": dt, "stats": s.accum_stats() or {}}


def _worker(clauses, solver_name, q):
    q.put(_solve(clauses, solver_name))


def solve(clauses, solver_name: str = "cadical195", time_limit: float | None = None) -> dict:
    """Kthen {"status": SAT|UNSAT|TIMEOUT, "model", "seconds", "stats"}."""
    if not time_limit:
        return _solve(clauses, solver_name)
    q = mp.Queue()
    p = mp.Process(target=_worker, args=(clauses, solver_name, q), daemon=True)
    p.start()
    try:
        res = q.get(timeout=time_limit + 5)    # +5 s për nisjen e procesit dhe ngarkimin e formulës
    except Exception:
        res = None
    if res is None or res["seconds"] > time_limit:
        if p.is_alive():
            p.terminate()
        p.join()
        return {"status": "TIMEOUT", "model": None, "seconds": time_limit, "stats": {}}
    p.join()
    return res
