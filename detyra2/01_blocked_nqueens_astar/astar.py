"""
A* për Blocked N-Queens (implementim nga zero).

Modeli i kërkimit
-----------------
* Gjendja: vendosje e pjesshme rresht pas rreshti, cols = (c_0, ..., c_{g-1}),
  ku c_r është kolona e mbretëreshës në rreshtin r.
* Gjendja fillestare: () – asnjë mbretëreshë.
* Pasardhësit: një mbretëreshë në rreshtin e ardhshëm g, në një qelizë të lirë
  (jo të bllokuar) dhe të sigurt (pa sulm nga mbretëreshat e vendosura).
* Kosto e çdo hapi = 1, pra g(n) = numri i mbretëreshave të vendosura.
* Testi i qëllimit: g = N.

Sulmet ruhen si bitmask-a:
    colmask – kolonat e zëna                       (biti c)
    d1      – diagonalet "\\" të zëna, indeksi c - r + N - 1
    d2      – diagonalet "/"  të zëna, indeksi r + c
Kolonat e sulmuara në rreshtin r = colmask | (d1 >> (N-1-r)) | (d2 >> r).
"""

from __future__ import annotations

import heapq
import itertools
import math
import time
from dataclasses import dataclass

from board import Board

INF = math.inf


# ============================================================================ ndihmëse

class Context:
    """Të dhënat e tabelës që përdorin A* dhe heuristikat."""

    def __init__(self, board: Board):
        self.n = board.n
        self.full = (1 << board.n) - 1
        self.free_rows = board.free_rows

    def safe(self, row: int, colmask: int, d1: int, d2: int) -> int:
        """Bitmask i qelizave të lira dhe të sigurta në rreshtin `row`."""
        attacked = colmask | (d1 >> (self.n - 1 - row)) | (d2 >> row)
        return self.free_rows[row] & ~attacked & self.full


def bits(mask: int):
    """Indekset e biteve 1 në mask."""
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def has_perfect_matching(masks: list[int]) -> bool:
    """A mund t'i caktohet çdo rreshti një kolonë e ndryshme nga maska e tij?
    (matching bipartit me augmenting paths – algoritmi i Kuhn-it)."""
    match = {}                                   # kolona -> rreshti

    def augment(i, seen):
        for c in bits(masks[i] & ~seen[0]):
            seen[0] |= 1 << c
            if c not in match or augment(match[c], seen):
                match[c] = i
                return True
        return False

    for i in sorted(range(len(masks)), key=lambda i: masks[i].bit_count()):
        if not augment(i, [0]):
            return False
    return True


# ============================================================================ heuristikat
# h(ctx, g, colmask, d1, d2) -> float ; INF = gjendja nuk mund të plotësohet

def h1(ctx, g, colmask, d1, d2):
    """h1 = numri i mbretëreshave që mbeten për t'u vendosur = N - g."""
    return float(ctx.n - g)


def h2(ctx, g, colmask, d1, d2):
    """h2 = N - g, por INF nëse ndonjë rresht i mbetur nuk ka asnjë qelizë të sigurt
    (zbulim i rrugës pa dalje)."""
    for r in range(g, ctx.n):
        if ctx.safe(r, colmask, d1, d2) == 0:
            return INF
    return float(ctx.n - g)


def h3(ctx, g, colmask, d1, d2):
    """h3 = (N - g) + Σ_{rreshtat e mbetur} 1/|qelizat e sigurta|   (ide MRV).
    Penalizon gjendjet ku rreshtat e ardhshëm kanë pak opsione. NUK është admissible
    (mund të japë deri në 2(N - g))."""
    h = float(ctx.n - g)
    for r in range(g, ctx.n):
        k = ctx.safe(r, colmask, d1, d2).bit_count()
        if k == 0:
            return INF
        h += 1.0 / k
    return h


