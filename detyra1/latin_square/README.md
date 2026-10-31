# Latin Square – IDDFS me Backtracking

## Problem definition

Për input `n`, duhet të ndërtohet një matricë `n x n` me numrat `1..n`, ku
çdo numër paraqitet saktësisht një herë në çdo row dhe column.

## State representation

Një `state` është lista e rows të plotësuar deri tani. Search depth është
numri i rows në state.

Row i parë fiksohet si `(1, 2, ..., n)`. Ky është symmetry breaking: numrat
mund të riemërtohen, prandaj nuk humbim zgjidhje reale.

## Initial state dhe goal test

- Initial state: vetëm row i parë i fiksuar.
- Goal: state ka `n` rows dhe çdo row/column përmban `1..n`.

## Variables, domain dhe constraints

- Variable formale: çdo qelizë `X[row, column]`.
- Domain: `{1, 2, ..., n}`.
- Çdo row është permutation e `1..n`.
- Një vlerë nuk përsëritet në të njëjtën column.

Në search, një successor shton një candidate row të plotë.

## Objective function

Latin Square është satisfaction problem:

```text
f(state) = rows që mungojnë + constraint violations
```

Goal state ka `f(state) = 0`.

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

Column constraints e zvogëlojnë më tej hapësirën reale.

## IDDFS me Backtracking

IDDFS ekzekuton Depth-Limited DFS disa herë, me limits `1, 2, ..., n`.

```text
for limit = 1 deri n:
    state = [first_row]
    nëse DLS(state, limit) gjen zgjidhje:
        kthe state
```

Brenda DLS:

```text
for candidate_row:
    nëse candidate_row është compatible me columns:
        shto candidate_row

        nëse DLS gjen zgjidhje:
            kthe SUCCESS

        largo candidate_row       <- backtracking
```

Assignment-i kërkon IDDFS. Për Latin Square e dimë se goal depth është `n`,
prandaj DFS i zakonshëm do të ishte më efikas; megjithatë kodi implementon
IDDFS real dhe përsërit DLS për çdo limit.

Nuk përdoret formula direkte ciklike për ta anashkaluar search-in.

## Complexity

- Branching factor: deri në `n!`.
- Depth: `n`.
- Time: `O((n!)^n)` në worst case.
- Recursion space: `O(n)` kur candidates gjenerohen një nga një.

## Funksionet kryesore

- `solve_latin_square_iddfs`: kontrollon limits dhe nis DLS.
- `depth_limited_search`: DFS rekursiv me limit.
- `is_compatible_row`: kontrollon column constraints.
- `is_valid_latin_square`: validon rezultatin në mënyrë të pavarur.

## Ekzekutimi

Nga root-i i repository-t:

```bash
python -m detyra1.latin_square.latin_square 5
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

### Statistikat për n=5

- IDDFS iterations: 5
- Nodes generated: 77,456
- Nodes visited: 2,589
- Backtracks: 2,580
- Solution depth: 5

## MBROJTJA – çfarë duhet të di

1. **Çfarë është state?** Rows që janë plotësuar deri tani.
2. **Pse row i parë fiksohet?** Për symmetry breaking pa humbur zgjidhje.
3. **Çfarë bën IDDFS?** Përsërit DLS me limits që rriten gradualisht.
4. **Ku ndodh backtracking?** Kur candidate row largohet pas dështimit.
5. **Cili është goal test?** Kemi `n` rows dhe të gjitha columns janë valide.
6. **Pse nuk përdorim formulë ciklike?** Sepse detyra kërkon search me IDDFS.
7. **Cila është dobësia e IDDFS këtu?** Goal depth dihet, prandaj përsërit
   punë që një DFS i vetëm nuk do ta përsëriste.
8. **Sa është raw search space?** `n^(n^2)` pa constraints.
