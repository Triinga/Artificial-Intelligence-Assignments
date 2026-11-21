# Problemi 2 – SAT: ulja e 100 mysafirëve

**Kërkesa e detyrës:** të definohet një formulë SAT për uljen e mysafirëve.

## 1. Problemi

100 mysafirë duhet të ulen në 10 tavolina me nga 10 karrige:

* **(a)** çiftet e një liste, p.sh. (M1, M5), **nuk** duhet të ulen në të njëjtën tavolinë;
* **(b)** çiftet e një liste tjetër **duhet** të ulen në të njëjtën tavolinë;
* **(c)** diferenca mes numrit të burrave dhe grave nuk e kalon ±3;
* **(d)** çdo mysafir ulet në saktësisht një tavolinë dhe çdo tavolinë ka saktësisht 10 mysafirë.

**Interpretimi i (c).** Kushtin e zbatojmë **për çdo tavolinë**. Me 10 vende dhe M burra, gratë janë
F = 10 − M, prandaj `|M − F| ≤ 3 ⇔ |2M − 10| ≤ 3 ⇔ M ∈ {4, 5, 6}`. Me 7 burra diferenca do të ishte
7 − 3 = 4 > 3.

## 2. Formula SAT

**Shënimet:** G = {1, …, 100} mysafirët, T = {1, …, 10} tavolinat, 𝓜 burrat, 𝓕 gratë,
K = lista e konflikteve (a), B = lista e çifteve "bashkë" (b).

**Variablat:**

$$x_{i,t} = 1 \iff \text{mysafiri } i \text{ ulet në tavolinën } t \qquad (100 \cdot 10 = 1000 \text{ variabla})$$

**(d1) Çdo mysafir në saktësisht një tavolinë** (ALO + AMO):

$$\bigwedge_{i \in G} \Big( \bigvee_{t \in T} x_{i,t} \Big)
\ \wedge\
\bigwedge_{i \in G}\ \bigwedge_{t < t'} \big(\neg x_{i,t} \lor \neg x_{i,t'}\big)$$

**(d2) Çdo tavolinë ka saktësisht 10 mysafirë.** Kodojmë `Σ_i x_{i,t} ≤ 10` për çdo t. Kushti
`≥ 10` **rrjedh vetvetiu**: nga (d1) shuma mbi të gjitha tavolinat është 100. Nëse 10 tavolina kanë
secila ≤ 10 dhe bashkë kanë 100, atëherë secila ka saktësisht 10.

$$\sum_{i \in G} x_{i,t} \le 10 \qquad \forall t \in T$$

**(a) Konfliktet:**

$$\bigwedge_{(a,b) \in K}\ \bigwedge_{t \in T} \big(\neg x_{a,t} \lor \neg x_{b,t}\big)$$

**(b) Bashkë** (`x_{a,t} ↔ x_{b,t}`):

$$\bigwedge_{(a,b) \in B}\ \bigwedge_{t \in T} \big(\neg x_{a,t} \lor x_{b,t}\big) \wedge \big(x_{a,t} \lor \neg x_{b,t}\big)$$

**(c) Gjinia** (`4 ≤ burra(t) ≤ 6`). Meqë tavolina ka saktësisht 10 veta,
`burra ≥ 4 ⇔ gra ≤ 6`, prandaj përdorim dy kufij të sipërm:

$$\sum_{i \in \mathcal{M}} x_{i,t} \le 6 \ \wedge\ \sum_{i \in \mathcal{F}} x_{i,t} \le 6 \qquad \forall t \in T$$

### Kodimi i kardinalitetit `x_1 + … + x_m ≤ r`: Sequential Counter (Sinz, 2005)

Variablat ndihmëse `s_{j,l}` (j = 1..m−1, l = 1..r) kanë kuptimin "ndër x_1..x_j të paktën l janë 1".
Klauzolat:

$$
\begin{aligned}
& \neg x_1 \lor s_{1,1} \qquad\qquad \neg s_{1,l} \quad (1 < l \le r) \\
& \text{për } 1 < j < m: \\
& \quad \neg x_j \lor s_{j,1} \qquad\qquad \neg s_{j-1,1} \lor s_{j,1} \\
& \quad \neg x_j \lor \neg s_{j-1,l-1} \lor s_{j,l} \qquad \neg s_{j-1,l} \lor s_{j,l} \quad (1 < l \le r) \\
& \quad \neg x_j \lor \neg s_{j-1,r} \qquad \text{(përndryshe } x_j \text{ do të ishte i } (r+1)\text{-ti)} \\
& \neg x_m \lor \neg s_{m-1,r}
\end{aligned}
$$

