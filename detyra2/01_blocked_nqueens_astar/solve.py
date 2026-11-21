"""
Zgjidh një instancë Blocked N-Queens me A*.

    python solve.py instances/example_page.lp
    python solve.py instances/example_page.lp --heuristic h2
    python solve.py --random 16 --density 0.3 --seed 2026
    python solve.py --random 12 --density 0.2 --seed 1 --save-instance my_board.lp --out solution.lp
"""

from __future__ import annotations

import argparse
import sys

from astar import DESCRIPTIONS, HEURISTICS, astar
from board import load_instance, random_board, render, solution_to_asp, to_asp, verify


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):               # konsola e Windows -> UTF-8
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Blocked N-Queens me A*")
    ap.add_argument("file", nargs="?", help="instanca në formatin ASP (num/block)")
    ap.add_argument("--random", type=int, metavar="N", help="gjenero tabelë të rastësishme N x N")
    ap.add_argument("--density", type=float, default=0.2, help="probabiliteti i bllokimit të qelizës")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--heuristic", choices=sorted(HEURISTICS), default="h4")
    ap.add_argument("--tie", choices=["deep", "fifo"], default="deep")
    ap.add_argument("--max-expanded", type=int, default=1_000_000)
    ap.add_argument("--time-limit", type=float, default=60.0)
    ap.add_argument("--save-instance", metavar="PATH", help="ruaj instancën në format ASP")
    ap.add_argument("--out", metavar="PATH", help="ruaj zgjidhjen si fakte queen(i,j).")
    args = ap.parse_args(argv)

    if args.file:
        board = load_instance(args.file)
    elif args.random:
        board = random_board(args.random, args.density, args.seed)
    else:
        ap.error("jep një skedar ose --random N")
    if args.save_instance:
        with open(args.save_instance, "w", encoding="utf-8") as fh:
            fh.write(to_asp(board))

    print(f"Instanca: {board.name}  N={board.n}  të bllokuara={len(board.blocked)} ({board.density:.0%})")
    print(f"Heuristika: {args.heuristic} – {DESCRIPTIONS[args.heuristic]}")
    r = astar(board, args.heuristic, args.tie, args.max_expanded, args.time_limit)
    print(f"Statusi: {r.status} | zgjeruara={r.expanded} gjeneruara={r.generated} "
          f"krasitura={r.pruned} max_open={r.max_open} koha={r.seconds:.3f}s")

    if r.solution is None:
        if r.status == "no_solution":
            print("Instanca NUK ka zgjidhje.")
        return 1
    errors = verify(board, r.solution)
    print("Verifikimi:", "OK" if not errors else "GABIM: " + "; ".join(errors))
    print()
    print(render(board, r.solution))
    print()
    print(solution_to_asp(r.solution))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(solution_to_asp(r.solution) + "\n")
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
