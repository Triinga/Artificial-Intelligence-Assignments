# Latin Square – IDDFS me Backtracking

## Problem definition

Për input `n`, duhet të ndërtohet një matricë `n x n` me numrat `1..n`, ku
çdo numër paraqitet saktësisht një herë në çdo row dhe column.

## State representation

Një `state` është lista e rows të plotësuar deri tani. Search depth është
numri i rows në state.

## Initial state dhe goal test

- Initial state: vetëm row i parë i fiksuar, `(1, 2, ..., n)`.
- Goal: state ka `n` rows dhe çdo row/column përmban `1..n`.

## Variables, domain dhe constraints

- Variable formale: çdo qelizë `X[row, column]`.
- Domain: `{1, 2, ..., n}`.
- Çdo row është permutation e `1..n`.
- Një vlerë nuk përsëritet në të njëjtën column.

Në search, një successor shton një candidate row të plotë.

## Symmetry breaking – reduced form

Kërkojmë vetëm Latin Squares në **reduced form**:

1. Row i parë është `1 2 ... n`.
2. Row `r` fillon me vlerën `r` (pra column e parë është `1 2 ... n`).

**Pse nuk humbim zgjidhje?** Çdo Latin Square mund të shndërrohet në reduced
form me dy veprime që e ruajnë vetinë "Latin":

- **Riemërtimi i numrave** (p.sh. çdo `3` bëhet `1`): row i parë bëhet
  `1 2 ... n`. Rows dhe columns mbeten pa përsëritje.
- **Ndërrimi i rendit të rows**: rows renditen sipas vlerës së parë, kështu
  column e parë bëhet `1 2 ... n`. Edhe kjo nuk krijon përsëritje.

Prandaj, nëse ekziston ndonjë Latin Square `n x n`, ekziston edhe një në
reduced form. Ne kërkojmë vetëm një zgjidhje, kështu që mjafton të kërkojmë
aty. Search tree bëhet shumë më i vogël.

## Successor generation – vetëm rows valide

`compatible_rows(square, n)` është një generator i vogël me backtracking që
ndërton row-in e ri qelizë pas qelize:

1. Row `r` fillon me vlerën `r` (reduced form).
2. Për çdo qelizë tjetër provohen vlerat `1..n`; një vlerë kapërcehet nëse
   është tashmë në këtë row ose në këtë column.
3. Kur row-i plotësohet, kthehet me `yield`, pra një row në një kohë.
4. Nëse një qelizë nuk ka asnjë vlerë të lejuar, largohet vlera e qelizës
   së mëparshme dhe provohet tjetra (backtracking brenda row-it).

Përfitimet:

- Gjenerohen **vetëm** rows që nuk shkelin asnjë column, prandaj nuk ka
  "candidate → kontrollo → hidh poshtë".
- Rows kthehen **një nga një** (`yield`), pra nuk ruhet listë me `n!` rows.

## Objective function

Latin Square është satisfaction problem:

```text
f(state) = rows që mungojnë + constraint violations
```

Goal state ka `f(state) = 0`. Meqë generator-i krijon vetëm rows valide,
constraint violations janë gjithmonë 0 dhe `f(state) = n - len(state)`.

## Landscape / search space

Pa constraints, kemi `n^2` qeliza me `n` vlera:

```text
n^(n^2)
```

Meqë çdo row duhet të jetë permutation, një row ka `n!` mundësi:

```text
(n!)^n
```

Me row-in e parë të fiksuar:

```text
(n!)^(n-1)
```

Column constraints dhe reduced form e zvogëlojnë më tej hapësirën reale.
Në reduced form, rows `2..n` kanë vlerën e parë të fiksuar, pra secili ka
maksimumi `(n-1)!` mundësi: `((n-1)!)^(n-1)`.

Vlerat konkrete për `n=5`:

| Modeli | Formula | Vlera për `n=5` |
|---|---|---:|
| Çdo qelizë lirisht `1..n` | `n^(n^2)` = `5^25` | 298,023,223,876,953,125 ≈ `2.98 * 10^17` |
| Çdo row permutation | `(n!)^n` = `(5!)^5` | 24,883,200,000 ≈ `2.49 * 10^10` |
| Row i parë fiks | `(n!)^(n-1)` = `(5!)^4` | 207,360,000 ≈ `2.07 * 10^8` |
| Reduced form (row `r` fillon me `r`) | `((n-1)!)^(n-1)` = `(4!)^4` | 331,776 |
| Reduced Latin Squares reale | – | 56 |

IDDFS ynë për `n=5` gjeneron gjithsej vetëm 185 nodes, sepse
`compatible_rows` nuk krijon kurrë një row që shkel një column.

## IDDFS me Backtracking

IDDFS ekzekuton Depth-Limited DFS disa herë, me limits `1, 2, ..., n`.
Çdo iteration fillon nga e para (nga initial state).

```text
for limit = 1 deri n:
    state = [first_row]
    nëse DLS(state, limit) gjen zgjidhje:
        kthe state
```

