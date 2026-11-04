# Sudoku Solver – BFS me Backtracking

## Problem definition

Duhet të plotësohet një Sudoku `9x9` në mënyrë që çdo row, column dhe box
`3x3` të përmbajë numrat `1-9` pa përsëritje. Programi përmban shembuj Easy,
Medium dhe Hard.

Niveli i vështirësisë përcaktohet nga numri i **givens** (numrat e dhënë):
sa më pak givens, aq më shumë qeliza bosh dhe aq më i vështirë.

| File | Givens | Qeliza bosh `k` |
|---|---:|---:|
| `easy.txt` | 36 | 45 |
| `medium.txt` | 30 | 51 |
| `hard.txt` | 28 | 53 |

## State representation

Një `state` është e gjithë tabela aktuale. Në kod ruhet si tuple me 81 numra:

- `0`: qelizë bosh;
- `1-9`: vlerë e vendosur.

Tuple përdoret sepse është immutable dhe mund të përdoret si key në
dictionary `parents` (ku ruhet edhe se cilët states janë parë).

## Initial state dhe goal test

- Initial state: tabela e lexuar nga file-i.
- Goal: nuk ka zero dhe çdo row, column dhe box përmban saktësisht `1-9`.

## Variables, domain dhe constraints

- Variable: çdo qelizë bosh `X[row, column]`.
- Domain: `{1,2,3,4,5,6,7,8,9}`.
- Constraints: vlera nuk përsëritet në row, column ose box `3x3`.
- Numrat fillestarë nuk ndryshohen.

## Objective function

Sudoku është satisfaction problem:

```text
f(board) = numri i qelizave bosh + numri i konflikteve
```

ku një konflikt është një vlerë që përsëritet në të njëjtin row, column ose
box. Goal ka `f(board) = 0`.

Meqë BFS-i ynë vendos vetëm vlera nga `valid_values`, konfliktet janë
gjithmonë 0, prandaj gjatë search-it `f(board)` = numri i qelizave bosh dhe
zvogëlohet me 1 në çdo level.

## Landscape / search space

Nëse kemi `k` qeliza bosh dhe deri në 9 vlera për secilën:

```text
raw search space = 9^k
```

Search tree ka depth `d = k` dhe branching factor `b <= 9`. Constraints
(dhe, opsionalisht, MRV) e zvogëlojnë shumë numrin real të states.

Vlerat konkrete për shembujt tanë:

| Niveli | Qeliza bosh `k` | Raw search space `9^k` | Nodes generated (BFS) | Nodes generated (`--mrv`) |
|---|---:|---:|---:|---:|
| Easy | 45 | `9^45 ≈ 8.73 * 10^42` | 68 | 45 |
| Medium | 51 | `9^51 ≈ 4.64 * 10^48` | 4,631 | 51 |
| Hard | 53 | `9^53 ≈ 3.76 * 10^50` | 22,918 | 205 |

Pra BFS shqyrton vetëm një pjesë shumë të vogël të landscape-it, sepse
gjeneron vetëm vlera që nuk shkelin constraints.

## Successor generation

1. Zgjidhet **qeliza e parë bosh** (`choose_first_empty_cell`).
2. Llogariten vlerat që nuk shkelin row, column dhe box (`valid_values`).
3. Për çdo vlerë krijohet një board i ri (child), dhe ruhet parent-i i tij.
4. Child-i shtohet në fund të FIFO queue (`deque`).

Meqë queue është FIFO, states zgjerohen level by level: level `i` ka `i`
qeliza të plotësuara më shumë se initial state.

## BFS me Backtracking

Te DFS, backtracking do të thotë "zhbëj zgjedhjen e fundit dhe provo
tjetrën". BFS nuk ka recursion, prandaj backtracking ndodh në dy mënyra:

1. **Dead ends hidhen.** Nëse një state ka një qelizë bosh pa asnjë vlerë
   valide, BFS nuk krijon children për të dhe e hedh (`dead_ends += 1`).
   Alternativat e tjera **janë tashmë në queue**, prandaj search-i vazhdon me
   state-in e radhës. Nuk duhet zhbërë asgjë, sepse çdo state është një
   tabelë e veçantë (tuple).
