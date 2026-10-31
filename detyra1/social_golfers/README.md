# Social Golfers – DFS me Backtracking

## Përgjigjja

Për 32 lojtarë, 8 grupe dhe 4 lojtarë në grup, maksimumi është **10 javë**.

Çdo lojtar takohet me `p - 1 = 3` lojtarë të rinj në javë dhe ka vetëm 31
lojtarë të tjerë:

```text
w * 3 <= 31
w <= floor(31 / 3) = 10
```

Orari i publikuar `8-4-10` kalon validator-in tonë, prandaj upper bound 10
arrihet dhe është optimal.

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

## Landscape / search space

Për një javë, numri i ndarjeve të `n` lojtarëve në `g` grupe të parenditura
me nga `p` lojtarë është:

```text
P = n! / ((p!)^g * g!)
```

Për `n=32`, `g=8`, `p=4`:

```text
P = 32! / ((4!)^8 * 8!) ≈ 5.94 * 10^19
```

Për `w` javë, raw search space është `P^w` para constraints. Search tree ka
thellësi `d = g * w`, sepse kodi shton nga një grup në çdo nivel. Branching
factor ndryshon sipas lojtarëve dhe çifteve që kanë mbetur.

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

### Complexity

- Time: `O(b^d)` në worst case.
- Space: `O(d + n^2)` kur successors gjenerohen një nga një; `n^2` mbulon
  ruajtjen e çifteve.

## File-t

- `social_golfers.py`: DFS, backtracking, validator dhe statistikat.
- `known_solution_8_4_10.py`: orari optimal i publikuar, vetëm si test/dëshmi.
- `verify_known_solution.py`: validon orarin 10-javor.
- `../tests/test_social_golfers.py`: testet automatike.

## Ekzekutimi

Nga root-i i repository-t:

```bash
python -m detyra1.social_golfers.social_golfers 2 2 3
python -m detyra1.social_golfers.verify_known_solution
python -m unittest discover -s detyra1/tests -v
```

Rasti `2-2-3` demonstron DFS. Rasti i njohur `8-4-10` demonstron se 10 javë
janë të mundshme dhe valide. Nuk pretendojmë se orari i publikuar është
gjeneruar nga DFS-i ynë.

## MBROJTJA – çfarë duhet të di

1. **Pse ruajmë `used_pairs`?** Që të kontrollojmë shpejt nëse një çift është
   takuar më herët.
2. **Ku ndodh backtracking?** Kur recursive call dështon; grupi dhe çiftet e
   tij largohen para provës tjetër.
3. **Pse maksimumi është 10?** Një lojtar takon 3 të rinj në javë dhe ka vetëm
   31 lojtarë të tjerë: `floor(31/3)=10`.
4. **Çfarë është state?** Orari parcial, lojtarët e mbetur dhe `used_pairs`.
5. **Çfarë është goal test?** Të gjitha javët janë plotësuar pa shkelje.
6. **Pse DFS?** Ka memory të ulët dhe lidhet natyrshëm me backtracking.
7. **Çfarë bën symmetry breaking?** Heq orare ekuivalente pa hequr zgjidhje
   reale.
8. **Sa është search space për një javë?**
   `32! / ((4!)^8 * 8!) ≈ 5.94 * 10^19`.

## Burimi i orarit optimal

Alejandro Aguado, [A 10 Days Solution to the Social Golfer Problem](https://www.mathpuzzle.com/MAA/54-Golf%20Tournaments/socgolf1.pdf).
