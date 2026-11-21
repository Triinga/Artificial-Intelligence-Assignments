# Rezultatet – SAT: ulja e mysafirëve

`python run_experiments.py` – solver CaDiCaL 1.9.5 (PySAT), limit 60 s.

## Instancat SAT / UNSAT

| instanca | simetri | variabla | klauzola | rezultati | verifikimi | koha (s) | konflikte |
|---|---|---|---|---|---|---|---|
| sat_party | jo | 16780 | 40210 | SAT | OK | 0.08 | 833 |
| sat_party | po | 16780 | 41110 | SAT | OK | 0.00 | 0 |
| unsat_big_family | jo | 16780 | 40390 | UNSAT |  | 0.00 | 10 |
| unsat_big_family | po | 16780 | 41290 | UNSAT |  | 0.00 | 9 |
| unsat_enemies | jo | 16780 | 40750 | TIMEOUT (> 60 s) |  | — | — |
| unsat_enemies | po | 16780 | 41650 | UNSAT |  | 0.00 | 1 |

## Thyerja e simetrisë: sat_party + 11 armiq të zgjedhur rastësisht (UNSAT)

| instanca | simetri | variabla | klauzola | rezultati | verifikimi | koha (s) | konflikte |
|---|---|---|---|---|---|---|---|
| armiq11_seed11 | jo | 16780 | 40760 | TIMEOUT (> 60 s) |  | — | — |
| armiq11_seed11 | po | 16780 | 41660 | UNSAT |  | 41.45 | 820884 |
| armiq11_seed12 | jo | 16780 | 40760 | TIMEOUT (> 60 s) |  | — | — |
| armiq11_seed12 | po | 16780 | 41660 | UNSAT |  | 10.04 | 225902 |
| armiq11_seed13 | jo | 16780 | 40760 | TIMEOUT (> 60 s) |  | — | — |
| armiq11_seed13 | po | 16780 | 41660 | UNSAT |  | 15.20 | 209232 |
| armiq11_seed14 | jo | 16780 | 40760 | UNSAT |  | 0.00 | 10 |
| armiq11_seed14 | po | 16780 | 41660 | UNSAT |  | 0.01 | 9 |