Brenda DLS:

```text
DLS(state, limit):
    nëse state ka n rows:  kthe SUCCESS
    nëse state ka limit rows: kthe FAILURE      # nuk zgjerohet më thellë

    për candidate_row në compatible_rows(state):
        shto candidate_row
        nëse DLS(state, limit) gjen zgjidhje:
            kthe SUCCESS
        largo candidate_row       <- backtracking
    kthe FAILURE
```

Nuk përdoret formula direkte ciklike për ta anashkaluar search-in.

### Pse IDDFS e përsërit punën këtu

Te Latin Square **të gjitha goals janë në depth `n`** (duhen saktësisht `n`
rows). Prandaj:

- Iterations me limit `1, 2, ..., n-1` **nuk mund të gjejnë kurrë goal**.
  Ato vetëm e eksplorojnë pemën deri në limit dhe dështojnë.
- Iteration `n-1` eksploron **çdo** rectangle valid me `n-1` rows
  (në reduced form). Numri i tyre rritet shumë shpejt.
- Vetëm iteration `n` gjen zgjidhjen.

IDDFS është i dobishëm kur nuk e dimë thellësinë e goal-it (p.sh. 8-Puzzle).
Këtu e dimë që thellësia është `n`, prandaj një **DFS i thjeshtë me limit
`n`** do të mjaftonte. Kodi përmban edhe `solve_latin_square_dfs` (opsioni
`--dfs`) **vetëm për krahasim**; algoritmi kryesor mbetet IDDFS, siç kërkon
detyra.

Nodes visited për çdo iteration (IDDFS):

| Limit | n=5 | n=6 |
|---:|---:|---:|
| 1 | 1 | 1 |
| 2 | 12 | 54 |
| 3 | 58 | 1,118 |
| 4 | 114 | 7,670 |
| 5 | **5** (goal) | 17,078 |
| 6 | – | **6** (goal) |

Iteration e fundit vizitohet vetëm `n` nodes, sepse DFS-i gjen zgjidhjen
pa asnjë backtrack. Gjithë puna tjetër është përsëritje nga iterations e
mëparshme.

## Complexity

- Branching factor: deri në `(n-1)!` (vlera e parë e row-it është fikse).
- Depth: `n` rows (`n-1` rows shtohen nga search-i).
- Time: `O(b^d)` në worst case; IDDFS e shumëzon këtë me maksimumi `n`
  iterations.
- Space: `O(n^2)`: vetë square (`n x n`) plus `n` generators aktivë, secili
  me `O(n)` memory. Nuk ruhet asnjë listë me `n!` rows.

## Funksionet kryesore

- `solve_latin_square_iddfs`: kontrollon limits dhe nis DLS.
- `solve_latin_square_dfs`: DFS i thjeshtë (një limit `n`), vetëm për krahasim.
- `depth_limited_search`: DFS rekursiv me limit.
- `compatible_rows`: generator me backtracking që jep vetëm rows valide.
- `is_valid_latin_square`: validon rezultatin në mënyrë të pavarur.

## Ekzekutimi

Nga root-i i repository-t:

```bash
python -m detyra1.latin_square.latin_square 5
python -m detyra1.latin_square.latin_square 6
python -m detyra1.latin_square.latin_square 6 --dfs
python -m unittest detyra1.tests.test_latin_square -v
```

Rezultati i testuar për `n=5`:

```text
1 2 3 4 5
2 1 4 5 3
3 4 5 1 2
4 5 2 3 1
5 3 1 2 4
```

Ky rezultat ndryshon nga shembulli i detyrës, por është valid: Latin Square
mund të ketë shumë zgjidhje.

### Statistikat e matura

| n | Algoritmi | Iterations | Nodes generated | Nodes visited | Backtracks | Koha |
|---:|---|---:|---:|---:|---:|---:|
| 5 | IDDFS | 5 | 185 | 190 | 181 | ~0.001 s |
| 5 | DFS | 1 | 4 | 5 | 0 | ~0.0001 s |
| 6 | IDDFS | 6 | 25,921 | 25,927 | 25,916 | ~0.18 s |
| 6 | DFS | 1 | 5 | 6 | 0 | ~0.0001 s |
| 7 | IDDFS | 7 | 43,507,247 | 43,507,254 | 43,507,241 | ~532 s |
| 7 | DFS | 1 | 6 | 7 | 0 | ~0.0002 s |

Kohët janë matur në një laptop dhe ndryshojnë pak nga ekzekutimi në
ekzekutim. Për `n=7` IDDFS zgjat rreth 9 minuta, sepse iteration 6 duhet të
kalojë nëpër të gjitha 16,942,080 rectangles me 6 rows në reduced form
(numri i reduced Latin Squares të rendit 7). DFS i thjeshtë e gjen të njëjtën
zgjidhje menjëherë. Ky është kufizimi real i IDDFS kur goal depth dihet.
