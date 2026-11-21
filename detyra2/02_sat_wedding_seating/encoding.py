"""
Kodimi SAT (CNF) i problemit të uljes së mysafirëve.

Variablat kryesore:  x(i, t) = "mysafiri i ulet në tavolinën t"   (i = 0..n-1, t = 0..T-1)

Grupet e klauzolave (shih README për formulën formale):
  (d)  ALO  – çdo mysafir ulet të paktën në një tavolinë
       AMO  – çdo mysafir ulet në të shumtën një tavolinë (pairwise)
       CAP  – çdo tavolinë ka saktësisht C mysafirë (kodim kardinaliteti)
  (a)  CONFLICT – çiftet që nuk ulen bashkë
  (b)  TOGETHER – çiftet që ulen bashkë
  (c)  GENDER   – në çdo tavolinë numri i burrave është në [L, U]
  SYM – thyerja e simetrisë së tavolinave (default aktive, --no-symmetry e çaktivizon)
"""

from __future__ import annotations

import math
from collections import OrderedDict

from instance import Instance


class Formula:
    """CNF me numërim të variablave dhe statistika për çdo grup klauzolash."""

    def __init__(self):
        self.nv = 0
        self.clauses: list[list[int]] = []
        self.groups: "OrderedDict[str, dict]" = OrderedDict()
        self._current = None

    def new_var(self) -> int:
        self.nv += 1
        if self._current is not None:
            self.groups[self._current]["aux"] += 1
        return self.nv

    def group(self, name: str):
        self.groups.setdefault(name, {"clauses": 0, "aux": 0, "literals": 0})
        self._current = name

    def add(self, clause: list[int]):
        self.clauses.append(clause)
        g = self.groups[self._current]
        g["clauses"] += 1
        g["literals"] += len(clause)


# ============================================================================ kardinaliteti

def at_most_seqcounter(f: Formula, lits: list[int], k: int) -> None:
    """Sequential counter (Sinz, 2005):  Σ lits <= k.

    Variabla ndihmëse s[i][j] (i = 0..n-2, j = 0..k-1) do të thotë
    "ndër lits[0..i] të paktën j+1 janë të vërteta". Klauzolat:
        ¬x_0 ∨ s[0][0]                       ;  ¬s[0][j]                 (j >= 1)
        për 0 < i < n-1:
            ¬x_i ∨ s[i][0]                   ;  ¬s[i-1][0] ∨ s[i][0]
            ¬x_i ∨ ¬s[i-1][j-1] ∨ s[i][j]    ;  ¬s[i-1][j] ∨ s[i][j]     (j >= 1)
            ¬x_i ∨ ¬s[i-1][k-1]              (mbingarkesa: x_i do të ishte i (k+1)-ti)
        ¬x_{n-1} ∨ ¬s[n-2][k-1]
    Madhësia: (n-1)·k variabla ndihmëse dhe 2nk + n - 3k - 1 klauzola.
    """
    n = len(lits)
    if k >= n:
        return
    if k == 0:
        for x in lits:
            f.add([-x])
        return
    s = [[f.new_var() for _ in range(k)] for _ in range(n - 1)]
    f.add([-lits[0], s[0][0]])
    for j in range(1, k):
        f.add([-s[0][j]])
    for i in range(1, n - 1):
        f.add([-lits[i], s[i][0]])
        f.add([-s[i - 1][0], s[i][0]])
        for j in range(1, k):
            f.add([-lits[i], -s[i - 1][j - 1], s[i][j]])
            f.add([-s[i - 1][j], s[i][j]])
        f.add([-lits[i], -s[i - 1][k - 1]])
    f.add([-lits[n - 1], -s[n - 2][k - 1]])


def at_least_seqcounter(f: Formula, lits: list[int], k: int) -> None:
    """Σ lits >= k  ⇔  Σ ¬lits <= n - k."""
    at_most_seqcounter(f, [-x for x in lits], len(lits) - k)