Numëruesi e "bart" numrin e variablave të vërteta nga e majta në të djathtë. Klauzola e fundit
ndalon që numri të kalojë r. Madhësia është **(m−1)·r variabla** dhe **2mr + m − 3r − 1 klauzola**.
Implementimi (`encoding.py`) testohet në mënyrë ezaustive: për çdo m ≤ 7, çdo r dhe çdo vlerësim
të x.

### Thyerja e simetrisë

Tavolinat janë të njëjta, prandaj çdo zgjidhje ka 10! = 3 628 800 kopje (ndërrime të tavolinave). Kjo
e bën vërtetimin e UNSAT shumë të shtrenjtë. Shtojmë klauzolat:

$$x_{i,t} \rightarrow \bigvee_{j < i} x_{j,t-1} \qquad \forall t \ge 2,\ \forall i$$

Kuptimi: mysafiri i ulet në tavolinën t vetëm nëse në tavolinën t−1 ulet dikush me numër më të
vogël. Kështu tavolinat renditen sipas mysafirit me numrin më të vogël.

**Pse nuk humbet asnjë zgjidhje:** çdo zgjidhje mund të riemërtohet duke i renditur tavolinat sipas
mysafirit më të vogël. Kushtet (a)–(d) nuk varen nga emrat e tavolinave, prandaj kopja e riemërtuar
mbetet zgjidhje dhe i plotëson këto klauzola. Kostoja është 9·100 = 900 klauzola.

### Numri i variablave dhe klauzolave

|Grupi | Numri i klauzolave | Klauzola | Variabla ndihmëse |
|---|---|---|---|
| x_{i,t} | – | – | 1 000 (kryesore) |
| (d1) ALO | 100 | 100 | 0 |
| (d1) AMO | 100 · C(10,2) | 4 500 | 0 |
| (d2) Σ ≤ 10 | 10 · (2·100·10 + 100 − 30 − 1) | 20 690 | 10 · 99 · 10 = 9 900 |
| (a) konflikte | 10 · \|K\| | 1 500 (\|K\| = 150) | 0 |
| (b) bashkë | 2 · 10 · \|B\| | 800 (\|B\| = 40) | 0 |
| (c) burra ≤ 6 | 10 · (2·50·6 + 50 − 18 − 1) | 6 310 | 10 · 49 · 6 = 2 940 |
| (c) gra ≤ 6 | njësoj | 6 310 | 2 940 |
| thyerja e simetrisë | 9 · 100 | 900 | 0 |
| **Gjithsej** | | **41 110 klauzola** | **16 780 variabla** |

Numrat vlejnë për instancën `sat_party` (50 burra, 150 konflikte, 40 çifte bashkë) dhe përputhen
me ato që printon programi.

## 3. Implementimi

| Skedari | Përmbajtja |
|---|---|
| `instance.py` | leximi/shkrimi i instancave (CSV) dhe gjeneratori i rastësishëm |
| `encoding.py` | formula CNF, sequential counter, thyerja e simetrisë, DIMACS, dekodimi, verifikimi |
| `sat_runner.py` | thirrja e SAT solver-it (PySAT / CaDiCaL) me limit kohe |
| `solve.py` | zgjidh një instancë, printon formulën, planin e uljes dhe verifikimin |
| `make_instances.py` | krijon instancat në `instances/` |
| `run_experiments.py` | eksperimentet → `results/results.md`, formulat → `dimacs/*.cnf` |
| `test_seating.py` | testet |

**Hyrja:** një folder me tre skedarë CSV, ku emrat ndjekin shembullin e detyrës (M1 … M100):

```text
guests.csv        conflicts.csv     together.csv
id,gender         a,b               a,b
M1,M              M1,M30            M2,M46
M3,F              M1,M63            ...
```

**Gjeneratori** (`--random SEED`) ndërton fillimisht një plan të fshehtë të vlefshëm. Konfliktet i
zgjedh vetëm mes mysafirëve në tavolina të ndryshme, ndërsa çiftet "bashkë" vetëm brenda së njëjtës
tavolinë. Kështu instanca është gjithmonë SAT.

**Dekodimi dhe verifikimi:** nga modeli merren variablat x_{i,t} = 1 dhe ndërtohet plani i uljes.
Funksioni `verify_plan` i kontrollon të gjitha kushtet (a)–(d) drejtpërdrejt mbi planin, **pa** e
përdorur formulën.

