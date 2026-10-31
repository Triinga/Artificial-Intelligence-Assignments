# Search Tree – 8-Puzzle

## Representation

State është pozita e 8 pllakave dhe e hapësirës bosh. `0` paraqet boshllëkun.
Successors krijohen duke lëvizur boshllëkun Down, Up, Left ose Right.

Initial state `S0`:

```text
1 2 3
4 0 6
7 5 8
```

Goal `G`:

```text
1 2 3
4 5 6
7 8 0
```

## BFS Search Tree

Move order: `Down, Up, Left, Right`. Lëvizja që kthehet menjëherë te parent-i
nuk gjenerohet përsëri.

```text
                              S0
                  1 2 3 / 4 0 6 / 7 5 8
               /Down        |Up        |Left       \Right
              /             |           |           \
            S1              S2          S3          S4
  1 2 3 / 4 5 6 / 7 0 8   1 0 3 /    1 2 3 /    1 2 3 /
                           4 2 6 /      0 4 6 /      4 6 0 /
                           7 5 8        7 5 8        7 5 8
          /Left       \Right
         /             \
       S5               G
  1 2 3 /          1 2 3 /
  4 5 6 /          4 5 6 /
  0 7 8            7 8 0
```

Solution path:

```text
S0 --Down--> S1 --Right--> G
```

- Solution depth: 2
- Path cost: 2 moves
- Goal test: board-i është identik me goal board.

## Çfarë duhet të shpjegoj

- Root është initial state.
- Çdo edge është një lëvizje valide e boshllëkut.
- BFS shqyrton states sipas depth-it dhe gjen zgjidhjen më të shkurtër kur
  çdo move ka cost 1.
- `visited` shmang cikle si kthimi Down pastaj Up.
