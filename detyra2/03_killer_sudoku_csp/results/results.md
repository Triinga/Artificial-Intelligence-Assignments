# Rezultatet – Killer Sudoku

`python run_experiments.py`. *nyje* = vlera të provuara, *backtrack* = vlera që dështuan. Për CP-SAT jepen degëzimet dhe konfliktet e solver-it; CP-SAT kërkon edhe një zgjidhje të dytë për të vërtetuar unicitetin.

| puzzle | solver | statusi | verifikimi | koha (ms) | nyje | backtrack |
|---|---|---|---|---|---|---|
| easy | BT | solved | OK | 0.7 | 284 | 234 |
| easy | BT + FC | solved | OK | 0.7 | 65 | 15 |
| easy | BT + FC + MRV | solved | OK | 1.0 | 59 | 9 |
| easy | BT + FC + MRV + kombinime | solved | OK | 0.7 | 50 | 0 |
| easy | CP-SAT (unike) | solved | OK | 5.3 | 0 degëzime | 0 konflikte |
| medium | BT | solved | OK | 0.6 | 313 | 258 |
| medium | BT + FC | solved | OK | 0.5 | 75 | 20 |
| medium | BT + FC + MRV | solved | OK | 0.9 | 61 | 6 |
| medium | BT + FC + MRV + kombinime | solved | OK | 0.7 | 55 | 0 |
| medium | CP-SAT (unike) | solved | OK | 1.6 | 0 degëzime | 0 konflikte |
| hard | BT | solved | OK | 4.0 | 2625 | 2554 |
| hard | BT + FC | solved | OK | 2.8 | 786 | 715 |
| hard | BT + FC + MRV | solved | OK | 4.8 | 578 | 507 |
| hard | BT + FC + MRV + kombinime | solved | OK | 0.5 | 71 | 0 |
| hard | CP-SAT (unike) | solved | OK | 1.9 | 0 degëzime | 0 konflikte |
| expert | BT | solved | OK | 5817.8 | 2512755 | 2512674 |
| expert | BT + FC | solved | OK | 3482.3 | 637270 | 637189 |
| expert | BT + FC + MRV | solved | OK | 3770.7 | 547009 | 546928 |
| expert | BT + FC + MRV + kombinime | solved | OK | 3.2 | 307 | 226 |
| expert | CP-SAT (unike) | solved | OK | 9.5 | 0 degëzime | 0 konflikte |

## Zgjidhjet

**easy** (32 kafaze, 31 shifra të dhëna)

```text
+-------+-------+-------+
| 8 2 3 | 4 9 6 | 1 5 7 |
| 7 5 4 | 2 1 8 | 3 9 6 |
| 1 6 9 | 7 5 3 | 2 8 4 |
+-------+-------+-------+
| 3 8 7 | 9 6 2 | 4 1 5 |
| 4 9 2 | 1 8 5 | 7 6 3 |
| 5 1 6 | 3 7 4 | 9 2 8 |
+-------+-------+-------+
| 6 3 1 | 8 2 7 | 5 4 9 |
| 9 4 8 | 5 3 1 | 6 7 2 |
| 2 7 5 | 6 4 9 | 8 3 1 |
+-------+-------+-------+
```

**medium** (34 kafaze, 26 shifra të dhëna)

```text
+-------+-------+-------+
| 2 6 9 | 4 1 5 | 3 7 8 |
| 5 8 1 | 7 6 3 | 4 2 9 |
| 4 7 3 | 9 2 8 | 5 6 1 |
+-------+-------+-------+
| 1 3 5 | 6 7 2 | 9 8 4 |
| 9 4 6 | 8 3 1 | 2 5 7 |
| 7 2 8 | 5 4 9 | 6 1 3 |
+-------+-------+-------+
| 6 9 4 | 1 5 7 | 8 3 2 |
| 8 1 2 | 3 9 6 | 7 4 5 |
| 3 5 7 | 2 8 4 | 1 9 6 |
+-------+-------+-------+
```

**hard** (34 kafaze, 10 shifra të dhëna)

```text
+-------+-------+-------+
| 9 3 1 | 4 2 7 | 5 6 8 |
| 6 7 8 | 9 1 5 | 3 4 2 |
| 2 4 5 | 6 8 3 | 1 9 7 |
+-------+-------+-------+
| 4 9 7 | 1 3 2 | 6 8 5 |
| 1 2 6 | 5 9 8 | 7 3 4 |
| 5 8 3 | 7 6 4 | 2 1 9 |
+-------+-------+-------+
| 3 5 4 | 8 7 1 | 9 2 6 |
| 7 6 2 | 3 4 9 | 8 5 1 |
| 8 1 9 | 2 5 6 | 4 7 3 |
+-------+-------+-------+
```

**expert** (34 kafaze, 0 shifra të dhëna)

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
