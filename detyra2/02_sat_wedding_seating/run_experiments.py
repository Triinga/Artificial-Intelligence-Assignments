"""
Eksperimentet (~5 min):

    python run_experiments.py

1) zgjidhja e instancave SAT / UNSAT me dhe pa thyerje simetrie (limit 60 s);
2) efekti i thyerjes së simetrisë në 4 instanca UNSAT me 11 armiq të zgjedhur rastësisht;
3) eksporti DIMACS i formulave në dimacs/.
Rezultatet: results/results.md
"""

from __future__ import annotations

import copy
import os
import random
import sys

from encoding import SeatingEncoding, verify_plan
from instance import load_instance
from sat_runner import solve

HERE = os.path.dirname(os.path.abspath(__file__))
TIME_LIMIT = 60.0


def run(inst, symmetry):
    enc = SeatingEncoding(inst, symmetry=symmetry)
    st = enc.stats()
    res = solve(enc.f.clauses, time_limit=TIME_LIMIT)
    verified = ""
    if res["status"] == "SAT":
        verified = "OK" if not verify_plan(inst, enc.decode(res["model"])) else "GABIM"
    status = f"TIMEOUT (> {TIME_LIMIT:.0f} s)" if res["status"] == "TIMEOUT" else res["status"]
    row = [inst.name, "po" if symmetry else "jo", st["variables"], st["clauses"], status, verified,
           f"{res['seconds']:.2f}" if res["status"] != "TIMEOUT" else "—", res["stats"].get("conflicts", "—")]
    print(" | ".join(map(str, row)), flush=True)
    return row


def table(rows):
    head = ["instanca", "simetri", "variabla", "klauzola", "rezultati", "verifikimi", "koha (s)", "konflikte"]
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] +
                     ["| " + " | ".join(map(str, r)) + " |" for r in rows])


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    names = ["sat_party", "unsat_big_family", "unsat_enemies"]
    insts = {n: load_instance(os.path.join(HERE, "instances", n)) for n in names}

    os.makedirs(os.path.join(HERE, "dimacs"), exist_ok=True)
    for n in names:
        SeatingEncoding(insts[n]).to_dimacs(os.path.join(HERE, "dimacs", f"{n}.cnf"))

    rows1 = [run(insts[n], s) for n in names for s in (False, True)]

    rows2 = []
    base = insts["sat_party"]
    for seed in (11, 12, 13, 14):
        inst = copy.deepcopy(base)
        group = random.Random(seed).sample(base.guests, 11)
        inst.conflicts += [(group[i], group[j]) for i in range(11) for j in range(i + 1, 11)]
        inst.name = f"armiq11_seed{seed}"
        rows2 += [run(inst, False), run(inst, True)]

    md = ["# Rezultatet – SAT: ulja e mysafirëve", "",
          f"`python run_experiments.py` – solver CaDiCaL 1.9.5 (PySAT), limit {TIME_LIMIT:.0f} s.", "",
          "## Instancat SAT / UNSAT", "", table(rows1), "",
          "## Thyerja e simetrisë: sat_party + 11 armiq të zgjedhur rastësisht (UNSAT)", "", table(rows2), ""]
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "results.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    print("\nU ruajt: results/results.md")


if __name__ == "__main__":
    main()