# ============================================================================ modeli

def gender_bounds(capacity: int, max_diff: int) -> tuple[int, int]:
    """Me C vende dhe |M - F| <= D, ku F = C - M:  |2M - C| <= D  ⇒  M ∈ [⌈(C-D)/2⌉, ⌊(C+D)/2⌋].
    Për C = 10, D = 3:  M ∈ [4, 6]  (M = 7 do të jepte 7 - 3 = 4 > 3)."""
    return math.ceil((capacity - max_diff) / 2), (capacity + max_diff) // 2


class SeatingEncoding:
    def __init__(self, inst: Instance, symmetry: bool = True):
        self.inst = inst
        self.symmetry = symmetry
        self.f = Formula()
        n, T = inst.n, inst.tables
        # Variablat x(i,t) janë 1..n·T:  x(i,t) = i·T + t + 1
        self.f.group("x (variablat kryesore)")
        for _ in range(n * T):
            self.f.new_var()
        self.f.groups["x (variablat kryesore)"]["aux"] = 0
        self.f.groups["x (variablat kryesore)"]["primary"] = n * T
        self._build()

    def x(self, i: int, t: int) -> int:
        return i * self.inst.tables + t + 1

    def decode_var(self, v: int) -> tuple[int, int]:
        return divmod(v - 1, self.inst.tables)

    def _build(self):
        inst, f = self.inst, self.f
        n, T, C = inst.n, inst.tables, inst.capacity
        if n != T * C:
            raise ValueError(f"{n} mysafirë nuk mbushin saktësisht {T} tavolina me {C} vende")
        idx = inst.index()

        # (d) çdo mysafir saktësisht në një tavolinë
        f.group("(d) ALO: çdo mysafir të paktën 1 tavolinë")
        for i in range(n):
            f.add([self.x(i, t) for t in range(T)])
        f.group("(d) AMO: çdo mysafir të shumtën 1 tavolinë")
        for i in range(n):
            for t1 in range(T):
                for t2 in range(t1 + 1, T):
                    f.add([-self.x(i, t1), -self.x(i, t2)])

        # (d) çdo tavolinë saktësisht C mysafirë. Mjafton "≤ C": çdo mysafir ulet në saktësisht
        #     një tavolinë, pra shuma e të gjitha tavolinave është n = T·C; nëse asnjë s'ka > C,
        #     atëherë secila ka saktësisht C (prova në README).
        f.group(f"(d) CAP: Σ_i x(i,t) ≤ {C}")
        for t in range(T):
            at_most_seqcounter(f, [self.x(i, t) for i in range(n)], C)

        # (a) konfliktet
        f.group("(a) CONFLICT: ¬x(a,t) ∨ ¬x(b,t)")
        for a, b in inst.conflicts:
            for t in range(T):
                f.add([-self.x(idx[a], t), -self.x(idx[b], t)])

        # (b) bashkë
        f.group("(b) TOGETHER: x(a,t) ↔ x(b,t)")
        for a, b in inst.together:
            for t in range(T):
                f.add([-self.x(idx[a], t), self.x(idx[b], t)])
                f.add([self.x(idx[a], t), -self.x(idx[b], t)])

        # (c) gjinia: L <= burrat(t) <= U. Meqë tavolina ka saktësisht C veta,
        #     burrat >= L  ⇔  gratë <= C - L. Përdorim dy kufij "at most".
        lo, hi = gender_bounds(C, inst.max_diff)
        men = [idx[g] for g in inst.guests if inst.gender[g] == "M"]
        women = [idx[g] for g in inst.guests if inst.gender[g] == "F"]
        f.group(f"(c) GENDER: burra(t) ≤ {hi}")
        for t in range(T):
            at_most_seqcounter(f, [self.x(i, t) for i in men], hi)
        f.group(f"(c) GENDER: gra(t) ≤ {C - lo}  (⇔ burra(t) ≥ {lo})")
        for t in range(T):
            at_most_seqcounter(f, [self.x(i, t) for i in women], C - lo)

        # Thyerja e simetrisë: tavolinat renditen sipas mysafirit me indeksin më të vogël.
        #   x(i,t) → ∨_{j<i} x(j,t-1)   për t >= 1
        if self.symmetry:
            f.group("SYM: x(i,t) → ∨_{j<i} x(j,t−1)")
            for t in range(1, T):
                for i in range(n):
                    f.add([-self.x(i, t)] + [self.x(j, t - 1) for j in range(i)])

    # ------------------------------------------------------------------ dalja

    def stats(self) -> dict:
        total_cl = len(self.f.clauses)
        return {"variables": self.f.nv, "primary": self.inst.n * self.inst.tables,
                "aux": self.f.nv - self.inst.n * self.inst.tables, "clauses": total_cl,
                "literals": sum(len(c) for c in self.f.clauses), "groups": self.f.groups}

    def to_dimacs(self, path: str) -> None:
        inst = self.inst
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f"c Seating SAT: {inst.n} guests, {inst.tables} tables x {inst.capacity} seats\n")
            fh.write(f"c instance={inst.name} symmetry={self.symmetry}\n")
            fh.write(f"c x(i,t) = i*{inst.tables} + t + 1  (i = guest index 0.., t = table 0..)\n")
            for name, g in self.f.groups.items():
                safe = name
                for a, b in (("Σ", "sum"), ("≤", "<="), ("≥", ">="), ("¬", "-"), ("∨", " v "), ("↔", "<->"),
                             ("→", "->"), ("⇔", "<=>"), ("−", "-"), ("ç", "c"), ("ë", "e")):
                    safe = safe.replace(a, b)
                safe = safe.encode("ascii", "replace").decode()
                fh.write(f"c group {safe}: clauses={g['clauses']} aux={g['aux']}\n")
            fh.write(f"p cnf {self.f.nv} {len(self.f.clauses)}\n")
            for cl in self.f.clauses:
                fh.write(" ".join(map(str, cl)) + " 0\n")

    def decode(self, model) -> list[list[str]]:
        """Modeli -> lista e mysafirëve për çdo tavolinë."""
        tables = [[] for _ in range(self.inst.tables)]
        limit = self.inst.n * self.inst.tables
        for v in model:
            if 0 < v <= limit:
                i, t = self.decode_var(v)
                tables[t].append(self.inst.guests[i])
        return tables


