# Problemi 3 – Killer Sudoku me Constraint Programming (CSP)

**Kërkesa e detyrës:** të zgjidhet Killer Sudoku ([sudoku.com/killer](https://sudoku.com/killer)) duke
përdorur Constraint Programming.

## 1. Rregullat

Tabela 9×9 duhet të mbushet me shifrat 1–9 ashtu që:
* çdo rresht, çdo kolonë dhe çdo kuti 3×3 të ketë shifrat 1–9 pa përsëritje (Sudoku standard);
* tabela është e ndarë në **kafaze** (cages, zonat me vija të ndërprera). Shifrat brenda një kafazi
  janë **të ndryshme** dhe **shuma** e tyre është numri i shkruar në kafaz.

Në nivelet më të lehta sudoku.com jep edhe disa shifra të paraplotësuara.

## 2. Modeli CSP

| | |
|---|---|
| **Variablat** | X₁, …, X₈₁ (një për çdo qelizë) |
| **Domeni** | D(Xᵢ) = {1, …, 9} |
| **Kufizimet** | AllDifferent(rresht r) për r = 1..9 |
| | AllDifferent(kolonë c) për c = 1..9 |
| | AllDifferent(kuti b) për b = 1..9 |
| | për çdo kafaz K me shumë S: AllDifferent(K) ∧ Σ_{i∈K} Xᵢ = S |
| | Xᵢ = d për shifrat e dhëna |

Kufizimi i kafazit nuk i përket vetëm Sudoku-së standarde. Ai e bën problemin "killer", sepse në
versionin expert nuk ka asnjë shifër të dhënë dhe e gjithë informata vjen nga shumat.

## 3. Zgjidhja A – solver CSP i implementuar nga zero (`csp_solver.py`)

**Backtracking** me tri teknika:

1. **Forward Checking (FC).** Pas çdo caktimi Xᵢ = d, vlera d hiqet nga domenet e të gjitha qelizave
   që ndajnë me Xᵢ rresht, kolonë, kuti ose kafaz. Nëse ndonjë domen mbetet bosh, provohet vlera tjetër
   (backtrack), pa e vazhduar më thellë.
2. **MRV (Minimum Remaining Values).** Si qelizë e ardhshme zgjidhet ajo me domenin më të vogël, pra
   variabla "më e kufizuar". Kështu dështimet dalin sa më herët.
3. **Krasitja me kombinimet e kafazeve.** Paraprakisht llogariten **të gjitha bashkësitë e shifrave të
   ndryshme** për çdo madhësi kafazi k dhe shumë S:

   | k | S | kombinimet | shifrat e mundshme |
   |---|---|---|---|
   | 2 | 3 | {1,2} | 1, 2 |
   | 2 | 17 | {8,9} | 8, 9 |
   | 3 | 6 | {1,2,3} | 1, 2, 3 |
   | 2 | 10 | {1,9} {2,8} {3,7} {4,6} | 1–4, 6–9 (jo 5) |

   * Në fillim, domeni i çdo qelize të kafazit = bashkimi i kombinimeve të tij.
   * Gjatë kërkimit, për kafazin e qelizës së caktuar llogariten shifrat e përdorura U, shuma e
     mbetur R dhe numri i qelizave të mbetura m. Domenet e qelizave të mbetura kufizohen te bashkimi i
     kombinimeve (m, R) që nuk përmbajnë shifra nga U.

   Shembull: në kafazin "22" me 4 qeliza është vendosur 9. Atëherë 3 qelizat e tjera duhet të kenë
   shumë 13 pa e përdorur 9-shin, dhe kombinimet e mbetura janë {1,4,8}, {1,5,7}, {2,3,8}, {2,4,7},
   {2,5,6}, {3,4,6}.

## 4. Zgjidhja B – Google OR-Tools CP-SAT (`cpsat_solver.py`)

I njëjti model me solver-in industrial të Constraint Programming:
`AddAllDifferent` për rreshtat, kolonat, kutitë dhe kafazet, si dhe `Add(Σ x == S)` për shumat.
CP-SAT përdoret për krahasim dhe për të **vërtetuar se zgjidhja është unike**: kërkon një zgjidhje të
dytë dhe vërteton që ajo nuk ekziston.

## 5. Puzzle-t

Katër puzzle nga sudoku.com/killer (screenshot më 21.11.2026), një për çdo nivel. Janë shkruar në
`puzzles/*.txt`:

| Puzzle | Kafaze | Shifra të dhëna | Zgjidhja |
|---|---|---|---|
| easy | 32 | 31 | unike |
| medium | 34 | 26 | unike |
| hard | 34 | 10 | unike |
| expert | 34 | 0 | unike |

Gjatë leximit programi kontrollon:
* a mbulon çdo qelizë saktësisht një kafaz;
* a është shuma e të gjitha kafazeve 405 (= 9 rreshta × 45);
* a është shuma e çdo kafazi e mundshme për madhësinë e tij.

Përveç kësaj, CP-SAT vërtetoi që secili puzzle ka **saktësisht një zgjidhje**, pra puzzle-t janë
transkriptuar saktë.

**Formati** (`.txt`):

```text
abbcccdee        <- 9 rreshta: çdo shkronjë = një kafaz
fgghhddee
...
..3....5.        <- 9 rreshta opsionalë: shifrat e dhëna ('.' = bosh)
...
a 8  b 5  c 19   <- shuma e çdo kafazi
```

Pranohet edhe JSON: `{"cages": [{"sum": 8, "cells": ["A1"]}, ...], "givens": {"A3": 3}}`.

## 6. Rezultatet

`python run_experiments.py`. Tabela e plotë dhe zgjidhjet janë te [results/results.md](results/results.md).
*Nyje* = vlera të provuara gjatë kërkimit, *backtrack* = vlera që dështuan.

| Puzzle | BT | BT + FC | BT + FC + MRV | **BT + FC + MRV + kombinime** | CP-SAT |
|---|---|---|---|---|---|
| easy | 284 nyje | 65 | 59 | **50 nyje, 0 backtrack** | 0 degëzime |
| medium | 313 | 75 | 61 | **55 nyje, 0 backtrack** | 0 degëzime |
| hard | 2 625 | 786 | 578 | **71 nyje, 0 backtrack** | 0 degëzime |
| expert | 2 512 755 (5.8 s) | 637 270 (3.5 s) | 547 009 (3.8 s) | **307 nyje, 226 backtrack (3 ms)** | 0 degëzime (10 ms) |

Zgjidhja e expert-it:

```text
+-------+-------+-------+
| 5 8 6 | 1 3 2 | 4 9 7 |
| 4 3 7 | 5 9 8 | 1 2 6 |
| 9 1 2 | 7 6 4 | 5 8 3 |
+-------+-------+-------+
| 6 2 9 | 8 7 1 | 3 5 4 |
| 1 5 8 | 3 4 9 | 7 6 2 |
| 3 7 4 | 2 5 6 | 8 1 9 |
+-------+-------+-------+
| 2 4 3 | 9 1 5 | 6 7 8 |
| 7 9 1 | 6 8 3 | 2 4 5 |
| 8 6 5 | 4 2 7 | 9 3 1 |
+-------+-------+-------+
```

**Analiza:**
* **Forward checking** e ul numrin e nyjave rreth 4 herë, sepse dështimet zbulohen një nivel më herët.
* **MRV** e ul edhe pak numrin e nyjave. Te puzzle-t e lehta ndihmon pak, sepse FC i lë shumë qeliza
  me domen 1.
* **Krasitja me kombinime** është teknika vendimtare. Te expert-i numri i nyjave bie nga 547 009 në
  **307**, rreth 1 800 herë më pak. Arsyeja: në Killer Sudoku pa shifra të dhëna informata vjen nga
  shumat, dhe kombinimet e kthejnë një kufizim aritmetik (Σ = S) në kufizim domeni.
* Te easy, medium dhe hard solver-i i plotë **nuk bën asnjë backtrack**: propagimi gjen gjithmonë
  vlerën e saktë. Te expert-i duhen 226 backtrack, sepse s'ka shifra të dhëna.
* **CP-SAT** i zgjidh të gjitha me **0 degëzime**, pra vetëm me presolve dhe propagim. Arsyeja është
  se CP-SAT bën propagim më të fortë mbi AllDifferent dhe mbi shumat lineare: arsyeton mbi të gjitha
  kufizimet njëkohësisht. FC, përkundrazi, shikon vetëm qelizat fqinje të variablës së sapocaktuar.
  Në kohë, solver-i ynë në Python (3 ms) dhe CP-SAT (≈ 10 ms, ku hyn edhe ndërtimi i modelit) janë
  të krahasueshëm për këtë madhësi.

## 7. Ekzekutimi

Nga ky folder:

```bash
python solve.py puzzles/expert.txt                  # të dy solver-at + verifikimi
python solve.py puzzles/hard.txt --solver csp       # vetëm solver-i ynë
python solve.py puzzles/easy.txt --solver cpsat --unique
python run_experiments.py                           # tabela -> results/results.md
python -m unittest test_killer -v
```

## 8. Skedarët

| Skedari | Përmbajtja |
|---|---|
| `killer.py` | leximi i puzzle-ve (txt/json), validimi, verifikimi i zgjidhjes, vizatimi |
| `csp_solver.py` | solver-i CSP: backtracking + FC + MRV + kombinimet e kafazeve |
| `cpsat_solver.py` | modeli me OR-Tools CP-SAT dhe kontrolli i unicitetit |
| `solve.py` | zgjidhja e një puzzle-i nga linja e komandës |
| `run_experiments.py` | krahasimi i solver-ave → `results/results.md` |
| `test_killer.py` | testet (puzzle të rastësishme, rast pa zgjidhje, verifikimi) |
| `puzzles/` | 4 puzzle-t nga sudoku.com |
