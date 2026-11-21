# Detyra 2 – Inteligjenca Artificiale (afati 03.12.2026)

Kërkesat zyrtare: [Detyra2.md](https://github.com/adrianymeri/Artificial-Intelligence-2026/blob/main/Detyra2.md)
– *Teknikat e informuara të kërkimit, CSP, SAT, Metaheuristikat.*

| # | Problemi | Teknika | Folderi |
|---|---|---|---|
| 1 | Blocked N-Queens | A* + 3 heuristika + heuristikë admissible e propozuar | [01_blocked_nqueens_astar](01_blocked_nqueens_astar/README.md) |
| 2 | Ulja e 100 mysafirëve | Formulë SAT (PySAT / CaDiCaL) | [02_sat_wedding_seating](02_sat_wedding_seating/README.md) |
| 3 | Killer Sudoku | Constraint Programming: solver CSP nga zero + OR-Tools CP-SAT | [03_killer_sudoku_csp](03_killer_sudoku_csp/README.md) |
| 4 | Torso Decompositions (ESA SpOC-3) | Metaheuristika (do të bëhet në Kaggle, sipas rekomandimit të profesorit) | – |

## Përmbledhje e rezultateve

Raporti i plotë: [REPORT.md](REPORT.md).

**1. Blocked N-Queens (A\*).**
* Heuristikat: h1 = N − g, h2 = h1 + zbulim i rreshtave pa dalje, h3 = penalizim MRV (jo-admissible).
* **h4** (e propozuar) = propagim i rreshtave të detyruar + matching rreshta–kolona. Është e vërtetuar
  formalisht si admissible dhe konsistente.
* Në 16 instanca, h4 përfundon 15 dhe zgjeron 239 747 nyje gjithsej. h1 përfundon 11 me 553 155 nyje,
  kurse h3 vetëm 8.
* Vëzhgimi kyç: çdo zgjidhje ka kosto N, prandaj heuristika mund të ndihmojë vetëm duke zbuluar
  rrugët pa dalje (h = ∞).

**2. SAT.**
* Variablat x_{i,t}. Kodimi: ALO/AMO, sequential counter për kapacitetin (≤ 10) dhe gjininë
  (4–6 burra për tavolinë), klauzola për konfliktet dhe çiftet "bashkë", thyerje simetrie.
* Madhësia: **16 780 variabla, 41 110 klauzola**.
* Instanca SAT zgjidhet dhe verifikohet. Dy instancat UNSAT vërtetohen.
* Thyerja e simetrisë e kthen pigeonhole-in me 11 armiq nga TIMEOUT (> 60 s) në UNSAT të vërtetuar.

**3. Killer Sudoku.**
* Modeli: 81 variabla me domen 1..9; AllDifferent për rreshtat, kolonat, kutitë dhe kafazet;
  Σ = S për çdo kafaz.
* Solver-i ynë përdor backtracking + forward checking + MRV + kombinimet e kafazeve. Te expert-i
  zgjidh me **307 nyje**, kundrejt 2.5 milion nyjeve të backtracking-ut të thjeshtë.
* CP-SAT i zgjidh 4 puzzle-t nga sudoku.com (easy–expert) me 0 degëzime dhe vërteton se zgjidhjet
  janë unike.

## Instalimi dhe ekzekutimi

```bash
pip install -r detyra2/requirements.txt      # python-sat, ortools (Python 3.10+)

cd detyra2/01_blocked_nqueens_astar && python solve.py instances/example_page.lp
cd detyra2/02_sat_wedding_seating   && python solve.py instances/sat_party
cd detyra2/03_killer_sudoku_csp     && python solve.py puzzles/expert.txt
```

Secili folder ka `run_experiments.py` (tabelat në `results/`) dhe teste
(`python -m unittest discover -p "test_*.py"`).