def verify_plan(inst: Instance, tables: list[list[str]]) -> list[str]:
    """Kontroll i pavarur i të gjitha kushteve (a)–(d). Kthen listën e shkeljeve."""
    errors = []
    seat = {}
    for t, members in enumerate(tables):
        for g in members:
            if g in seat:
                errors.append(f"(d) {g} është në tavolinat {seat[g] + 1} dhe {t + 1}")
            seat[g] = t
    for g in inst.guests:
        if g not in seat:
            errors.append(f"(d) {g} nuk ka vend")
    if len(tables) != inst.tables:
        errors.append(f"(d) {len(tables)} tavolina në vend të {inst.tables}")
    for t, members in enumerate(tables):
        if len(members) != inst.capacity:
            errors.append(f"(d) tavolina {t + 1} ka {len(members)} mysafirë")
        m = sum(inst.gender[g] == "M" for g in members)
        if abs(m - (len(members) - m)) > inst.max_diff:
            errors.append(f"(c) tavolina {t + 1}: {m} burra, {len(members) - m} gra")
    for a, b in inst.conflicts:
        if a in seat and seat.get(a) == seat.get(b):
            errors.append(f"(a) {a} dhe {b} janë në tavolinën {seat[a] + 1}")
    for a, b in inst.together:
        if seat.get(a) != seat.get(b):
            errors.append(f"(b) {a} dhe {b} janë në tavolina të ndryshme")
    return errors
