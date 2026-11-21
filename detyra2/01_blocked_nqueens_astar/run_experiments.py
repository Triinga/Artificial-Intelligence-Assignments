"""
Eksperimentet: krahasimi i heuristikave h1–h4 me A*.

    python run_experiments.py        (~5 min)

Rezultatet ruhen në results/results.md dhe results/results.csv.
Limiti për çdo ekzekutim: 100 000 nyje të zgjeruara (numri i nyjave nuk varet nga kompjuteri).
"""

from __future__ import annotations

import csv
import os
import sys

from astar import HEURISTICS, astar
from board import Board, load_instance, random_board, verify

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 2026
MAX_EXPANDED = 100_000
TIME_LIMIT = 120.0   # vetëm siguri; limiti real është numri i nyjave (rezultate deterministe)


def instances() -> list[Board]:
    inst = os.path.join(HERE, "instances")
    boards = [load_instance(os.path.join(inst, "example_page.lp")),
              load_instance(os.path.join(inst, "unsat_n3.lp")),
              Board(8, {(r, 3) for r in range(8)}, "unsat_kolona4_n8")]   # kolona 4 e bllokuar
    for n in (8, 12, 16, 20, 24, 28):
        for d in (0.1, 0.3):
            boards.append(random_board(n, d, SEED))
    boards.append(load_instance(os.path.join(inst, "official", "156.48.1960.36.1721297189.dat")))
    return boards


def run(board, h, tie="deep"):
    r = astar(board, h, tie, MAX_EXPANDED, TIME_LIMIT)
    if r.solution is not None:
        assert not verify(board, r.solution), board.name
    return {"instanca": board.name, "N": board.n, "bllokuara": len(board.blocked),
            "heuristika": h, "tie": tie, "statusi": r.status, "zgjeruara": r.expanded,
            "gjeneruara": r.generated, "krasitura": r.pruned, "max_open": r.max_open,
            "nyje_ne_memorie": r.max_open + r.closed, "koha_s": round(r.seconds, 3)}


STATUS = {"solved": "✔ zgjidhur", "no_solution": "✘ pa zgjidhje (vërtetuar)",
          "node_limit": "limit nyjash", "time_limit": "limit kohe"}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rows = []
    for b in instances():
        for h in HEURISTICS:
            row = run(b, h)
            rows.append(row)
            print(f"{b.name:<32} {h} {row['statusi']:<11} zgjeruara={row['zgjeruara']:<7} "
                  f"koha={row['koha_s']}s", flush=True)

    # Tie-breaking: me h1 vlera f = N është e njëjtë për të gjitha nyjat.
    tie_rows = [run(random_board(n, 0.2, SEED), "h1", t) for n in (8, 10, 12) for t in ("fifo", "deep")]

    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "results.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows + tie_rows)

    cols = ["instanca", "N", "heuristika", "statusi", "zgjeruara", "gjeneruara", "krasitura",
            "nyje_ne_memorie", "koha_s"]

    def table(rs, cols=cols):
        out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        for r in rs:
            out.append("| " + " | ".join(STATUS.get(str(r[c]), str(r[c])) if c == "statusi" else str(r[c])
                                         for c in cols) + " |")
        return "\n".join(out)

    summary = ["| heuristika | të përfunduara | Σ zgjeruara | Σ koha (s) |", "|---|---|---|---|"]
    for h in HEURISTICS:
        rs = [r for r in rows if r["heuristika"] == h]
        ok = sum(r["statusi"] in ("solved", "no_solution") for r in rs)
        summary.append(f"| {h} | {ok}/{len(rs)} | {sum(r['zgjeruara'] for r in rs)} | "
                       f"{sum(r['koha_s'] for r in rs):.2f} |")

    md = ["# Rezultatet – Blocked N-Queens me A*", "",
          f"`python run_experiments.py` – seed {SEED}, limit {MAX_EXPANDED} nyje të zgjeruara, tie = deep.",
          "*nyje_ne_memorie* = max |open| + |closed|.", "",
          "## Përmbledhje", "", "\n".join(summary), "",
          "## Të gjitha ekzekutimet", "", table(rows), "",
          "## Tie-breaking me h1 (FIFO kundrejt deep)", "", table(tie_rows, ["instanca", "N", "heuristika", "tie", "statusi", "zgjeruara", "nyje_ne_memorie", "koha_s"]), ""]
    with open(os.path.join(HERE, "results", "results.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    print("\nU ruajt: results/results.md")


if __name__ == "__main__":
    main()
