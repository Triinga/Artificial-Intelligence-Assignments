# Social Golfers – DFS me Backtracking

## Përgjigjja

Për 32 lojtarë, 8 grupe dhe 4 lojtarë në grup, maksimumi është **10 javë**.

Kjo përgjigje vjen nga **dy pjesë**, dhe është e rëndësishme t'i ndajmë:

1. **Upper bound (matematikë, jo search).** Çdo lojtar takohet me `p - 1 = 3`
   lojtarë të rinj në javë dhe ka vetëm 31 lojtarë të tjerë:

   ```text
   w * 3 <= 31
   w <= floor(31 / 3) = 10
   ```

   Pra më shumë se 10 javë është e pamundur.

2. **Orari 10-javor ekziston (burim i publikuar).** Orari `8-4-10` i
   Alejandro Aguado-s (shih burimin në fund) kalon validator-in tonë
   (`verify_known_solution.py`). Pra 10 javë arrihen, dhe bound-i është
   optimal.

**Çfarë NUK e bën DFS-i ynë:** DFS-i ynë **nuk** e gjen vetë orarin
10-javor. Ai gjen shpejt `8-4-5`, por nuk e përfundon `8-4-6` as brenda
20 sekondave (shih tabelën më poshtë). Orari 10-javor është marrë nga
literatura dhe ne vetëm e **verifikojmë**. Kjo është arsyeja pse kodi ka
opsionin `--time-limit`.

### Maksimumi me një komandë

```bash
python -m detyra1.social_golfers.max_weeks 8 4
```

`max_weeks.py` provon DFS-in për `w = 1, 2, 3, ...` (me time limit për çdo
`w`, default 20 s) dhe ndalet në njërin nga tre rastet:

| Rasti | Çfarë do të thotë | Përgjigjja |
|---|---|---|
| DFS gjen orar për `w = upper bound` | bound-i arrihet | maksimumi = bound (i provuar nga DFS) |
| DFS e kërkon gjithë pemën dhe nuk gjen orar për `w` | `w` javë janë të pamundura | maksimumi = `w - 1` (i provuar nga DFS) |
| Kalon time limit | DFS jep vetëm një kufi të poshtëm | për `8 4` verifikohet orari i publikuar |

Rezultatet e matura:

| Instanca | Upper bound | DFS gjen deri në | Ndalet sepse | Përgjigjja |
|---|---:|---:|---|---|
| `2 2` | 3 | 3 | bound arrihet | 3 |
| `2 3` | 2 | 1 | `w=2` pa orar | 1 |
| `3 3` | 4 | 4 | bound arrihet | 4 |
| `5 5` | 6 | 6 | bound arrihet | 6 |
| `8 4` | 10 | 5 | time limit te `w=6` | **10** (orari i publikuar, i validuar) |

Pra për instancat e vogla maksimumi del **vetëm nga DFS-i**. Për `8 4`
programi e shkruan qartë se DFS-i arrin 5 javë dhe se përgjigjja 10 vjen
nga orari i publikuar që validohet.

Rasti "pa orar" është provë e vërtetë: DFS me backtracking është complete,
pra kur nuk gjen asgjë, orari nuk ekziston. Fiksimi i javës së parë nuk e
prish këtë, sepse çdo javë e parë mund të riemërtohet në atë formë.

### Rezultatet e matura të DFS-it

| Instanca | Rezultati | Nodes generated | Nodes visited | Backtracks | Koha |
|---|---|---:|---:|---:|---:|
| `2 2 3` | gjendet | 7 | 6 | 0 | ~0.00003 s |
| `5 5 6` | gjendet | 245,253 | 97 | 53 | ~0.13 s |
| `8 4 4` | gjendet | 9,882 | 27 | 0 | ~0.004 s |
| `8 4 5` | gjendet | 14,274 | 36 | 0 | ~0.006 s |
| `8 4 6` | **time limit 20 s** | ~31–46 milion | ~0.7–1.1 milion | ~0.7–1.1 milion | 20 s |

