"""
Ulja e 100 mysafirëve në 10 tavolina me SAT (PySAT, solver CaDiCaL).

    python solve.py instances/sat_party
    python solve.py instances/unsat_big_family
    python solve.py instances/sat_party --dimacs dimacs/sat_party.cnf
    python solve.py instances/unsat_enemies --no-symmetry --time-limit 60
    python solve.py --random 7 --conflicts 300 --together 60 --save-instance instances/my_party
"""

from __future__ import annotations

import argparse
import os
import sys

from encoding import SeatingEncoding, gender_bounds, verify_plan
from instance import generate, load_instance, save_instance
from sat_runner import solve


def print_plan(inst, tables):
    for t, members in enumerate(tables):
        men = sum(inst.gender[g] == "M" for g in members)
        names = ", ".join(f"{g}({inst.gender[g]})" for g in sorted(members, key=lambda g: int(g[1:])))
        print(f"Tavolina {t + 1:2d} [{men} burra / {len(members) - men} gra]: {names}")


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Ulja e mysafirëve me SAT")
    ap.add_argument("instance", nargs="?", help="folder me guests.csv, conflicts.csv, together.csv")
    ap.add_argument("--random", type=int, metavar="SEED", help="gjenero instancë të rastësishme (SAT e garantuar)")
    ap.add_argument("--conflicts", type=int, default=150)
    ap.add_argument("--together", type=int, default=40)
    ap.add_argument("--save-instance", metavar="DIR")
    ap.add_argument("--no-symmetry", action="store_true", help="pa thyerje të simetrisë së tavolinave")
    ap.add_argument("--time-limit", type=float, default=None, help="sekonda (default pa limit)")
    ap.add_argument("--dimacs", metavar="PATH", help="eksporto formulën në DIMACS .cnf")
    args = ap.parse_args(argv)

    if args.instance:
        inst = load_instance(args.instance)
    elif args.random is not None:
        inst = generate(args.random, args.conflicts, args.together)
        if args.save_instance:
            save_instance(inst, args.save_instance, f"generate(seed={args.random})")
    else:
        ap.error("jep një folder instance ose --random SEED")

    lo, hi = gender_bounds(inst.capacity, inst.max_diff)
    print(f"Instanca: {inst.name} | {inst.n} mysafirë ({len(inst.men())} burra), {inst.tables} tavolina × "
          f"{inst.capacity} | {len(inst.conflicts)} konflikte, {len(inst.together)} çifte bashkë | "
          f"burra për tavolinë ∈ [{lo}, {hi}]")
    enc = SeatingEncoding(inst, symmetry=not args.no_symmetry)
    st = enc.stats()
    print(f"Formula: {st['variables']} variabla ({st['primary']} x(i,t) + {st['aux']} ndihmëse), "
          f"{st['clauses']} klauzola")
    for name, g in st["groups"].items():
        if g["clauses"]:
            print(f"   {name:<44} {g['clauses']:>6} klauzola  {g['aux']:>5} ndihmëse")
    if args.dimacs:
        os.makedirs(os.path.dirname(os.path.abspath(args.dimacs)), exist_ok=True)
        enc.to_dimacs(args.dimacs)
        print("DIMACS:", args.dimacs)

    res = solve(enc.f.clauses, time_limit=args.time_limit)
    print(f"Rezultati: {res['status']} ({res['seconds']:.3f} s, konflikte = {res['stats'].get('conflicts', '-')})")
    if res["status"] != "SAT":
        if res["status"] == "UNSAT":
            print("Nuk ekziston asnjë plan uljeje që plotëson të gjitha kushtet.")
        return 1
    tables = enc.decode(res["model"])
    print_plan(inst, tables)
    errors = verify_plan(inst, tables)
    print("Verifikimi i kushteve (a)–(d):", "OK" if not errors else "GABIM")
    for e in errors:
        print("  ", e)
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
