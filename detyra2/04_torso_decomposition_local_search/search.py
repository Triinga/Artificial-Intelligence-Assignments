"""
Zgjidhjet fillestare (konstruktive) dhe metaheuristikat për Torso Decompositions.

* Evaluator – mban permutacionin dhe fqinjësinë në "hapësirën e pozicioneve" si bitset-e, që lëvizjet
  swap/insert të përditësohen në mënyrë inkrementale (pa e rindërtuar nga lista e brinjëve).
* Konstruktive: min-degree dhe min-fill (renditje eliminimi klasike për treewidth).
* Metaheuristikat: Simulated Annealing (SA) dhe Iterated Local Search (ILS).
  Funksioni objektiv (maksimizohet) = hypervolume i frontit të plotë që jep permutacioni,
  HV(π) = Σ_t (501 − w_π(t)), ku w_π(t) = gjerësia e torsos me prag t.
"""

from __future__ import annotations

import math
import random
import time

from torso import WIDTH_CAP, Graph, front_from_widths, suffix_widths


# ============================================================================ vlerësues inkremental

class Evaluator:
    def __init__(self, g: Graph, perm: list[int]):
        self.g = g
        n = self.n = g.n
        self.perm = list(perm)
        self.pos = [0] * n
        for i, v in enumerate(self.perm):
            self.pos[v] = i
        # P[i] = bitset i pozicioneve të fqinjëve të nyjes në pozicionin i
        self.P = [0] * n
        for i, v in enumerate(self.perm):
            m = 0
            for u in g.nbrs[v]:
                m |= 1 << self.pos[u]
            self.P[i] = m
        full = (1 << n) - 1
        self.later = [full ^ ((1 << (i + 1)) - 1) for i in range(n)]   # bitet j > i
        self.evals = 0

    def widths(self) -> list[int]:
        """Gjerësia e torsos për çdo prag t (loja e eliminimit, O(n) operacione bitset)."""
        self.evals += 1
        n, P, later = self.n, self.P, self.later
        out = [P[i] & later[i] for i in range(n)]
        deg = [0] * n
        for i in range(n):
            m = out[i]
            if m:
                low = m & -m
                out[low.bit_length() - 1] |= m ^ low
                deg[i] = m.bit_count()
        self.deg = deg
        return suffix_widths(deg)

    # ---------------------------------------------------------------- lëvizjet
    def swap(self, a: int, b: int) -> None:
        """Ndërron nyjet në pozicionet a dhe b."""
        if a == b:
            return
        na, nb = self.perm[a], self.perm[b]
        P, pos, mask = self.P, self.pos, (1 << a) | (1 << b)
        for u in set(self.g.nbrs[na]) | set(self.g.nbrs[nb]):
            k = pos[u]
            r = P[k]
            if ((r >> a) ^ (r >> b)) & 1:          # vetëm njëri nga bitet është 1
                P[k] = r ^ mask
        P[a], P[b] = P[b], P[a]
        self.perm[a], self.perm[b] = nb, na
        pos[na], pos[nb] = b, a

    def insert(self, i: int, j: int) -> None:
        """Heq nyjen nga pozicioni i dhe e vendos në pozicionin j (të tjerat zhvendosen)."""
        if i == j:
            return
        lo, hi = min(i, j), max(i, j)
        seg = ((1 << (hi - lo + 1)) - 1) << lo
        P = self.P
        if i < j:      # biti i -> j, bitet i+1..j -> një poshtë
            for k in range(self.n):
                r = P[k]
                s = r & seg
                if s:
                    P[k] = (r ^ s) | ((s >> 1) & seg) | (((s >> i) & 1) << j)
        else:          # biti i -> j (j < i), bitet j..i-1 -> një lart
            for k in range(self.n):
                r = P[k]
                s = r & seg
                if s:
                    P[k] = (r ^ s) | ((s << 1) & seg) | (((s >> i) & 1) << j)
        P.insert(j, P.pop(i))
        self.perm.insert(j, self.perm.pop(i))
        for k in range(lo, hi + 1):
            self.pos[self.perm[k]] = k


def hv_of(w: list[int]) -> int:
    return sum(WIDTH_CAP - x for x in w)


# ============================================================================ konstruktive