Për `8 4 6` numrat varen nga shpejtësia e kompjuterit, sepse search-i
ndalet nga ora: në dy ekzekutime morëm 31,239,467 dhe 45,963,337 nodes
generated (726,048 dhe 1,076,300 backtracks). Në të dyja rastet nuk u gjet
orar. Rastet e tjera janë deterministe dhe japin gjithmonë të njëjtët numra.

Për `8 4 6`, maximum depth mbetet 40 = 5 javë × 8 grupe: brenda 20 sekondave
DFS-i nuk arrin të vendosë as grupin e parë të javës 6. Zgjedhjet e javëve
2–5 duhet të ndryshohen thellë në pemë, dhe DFS i thjeshtë (pa heuristics)
e ka këtë shumë të vështirë. Kur kalon time limit, programi shkruan se nuk u
gjet orar **ende**. Kjo **nuk** provon se orari nuk ekziston.

## Modeli i problemit

Parametrat janë:

- `g`: numri i grupeve në javë;
- `p`: numri i lojtarëve në grup;
- `w`: numri i javëve;
- `n = g * p`: numri total i lojtarëve.

### State representation

```text
schedule[week][group] = lojtarët e grupit
```

State-i i DFS-it ruan edhe:

- grupet e plotësuara;
- lojtarët që kanë mbetur në javën aktuale;
- `used_pairs`, çiftet që kanë luajtur tashmë bashkë.

### Initial state

Orari dhe `used_pairs` fillojnë bosh. Si symmetry breaking opsional, java e
parë mund të fiksohet në grupe të njëpasnjëshme.

### Goal state

Goal arrihet kur janë plotësuar të gjitha `w` javët dhe asnjë constraint nuk
është shkelur.

## Variables dhe domain

Formalisht, një variabël mund të shkruhet si `X[week, group, position]`.
Vlera e saj tregon cili lojtar gjendet në atë pozitë.

```text
Domain = {0, 1, ..., n - 1}
```

Për rastin konkret domain është `{0, 1, ..., 31}`.

## Constraints

1. Çdo grup ka saktësisht `p` lojtarë.
2. Çdo lojtar paraqitet saktësisht një herë në çdo javë.
3. Çdo çift lojtarësh luan bashkë maksimumi një herë.

Një grup me 4 lojtarë krijon `C(4, 2) = 6` çifte që kontrollohen në
`used_pairs`.

## Objective function

Problemi origjinal kërkon:

```text
maximize w
```

duke respektuar të gjitha constraints. Për `g`, `p` dhe `w` të dhëna, DFS
kërkon një schedule me zero shkelje.

Për çdo state (orar i plotë ose i pjesshëm) përkufizojmë një funksion
numerik që numëron shkeljet:

```text
f(schedule) = numri i çifteve që luajnë bashkë më shumë se një herë
```

Më saktë: për çdo çift lojtarësh `{a, b}`, le të jetë `m(a, b)` numri i
grupeve ku janë bashkë. Atëherë:

```text
f(schedule) = Σ max(0, m(a, b) - 1)    për të gjitha çiftet {a, b}
```

- **Goal:** `f(schedule) = 0` dhe të gjitha `w` javët janë plotësuar.
- **Problemi i plotë:** `maximize w` me kusht `f(schedule) = 0`.

Shembull: nëse lojtarët 0 dhe 1 janë bashkë në javën 1 dhe sërish në javën
2, atëherë `m(0, 1) = 2` dhe ky çift shton `1` te `f`.

DFS-i ynë nuk e shton kurrë një grup që përsërit një çift (kontrolli me
`used_pairs`), prandaj gjatë gjithë search-it `f` mbetet `0`. Funksioni `f`
shërben për të treguar formalisht se çfarë do të thotë "orar valid"; në kod,
të njëjtën gjë e kontrollon `validate_schedule`.

## Landscape / search space

Për një javë, numri i ndarjeve të `n` lojtarëve në `g` grupe të parenditura
me nga `p` lojtarë është:

```text
P = n! / ((p!)^g * g!)
```

Për `n=32`, `g=8`, `p=4`:

```text
P = 32! / ((4!)^8 * 8!) ≈ 5.93 * 10^19
```

Vlera e saktë është `P = 59,287,247,761,257,140,625`.

