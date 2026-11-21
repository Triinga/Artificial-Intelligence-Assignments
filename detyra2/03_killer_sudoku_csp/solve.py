"""
Zgjidh një Killer Sudoku me solver-in CSP (nga zero) dhe/ose me OR-Tools CP-SAT.

    python solve.py puzzles/easy.txt
    python solve.py puzzles/expert.txt --solver cpsat
    python solve.py puzzles/hard.txt --solver both --unique
"""

from __future__ import annotations

import argparse
import sys

from cpsat_solver import solve_cpsat
from csp_solver import solve_csp
from killer import load_puzzle, render, verify


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Killer Sudoku me CSP")
    ap.add_argument("puzzle", help="skedari .txt ose .json")
    ap.add_argument("--solver", choices=["csp", "cpsat", "both"], default="both")
    ap.add_argument("--unique", action="store_true", help="kontrollo me CP-SAT nëse zgjidhja është unike")
    ap.add_argument("--time-limit", type=float, default=60.0)
    args = ap.parse_args(argv)

    p = load_puzzle(args.puzzle)
    print(f"Puzzle: {p.name} | {len(p.cages)} kafaze")
    print(render(p))
    code = 0
    if args.solver in ("csp", "both"):
        r = solve_csp(p, args.time_limit)
        print(f"\nCSP (backtracking + MRV + forward checking): {r['status']}, {r['seconds']:.3f} s, "
              f"nyje = {r['nodes']}, backtrack = {r['backtracks']}")
        if r["grid"]:
            print(render(p, r["grid"]))
            errors = verify(p, r["grid"])
            print("Verifikimi:", "OK" if not errors else errors)
            code |= bool(errors)
    if args.solver in ("cpsat", "both"):
        r = solve_cpsat(p, args.time_limit, 2 if args.unique else 0)
        print(f"\nCP-SAT: {r['status']}, {r['seconds']:.3f} s, degëzime = {r['branches']}, konflikte = {r['conflicts']}")
        if r["grid"]:
            if args.solver == "cpsat":
                print(render(p, r["grid"]))
            print("Verifikimi:", "OK" if not verify(p, r["grid"]) else verify(p, r["grid"]))
        if args.unique:
            print("Zgjidhja është", "UNIKE" if r["solutions"] == 1 else f"JO unike ({r['solutions']}+ zgjidhje)")
    return code


if __name__ == "__main__":
    sys.exit(main())
