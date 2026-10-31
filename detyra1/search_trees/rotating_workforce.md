# Search Tree – Rotating Workforce Scheduling

## Shembulli i zgjedhur

Kemi tre punëtorë: `A`, `B`, `C`.

Kemi tre shifts çdo ditë:

- Morning (`M`)
- Evening (`E`)
- Night (`N`)

Orari zgjat 3 ditë. Constraints:

1. Çdo punëtor punon një shift në ditë.
2. Çdo shift ka saktësisht një punëtor në ditë.
3. Brenda tri ditëve, çdo punëtor duhet ta punojë secilin shift saktësisht
   një herë.

State është lista e assignments për ditët e planifikuara. Një tuple tregon
punëtorin për `(M, E, N)`.

## Initial state

Për symmetry breaking fiksojmë ditën e parë:

```text
Day 1: (A, B, C)
```

Pra A punon Morning, B Evening dhe C Night.

## Search Tree

Në Day 2, askush nuk mund ta përsërisë shift-in e Day 1. Vetëm dy
permutations janë valide:

```text
                         S0
                  Day 1: (A,B,C)
                    /             \
                   /               \
            S1: Day 2 (B,C,A)   S2: Day 2 (C,A,B)
                   |               |
                   |               |
            Day 3 (C,A,B)       Day 3 (B,C,A)
                   |               |
                  G1              G2
```

Të dy leaves janë goal states valide.

Orari `G1`:

| Day | Morning | Evening | Night |
|---|---|---|---|
| 1 | A | B | C |
| 2 | B | C | A |
| 3 | C | A | B |

## Search components

- Variable: assignment i një punëtori në një shift të një dite.
- Domain: `{A, B, C}`.
- Successor: një permutation valide për ditën tjetër.
- Goal: 3 ditë të plotësuara dhe çdo punëtor ka punuar çdo shift një herë.
- Invalid branch: përsërit një punëtor në të njëjtin shift ose përdor një
  punëtor dy herë në të njëjtën ditë.

Kjo është një Search Tree e vogël, por demonstron qartë branching, constraints,
symmetry breaking dhe goal states.