Për `w` javë, raw search space është `P^w` para constraints. Me javën e parë
të fiksuar (symmetry breaking) mbetet `P^(w-1)`.

| Javë `w` | `P^w` | `P^(w-1)` (java 1 fiks) |
|---:|---:|---:|
| 1 | `5.93 * 10^19` | 1 |
| 2 | `3.51 * 10^39` | `5.93 * 10^19` |
| 5 | `7.32 * 10^98` | `1.24 * 10^79` |
| 6 | `4.34 * 10^118` | `7.32 * 10^98` |
| 10 | `5.37 * 10^197` | `9.05 * 10^177` |

Këto janë numra **para** pair constraint. Constraint-i "çdo çift luan bashkë
maksimumi një herë" pret pjesën më të madhe të tyre (p.sh. për `8-4-5`
kemi 14,242 grupe të prera nga 14,274 të gjeneruara), por hapësira mbetet
shumë e madhe. Kjo shpjegon pse DFS-i gjen `8-4-5` menjëherë, por nuk e
përfundon `8-4-6` brenda 20 sekondave.

Search tree ka thellësi `d = g * w`, sepse kodi shton nga një grup në çdo
nivel. Branching factor ndryshon sipas lojtarëve dhe çifteve që kanë mbetur.

## DFS me Backtracking

```text
DFS(state):
    nëse të gjitha javët janë plotësuar:
        kthe SUCCESS

    për çdo candidate group:
        nëse ndonjë çift është përdorur:
            vazhdo te grupi tjetër

        shto grupin dhe çiftet e tij

        nëse DFS(state) ka sukses:
            kthe SUCCESS

        largo grupin dhe çiftet e tij   <- backtracking

    kthe FAILURE
```

DFS është i përshtatshëm sepse kërkon më pak memory se BFS dhe backtracking
lejon zhbërjen e menjëhershme të një zgjedhjeje që çon në dead end.

### Time limit

Me `--time-limit SECONDS`, DFS-i kontrollon orën në çdo node. Kur koha
kalon, hidhet një exception (`_TimeLimitReached`) që e ndalon gjithë
recursion-in menjëherë, dhe rezultati ka `timed_out = True`. Pa këtë opsion
DFS-i vazhdon pa kufi.

### Complexity

- Time: `O(b^d)` në worst case.
- Space: `O(d + n^2)` kur successors gjenerohen një nga një; `n^2` mbulon
  ruajtjen e çifteve.

## File-t

- `social_golfers.py`: DFS, backtracking, validator dhe statistikat.
- `known_solution_8_4_10.py`: orari optimal i publikuar, vetëm si test/dëshmi.
- `verify_known_solution.py`: validon orarin 10-javor.
- `max_weeks.py`: gjen maksimumin e javëve me DFS për `w = 1, 2, ...`.
- `../tests/test_social_golfers.py`: testet automatike.

## Ekzekutimi

Nga root-i i repository-t:

```bash
python -m detyra1.social_golfers.max_weeks 8 4
python -m detyra1.social_golfers.max_weeks 5 5
python -m detyra1.social_golfers.social_golfers 5 5 6
python -m detyra1.social_golfers.social_golfers 8 4 5
python -m detyra1.social_golfers.social_golfers 8 4 6 --time-limit 20
python -m detyra1.social_golfers.verify_known_solution
python -m unittest discover -s detyra1/tests -v
```

Rasti `5-5-6` demonstron DFS me backtracking real (53 backtracks). Rasti
`2-2-3` zgjidhet me 0 backtracks, prandaj nuk e tregon backtracking-un.
Rasti `8-4-5` tregon se DFS-i gjen 5 javë për problemin e detyrës, kurse
`8-4-6` tregon kufirin e tij. Rasti i njohur `8-4-10` demonstron se 10 javë
janë të mundshme dhe valide. Nuk pretendojmë se orari i publikuar është
gjeneruar nga DFS-i ynë.

## Burimi i orarit optimal

Alejandro Aguado, [A 10 Days Solution to the Social Golfer Problem](https://www.mathpuzzle.com/MAA/54-Golf%20Tournaments/socgolf1.pdf).
