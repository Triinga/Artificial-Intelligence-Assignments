# Sudoku Solver – BFS me Backtracking

## Problem definition

Duhet të plotësohet një Sudoku `9x9` në mënyrë që çdo row, column dhe box
`3x3` të përmbajë numrat `1-9` pa përsëritje. Programi përmban shembuj Easy,
Medium dhe Hard.

## State representation

Një `state` është e gjithë tabela aktuale. Në kod ruhet si tuple me 81 numra:

- `0`: qelizë bosh;
- `1-9`: vlerë e vendosur.

Tuple përdoret sepse është immutable dhe mund të ruhet në `parents`/`visited`.

## Initial state dhe goal test

- Initial state: tabela e lexuar nga file-i.
- Goal: nuk ka zero dhe çdo row, column dhe box përmban saktësisht `1-9`.

## Variables, domain dhe constraints

- Variable: çdo qelizë bosh `X[row, column]`.
- Domain: `{1,2,3,4,5,6,7,8,9}`.
- Constraints: vlera nuk përsëritet në row, column ose box `3x3`.
- Numrat fillestarë nuk ndryshohen.

## Objective function

Sudoku është satisfaction problem. Meqë kodi nuk gjeneron states që shkelin
constraints, mund të përdorim:

```text
f(board) = numri i qelizave bosh
```

Goal ka `f(board) = 0`.

## Landscape / search space

Nëse kemi `k` qeliza bosh dhe deri në 9 vlera për secilën:

```text
raw search space = 9^k
```

Search tree ka depth `d = k` dhe branching factor `b <= 9`. Constraints dhe
MRV e zvogëlojnë shumë numrin real të states.

## Successor generation

1. Zgjidhet një qelizë bosh.
2. Llogariten vlerat që nuk shkelin row, column dhe box.
3. Për çdo vlerë krijohet një board i ri.
4. Board-i i ri shtohet në fund të FIFO queue.

## BFS me Backtracking

Assignment-i kërkon shprehimisht BFS me Backtracking. Normalisht Sudoku shpesh
zgjidhet me DFS + recursive backtracking, por këtu kemi implementuar kërkesën:

- `deque` është FIFO queue, prandaj states zgjerohen level by level;
- çdo level plotëson një qelizë më shumë;
- dead-end states nuk kanë successors;
- për çdo child ruhet parent-i;
- pasi gjendet solution, `reconstruct_path` kthehet nga goal te initial state.

Ky kthim përmes parents është backtracking-u në implementimin tonë; nuk e
paraqesim si recursive DFS.

### Optional optimization: MRV

`choose_empty_cell` zgjedh qelizën me më së paku valid values. MRV ndryshon
vetëm rendin e variable-ve dhe zvogëlon branching; queue vazhdon të jetë BFS.

## Pseudokodi

```text
queue <- [initial]
parent[initial] <- NONE

while queue nuk është bosh:
    current <- hiq state-in e parë

    if current është goal:
        return BACKTRACK_PATH(current, parent)

    cell <- qeliza bosh me më së paku kandidatë

    for value in valid_values(cell):
        child <- current me value në cell
        parent[child] <- current
        shto child në fund të queue

return NO SOLUTION
```

## Complexity

- Time: `O(b^d)` në worst case.
- Space: `O(b^d)`, sepse BFS ruan frontier-in e plotë.

Space complexity është dobësia kryesore e BFS për Sudoku.

## Funksionet kryesore

- `parse_puzzle`: lexon dhe kontrollon input-in.
- `valid_values`: gjen domain-in valid të një qelize.
- `choose_empty_cell`: aplikon MRV.
- `solve_sudoku_bfs`: kryen BFS me FIFO queue.
- `reconstruct_path`: bën parent backtracking.
- `is_valid_solution`: validon rezultatin në mënyrë të pavarur.

## Ekzekutimi

Nga root-i i repository-t:

```bash
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/easy.txt
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/medium.txt
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/hard.txt
python -m unittest detyra1.tests.test_sudoku -v
```

## Rezultatet

| Niveli | Generated | Visited | Dead ends | Max frontier | Solution depth |
|---|---:|---:|---:|---:|---:|
| Easy | 51 | 52 | 0 | 1 | 51 |
| Medium | 45 | 46 | 0 | 1 | 45 |
| Hard | 205 | 206 | 11 | 9 | 53 |

Të tri zgjidhjet kalojnë `is_valid_solution`.

## MBROJTJA – çfarë duhet të di

1. **Çfarë është state?** E gjithë tabela aktuale e Sudoku-t.
2. **Çfarë paraqet një BFS level?** Një qelizë më shumë e plotësuar.
3. **Ku është queue?** Në `solve_sudoku_bfs`, si `deque` FIFO.
4. **Ku është backtracking?** Në `reconstruct_path`, nga goal te parents.
5. **Pse BFS harxhon shumë memory?** Sepse ruan të gjitha states në frontier.
6. **Çfarë bën MRV?** Zgjedh qelizën me më së paku kandidatë.
7. **Cili është goal test?** Zero qeliza bosh dhe të gjitha constraints valide.
8. **Çfarë ndodh me një dead end?** Nuk gjeneron children dhe BFS vazhdon me
   state-in tjetër në queue.
