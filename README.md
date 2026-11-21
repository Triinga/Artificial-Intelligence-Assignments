# Inteligjenca Artificiale – Detyrat

Detyrat për lëndën **Inteligjenca Artificiale** (Master).

Materiali dhe kërkesat zyrtare të lëndës:
<https://github.com/adrianymeri/Artificial-Intelligence-2026>

## Detyrat

| Detyra | Tema | Dokumentimi |
|---|---|---|
| Detyra 1 | Uninformed Search Techniques | [detyra1/README.md](detyra1/README.md) |
| Detyra 2 | Informed Search (A*), SAT, CSP, Metaheuristika | [detyra2/README.md](detyra2/README.md) |

### Detyra 1 – përmbajtja

| Problemi | Algoritmi | Dokumentimi |
|---|---|---|
| Social Golfers | DFS me Backtracking | [social_golfers](detyra1/social_golfers/README.md) |
| Sudoku Solver (Easy, Medium, Hard) | BFS me Backtracking | [sudoku](detyra1/sudoku/README.md) |
| Latin Square | IDDFS me Backtracking | [latin_square](detyra1/latin_square/README.md) |
| 8-Puzzle, Missionaries and Cannibals, Rotating Workforce Scheduling | Search Trees (të vizatuara në letër) | [search_trees](detyra1/search_trees/README.md) |

### Detyra 2 – përmbajtja

| Problemi | Teknika | Dokumentimi |
|---|---|---|
| Blocked N-Queens | A* me heuristikat h1–h4 (h4 admissible, e propozuar) | [01_blocked_nqueens_astar](detyra2/01_blocked_nqueens_astar/README.md) |
| Ulja e 100 mysafirëve | Formulë SAT (PySAT) | [02_sat_wedding_seating](detyra2/02_sat_wedding_seating/README.md) |
| Killer Sudoku | CSP (solver nga zero + OR-Tools CP-SAT) | [03_killer_sudoku_csp](detyra2/03_killer_sudoku_csp/README.md) |
| Torso Decompositions (ESA SpOC-3) | Simulated Annealing + Iterated Local Search (Kaggle) | [04_torso_decomposition_local_search](detyra2/04_torso_decomposition_local_search/README.md) |

Për çdo problem dokumentimi përmban modelin, reprezentimin (variablat,
domain), objective function, landscape, algoritmin dhe rezultatet e matura.

## Kërkesat

- Python 3.10 ose më i ri
- Detyra 1: nuk përdoren external libraries
- Detyra 2: `pip install -r detyra2/requirements.txt` (python-sat, ortools, matplotlib)

## Ekzekutimi

Të gjitha komandat ekzekutohen nga root-i i repository-t:

```bash
# Social Golfers: sa javë maksimumi për 32 lojtarë në 8 grupe me 4
python -m detyra1.social_golfers.max_weeks 8 4

# Sudoku
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/hard.txt

# Latin Square
python -m detyra1.latin_square.latin_square 5

# Të gjitha testet
python -m unittest discover -s detyra1/tests -v
```

Komandat e tjera dhe opsionet (`--time-limit`, `--mrv`, `--dfs`) janë te
[detyra1/README.md](detyra1/README.md).

## Struktura

```text
.
|-- README.md
|-- detyra1/
|   |-- README.md
|   |-- social_golfers/
|   |-- sudoku/
|   |   `-- examples/
|   |-- latin_square/
|   |-- search_trees/
|   |   `-- images/
|   `-- tests/
`-- detyra2/
    |-- README.md
    |-- requirements.txt
    |-- 01_blocked_nqueens_astar/
    |-- 02_sat_wedding_seating/
    |-- 03_killer_sudoku_csp/
    `-- 04_torso_decomposition_local_search/
```