2. **Path-i rindërtohet me parent links.** Kur gjendet goal,
   `reconstruct_path` ndjek `parent[goal]`, pastaj parent-in e tij, deri te
   initial state. Kjo jep vendosjet një qelizë për hap.

Shembull: nëse qeliza `X` ka kandidatët `{4, 7}`, queue merr dy children,
`X=4` dhe `X=7`. Nëse më vonë `X=4` çon në një qelizë pa vlera, ai state
hidhet dhe search-i vazhdon me states që vijnë nga `X=7`, të cilat po presin
në queue.

### Optional optimization: MRV (`--mrv`)

MRV (Minimum Remaining Values): `choose_empty_cell` zgjedh qelizën me më së
paku valid values në vend të qelizës së parë bosh. Ndryshon vetëm rendin e
variable-ve; queue mbetet FIFO, pra algoritmi mbetet BFS.

Me MRV, te Easy dhe Medium gjendet gjithmonë një qelizë me vetëm një
kandidat, prandaj çdo state ka saktësisht një child dhe BFS bëhet **një path
i vetëm** (max frontier 1, 0 dead ends). Për këtë arsye MRV nuk është
default.

## Complexity

- Time: `O(b^d)` në worst case.
- Space: `O(b^d)`, sepse BFS ruan frontier-in e plotë.

Space complexity është dobësia kryesore e BFS për Sudoku.

## Funksionet kryesore

- `parse_puzzle`: lexon dhe kontrollon input-in.
- `valid_values`: gjen domain-in valid të një qelize.
- `choose_first_empty_cell`: zgjedh qelizën e parë bosh (default).
- `choose_empty_cell`: aplikon MRV (`--mrv`).
- `solve_sudoku_bfs`: kryen BFS me FIFO queue (`use_mrv=False` si default).
- `reconstruct_path`: bën parent backtracking.
- `is_valid_solution`: validon rezultatin në mënyrë të pavarur.

## Ekzekutimi

Nga root-i i repository-t:

```bash
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/easy.txt
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/medium.txt
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/hard.txt

# me optimizimin opsional MRV
python -m detyra1.sudoku.sudoku_solver detyra1/sudoku/examples/hard.txt --mrv

python -m unittest detyra1.tests.test_sudoku -v
```

## Rezultatet

### BFS (default, qeliza e parë bosh)

| Niveli | Givens | Generated | Visited | Dead ends | Max frontier | Solution depth |
|---|---:|---:|---:|---:|---:|---:|
| Easy | 36 | 68 | 69 | 11 | 5 | 45 |
| Medium | 30 | 4,631 | 4,632 | 1,371 | 738 | 51 |
| Hard | 28 | 22,918 | 22,919 | 6,674 | 3,616 | 53 |

### Me MRV (`--mrv`)

| Niveli | Givens | Generated | Visited | Dead ends | Max frontier | Solution depth |
|---|---:|---:|---:|---:|---:|---:|
| Easy | 36 | 45 | 46 | 0 | 1 | 45 |
| Medium | 30 | 51 | 52 | 0 | 1 | 51 |
| Hard | 28 | 205 | 206 | 11 | 9 | 53 |

Të gjashtë zgjidhjet kalojnë `is_valid_solution`. Koha është nën 0.2 sekonda
në të gjitha rastet.

Çfarë tregojnë tabelat:

- BFS ruan shumë alternativa njëkohësisht: frontier-i arrin 3,616 states te
  Hard dhe ka shumë dead ends. Kjo është sjellja tipike e BFS, prandaj ai
  harxhon shumë memory.
- Rendi Easy < Medium < Hard i numrit të nodes përputhet me numrin e givens.
- Me MRV, Easy dhe Medium kanë `max frontier = 1` dhe `0` dead ends: BFS
  bëhet vetëm një path.
- Solution depth është gjithmonë `k` (numri i qelizave bosh), sepse çdo level
  plotëson një qelizë.
