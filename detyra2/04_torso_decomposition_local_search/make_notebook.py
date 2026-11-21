"""
Ndërton notebook-un e Kaggle (kaggle/torso_decompositions.ipynb) nga skedarët e këtij folderi,
që kodi në Kaggle të jetë identik me atë në repository.

    python make_notebook.py --seconds 900 --seeds 2
"""

from __future__ import annotations

import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": text.strip("\n").splitlines(keepends=True)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=int, default=900)
    ap.add_argument("--seeds", type=int, default=2)
    args = ap.parse_args()

    cells = [md(f"""
# Torso Decompositions (ESA SpOC-3) – Metaheuristika

Detyra 2, Problemi 4 – Inteligjenca Artificiale (Master), Universiteti i Prishtinës.

* **Problemi** ([README zyrtar](https://github.com/esa/SpOC3/tree/main/Challenge%201%20Torso%20Decompositions)):
  vektori `x = [p_1..p_n, t]` (permutacion + prag). Torso = n − t nyjet e fundit. Objektivat: madhësia e
  torsos ↑ dhe gjerësia e torsos (outdegree max pas shtimit të brinjëve) ↓. Dorëzohen ≤ 20 vektorë,
  vlerësimi bëhet me hypervolume.
* **Zgjidhja:** renditje konstruktive (min-degree, min-fill) → **Simulated Annealing** dhe
  **Iterated Local Search** me lëvizjet swap/insert. Objektivi = hypervolume i frontit të permutacionit.
  Në fund bashkohen frontet dhe zgjidhen 20 pikat me HV maksimal (programim dinamik).
* Çdo ekzekutim zgjat **{args.seconds} s**, me **{args.seeds} seed** për algoritëm, paralelisht në të gjitha CPU-të e Kaggle.
"""),
             code("""
import os, glob, urllib.request
DATA = "data"
os.makedirs(DATA, exist_ok=True)
for name in ("easy", "medium", "hard"):
    found = glob.glob(f"/kaggle/input/**/{name}.gr", recursive=True)
    dst = os.path.join(DATA, f"{name}.gr")
    if found:
        os.system(f"cp '{found[0]}' '{dst}'")
    elif not os.path.exists(dst):
        url = f"https://raw.githubusercontent.com/esa/SpOC3/main/Challenge%201%20Torso%20Decompositions/data/{name}.gr"
        urllib.request.urlretrieve(url, dst)
    print(name, os.path.getsize(dst), "bytes")
print("CPU:", os.cpu_count())
""")]
    for fname in ("torso.py", "search.py", "run.py"):
        with open(os.path.join(HERE, fname), encoding="utf-8") as fh:
            src = fh.read()
        cells.append(md(f"### `{fname}`"))
        cells.append(code(f"%%writefile {fname}\n" + src))
    cells += [
        md("### Testet (vlerësimi kundrejt shembullit zyrtar dhe procedurës fjalë për fjalë)"),
        code("%%writefile test_torso.py\n" + open(os.path.join(HERE, "test_torso.py"), encoding="utf-8").read()),
        code("!python -m unittest test_torso -v"),
        md("### Ekzekutimi"),
        code(f"!python run.py --seconds {args.seconds} --seeds {args.seeds} --data data --out ."),
        md("### Rezultatet"),
        code("""
from IPython.display import Markdown, Image, display
display(Markdown(open("results/results.md", encoding="utf-8").read().split("![")[0]))
display(Image("results/convergence.png"))
display(Image("results/pareto_fronts.png"))
"""),
    ]
    nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                       "language_info": {"name": "python"}},
          "nbformat": 4, "nbformat_minor": 5}
    os.makedirs(os.path.join(HERE, "kaggle"), exist_ok=True)
    path = os.path.join(HERE, "kaggle", "torso_decompositions.ipynb")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(nb, fh, ensure_ascii=False, indent=1)
    print("U krijua:", path)


if __name__ == "__main__":
    main()
