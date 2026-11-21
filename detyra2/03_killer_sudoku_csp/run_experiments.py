"""
Krahasimi i solver-ave për 4 puzzle-t (easy / medium / hard / expert):

    python run_experiments.py        (~30 s)

* solver-i CSP me teknikat e aktivizuara një nga një (BT, +FC, +MRV, +kombinimet e kafazeve);
* OR-Tools CP-SAT (dhe kontrolli që zgjidhja është unike).
Rezultatet: results/results.md
"""

from __future__ import annotations

import os
import sys

from cpsat_solver import solve_cpsat
from csp_solver import solve_csp
from killer import load_puzzle, render, verify

HERE = os.path.dirname(os.path.abspath(__file__))
PUZZLES = ["easy", "medium", "hard", "expert"]
VARIANTS = [
    ("BT", dict(fc=False, mrv=False, combos=False)),
    ("BT + FC", dict(mrv=False, combos=False)),
    ("BT + FC + MRV", dict(combos=False)),
    ("BT + FC + MRV + kombinime", dict()),
]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rows, grids = [], []
    for name in PUZZLES:
        p = load_puzzle(os.path.join(HERE, "puzzles", f"{name}.txt"))
        n_given = sum(1 for g in p.givens if g)
        for label, kw in VARIANTS:
            r = solve_csp(p, 120, **kw)
            ok = "OK" if r["grid"] and not verify(p, r["grid"]) else "—"
            rows.append([name, label, r["status"], ok, f"{r['seconds'] * 1000:.1f}", r["nodes"], r["backtracks"]])
            print(" | ".join(map(str, rows[-1])), flush=True)
        c = solve_cpsat(p, 60, count_limit=2)
        ok = "OK" if c["grid"] and not verify(p, c["grid"]) else "—"
        uniq = "unike" if c["solutions"] == 1 else f"{c['solutions']} zgjidhje"
        rows.append([name, f"CP-SAT ({uniq})", c["status"], ok, f"{c['seconds'] * 1000:.1f}",
                     f"{c['branches']} degëzime", f"{c['conflicts']} konflikte"])
        print(" | ".join(map(str, rows[-1])), flush=True)
        grids.append((name, len(p.cages), n_given, render(p, c["grid"])))

    head = ["puzzle", "solver", "statusi", "verifikimi", "koha (ms)", "nyje", "backtrack"]
    md = ["# Rezultatet – Killer Sudoku", "",
          "`python run_experiments.py`. *nyje* = vlera të provuara, *backtrack* = vlera që dështuan. "
          "Për CP-SAT jepen degëzimet dhe konfliktet e solver-it; CP-SAT kërkon edhe një zgjidhje të dytë "
          "për të vërtetuar unicitetin.", "",
          "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    md += ["| " + " | ".join(map(str, r)) + " |" for r in rows]
    md += ["", "## Zgjidhjet", ""]
    for name, n_cages, n_given, g in grids:
        md += [f"**{name}** ({n_cages} kafaze, {n_given} shifra të dhëna)", "", "```text", g, "```", ""]
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "results.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    print("\nU ruajt: results/results.md")


if __name__ == "__main__":
    main()