## 4. Instancat

| Instanca | Përshkrimi | Rezultati |
|---|---|---|
| `sat_party` | 100 mysafirë (50 burra), 150 konflikte, 40 çifte bashkë | **SAT** |
| `unsat_big_family` | `sat_party` + familja M90..M100 (11 veta) duhet të ulet bashkë, por tavolina ka 10 vende | **UNSAT** |
| `unsat_enemies` | `sat_party` + M1..M11 janë armiq dy nga dy: 11 veta duhet të ndahen në 10 tavolina | **UNSAT** |

## 5. Ekzekutimi

```bash
python solve.py instances/sat_party                  # SAT: printon planin dhe verifikimin
python solve.py instances/unsat_big_family           # UNSAT
python solve.py instances/sat_party --dimacs dimacs/sat_party.cnf
python solve.py instances/unsat_enemies --no-symmetry --time-limit 60
python solve.py --random 7 --conflicts 300 --together 60
python run_experiments.py                            # ~6 min -> results/results.md
python -m unittest test_seating -v
```

## 6. Rezultatet

`python run_experiments.py`, me solver CaDiCaL 1.9.5 (PySAT) dhe limit 60 s. Tabela e plotë është te
[results/results.md](results/results.md).

**Instancat:**

| Instanca | Simetri | Variabla | Klauzola | Rezultati | Koha | Konflikte |
|---|---|---|---|---|---|---|
| sat_party | jo | 16 780 | 40 210 | SAT, verifikuar OK | 0.08 s | 833 |
| sat_party | po | 16 780 | 41 110 | SAT, verifikuar OK | < 0.01 s | 0 |
| unsat_big_family | jo | 16 780 | 40 390 | UNSAT | < 0.01 s | 10 |
| unsat_big_family | po | 16 780 | 41 290 | UNSAT | < 0.01 s | 9 |
| unsat_enemies | jo | 16 780 | 40 750 | **TIMEOUT (> 60 s)** | – | – |
| unsat_enemies | po | 16 780 | 41 650 | UNSAT | < 0.01 s | 1 |

**Thyerja e simetrisë në UNSAT:** `sat_party` + 11 armiq të zgjedhur rastësisht:

| Seed | Pa simetri | Me simetri |
|---|---|---|
| 11 | TIMEOUT (> 60 s) | UNSAT, 41.5 s |
| 12 | TIMEOUT (> 60 s) | UNSAT, 10.0 s |
| 13 | TIMEOUT (> 60 s) | UNSAT, 15.2 s |
| 14 | UNSAT, < 0.01 s | UNSAT, 0.01 s |

**Analiza:**
* Plani i instancës SAT dekodohet dhe **verifikohet** për të gjitha kushtet (a)–(d): çdo tavolinë ka
  10 veta dhe 4–6 burra, asnjë konflikt nuk ulet bashkë dhe çdo çift "bashkë" është në të njëjtën
  tavolinë.
* `unsat_big_family` vërtetohet menjëherë. Çiftet "bashkë" detyrojnë 11 veta në të njëjtën tavolinë,
  dhe numëruesi i kapacitetit e zbulon kontradiktën me unit propagation.
* `unsat_enemies` është **problemi i pigeonhole** (11 pëllumba në 10 vrima), i njohur si shumë i
  vështirë për SAT solver-at me rezolucion. Arsyeja janë simetritë: pa thyerje, solver-i duhet ta
  refuzojë veç e veç çdo mënyrë të vendosjes së armiqve në tavolina "të ndryshme" (10! ndërrime).
  **Me thyerjen e simetrisë** tavolinat e para mbushen në një rend kanonik dhe kontradikta del menjëherë.
* Te armiqtë e rastësishëm, thyerja e simetrisë e kthen TIMEOUT-in në vërtetim UNSAT brenda 10–42 s.
  Te seed 14 solver-i gjen rastësisht një vërtetim të shkurtër edhe pa të (10 konflikte), sepse
  vështirësia e UNSAT varet nga mënyra si klika ndërthuret me kufizimet e tjera.
* Te instanca SAT, thyerja e simetrisë e ul numrin e konflikteve nga 833 në 0.

**Formulat DIMACS** janë në `dimacs/` (`p cnf 16780 41110` për `sat_party`). Mund t'i zgjidhë çdo SAT
solver standard, p.sh. `minisat dimacs/sat_party.cnf`.
