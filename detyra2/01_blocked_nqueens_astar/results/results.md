# Rezultatet – Blocked N-Queens me A*

`python run_experiments.py` – seed 2026, limit 100000 nyje të zgjeruara, tie = deep.
*nyje_ne_memorie* = max |open| + |closed|.

## Përmbledhje

| heuristika | të përfunduara | Σ zgjeruara | Σ koha (s) |
|---|---|---|---|
| h1 | 11/16 | 553155 | 2.87 |
| h2 | 12/16 | 457746 | 8.22 |
| h3 | 8/16 | 856755 | 123.50 |
| h4 | 15/16 | 239747 | 57.44 |

## Të gjitha ekzekutimet

| instanca | N | heuristika | statusi | zgjeruara | gjeneruara | krasitura | nyje_ne_memorie | koha_s |
|---|---|---|---|---|---|---|---|---|
| example_page | 4 | h1 | ✔ zgjidhur | 7 | 8 | 0 | 10 | 0.0 |
| example_page | 4 | h2 | ✔ zgjidhur | 6 | 8 | 1 | 9 | 0.0 |
| example_page | 4 | h3 | ✔ zgjidhur | 4 | 6 | 0 | 7 | 0.0 |
| example_page | 4 | h4 | ✔ zgjidhur | 4 | 6 | 2 | 5 | 0.0 |
| unsat_n3 | 3 | h1 | ✘ pa zgjidhje (vërtetuar) | 6 | 5 | 0 | 9 | 0.0 |
| unsat_n3 | 3 | h2 | ✘ pa zgjidhje (vërtetuar) | 3 | 5 | 3 | 5 | 0.0 |
| unsat_n3 | 3 | h3 | ✘ pa zgjidhje (vërtetuar) | 3 | 5 | 3 | 5 | 0.0 |
| unsat_n3 | 3 | h4 | ✘ pa zgjidhje (vërtetuar) | 1 | 3 | 3 | 2 | 0.0 |
| unsat_kolona4_n8 | 8 | h1 | ✘ pa zgjidhje (vërtetuar) | 722 | 721 | 0 | 738 | 0.001 |
| unsat_kolona4_n8 | 8 | h2 | ✘ pa zgjidhje (vërtetuar) | 293 | 517 | 225 | 306 | 0.001 |
| unsat_kolona4_n8 | 8 | h3 | ✘ pa zgjidhje (vërtetuar) | 293 | 517 | 225 | 405 | 0.001 |
| unsat_kolona4_n8 | 8 | h4 | ✘ pa zgjidhje (vërtetuar) | 0 | 0 | 0 | 0 | 0.0 |
| rand_n8_d10_s2026 | 8 | h1 | ✔ zgjidhur | 119 | 129 | 0 | 138 | 0.0 |
| rand_n8_d10_s2026 | 8 | h2 | ✔ zgjidhur | 54 | 102 | 38 | 71 | 0.0 |
| rand_n8_d10_s2026 | 8 | h3 | ✔ zgjidhur | 143 | 404 | 36 | 372 | 0.001 |
| rand_n8_d10_s2026 | 8 | h4 | ✔ zgjidhur | 23 | 58 | 26 | 38 | 0.001 |
| rand_n8_d30_s2026 | 8 | h1 | ✔ zgjidhur | 13 | 21 | 0 | 24 | 0.0 |
| rand_n8_d30_s2026 | 8 | h2 | ✔ zgjidhur | 8 | 18 | 2 | 17 | 0.0 |
| rand_n8_d30_s2026 | 8 | h3 | ✔ zgjidhur | 38 | 97 | 19 | 80 | 0.0 |
| rand_n8_d30_s2026 | 8 | h4 | ✔ zgjidhur | 8 | 18 | 3 | 16 | 0.0 |
| rand_n12_d10_s2026 | 12 | h1 | ✔ zgjidhur | 139 | 171 | 0 | 179 | 0.0 |
| rand_n12_d10_s2026 | 12 | h2 | ✔ zgjidhur | 61 | 137 | 45 | 100 | 0.0 |
| rand_n12_d10_s2026 | 12 | h3 | ✔ zgjidhur | 6440 | 24321 | 357 | 23965 | 0.119 |
| rand_n12_d10_s2026 | 12 | h4 | ✔ zgjidhur | 22 | 80 | 27 | 57 | 0.004 |
| rand_n12_d30_s2026 | 12 | h1 | ✔ zgjidhur | 200 | 221 | 0 | 228 | 0.001 |
| rand_n12_d30_s2026 | 12 | h2 | ✔ zgjidhur | 66 | 134 | 49 | 91 | 0.001 |
| rand_n12_d30_s2026 | 12 | h3 | ✔ zgjidhur | 705 | 2825 | 24 | 2802 | 0.024 |
| rand_n12_d30_s2026 | 12 | h4 | ✔ zgjidhur | 18 | 55 | 19 | 38 | 0.001 |
| rand_n16_d10_s2026 | 16 | h1 | ✔ zgjidhur | 13404 | 13457 | 0 | 13475 | 0.038 |
| rand_n16_d10_s2026 | 16 | h2 | ✔ zgjidhur | 5728 | 9909 | 4128 | 5796 | 0.038 |
| rand_n16_d10_s2026 | 16 | h3 | limit nyjash | 100001 | 586504 | 22 | 586484 | 4.29 |
| rand_n16_d10_s2026 | 16 | h4 | ✔ zgjidhur | 1155 | 3263 | 2055 | 1219 | 0.066 |
| rand_n16_d30_s2026 | 16 | h1 | ✔ zgjidhur | 2469 | 2509 | 0 | 2525 | 0.01 |
| rand_n16_d30_s2026 | 16 | h2 | ✔ zgjidhur | 942 | 1651 | 670 | 996 | 0.007 |
| rand_n16_d30_s2026 | 16 | h3 | ✔ zgjidhur | 49121 | 237071 | 566 | 236507 | 2.346 |
| rand_n16_d30_s2026 | 16 | h4 | ✔ zgjidhur | 208 | 571 | 324 | 257 | 0.011 |
| rand_n20_d10_s2026 | 20 | h1 | ✔ zgjidhur | 6368 | 6460 | 0 | 6474 | 0.022 |
| rand_n20_d10_s2026 | 20 | h2 | ✔ zgjidhur | 2274 | 4195 | 1829 | 2378 | 0.016 |
| rand_n20_d10_s2026 | 20 | h3 | limit nyjash | 100001 | 913206 | 0 | 913208 | 9.247 |
| rand_n20_d10_s2026 | 20 | h4 | ✔ zgjidhur | 385 | 1183 | 708 | 484 | 0.05 |
| rand_n20_d30_s2026 | 20 | h1 | ✔ zgjidhur | 29703 | 29775 | 0 | 29788 | 0.152 |
| rand_n20_d30_s2026 | 20 | h2 | ✔ zgjidhur | 10626 | 18510 | 7813 | 10710 | 0.141 |
| rand_n20_d30_s2026 | 20 | h3 | limit nyjash | 100001 | 715588 | 0 | 715590 | 11.031 |
| rand_n20_d30_s2026 | 20 | h4 | ✔ zgjidhur | 2085 | 5214 | 3061 | 2167 | 0.123 |
| rand_n24_d10_s2026 | 24 | h1 | limit nyjash | 100001 | 100136 | 0 | 100157 | 0.463 |
| rand_n24_d10_s2026 | 24 | h2 | ✔ zgjidhur | 37681 | 65734 | 27918 | 37836 | 0.376 |
| rand_n24_d10_s2026 | 24 | h3 | limit nyjash | 100001 | 1196124 | 0 | 1196126 | 18.656 |
| rand_n24_d10_s2026 | 24 | h4 | ✔ zgjidhur | 5966 | 16543 | 10443 | 6118 | 0.667 |
| rand_n24_d30_s2026 | 24 | h1 | limit nyjash | 100001 | 100097 | 0 | 100126 | 0.464 |
| rand_n24_d30_s2026 | 24 | h2 | limit nyjash | 100001 | 177593 | 77489 | 100125 | 1.337 |
| rand_n24_d30_s2026 | 24 | h3 | limit nyjash | 100001 | 1053205 | 0 | 1053207 | 17.191 |
| rand_n24_d30_s2026 | 24 | h4 | ✔ zgjidhur | 19570 | 55411 | 35743 | 19686 | 3.657 |
| rand_n28_d10_s2026 | 28 | h1 | limit nyjash | 100001 | 100207 | 0 | 100224 | 0.552 |
| rand_n28_d10_s2026 | 28 | h2 | limit nyjash | 100001 | 178905 | 78709 | 100222 | 1.855 |
| rand_n28_d10_s2026 | 28 | h3 | limit nyjash | 100001 | 1608501 | 0 | 1608503 | 28.59 |
| rand_n28_d10_s2026 | 28 | h4 | ✔ zgjidhur | 68797 | 195591 | 126601 | 69012 | 6.544 |
| rand_n28_d30_s2026 | 28 | h1 | limit nyjash | 100001 | 100151 | 0 | 100178 | 0.48 |
| rand_n28_d30_s2026 | 28 | h2 | limit nyjash | 100001 | 191463 | 91312 | 100173 | 1.365 |
| rand_n28_d30_s2026 | 28 | h3 | limit nyjash | 100001 | 1295646 | 0 | 1295648 | 21.171 |
| rand_n28_d30_s2026 | 28 | h4 | ✔ zgjidhur | 41504 | 131929 | 90282 | 41668 | 5.67 |
| 156.48.1960.36.1721297189 | 48 | h1 | limit nyjash | 100001 | 100056 | 0 | 100074 | 0.688 |
| 156.48.1960.36.1721297189 | 48 | h2 | limit nyjash | 100001 | 176853 | 76806 | 100069 | 3.085 |
| 156.48.1960.36.1721297189 | 48 | h3 | limit nyjash | 100001 | 434308 | 2704 | 431606 | 10.833 |
| 156.48.1960.36.1721297189 | 48 | h4 | limit nyjash | 100001 | 277124 | 177091 | 100056 | 40.648 |

## Tie-breaking me h1 (FIFO kundrejt deep)

| instanca | N | heuristika | tie | statusi | zgjeruara | nyje_ne_memorie | koha_s |
|---|---|---|---|---|---|---|---|
| rand_n8_d20_s2026 | 8 | h1 | fifo | ✔ zgjidhur | 964 | 1237 | 0.003 |
| rand_n8_d20_s2026 | 8 | h1 | deep | ✔ zgjidhur | 13 | 28 | 0.0 |
| rand_n10_d20_s2026 | 10 | h1 | fifo | ✔ zgjidhur | 13725 | 17210 | 0.048 |
| rand_n10_d20_s2026 | 10 | h1 | deep | ✔ zgjidhur | 292 | 314 | 0.001 |
| rand_n12_d20_s2026 | 12 | h1 | fifo | limit nyjash | 100001 | 173489 | 0.522 |
| rand_n12_d20_s2026 | 12 | h1 | deep | ✔ zgjidhur | 417 | 450 | 0.001 |
