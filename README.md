# Inteligjenca Artificiale – Detyrat

Detyrat për lëndën **Inteligjenca Artificiale** (Master).

Materiali dhe kërkesat zyrtare të lëndës:
<https://github.com/adrianymeri/Artificial-Intelligence-2026>

## Detyrat

| Detyra | Tema | Dokumentimi |
|---|---|---|
| Detyra 1 | Uninformed Search Techniques | [detyra1/README.md](detyra1/README.md) |

### Detyra 1 – përmbajtja

| Problemi | Algoritmi | Dokumentimi |
|---|---|---|
| Social Golfers | DFS me Backtracking | [social_golfers](detyra1/social_golfers/README.md) |
| Sudoku Solver (Easy, Medium, Hard) | BFS me Backtracking | [sudoku](detyra1/sudoku/README.md) |
| Latin Square | IDDFS me Backtracking | [latin_square](detyra1/latin_square/README.md) |
| 8-Puzzle, Missionaries and Cannibals, Rotating Workforce Scheduling | Search Trees (të vizatuara në letër) | [search_trees](detyra1/search_trees/README.md) |

Për çdo problem dokumentimi përmban modelin, reprezentimin (variablat,
domain), objective function, landscape, algoritmin dhe rezultatet e matura.

## Kërkesat

- Python 3.10 ose më i ri
- Nuk përdoren external libraries

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
`-- detyra1/
    |-- README.md
    |-- social_golfers/
    |-- sudoku/
    |   `-- examples/
    |-- latin_square/
    |-- search_trees/
    |   `-- images/
    `-- tests/
```
