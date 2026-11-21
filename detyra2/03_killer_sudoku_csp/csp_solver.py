"""
Solver-i CSP i implementuar nga zero për Killer Sudoku.

Modeli CSP
----------
* Variablat: 81 qeliza X_0..X_80.
* Domeni: {1..9} (ruhet si bitmask: biti d = shifra d).
* Kufizimet: AllDifferent(rresht), AllDifferent(kolonë), AllDifferent(kuti 3×3),
  për çdo kafaz: AllDifferent(kafaz) ∧ Σ = S, dhe X_i = d për shifrat e dhëna.

Algoritmi
---------
Backtracking + MRV + Forward Checking + krasitje me kombinimet e kafazeve:
* Kombinimet: për çdo (k, S) llogariten paraprakisht të gjitha bashkësitë me k shifra të
  ndryshme me shumë S, p.sh. (2, 3) -> {1,2}, (3, 23) -> {6,8,9}. Domeni fillestar i qelizave të
  një kafazi = bashkimi i kombinimeve të tij.
* MRV: zgjidhet qeliza e pacaktuar me domenin më të vogël.
* Forward checking pas caktimit X_i = d:
    - d hiqet nga domenet e të gjitha qelizave "fqinje" (rresht, kolonë, kuti, kafaz);
    - për kafazin e X_i: me shifrat e përdorura U, shumën e mbetur R dhe m qeliza të mbetura,
      domenet e qelizave të mbetura kufizohen te bashkimi i kombinimeve (m, R) që nuk prekin U;
    - nëse ndonjë domen bëhet bosh -> backtrack.
"""

from __future__ import annotations

import time
from itertools import combinations

from killer import UNITS, Puzzle

ALL = 0b1111111110          # bitet 1..9


def _combos():
    """combos[k][s] = lista e bitmask-ave të bashkësive me k shifra të ndryshme dhe shumë s."""
    table = [[[] for _ in range(46)] for _ in range(10)]
    for k in range(1, 10):
        for comb in combinations(range(1, 10), k):
            m = 0
            for d in comb:
                m |= 1 << d
            table[k][sum(comb)].append(m)
    return table


COMBOS = _combos()


class KillerCSP:
    """mrv / fc / combos lejojnë të çaktivizohen teknikat një nga një (për krahasim)."""

    def __init__(self, puzzle: Puzzle, mrv: bool = True, fc: bool = True, combos: bool = True):
        self.p = puzzle
        self.mrv = mrv and fc            # MRV ka kuptim vetëm kur domenet përditësohen (FC)
        self.fc = fc
        self.combos = combos
        self.cage_of = [0] * 81
        for k, cage in enumerate(puzzle.cages):
            for c in cage.cells:
                self.cage_of[c] = k
        # Fqinjët: qelizat që ndajnë rresht, kolonë, kuti ose kafaz.
        self.peers = [set() for _ in range(81)]
        for unit in UNITS:
            for a in unit:
                self.peers[a].update(unit)
        for cage in puzzle.cages:
            for a in cage.cells:
                self.peers[a].update(cage.cells)
        for a in range(81):
            self.peers[a].discard(a)
        self.peers = [sorted(s) for s in self.peers]
        self.nodes = 0           # caktime të provuara
        self.backtracks = 0      # vlera të provuara që dështuan (konflikt ose nënpemë pa zgjidhje)

    # ------------------------------------------------------------------ krasitja e kafazit

    def _cage_allowed(self, k: int, values: list[int]) -> int | None:
        """Shifrat e lejuara për qelizat e pacaktuara të kafazit k (None = kafazi s'ka zgjidhje)."""
        cage = self.p.cages[k]
        used, rest, free = 0, cage.total, 0
        for c in cage.cells:
            if values[c]:
                used |= 1 << values[c]
                rest -= values[c]
            else:
                free += 1
        if free == 0:
            return 0 if rest == 0 else None
        if not free * (free + 1) // 2 <= rest <= sum(range(10 - free, 10)):
            return None                            # shuma e mbetur s'arrihet me `free` shifra
        if not self.combos:                        # pa kombinime: vetëm shifrat e papërdorura
            return ALL & ~used
        allowed = 0
        for m in COMBOS[free][rest]:
            if m & used == 0:
                allowed |= m
        return allowed or None

    def initial_domains(self) -> list[int] | None:
        doms = [ALL] * 81
        values = [0] * 81
        for k, cage in enumerate(self.p.cages):
            allowed = self._cage_allowed(k, values)
            if allowed is None:
                return None
            for c in cage.cells:
                doms[c] &= allowed
        return doms

    # ------------------------------------------------------------------ forward checking

    def _assign(self, doms, values, cell, d):
        """Kthen domenet e reja pas X_cell = d, ose None nëse ndonjë domen bëhet bosh."""
        if not self.fc:
            # Backtracking i thjeshtë: vetëm kontrollohet që caktimi s'bie ndesh me qelizat e caktuara.
            if any(values[q] == d for q in self.peers[cell]):
                return None
            values[cell] = d
            return doms if self._cage_allowed(self.cage_of[cell], values) is not None else None
        doms = doms[:]
        values[cell] = d
        doms[cell] = 1 << d
        bit = 1 << d
        for q in self.peers[cell]:
            if not values[q] and doms[q] & bit:
                doms[q] &= ~bit
                if not doms[q]:
                    return None
        k = self.cage_of[cell]
        allowed = self._cage_allowed(k, values)
        if allowed is None:
            return None
        for q in self.p.cages[k].cells:
            if not values[q]:
                doms[q] &= allowed
                if not doms[q]:
                    return None
        return doms

    # ------------------------------------------------------------------ backtracking

    def solve(self, time_limit: float = 60.0):
        self.nodes = self.backtracks = 0
        self.t0 = time.perf_counter()
        self.time_limit = time_limit
        doms = self.initial_domains()
        values = [0] * 81
        for cell, d in enumerate(self.p.givens):          # shifrat e dhëna caktohen me forward checking
            if d and doms is not None:
                doms = self._assign(doms, values, cell, d) if doms[cell] >> d & 1 else None
        return self._search(doms, values) if doms is not None else None

    def _search(self, doms, values):
        best, best_size = -1, 10
        if self.mrv:                               # MRV: qeliza e pacaktuar me më pak vlera
            for i in range(81):
                if not values[i]:
                    size = doms[i].bit_count()
                    if size < best_size:
                        best, best_size = i, size
                        if size == 1:
                            break
        else:                                      # rend statik: qeliza e parë e pacaktuar
            best = next((i for i in range(81) if not values[i]), -1)
        if best < 0:
            return values[:]                       # të gjitha qelizat janë caktuar
        if time.perf_counter() - self.t0 > self.time_limit:
            raise TimeoutError
        m = doms[best]
        while m:
            low = m & -m
            d = low.bit_length() - 1
            m ^= low
            self.nodes += 1
            new = self._assign(doms, values, best, d)
            if new is not None:
                res = self._search(new, values)
                if res is not None:
                    return res
            self.backtracks += 1
            values[best] = 0
        return None


def solve_csp(puzzle: Puzzle, time_limit: float = 60.0, mrv=True, fc=True, combos=True) -> dict:
    csp = KillerCSP(puzzle, mrv, fc, combos)
    t0 = time.perf_counter()
    try:
        grid = csp.solve(time_limit)
        status = "solved" if grid else "no_solution"
    except TimeoutError:
        grid, status = None, "timeout"
    return {"grid": grid, "status": status, "seconds": time.perf_counter() - t0,
            "nodes": csp.nodes, "backtracks": csp.backtracks}
