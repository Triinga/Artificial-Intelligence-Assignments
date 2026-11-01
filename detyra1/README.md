# Detyra 1 – Uninformed Search Techniques

Source of truth: [official Detyra1.md](https://github.com/adrianymeri/Artificial-Intelligence-2026/blob/main/Detyra1.md).

## Përmbajtja

### 1. Social Golfers

- [Teoria dhe udhëzimet](social_golfers/README.md)
- Algoritmi: DFS me Backtracking
- Përgjigjja për `8-4-w`: maksimumi 10 javë
- Orari optimal `8-4-10` është validuar në mënyrë të pavarur

### 2. Sudoku Solver

- [Teoria dhe udhëzimet](sudoku/README.md)
- Algoritmi: BFS me FIFO queue dhe parent backtracking
- Shembuj: Easy, Medium dhe Hard
- Optional optimization: MRV për zgjedhjen e qelizës

### 3. Latin Square

- [Teoria dhe udhëzimet](latin_square/README.md)
- Algoritmi: IDDFS me Depth-Limited DFS dhe Backtracking
- Testet: `n=1`, `n=3` dhe shembulli `n=5`

### 4. Search Trees

- [8-Puzzle](search_trees/eight_puzzle.md)
- [Missionaries and Cannibals](search_trees/missionaries_cannibals.md)
- [Rotating Workforce Scheduling](search_trees/rotating_workforce.md)

## Si ekzekutohet

Nuk përdoren external libraries. Kërkohet vetëm Python 3.

Nga root-i i repository-t:

```bash
# Social Golfers – demonstrim i DFS
python -m detyra1.social_golfers.social_golfers 2 2 3

# Verifikimi i maksimumit 8-4-10
python -m detyra1.social_golfers.verify_known_solution

# Sudoku
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/easy.txt
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/medium.txt
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/hard.txt

# Latin Square
python -m detyra1.latin_square.latin_square 5

# Të gjitha testet
python -m unittest discover -s detyra1/tests -v
```

## Complexity review

| Problem | Algorithm | Worst-case time | Worst-case space |
|---|---|---|---|
| Social Golfers | DFS + Backtracking | `O(b^d)` | `O(d + n^2)` me successors një nga një |
| Sudoku | BFS + parent backtracking | `O(b^d)` | `O(b^d)` |
| Latin Square | IDDFS + Backtracking | `O((n!)^n)` | `O(n)` recursion, plus candidate rows |

Ku `b` është branching factor dhe `d` është solution depth.

## Rezultatet kryesore

- Social Golfers: upper bound 10 dhe orari 10-javor është valid.
- Sudoku: Easy, Medium dhe Hard zgjidhen dhe validohen.
- Latin Square `n=5`: 5 IDDFS iterations dhe 2,580 backtracks.
- Të gjitha testet automatike kalojnë.

## Progress

- [x] Repository analysed
- [x] Project structure created
- [x] Social Golfers – theory and pseudocode
- [x] Social Golfers – core DFS + Backtracking implementation
- [x] Social Golfers – unit tests and small-instance tests
- [x] Social Golfers – final 32-player/max-week verification
- [x] Social Golfers – documentation and oral-defense notes
- [x] Sudoku – theory and pseudocode
- [x] Sudoku – BFS + Backtracking implementation
- [x] Sudoku – Easy/Medium/Hard tests
- [x] Sudoku – documentation and oral-defense notes
- [x] Latin Square – theory and pseudocode
- [x] Latin Square – IDDFS + Backtracking implementation
- [x] Latin Square – tests for n=1, n=3 and n=5
- [x] Latin Square – documentation and oral-defense notes
- [x] Search Tree – 8-Puzzle, paper drawing verified and included
- [x] Search Tree – Missionaries and Cannibals, paper drawing verified and included
- [x] Search Tree – Rotating Workforce Scheduling, paper drawing verified and included
- [x] Complexity review
- [x] Final documentation
- [ ] Oral-defense review

## Structure

```text
detyra1/
|-- social_golfers/
|-- sudoku/
|   `-- examples/
|-- latin_square/
|-- search_trees/
`-- tests/
```