def min_degree_order(g: Graph, rng: random.Random | None = None) -> list[int]:
    """Eliminon gjithmonë nyjen me shkallën më të vogël në grafin aktual (me brinjët e shtuara)."""
    adj = list(g.adj)
    alive = (1 << g.n) - 1
    deg = [a.bit_count() for a in adj]
    order = []
    remaining = set(range(g.n))
    for _ in range(g.n):
        dmin = min(deg[v] for v in remaining)
        cands = [v for v in remaining if deg[v] == dmin]
        v = rng.choice(cands) if rng else cands[0]
        order.append(v)
        remaining.discard(v)
        alive &= ~(1 << v)
        nb = adj[v] & alive
        m = nb
        while m:                                  # fqinjët bëhen klikë
            low = m & -m
            u = low.bit_length() - 1
            m ^= low
            adj[u] = (adj[u] | nb) & ~low & alive
            deg[u] = adj[u].bit_count()
    return order


def min_fill_order(g: Graph, rng: random.Random | None = None) -> list[int]:
    """Eliminon nyjen që shton më pak brinjë të reja (fill-in). Më e shtrenjtë se min-degree."""
    adj = list(g.adj)
    alive = (1 << g.n) - 1
    remaining = set(range(g.n))

    def fill(v):
        nb = adj[v] & alive
        missing, m = 0, nb
        while m:
            low = m & -m
            u = low.bit_length() - 1
            m ^= low
            missing += (nb & ~adj[u] & ~low).bit_count()
        return missing // 2

    score = {v: fill(v) for v in remaining}
    order = []
    for _ in range(g.n):
        best = min(score[v] for v in remaining)
        cands = [v for v in remaining if score[v] == best]
        v = rng.choice(cands) if rng else min(cands, key=lambda c: adj[c].bit_count())
        order.append(v)
        remaining.discard(v)
        alive &= ~(1 << v)
        nb = adj[v] & alive
        m = nb
        while m:
            low = m & -m
            u = low.bit_length() - 1
            m ^= low
            adj[u] = (adj[u] | nb) & ~low & alive
        # fill ndryshon vetëm për nyjet në distancë ≤ 2 nga v
        touched, m = nb, nb
        while m:
            low = m & -m
            m ^= low
            touched |= adj[low.bit_length() - 1] & alive
        m = touched
        while m:
            low = m & -m
            m ^= low
            score[low.bit_length() - 1] = fill(low.bit_length() - 1)
        score.pop(v, None)
    return order


# ============================================================================ metaheuristikat

def random_move(ev: Evaluator, rng: random.Random, w=None, window: int = 30):
    """Gjeneron një lëvizje dhe lëvizjen e kundërt (për undo).

    * 50%: lëvizje lokale – j zgjidhet në dritaren |i − j| ≤ window (ndryshim i vogël i renditjes);
    * 30%: lëvizje mbi një nyje kritike (deg[i] = w[i], d.m.th. nyja që përcakton gjerësinë e torsos
      për një prag) – zhvendoset brenda dritares;
    * 20%: swap/insert mes dy pozicioneve krejt të rastit (diversifikim).
    """
    n = ev.n
    r = rng.random()
    if r < 0.8:
        if r >= 0.5 and w is not None and getattr(ev, "deg", None) is not None:
            crit = [i for i in range(n - 1) if ev.deg[i] == w[i] and ev.deg[i] > 0]
            a = rng.choice(crit) if crit else rng.randrange(n)
        else:
            a = rng.randrange(n)
        b = min(n - 1, max(0, a + rng.randint(-window, window)))
        if b == a:
            b = a + 1 if a + 1 < n else a - 1
    else:
        a, b = rng.randrange(n), rng.randrange(n)
        while b == a:
            b = rng.randrange(n)
    if rng.random() < 0.5:
        return ("swap", a, b), ("swap", a, b)
    return ("insert", a, b), ("insert", b, a)


def apply(ev: Evaluator, move):
    if move[0] == "swap":
        ev.swap(move[1], move[2])
    else:
        ev.insert(move[1], move[2])


class Archive:
    """Ruaj pikat jo-dominuese (t, gjerësia) dhe permutacionin që i jep secilën."""

    def __init__(self):
        self.best = {}                                 # gjerësia -> (t, perm)

    def add(self, w, perm) -> None:
        for t, wt in front_from_widths(w):
            if wt not in self.best or t < self.best[wt][0]:
                self.best[wt] = (t, list(perm))

    def points(self):
        return [(t, wt) for wt, (t, _) in self.best.items()]


