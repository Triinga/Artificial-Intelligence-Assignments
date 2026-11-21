"""
Ekzekutimi i plotë për Torso Decompositions (përdoret lokalisht dhe në Kaggle).

    python run.py --seconds 30                 # provë e shpejtë lokale
    python run.py --seconds 900 --seeds 2      # versioni i Kaggle (paralel në të gjitha CPU-të)

Hapat:
1. zgjidhjet konstruktive (min-degree, min-fill) për çdo instancë;
2. SA dhe ILS për çdo instancë dhe çdo seed, paralelisht (multiprocessing);
3. bashkimi i fronteve, zgjedhja e ≤ 20 pikave me hypervolume maksimal (DP);
4. verifikimi i çdo vektori me vlerësimin e pavarur `torso.evaluate`;
5. dalja: submissions/*.json, results/results.md, results/*.png, results/summary.json.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import random
import time

from search import Evaluator, hv_of, iterated_local_search, min_degree_order, min_fill_order, simulated_annealing
from torso import (CHALLENGE_ID, PROBLEM_IDS, WIDTH_CAP, evaluate, front_from_widths, hypervolume,
                   load_graph, pareto_filter, select_best_subset)

INSTANCES = ["easy", "medium", "hard"]
ALGOS = {"SA": simulated_annealing, "ILS": iterated_local_search}


def constructive(name, data_dir):
    g = load_graph(os.path.join(data_dir, f"{name}.gr"))
    out = {}
    t = time.perf_counter()
    out["min-degree"] = (min_degree_order(g), time.perf_counter() - t)
    if g.m < 50_000:                      # min-fill është shumë i shtrenjtë për grafin hard
        t = time.perf_counter()
        out["min-fill"] = (min_fill_order(g), time.perf_counter() - t)
    return out


def task(args):
    name, algo, seed, start, seconds, data_dir = args
    g = load_graph(os.path.join(data_dir, f"{name}.gr"))
    r = ALGOS[algo](g, start, seconds, seed)
    pts = pareto_filter(r["archive"].points())
    keep = {wt: r["archive"].best[wt] for _, wt in pts}          # vetëm pikat jo-dominuese
    return {"instance": name, "algo": algo, "seed": seed, "best_hv": r["best_hv"], "evals": r["evals"],
            "history": r["history"], "archive": keep,
            "hv20": hypervolume(select_best_subset(pts, g.n), g.n), "n_points": len(pts)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=30)
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--data", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    args = ap.parse_args()
    res_dir, sub_dir = os.path.join(args.out, "results"), os.path.join(args.out, "submissions")
    os.makedirs(res_dir, exist_ok=True)
    os.makedirs(sub_dir, exist_ok=True)
    t_all = time.perf_counter()

    # 1. konstruktive
    graphs, starts, cons_rows = {}, {}, []
    for name in INSTANCES:
        g = graphs[name] = load_graph(os.path.join(args.data, f"{name}.gr"))
        cons = constructive(name, args.data)
        for cname, (perm, secs) in cons.items():
            w = Evaluator(g, perm).widths()
            pts = front_from_widths(w)
            cons_rows.append({"instance": name, "method": cname, "seconds": round(secs, 2),
                              "width_t0": w[0], "staircase_hv": hv_of(w),
                              "hv20": hypervolume(select_best_subset(pts, g.n), g.n), "perm": perm, "w": w})
        best = max((r for r in cons_rows if r["instance"] == name), key=lambda r: r["staircase_hv"])
        starts[name] = best["perm"]
        print(f"[{name}] n={g.n} m={g.m} | " + ", ".join(
            f"{r['method']}: w(t=0)={r['width_t0']} HV={r['staircase_hv']}" for r in cons_rows if r["instance"] == name),
            flush=True)

    # 2. metaheuristikat (paralel)
    tasks = [(name, algo, seed, starts[name], args.seconds, args.data)
             for name in INSTANCES for algo in ALGOS for seed in range(1, args.seeds + 1)]
    print(f"{len(tasks)} ekzekutime × {args.seconds:.0f} s në {args.workers} procese ...", flush=True)
    with mp.Pool(min(args.workers, len(tasks))) as pool:
        runs = pool.map(task, tasks)
    for r in runs:
        print(f"[{r['instance']}] {r['algo']} seed={r['seed']}: staircase HV {r['history'][0][2]} -> {r['best_hv']}, "
              f"HV20 = {r['hv20']}, evals = {r['evals']}", flush=True)

    # 3–4. bashkimi, zgjedhja e 20 pikave, verifikimi, dorëzimi
    summary = {}
    for name in INSTANCES:
        g = graphs[name]
        pool_pts = {}                                          # gjerësia -> (t, perm)
        sources = [(r["archive"]) for r in runs if r["instance"] == name]
        for c in cons_rows:
            if c["instance"] == name:
                sources.append({wt: (t, c["perm"]) for t, wt in front_from_widths(c["w"])})
        for src in sources:
            for wt, (t, perm) in src.items():
                if wt not in pool_pts or t < pool_pts[wt][0]:
                    pool_pts[wt] = (t, perm)
        chosen = select_best_subset([(t, wt) for wt, (t, _) in pool_pts.items()], g.n)
        vectors = []
        for t, wt in chosen:
            x = list(pool_pts[wt][1]) + [t]
            size, width = evaluate(g, x)                       # vlerësim i pavarur
            assert (size, width) == (g.n - t, wt), "verifikimi dështoi"
            vectors.append(x)
        hv = hypervolume(chosen, g.n)
        summary[name] = {"n": g.n, "m": g.m, "hv": hv, "hv_normalized": hv / (g.n * WIDTH_CAP),
                         "points": [{"torso_size": g.n - t, "torso_width": wt} for t, wt in chosen]}
        with open(os.path.join(sub_dir, f"{name}_{PROBLEM_IDS[name]}.json"), "w") as fh:
            json.dump([{"decisionVector": vectors, "problem": PROBLEM_IDS[name], "challenge": CHALLENGE_ID,
                        "name": f"torso-{name}", "description": "SA + ILS, Detyra 2 AI (UP)"}], fh)
        print(f"[{name}] fronti final: {len(chosen)} pika, HV = {hv} (normalizuar {hv / (g.n * WIDTH_CAP):.4f})",
              flush=True)

    with open(os.path.join(res_dir, "summary.json"), "w") as fh:
        json.dump({"seconds_per_run": args.seconds, "seeds": args.seeds, "instances": summary,
                   "constructive": [{k: v for k, v in c.items() if k not in ("perm", "w")} for c in cons_rows],
                   "runs": [{k: v for k, v in r.items() if k != "archive"} for r in runs],
                   "total_seconds": time.perf_counter() - t_all}, fh)
    write_report(res_dir, args, graphs, cons_rows, runs, summary)
    plots(res_dir, graphs, cons_rows, runs, summary)
    print(f"Gjithsej {time.perf_counter() - t_all:.0f} s. Rezultatet në {res_dir}, dorëzimet në {sub_dir}")


def write_report(res_dir, args, graphs, cons_rows, runs, summary):
    md = ["# Rezultatet – Torso Decompositions (ESA SpOC-3)", "",
          f"{args.seconds:.0f} s për ekzekutim, {args.seeds} seed për algoritëm. Hypervolume: minimizim i (t, gjerësia), "
          f"pika e referencës (n, 501). *Staircase HV* = HV i frontit të plotë të një permutacioni (funksioni "
          f"objektiv); *HV20* = HV i 20 pikave më të mira (sa lejon dorëzimi).", "",
          "## Instancat dhe zgjidhjet konstruktive", "",
          "| instanca | n | m | metoda | koha (s) | gjerësia (t=0) | staircase HV | HV20 |", "|---|---|---|---|---|---|---|---|"]
    for c in cons_rows:
        g = graphs[c["instance"]]
        md.append(f"| {c['instance']} | {g.n} | {g.m} | {c['method']} | {c['seconds']} | {c['width_t0']} | "
                  f"{c['staircase_hv']} | {c['hv20']} |")
    md += ["", "## Metaheuristikat", "",
           "| instanca | algoritmi | seed | vlerësime | staircase HV fillim → fund | HV20 | pika jo-dominuese |",
           "|---|---|---|---|---|---|---|"]
    for r in runs:
        md.append(f"| {r['instance']} | {r['algo']} | {r['seed']} | {r['evals']} | {r['history'][0][2]} → {r['best_hv']} | "
                  f"{r['hv20']} | {r['n_points']} |")
    md += ["", "## Fronti final (bashkimi i të gjitha ekzekutimeve, 20 pikat me HV maksimal)", "",
           "| instanca | HV | HV i normalizuar | pikat (madhësia, gjerësia) |", "|---|---|---|---|"]
    for name, s in summary.items():
        pts = ", ".join(f"({p['torso_size']}, {p['torso_width']})" for p in s["points"])
        md.append(f"| {name} | {s['hv']} | {s['hv_normalized']:.4f} | {pts} |")
    md += ["", "![Konvergjenca](convergence.png)", "", "![Frontet Pareto](pareto_fronts.png)", ""]
    with open(os.path.join(res_dir, "results.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))


def plots(res_dir, graphs, cons_rows, runs, summary):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = {"SA": "#2a6fdb", "ILS": "#e07b1f"}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, name in zip(axes, INSTANCES):
        for r in runs:
            if r["instance"] == name:
                ts = [h[0] for h in r["history"]]
                hv = [h[2] for h in r["history"]]
                ax.plot(ts, hv, color=colors[r["algo"]], alpha=0.85, label=f"{r['algo']} seed {r['seed']}")
        ax.set_title(f"{name} (n={graphs[name].n})")
        ax.set_xlabel("koha (s)")
        ax.set_ylabel("staircase HV (më i miri)")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Konvergjenca e SA dhe ILS")
    fig.tight_layout()
    fig.savefig(os.path.join(res_dir, "convergence.png"), dpi=130)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, name in zip(axes, INSTANCES):
        g = graphs[name]
        for c in cons_rows:
            if c["instance"] == name:
                pts = front_from_widths(c["w"])
                ax.step([g.n - t for t, _ in pts], [w for _, w in pts], where="post", alpha=0.6,
                        label=f"{c['method']}")
        fin = summary[name]["points"]
        ax.plot([p["torso_size"] for p in fin], [p["torso_width"] for p in fin], "o", color="crimson",
                label="fronti final (20 pika)")
        ax.set_title(f"{name}: HV = {summary[name]['hv_normalized']:.4f}")
        ax.set_xlabel("madhësia e torsos (n − t)")
        ax.set_ylabel("gjerësia e torsos")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Frontet Pareto (madhësia ↑, gjerësia ↓)")
    fig.tight_layout()
    fig.savefig(os.path.join(res_dir, "pareto_fronts.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
