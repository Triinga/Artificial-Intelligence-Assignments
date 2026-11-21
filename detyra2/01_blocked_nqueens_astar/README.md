# Problemi 1 – Blocked N-Queens me A*

**Kërkesat e detyrës:** (1) zgjidhja e problemit me algoritmin A*, (2) të paktën tre heuristika,
(3) propozimi i një heuristike *admissible* bazuar në rezultatet.

## 1. Problemi

Burimi: [ASP Competition 2009 – Blocked N-Queens](https://dtai.cs.kuleuven.be/events/ASP-competition/Benchmarks/BlockedQueens.shtml).

Në një tabelë N×N disa qeliza janë të bllokuara. Duhet të vendosen N mbretëresha në qeliza të lira
ashtu që asnjë çift të mos jetë në të njëjtin rresht, kolonë ose diagonale.

**Hyrja** (formati zyrtar, indekse 1..N):

```text
num(1). num(2). num(3). num(4).
block(1,1). block(2,2). block(4,3).
```

**Dalja** (formati zyrtar) dhe vizatimi (`Q` mbretëreshë, `#` e bllokuar, `.` e lirë):

```text
# . Q .
Q # . .
. . . Q
. Q # .

queen(1,3). queen(2,1). queen(3,4). queen(4,2).
```

## 2. Modeli i kërkimit për A*

| Elementi | Përkufizimi |
|---|---|
| Gjendja | vendosje e pjesshme rresht pas rreshti: `(c_1, …, c_g)` = kolonat e mbretëreshave në rreshtat 1..g |
| Gjendja fillestare | tabela bosh, g = 0 |
| Pasardhësit | një mbretëreshë në rreshtin g+1, në një qelizë **të lirë** dhe **të sigurt** |
| Kosto e hapit | 1, pra `g(n)` = numri i mbretëreshave të vendosura |
| Qëllimi | g = N |

**A\*** (`astar.py`, nga zero):
* *open list* = priority queue (`heapq`) e renditur sipas `f(n) = g(n) + h(n)`;
* *closed set* = gjendjet e zgjeruara (nuk zgjerohen dy herë);
* testi i qëllimit bëhet kur nyja nxirret nga open list;
* fëmijët me `h = ∞` (pa zgjidhje) nuk futen në open list;
* kur f është i barabartë, zgjidhet nyja me g më të madh (*tie-breaking* "deep", shih §5).

Sulmet ruhen në tre bitmask-a (kolonat, dy drejtimet e diagonaleve), prandaj qelizat e sigurta të një
rreshti gjenden me disa operacione mbi bitë.

## 3. Heuristikat

`R` = rreshtat e mbetur, `S(r)` = qelizat e lira dhe të sigurta të rreshtit r.

| | Përkufizimi | Admissible? |
|---|---|---|
| **h1** | `N − g` (numri i mbretëreshave që mbeten) | po |
| **h2** | `N − g`, por `∞` nëse ndonjë rresht `r ∈ R` ka `S(r) = ∅` (rrugë pa dalje) | po |
| **h3** | `(N − g) + Σ_{r∈R} 1/|S(r)|` (ide MRV: penalizon rreshtat me pak opsione) | **jo** |
| **h4** | e propozuar, shih §4 | po |

### Vëzhgimi kyç: si duket kosto e vërtetë h*

Çdo zgjidhje ka saktësisht N mbretëresha, pra **çdo zgjidhje ka të njëjtën kosto N**. Për një nyje n
me g mbretëresha:

$$h^*(n) = \begin{cases} N - g & \text{nëse } n \text{ mund të plotësohet në zgjidhje} \\ \infty & \text{nëse jo} \end{cases}$$

Prej kësaj rrjedhin tri gjëra:
1. h1 = N − g është admissible dhe është **e barabartë me h\*** në çdo nyje që ka zgjidhje. Prandaj
   një heuristikë mund të jetë më e mirë se h1 **vetëm duke zbuluar më herët nyjat pa zgjidhje (∞)**.
2. Me h1, h2, h4 kemi `f = N` për çdo nyje në open list. Rendin e zgjerimit e vendos tie-breaking
   (§5).
3. h3 nuk është admissible, sepse mund të japë deri në 2(N − g) > h\*. Këtu kjo nuk e prish cilësinë e
   zgjidhjes, sepse çdo zgjidhje është optimale. Megjithatë vlerat e f nuk janë më të barabarta dhe
   nyjat e cekëta me penalizim të vogël kalojnë para nyjave të thella. Kërkimi i afrohet BFS-së
   dhe open list rritet shumë (shih rezultatet).

## 4. Heuristika e propozuar admissible h4

**Ideja nga rezultatet:** h2 është më e mirë se h1, sepse zbulon disa rrugë pa dalje. h3, e cila
ndryshon vlerat e f, del më e keqja. Prandaj propozojmë një heuristikë që e mban formën
`h ∈ {N − g, ∞}` por e zbulon "∞" shumë më herët:

1. **Propagim:** nëse një rresht i mbetur ka vetëm **një** qelizë të sigurt, mbretëresha e tij duhet
   të jetë aty. E vendosim virtualisht dhe heqim kolonën dhe diagonalet e saj nga rreshtat e tjerë.
   Përsëritet derisa të mos ketë më rreshta të tillë. Nëse një rresht mbetet pa qeliza, h4 = ∞.
2. **Matching:** rreshtat e mbetur duhet të marrin kolona **të ndryshme**. Nëse nuk ekziston
   *matching* i plotë rreshta→kolona në grafin bipartit `{(r, c) : c ∈ S(r)}` (algoritmi i Kuhn-it),
   atëherë h4 = ∞.
3. Përndryshe h4 = N − g.

**Teorema.** `h4(n) ≤ h*(n)` për çdo nyje n, pra h4 është admissible.

**Prova.**
* Nëse `h4(n) = N − g`: gjithmonë `h*(n) ∈ {N − g, ∞}`, prandaj `h4(n) ≤ h*(n)`.
* Nëse `h4(n) = ∞`: tregojmë që n nuk ka zgjidhje. Supozojmë të kundërtën, se ekziston një plotësim Q.
  * *Propagimi është korrekt:* nëse rreshti r ka vetëm një qelizë të sigurt (r, c), mbretëresha e Q në
    rreshtin r duhet të jetë në (r, c), sepse të gjitha qelizat e tjera janë të bllokuara ose të
    sulmuara. Me induksion, çdo vendosje virtuale është pjesë e Q dhe çdo qelizë e hequr sulmohet nga
    një mbretëreshë e Q. Pra mbretëreshat e Q janë gjithmonë në qeliza që nuk hiqen, dhe asnjë rresht
    nuk mund të mbetet pa qeliza.
  * *Matching-u është korrekt:* mbretëreshat e Q në rreshtat e mbetur janë në kolona të ndryshme dhe
    në qeliza të lejuara, pra vetë ato formojnë një matching të plotë.

  Në të dy rastet dalim në kontradiktë, pra `h*(n) = ∞`. ∎

**Konsistenca.** Një nyje që zgjerohet ka `h4 = N − g` (nyjat me ∞ nuk futen në open). Çdo fëmijë ka
`h4 ∈ {N − g − 1, ∞}` dhe kosto hapi 1. Pra `h4(n) ≤ 1 + h4(n')`, prandaj h4 është edhe
**konsistente**.

**Dominanca.** `h1 ≤ h2 ≤ h4 ≤ h*`. Nëse h2 = ∞, një rresht s'ka qeliza, prandaj as matching-u nuk
ekziston dhe h4 = ∞. h4 është pra më e informuara nga heuristikat admissible.

**Kostoja:** h4 llogaritet në O(N³) për nyje (h1 në O(1)), por kursen shumë nyje.

Admissibility kontrollohet edhe me test automatik: në 10 tabela 6×6 kalohen **të gjitha** gjendjet,
h\* llogaritet me forcë brutale dhe verifikohet `h ≤ h*` për h1, h2, h4.

## 5. Rezultatet

`python run_experiments.py` (rreth 5 min). Tabelat e plota janë në [results/results.md](results/results.md).
Limiti për çdo ekzekutim: **100 000 nyje të zgjeruara**. Seed i fiksuar: 2026. Limiti është numri i
nyjave dhe jo koha, prandaj numrat e nyjave dalin identikë në çdo kompjuter.

**Instancat** (16):
* `example_page`: shembulli nga faqja zyrtare;
* dy instanca pa zgjidhje: `unsat_n3`, tabelë 3×3, dhe `unsat_kolona4_n8`, tabelë 8×8 me kolonën 4
  të bllokuar;
* 12 tabela të rastësishme me N = 8, 12, 16, 20, 24, 28 dhe densitet bllokimi 10% e 30%;
* një instancë zyrtare e garës (N = 48, 1962 qeliza të bllokuara).

**Përmbledhja:**

| Heuristika | Të përfunduara (zgjidhje ose vërtetim pa zgjidhje) | Σ nyje të zgjeruara |
|---|---|---|
| h1 | 11/16 | 553 155 |
| h2 | 12/16 | 457 746 |
| h3 | 8/16 | 856 755 |
| **h4** | **15/16** | **239 747** |

**Nyjet e zgjeruara në disa instanca** ("limit" = mbi 100 000 nyje pa përfunduar):

| Instanca | h1 | h2 | h3 | h4 |
|---|---|---|---|---|
| N=12, 10% | 139 | 61 | 6 440 | **22** |
| N=16, 10% | 13 404 | 5 728 | limit | **1 155** |
| N=20, 30% | 29 703 | 10 626 | limit | **2 085** |
| N=24, 30% | limit | limit | limit | **19 570** |
| N=28, 10% | limit | limit | limit | **68 797** |
| N=28, 30% | limit | limit | limit | **41 504** |
| 8×8 me kolonë të bllokuar (pa zgjidhje) | 722 | 293 | 293 | **0** |
| zyrtare N=48 | limit | limit | limit | limit |

**Tie-breaking.** Me h1, `f = N` për të gjitha nyjat. Me FIFO, A\* zgjeron nivel pas niveli si BFS:
964, 13 725 dhe > 100 000 nyje për N = 8, 10, 12. Me "deep" zgjeron 13, 292 dhe 417 nyje.

**Analiza:**
* **h4 nuk zgjeron në asnjë instancë më shumë nyje se h1 ose h2.** Në shumicën e instancave zgjeron
  shumë më pak. Te 8×8 me kolonë të bllokuar, matching-u e vërteton menjëherë që s'ka zgjidhje
  (0 nyje), kurse h1 duhet të provojë 722 nyje.
* h2 ul numrin e nyjave rreth 2–3 herë krahasuar me h1. h4 e ul edhe 2–6 herë krahasuar me h2.
* h3 (jo-admissible) është më e keqja. Te N = 12 zgjeron 6 440 nyje kundrejt 139 të h1, sepse
  penalizimi e prish `f = N` dhe kërkimi kthehet drejt BFS. Edhe memoria rritet shumë: open list
  arrin deri në 1.6 milion nyje, kurse te h4 mbetet nën 70 000.
* Për nyje, h4 kushton më shumë kohë se h1 (O(N³) kundrejt O(1)). Prandaj në instanca të vogla h1
  mund të jetë pak më e shpejtë në sekonda, por për N ≥ 24 h4 është e vetmja që përfundon.
* **Instancat zyrtare** (N = 48, 85% të bllokuara) janë instanca gare të ndërtuara për të qenë të
  vështira. Asnjë heuristikë nuk e zgjidh instancën brenda limitit. Me rend fiks të rreshtave, A\*
  sillet si kërkim në thellësi me lookahead dhe nuk mund ta "korrigjojë" një vendim të gabuar në
  rreshtat e parë pa e eksploruar gjithë nënpemën.
* **Closed set** në këtë model nuk gjen kurrë duplikate. Rreshtat mbushen sipas një rendi fiks, prandaj
  çdo gjendje ka vetëm një prind dhe hapësira e gjendjeve është pemë.

## 6. Ekzekutimi

Nga ky folder:

```bash
python solve.py instances/example_page.lp                 # default h4
python solve.py instances/example_page.lp --heuristic h2  # h1 | h2 | h3 | h4
python solve.py --random 16 --density 0.3 --seed 2026     # tabelë e rastësishme
python solve.py --random 12 --save-instance board.lp --out solution.lp
python run_experiments.py                                 # tabelat -> results/
python -m unittest test_astar -v                          # testet
```

## 7. Skedarët

| Skedari | Përmbajtja |
|---|---|
| `board.py` | tabela, leximi/shkrimi i formatit ASP, gjeneratori i rastësishëm, verifikimi, vizatimi |
| `astar.py` | A* dhe heuristikat h1–h4 |
| `solve.py` | zgjidhja e një instance nga linja e komandës |
| `run_experiments.py` | krahasimi i heuristikave → `results/` |
| `test_astar.py` | teste: krahasim me forcë brutale, admissibility, instanca pa zgjidhje |
| `instances/` | shembulli i faqes, instanca pa zgjidhje, një shembull i rastësishëm, 2 instanca zyrtare |
