# Detyra 1 – Uninformed Search Techniques

Kërkesat zyrtare: [Detyra1.md](https://github.com/adrianymeri/Artificial-Intelligence-2026/blob/main/Detyra1.md).

## Përmbajtja

### 1. Social Golfers

- [Teoria dhe udhëzimet](social_golfers/README.md)
- Algoritmi: DFS me Backtracking (me opsionin `--time-limit`)
- Përgjigjja për `8-4-w`: maksimumi 10 javë
- 10 = upper bound `floor(31/3)` + orari i publikuar `8-4-10` (Aguado), i
  validuar në mënyrë të pavarur. DFS-i ynë gjen vetë `8-4-5`, por jo `8-4-6`
  brenda 20 s.

### 2. Sudoku Solver

- [Teoria dhe udhëzimet](sudoku/README.md)
- Algoritmi: BFS me FIFO queue; dead ends hidhen dhe path-i rindërtohet me
  parent links
- Shembuj: Easy (36 givens), Medium (30), Hard (28)
- Default: BFS i thjeshtë (qeliza e parë bosh); MRV si optimizim opsional
  me `--mrv`

### 3. Latin Square

- [Teoria dhe udhëzimet](latin_square/README.md)
- Algoritmi: IDDFS me Depth-Limited DFS dhe Backtracking
- Rows valide gjenerohen një nga një; reduced form si symmetry breaking
- DFS i thjeshtë (`--dfs`) vetëm për krahasim
- Testet: `n=1..6`

### 4. Search Trees

- [Search Trees](search_trees/README.md): 8-Puzzle, Missionaries and
  Cannibals dhe Rotating Workforce Scheduling, të vizatuara në letër

## Si ekzekutohet

Nuk përdoren external libraries. Kërkohet vetëm Python 3.

Nga root-i i repository-t:

```bash
# Social Golfers – sa javë maksimumi (bound + DFS + verifikim)
python -m detyra1.social_golfers.max_weeks 8 4

# Social Golfers – demonstrim i DFS me backtracking
python -m detyra1.social_golfers.social_golfers 5 5 6
python -m detyra1.social_golfers.social_golfers 8 4 5
python -m detyra1.social_golfers.social_golfers 8 4 6 --time-limit 20

# Verifikimi i maksimumit 8-4-10
python -m detyra1.social_golfers.verify_known_solution

# Sudoku (BFS; --mrv si optimizim opsional)
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/easy.txt
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/medium.txt
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/hard.txt
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/hard.txt --mrv

# Latin Square (IDDFS, dhe DFS për krahasim)
python -m detyra1.latin_square.latin_square 5
python -m detyra1.latin_square.latin_square 6
python -m detyra1.latin_square.latin_square 6 --dfs

# Të gjitha testet
python -m unittest discover -s detyra1/tests -v
```

## Complexity review

| Problem | Algorithm | Worst-case time | Worst-case space |
|---|---|---|---|
| Social Golfers | DFS + Backtracking | `O(b^d)` | `O(d + n^2)` me successors një nga një |
| Sudoku | BFS + parent backtracking | `O(b^d)` | `O(b^d)` |
| Latin Square | IDDFS + Backtracking | `O(b^d)`, `b <= (n-1)!`, `d = n` | `O(n^2)` (square + `n` generators) |

Ku `b` është branching factor dhe `d` është solution depth.

## Rezultatet kryesore

| Problem | Instanca | Rezultati | Nodes generated | Backtracks / dead ends | Koha |
|---|---|---|---:|---:|---:|
| Social Golfers | `5 5 6` | valid | 245,253 | 53 backtracks | ~0.13 s |
| Social Golfers | `8 4 5` | valid | 14,274 | 0 backtracks | ~0.006 s |
| Social Golfers | `8 4 6` | time limit 20 s, pa orar | ~31–46 milion | ~0.7–1.1 milion backtracks | 20 s |
| Social Golfers | `8 4 10` (Aguado) | valid (verifikim) | – | – | – |
| Sudoku BFS | Easy / Medium / Hard | valid | 68 / 4,631 / 22,918 | 11 / 1,371 / 6,674 dead ends | < 0.2 s |
| Sudoku BFS + `--mrv` | Easy / Medium / Hard | valid | 45 / 51 / 205 | 0 / 0 / 11 dead ends | < 0.01 s |
| Latin Square IDDFS | `n=5` | valid | 185 | 181 | ~0.001 s |
| Latin Square IDDFS | `n=6` | valid | 25,921 | 25,916 | ~0.18 s |
| Latin Square IDDFS | `n=7` | valid | 43,507,247 | 43,507,241 | ~532 s |
| Latin Square DFS | `n=7` | valid | 6 | 0 | ~0.0002 s |

Kohët janë matur në një laptop dhe ndryshojnë pak nga ekzekutimi në
ekzekutim. Numrat e nodes janë deterministë, përveç `8 4 6`, ku search-i
ndalet nga ora. Të gjitha testet automatike (27) kalojnë.

## Structure

```text
detyra1/
|-- social_golfers/
|-- sudoku/
|   `-- examples/
|-- latin_square/
|-- search_trees/
|   `-- images/
`-- tests/
```
