# Raport – Detyra 2, Inteligjenca Artificiale

**Lënda:** Inteligjenca Artificiale (Master), Universiteti i Prishtinës
**Afati:** 03.12.2026
**Kërkesat:** [Detyra2.md](https://github.com/adrianymeri/Artificial-Intelligence-2026/blob/main/Detyra2.md)

---

## 1. Hyrje

Detyra përbëhet nga katër probleme, secili me një teknikë tjetër të Inteligjencës Artificiale:

| # | Problemi | Teknika |
|---|---|---|
| 1 | Blocked N-Queens | Kërkim i informuar – A* me heuristika |
| 2 | Ulja e 100 mysafirëve në 10 tavolina | Satisfiability (SAT) |
| 3 | Killer Sudoku | Constraint Programming (CSP) |
| 4 | Torso Decompositions (ESA SpOC-3) | Metaheuristika – sipas rekomandimit të profesorit do të realizohet në Kaggle |

Ky raport përfshin problemet 1–3. Të gjitha zgjidhjet janë në Python 3 dhe mund të riprodhohen me një
komandë për problem. Kodi, instancat, testet dhe tabelat e plota janë në folderët përkatës.

---

## 2. Problemi 1 – Blocked N-Queens me A*

### 2.1 Problemi

Në një tabelë N×N disa qeliza janë të bllokuara. Duhet të vendosen N mbretëresha në qeliza të lira
ashtu që asnjë çift të mos sulmohet: as në rresht, as në kolonë, as në diagonale. Përdoret formati
zyrtar i ASP Competition 2009 (`num(i).`, `block(i,j).`, dalja `queen(i,j).`).

### 2.2 Modeli i kërkimit

* **Gjendja:** vendosje e pjesshme rresht pas rreshti `(c₁, …, c_g)`.
* **Pasardhësit:** një mbretëreshë në rreshtin g+1, në një qelizë të lirë dhe të sigurt.
* **Kosto:** 1 për hap, pra g(n) = numri i mbretëreshave.
* **Qëllimi:** g = N.

**A\*** është implementuar nga zero: open list me `heapq` sipas f = g + h, closed set, test i qëllimit kur
nyja nxirret, dhe krasitje e fëmijëve me h = ∞. Kur f është i barabartë, zgjerohet nyja me g më të madh.

### 2.3 Heuristikat

| | Përkufizimi | Admissible |
|---|---|---|
| h1 | N − g | po |
| h2 | N − g, ose ∞ nëse ndonjë rresht i mbetur s'ka qelizë të sigurt | po |
| h3 | (N − g) + Σ 1/\|qelizat e sigurta të rreshtit\| (ide MRV) | jo |
| **h4** | propagim i rreshtave me një qelizë + matching rreshta–kolona; N − g ose ∞ | **po (e propozuar)** |

**Vëzhgimi kyç.** Çdo zgjidhje ka kosto N, prandaj h\*(n) = N − g nëse n mund të plotësohet, përndryshe
∞. Pasojat:
* h1 është tashmë e barabartë me h\* në çdo nyje me zgjidhje;
* një heuristikë mund të jetë më e mirë **vetëm duke zbuluar më herët nyjat pa zgjidhje**;
* me h1, h2, h4 vlen f = N për të gjitha nyjat.

### 2.4 Heuristika e propozuar admissible (h4) – argumenti formal

* Nëse h4 = N − g, atëherë h4 ≤ h\*, sepse h\* ∈ {N − g, ∞}.
* Nëse h4 = ∞, nyja nuk ka zgjidhje:
  * çdo rresht me vetëm një qelizë të sigurt e ka mbretëreshën aty në çdo zgjidhje, prandaj propagimi
    heq vetëm qeliza që asnjë zgjidhje s'mund t'i përdorë;
  * çdo zgjidhje vendos mbretëreshat e mbetura në kolona të ndryshme, pra formon një matching të plotë.

  Nëse propagimi ose matching-u dështojnë, zgjidhje nuk ka.
* Për nyjat që zgjerohen, fëmijët kanë h ∈ {N − g − 1, ∞}, prandaj h4(n) ≤ 1 + h4(n′): h4 është
  **konsistente**.
* Gjithashtu h1 ≤ h2 ≤ h4 ≤ h\*.

Admissibility kontrollohet edhe me test automatik: në tabela 6×6 llogaritet h\* me forcë brutale për
çdo gjendje dhe verifikohet h ≤ h\*.

### 2.5 Eksperimentet

16 instanca:
* shembulli i faqes zyrtare;
* 2 instanca pa zgjidhje;
* 12 tabela të rastësishme (N = 8…28, 10% dhe 30% qeliza të bllokuara, seed 2026);
* 1 instancë zyrtare e garës (N = 48).

Limiti: 100 000 nyje të zgjeruara.

| Heuristika | Të përfunduara | Σ nyje të zgjeruara |
|---|---|---|
| h1 | 11/16 | 553 155 |
| h2 | 12/16 | 457 746 |
| h3 | 8/16 | 856 755 |
| **h4** | **15/16** | **239 747** |

| Instanca | h1 | h2 | h3 | h4 |
|---|---|---|---|---|
| N=16, 10% | 13 404 | 5 728 | > 100 000 | **1 155** |
| N=20, 30% | 29 703 | 10 626 | > 100 000 | **2 085** |
| N=24, 30% | > 100 000 | > 100 000 | > 100 000 | **19 570** |
| N=28, 10% | > 100 000 | > 100 000 | > 100 000 | **68 797** |
| 8×8 me kolonë të bllokuar (pa zgjidhje) | 722 | 293 | 293 | **0** |

**Tie-breaking** (h1, f = N konstant): me FIFO zgjerohen 964 / 13 725 / > 100 000 nyje për
N = 8 / 10 / 12, kurse duke preferuar g më të madh zgjerohen 13 / 292 / 417.

### 2.6 Përfundime

* **h4 nuk zgjeron në asnjë instancë më shumë nyje se h1 ose h2** dhe në shumicën zgjeron 2–6 herë më
  pak se h2. Është e vetmja që përfundon për N ≥ 24. Instancat pa zgjidhje i vërteton menjëherë.
* h3 (jo-admissible) është më e keqja: e prish f = N, kërkimi kthehet drejt BFS, dhe open list arrin
  deri në 1.6 milion nyje.
* Instanca zyrtare (N = 48, 85% e bllokuar) mbetet e pazgjidhur brenda limitit. Me rend fiks
  rreshtash, A\* sillet si kërkim në thellësi dhe nuk mund ta korrigjojë një vendim të gabuar në
  rreshtat e parë.

---

## 3. Problemi 2 – SAT: ulja e mysafirëve

### 3.1 Problemi

100 mysafirë, 10 tavolina me nga 10 vende:
* (a) çiftet që nuk ulen bashkë;
* (b) çiftet që ulen bashkë;
* (c) |burra − gra| ≤ 3 në çdo tavolinë;
* (d) çdo mysafir saktësisht në një tavolinë dhe çdo tavolinë saktësisht 10 veta.

Me 10 vende kushti (c) do të thotë **4 ≤ burra ≤ 6**.

### 3.2 Formula

Variablat x_{i,t} ⇔ "mysafiri i ulet në tavolinën t" (1 000 variabla).

| Kushti | Klauzolat |
|---|---|
| (d) ALO | ∨_t x_{i,t} për çdo i |
| (d) AMO | ¬x_{i,t} ∨ ¬x_{i,t′} për çdo i, t < t′ |
| (d) kapaciteti | Σ_i x_{i,t} ≤ 10 (sequential counter); "≥ 10" rrjedh nga (d), sepse 10 tavolina × ≤ 10 = 100 mysafirë |
| (a) | ¬x_{a,t} ∨ ¬x_{b,t} për çdo t |
| (b) | (¬x_{a,t} ∨ x_{b,t}) ∧ (x_{a,t} ∨ ¬x_{b,t}) për çdo t |
| (c) | Σ_{burra} x_{i,t} ≤ 6 ∧ Σ_{gra} x_{i,t} ≤ 6 (sequential counter) |
| simetria | x_{i,t} → ∨_{j<i} x_{j,t−1} për t ≥ 2 |

**Sequential counter** (Sinz, 2005) për Σ ≤ r mbi m variabla përdor (m − 1)·r variabla ndihmëse dhe
2mr + m − 3r − 1 klauzola. Ruan arc-consistency me unit propagation.

**Thyerja e simetrisë.** Klauzolat i renditin tavolinat sipas mysafirit me numrin më të vogël. Kjo e
ruan plotësueshmërinë, sepse çdo zgjidhje mund të riemërtohet në këtë rend. Kështu eliminohen 10!
kopjet simetrike.

**Madhësia** (instanca me 50 burra, 150 konflikte, 40 çifte): **16 780 variabla, 41 110 klauzola**.

### 3.3 Rezultatet (CaDiCaL përmes PySAT, limit 60 s)

| Instanca | Pa simetri | Me simetri |
|---|---|---|
| sat_party | SAT, 0.08 s, 833 konflikte | SAT, < 0.01 s, 0 konflikte |
| unsat_big_family (11 veta duhet bashkë) | UNSAT, < 0.01 s | UNSAT, < 0.01 s |
| unsat_enemies (11 armiq, pigeonhole) | **TIMEOUT** | UNSAT, < 0.01 s |
| 11 armiq të rastësishëm, seed 11 / 12 / 13 | TIMEOUT / TIMEOUT / TIMEOUT | UNSAT 41.5 s / 10.0 s / 15.2 s |

Plani i uljes dekodohet nga modeli dhe verifikohet në mënyrë të pavarur për të gjitha kushtet (a)–(d).

### 3.4 Përfundime

* Formula është kompakte (≈ 41 000 klauzola) dhe instancat SAT zgjidhen menjëherë.
* Kontradiktat "lokale" (familja me 11 anëtarë) vërtetohen me unit propagation.
* Problemi i **pigeonhole** është klasikisht i vështirë për rezolucionin. **Thyerja e simetrisë**
  është vendimtare: e kthen TIMEOUT-in në UNSAT të vërtetuar.

---

## 4. Problemi 3 – Killer Sudoku me CSP

### 4.1 Modeli CSP

* **Variablat:** X₁…X₈₁.
* **Domeni:** {1..9}.
* **Kufizimet:**
  * AllDifferent për 9 rreshtat, 9 kolonat dhe 9 kutitë;
  * për çdo kafaz K me shumë S: AllDifferent(K) ∧ Σ_{i∈K} Xᵢ = S;
  * Xᵢ = d për shifrat e dhëna.

### 4.2 Algoritmet

**A. Solver CSP nga zero:** backtracking me
* **forward checking:** pas caktimit, vlera hiqet nga qelizat në të njëjtin rresht, kolonë, kuti dhe
  kafaz;
* **MRV:** zgjidhet qeliza me domenin më të vogël;
* **krasitje me kombinimet e kafazeve:** të gjitha bashkësitë me k shifra të ndryshme dhe shumë S
  llogariten paraprakisht, p.sh. (2, 17) → {8, 9}. Domenet e qelizave të pacaktuara kufizohen te
  kombinimet që përputhen me shumën e mbetur dhe shifrat e përdorura.

**B. Google OR-Tools CP-SAT:** i njëjti model me `AddAllDifferent` dhe kufizime lineare. Përdoret për
krahasim dhe për të vërtetuar se zgjidhja është unike.

### 4.3 Puzzle-t dhe rezultatet

Katër puzzle nga sudoku.com/killer (easy, medium, hard, expert). Kanë 31 / 26 / 10 / 0 shifra të dhëna
dhe secili ka **zgjidhje unike** (e vërtetuar me CP-SAT). Të gjitha zgjidhjet verifikohen.

| Puzzle | BT | BT + FC | BT + FC + MRV | BT + FC + MRV + kombinime | CP-SAT |
|---|---|---|---|---|---|
| easy | 284 nyje | 65 | 59 | **50 (0 backtrack)** | 0 degëzime |
| medium | 313 | 75 | 61 | **55 (0 backtrack)** | 0 degëzime |
| hard | 2 625 | 786 | 578 | **71 (0 backtrack)** | 0 degëzime |
| expert | 2 512 755 (5.8 s) | 637 270 (3.5 s) | 547 009 (3.8 s) | **307 (3 ms)** | 0 degëzime (10 ms) |

### 4.4 Përfundime

* Forward checking e ul numrin e nyjave rreth 4 herë. MRV e ul edhe pak.
* **Krasitja me kombinime është teknika vendimtare.** Te expert-i nyjet bien nga 547 009 në 307, rreth
  1 800 herë më pak, sepse shuma kthehet në kufizim domeni.
* Me të gjitha teknikat, puzzle-t easy–hard zgjidhen pa asnjë backtrack. CP-SAT, me propagim më të
  fortë mbi të gjitha kufizimet, i zgjidh të katërt pa degëzim.

---

## 5. Përfundime të përgjithshme

* **Informata e domenit vendos efikasitetin.** Te të tri problemet fitimi më i madh nuk erdhi nga
  algoritmi i kërkimit, por nga njohuria specifike për problemin:
  * matching-u te N-Queens;
  * thyerja e simetrisë te SAT;
  * kombinimet e kafazeve te Killer Sudoku.
* **Zbulimi i hershëm i dështimit** (h = ∞, forward checking, unit propagation) është ideja e
  përbashkët. Kur të gjitha zgjidhjet kanë të njëjtën kosto, kjo është e vetmja mënyrë që një
  heuristikë ta ndihmojë A\*-n.
* **Admissibility nuk është gjithmonë kriteri kryesor:** h3 jo-admissible nuk e prish cilësinë e
  zgjidhjes, por e prish rendin e kërkimit dhe performancën.
* **Kufizimet:**
  * instancat zyrtare 48×48 të Blocked N-Queens mbeten të vështira për A\* me rend fiks rreshtash;
  * instancat UNSAT të bazuara në numërim (p.sh. "61 burra") janë të vështira për SAT solver-at me
    rezolucion.

---

## 6. Referencat

1. S. Russell, P. Norvig – *Artificial Intelligence: A Modern Approach*, bot. 4, Pearson, 2020 (kap. 3: A\*, admissibility dhe konsistenca; kap. 6: CSP, forward checking, MRV).
2. ASP Competition 2009 – Blocked N-Queens, KU Leuven: <https://dtai.cs.kuleuven.be/events/ASP-competition/Benchmarks/BlockedQueens.shtml>
3. C. Sinz – *Towards an Optimal CNF Encoding of Boolean Cardinality Constraints*, CP 2005.
4. A. Ignatiev, A. Morgado, J. Marques-Silva – *PySAT: A Python Toolkit for Prototyping with SAT Oracles*, SAT 2018.
5. A. Biere, K. Fazekas, M. Fleury, M. Heisinger – *CaDiCaL, Kissat, Paracooba, Plingeling and Treengeling Entering the SAT Competition 2020*, Proc. SAT Competition 2020.
6. Google OR-Tools, CP-SAT solver: <https://developers.google.com/optimization>
7. Killer Sudoku: <https://sudoku.com/killer>
8. H. W. Kuhn – *The Hungarian Method for the Assignment Problem*, Naval Research Logistics Quarterly, 1955 (matching bipartit).