def calibrate_t0(ev, rng, samples=100):
    """T0 = mesatarja e |Δ| për lëvizje të rastit që e përkeqësojnë zgjidhjen: në fillim një
    përkeqësim "tipik" pranohet me probabilitet e^-1 ≈ 0.37."""
    w = ev.widths()
    base, deltas = hv_of(w), []
    for _ in range(samples):
        move, undo = random_move(ev, rng, w)
        apply(ev, move)
        d = hv_of(ev.widths()) - base
        apply(ev, undo)
        if d < 0:
            deltas.append(-d)
    ev.widths()
    return sum(deltas) / len(deltas) if deltas else 1.0


def simulated_annealing(g, start, seconds, seed, log_every=1.0):
    """SA: pranon përkeqësime me probabilitet exp(Δ/T); T zvogëlohet gjeometrikisht me kohën
    nga T0 (i kalibruar) deri në 0.01."""
    rng = random.Random(seed)
    ev = Evaluator(g, start)
    w = ev.widths()
    cur, cur_w, cur_deg = hv_of(w), w, ev.deg
    best, best_perm = cur, list(ev.perm)
    archive = Archive()
    archive.add(w, ev.perm)
    T0 = max(1.0, calibrate_t0(ev, rng))
    cur_deg = ev.deg
    T_end = 0.01
    start_t = time.perf_counter()
    history = [(0.0, ev.evals, best)]
    next_log = log_every
    while True:
        el = time.perf_counter() - start_t
        if el >= seconds:
            break
        T = T0 * (T_end / T0) ** (el / seconds)
        move, undo = random_move(ev, rng, cur_w)
        apply(ev, move)
        w = ev.widths()
        val = hv_of(w)
        d = val - cur
        if d >= 0 or rng.random() < math.exp(d / T):
            cur, cur_w, cur_deg = val, w, ev.deg
            archive.add(w, ev.perm)
            if cur > best:
                best, best_perm = cur, list(ev.perm)
        else:
            apply(ev, undo)
            ev.deg = cur_deg
        if el >= next_log:
            history.append((el, ev.evals, best))
            next_log += log_every
    history.append((time.perf_counter() - start_t, ev.evals, best))
    return {"best_hv": best, "best_perm": best_perm, "archive": archive, "history": history, "evals": ev.evals}


def iterated_local_search(g, start, seconds, seed, ls_tries=200, kick=8, log_every=1.0):
    """ILS: hill climbing (first improvement me lëvizje të rastit) deri në `ls_tries` dështime
    radhazi, pastaj perturbim me `kick` lëvizje të rastit; pranohet nëse s'është më keq se më i miri."""
    rng = random.Random(seed)
    ev = Evaluator(g, start)
    w = ev.widths()
    cur, cur_w, cur_deg = hv_of(w), w, ev.deg
    best, best_perm = cur, list(ev.perm)
    archive = Archive()
    archive.add(w, ev.perm)
    start_t = time.perf_counter()
    history = [(0.0, ev.evals, best)]
    next_log = log_every
    while time.perf_counter() - start_t < seconds:
        # --- kërkim lokal
        fails = 0
        while fails < ls_tries and time.perf_counter() - start_t < seconds:
            move, undo = random_move(ev, rng, cur_w)
            apply(ev, move)
            w = ev.widths()
            val = hv_of(w)
            if val > cur:
                cur, cur_w, cur_deg, fails = val, w, ev.deg, 0
                archive.add(w, ev.perm)
            elif val == cur:                           # lëvizje anësore (plateau), lejohet
                cur_w, cur_deg = w, ev.deg
                fails += 1
                archive.add(w, ev.perm)
            else:
                apply(ev, undo)
                ev.deg = cur_deg
                fails += 1
            el = time.perf_counter() - start_t
            if el >= next_log:
                history.append((el, ev.evals, max(best, cur)))
                next_log += log_every
        # --- pranimi
        if cur >= best:
            best, best_perm = cur, list(ev.perm)
        else:                                          # kthehu te zgjidhja më e mirë
            ev = _restart(ev, g, best_perm)
            cur = best
        # --- perturbimi
        for _ in range(kick):
            apply(ev, random_move(ev, rng)[0])
        w = ev.widths()
        cur, cur_w, cur_deg = hv_of(w), w, ev.deg
        archive.add(w, ev.perm)
    history.append((time.perf_counter() - start_t, ev.evals, best))
    return {"best_hv": best, "best_perm": best_perm, "archive": archive, "history": history, "evals": ev.evals}


def _restart(ev, g, perm):
    evals = ev.evals
    new = Evaluator(g, perm)
    new.evals = evals
    return new