def h4(ctx, g, colmask, d1, d2):
    """h4 – heuristika e PROPOZUAR admissible.

    1) Propagim: nëse një rresht ka vetëm NJË qelizë të sigurt, çdo zgjidhje duhet ta
       përdorë; e vendosim virtualisht dhe heqim kolonën e diagonalet e saj nga rreshtat e
       tjerë. Përsëritet derisa të mos ketë më rreshta të tillë. Rresht pa qeliza -> INF.
    2) Matching: rreshtat e mbetur duhet të marrin kolona të ndryshme; nëse nuk ekziston
       matching i plotë rreshta->kolona -> INF.
    Përndryshe h4 = N - g. Prova e admissibility-t është në README."""
    n = ctx.n
    masks = {r: ctx.safe(r, colmask, d1, d2) for r in range(g, n)}
    changed = True
    while changed:
        changed = False
        for r in list(masks):
            m = masks.get(r)
            if m is None:                         # u hoq më parë në këtë kalim
                continue
            if m == 0:
                return INF
            if m & (m - 1) == 0:                  # vetëm një qelizë -> rresht i detyruar
                c = m.bit_length() - 1
                del masks[r]
                for r2 in masks:
                    d = abs(r2 - r)
                    kill = 1 << c
                    if c + d < n:
                        kill |= 1 << (c + d)
                    if c - d >= 0:
                        kill |= 1 << (c - d)
                    masks[r2] &= ~kill
                changed = True
    rest = list(masks.values())
    if any(m == 0 for m in rest) or not has_perfect_matching(rest):
        return INF
    return float(n - g)


HEURISTICS = {"h1": h1, "h2": h2, "h3": h3, "h4": h4}

DESCRIPTIONS = {
    "h1": "mbretëreshat e mbetura (N - g)",
    "h2": "h1 + rresht pa qeliza të sigurta → ∞",
    "h3": "h1 + Σ 1/|qelizat e sigurta| (MRV, jo-admissible)",
    "h4": "propagim + matching rreshta–kolona (admissible, e propozuar)",
}


# ============================================================================ A*

@dataclass
class Result:
    solution: tuple[int, ...] | None   # solution[r] = kolona e mbretëreshës në rreshtin r
    status: str                        # solved | no_solution | node_limit | time_limit
    expanded: int                      # nyje të nxjerra nga open dhe të zgjeruara
    generated: int                     # fëmijë të krijuar
    pruned: int                        # fëmijë me h = ∞ (nuk futen në open)
    max_open: int                      # madhësia maksimale e open list
    closed: int                        # madhësia e closed set
    seconds: float


def astar(board: Board, heuristic: str = "h4", tie: str = "deep",
          max_expanded: int = 100_000, time_limit: float = 10.0) -> Result:
    """A*: open list = priority queue (heapq) me f = g + h; closed set i gjendjeve të zgjeruara.

    tie = "deep": kur f është i barabartë, zgjerohet nyja me g më të madh;
    tie = "fifo": kur f është i barabartë, zgjerohet nyja më e vjetër.
    """
    h = HEURISTICS[heuristic]
    ctx = Context(board)
    n = board.n
    counter = itertools.count()
    t0 = time.perf_counter()

    def key(f, g):
        return (f, -g, next(counter)) if tie == "deep" else (f, next(counter))

    open_list = []
    if h(ctx, 0, 0, 0, 0) < INF:
        heapq.heappush(open_list, (key(h(ctx, 0, 0, 0, 0), 0), (), 0, 0, 0))
    closed = set()
    expanded = generated = pruned = 0
    max_open = len(open_list)

    def done(cols, status):
        return Result(cols, status, expanded, generated, pruned, max_open, len(closed),
                      time.perf_counter() - t0)

    while open_list:
        _, cols, colmask, d1, d2 = heapq.heappop(open_list)
        g = len(cols)
        if g == n:                               # testi i qëllimit kur nyja nxirret
            return done(cols, "solved")
        if cols in closed:
            continue
        closed.add(cols)
        expanded += 1
        if expanded > max_expanded:
            return done(None, "node_limit")
        if expanded % 256 == 0 and time.perf_counter() - t0 > time_limit:
            return done(None, "time_limit")

        for c in bits(ctx.safe(g, colmask, d1, d2)):   # qelizat e sigurta të rreshtit g
            c_colmask = colmask | (1 << c)
            c_d1 = d1 | (1 << (c - g + n - 1))
            c_d2 = d2 | (1 << (g + c))
            generated += 1
            hc = h(ctx, g + 1, c_colmask, c_d1, c_d2)
            if hc == INF:
                pruned += 1
                continue
            heapq.heappush(open_list, (key(g + 1 + hc, g + 1), cols + (c,), c_colmask, c_d1, c_d2))
        max_open = max(max_open, len(open_list))

    return done(None, "no_solution")            # e gjithë hapësira u eksplorua
