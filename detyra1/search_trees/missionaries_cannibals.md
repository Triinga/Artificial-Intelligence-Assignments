# Search Tree – Missionaries and Cannibals

## Rregullat

- 3 missionaries (`M`) dhe 3 cannibals (`C`) fillojnë në bregun e majtë.
- Barka mban 1 ose 2 persona.
- Në asnjë breg cannibals nuk mund të jenë më shumë se missionaries, përveç
  kur në atë breg nuk ka missionaries.

State representation:

```text
(M_left, C_left, BoatSide)
```

Initial: `(3,3,L)`

Goal: `(0,0,R)`

Boat moves: `2M`, `2C`, `1M1C`, `1M`, `1C`.

## BFS Search Tree i reduktuar

States invalidë eliminohen. States të përsëritur shënohen `visited`.

```text
S0 (3,3,L)
├── 2C  → S1 (3,1,R)
│          └── 1C  ← S2 (3,2,L)
│                       └── 2C  → S3 (3,0,R)
│                                    └── 1C  ← S4 (3,1,L)
│                                                 └── 2M  → S5 (1,1,R)
│                                                              └── 1M1C ← S6 (2,2,L)
│                                                                           └── 2M → S7 (0,2,R)
│                                                                                     └── 1C ← S8 (0,3,L)
│                                                                                                  └── 2C → S9 (0,1,R)
│                                                                                                               ├── 1M ← S10a (1,1,L)
│                                                                                                               │          └── 1M1C → G (0,0,R)
│                                                                                                               └── 1C ← S10b (0,2,L)
│                                                                                                                          └── 2C → G (0,0,R)
├── 1M1C → A (2,2,R) ── kthimet çojnë te S0 ose S2 (visited)
└── 1C   → B (3,2,R) ── kthimi çon te S0 (visited)
```

Një solution path me 11 kalime:

| Hapi | Move | State pas move-it |
|---:|---|---|
| 0 | Start | `(3,3,L)` |
| 1 | `2C →` | `(3,1,R)` |
| 2 | `1C ←` | `(3,2,L)` |
| 3 | `2C →` | `(3,0,R)` |
| 4 | `1C ←` | `(3,1,L)` |
| 5 | `2M →` | `(1,1,R)` |
| 6 | `1M1C ←` | `(2,2,L)` |
| 7 | `2M →` | `(0,2,R)` |
| 8 | `1C ←` | `(0,3,L)` |
| 9 | `2C →` | `(0,1,R)` |
| 10 | `1M ←` | `(1,1,L)` |
| 11 | `1M1C →` | `(0,0,R)` |

## Goal test dhe validimi

Goal arrihet kur të gjithë janë në bregun e djathtë dhe barka është djathtas.
Për çdo state kontrollohet siguria në të dy brigjet.
