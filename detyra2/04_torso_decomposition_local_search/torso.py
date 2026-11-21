"""
ESA SpOC-3, Challenge 1 – Torso Decompositions: grafi, vlerësimi, fronti Pareto dhe hypervolume.

Përkufizimet (README zyrtar, https://github.com/esa/SpOC3):
* Vektori i vendimit x = [p_1, ..., p_n, t]: permutacion i nyjeve 0..n-1 dhe pragu t ∈ {0..n-1}.
* Brinja {u, v} orientohet (u, v) nëse u del para v në permutacion.
* Skanohet permutacioni nga e majta në të djathtë; kur nyja u ka dy brinjë dalëse drejt v dhe w që
  nuk janë fqinjë, shtohet brinja {v, w} (e orientuar sipas permutacionit).
* Torso = n - t elementet e fundit; madhësia = n - t; gjerësia = outdegree maksimal (me brinjët e reja)
  i një nyjeje në torso.
* Objektivat: madhësia max (t min) dhe gjerësia min. Gjerësia > 500 vlerësohet si 501. Deri 20 vektorë
  për dorëzim, cilësia matet me hypervolume.

Vlerësimi efikas
----------------
Punojmë në "hapësirën e pozicioneve": out[i] = bitset i pozicioneve j > i që janë fqinjë me nyjen në
pozicionin i. Procedura zyrtare e shtimit të brinjëve është "loja e eliminimit": kur përpunohet
pozicioni i, fqinjët e tij të mëvonshëm bëhen klikë. Mjafton t'ia kalojmë bashkësinë out[i] fqinjit më
të hershëm v (out[v] |= out[i] \\ {v}); kur të përpunohet v, klika përhapet më tej. Kjo jep të njëjtin
graf të mbushur (Rose, Tarjan & Lueker, 1976) dhe outdegree[i] = |out[i]|. Kosto: O(n) operacione mbi
bitset-e, pra disa milisekonda edhe për grafin hard.
"""

from __future__ import annotations

import os

WIDTH_CAP = 501          # gjerësia > 500 vlerësohet si 501 (rregullat zyrtare)
MAX_POINTS = 20          # maksimumi i vektorëve në një dorëzim

PROBLEM_IDS = {"easy": "small-graph", "medium": "medium-graph", "hard": "large-graph"}
CHALLENGE_ID = "spoc-3-torso-decompositions"


class Graph:
    def __init__(self, n: int, edges: list[tuple[int, int]], name: str = "graph"):
        self.n = n
        self.name = name
        self.edges = edges
        self.adj = [0] * n                    # bitset i fqinjëve (në hapësirën e nyjeve)
        self.nbrs = [[] for _ in range(n)]
        for u, v in edges:
            if not (self.adj[u] >> v) & 1:
                self.adj[u] |= 1 << v
                self.adj[v] |= 1 << u
                self.nbrs[u].append(v)
                self.nbrs[v].append(u)
        self.m = sum(len(a) for a in self.nbrs) // 2


def load_graph(path: str) -> Graph:
    edges, n = [], 0
    with open(path) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) >= 2:
                u, v = int(parts[0]), int(parts[1])
                if u != v:
                    edges.append((u, v))
                    n = max(n, u + 1, v + 1)
    return Graph(n, edges, os.path.splitext(os.path.basename(path))[0])


# ============================================================================ vlerësimi

def outdegrees(g: Graph, perm: list[int]) -> list[int]:
    """outdeg[i] = outdegree (me brinjët e shtuara) i nyjes në pozicionin i të permutacionit."""
    n = g.n
    pos = [0] * n
    for i, v in enumerate(perm):
        pos[v] = i
    out = [0] * n
    for i, v in enumerate(perm):
        m = 0
        for u in g.nbrs[v]:
            j = pos[u]
            if j > i:
                m |= 1 << j
        out[i] = m
    deg = [0] * n
    for i in range(n):
        m = out[i]
        if m:
            low = m & -m                       # fqinji i mëvonshëm më i hershëm
            v = low.bit_length() - 1
            out[v] |= m ^ low
            deg[i] = m.bit_count()
    return deg


def suffix_widths(deg: list[int]) -> list[int]:
    """w[t] = gjerësia e torsos kur pragu është t = max(deg[t:]), e kufizuar në 501."""
    n = len(deg)
    w = [0] * n
    best = 0
    for i in range(n - 1, -1, -1):
        if deg[i] > best:
            best = deg[i]
        w[i] = min(best, WIDTH_CAP)
    return w


def evaluate(g: Graph, x: list[int]) -> tuple[int, int]:
    """Vlerësimi i një vektori x = [p_1..p_n, t] → (madhësia e torsos, gjerësia e torsos)."""
    perm, t = list(x[:-1]), int(x[-1])
    assert sorted(perm) == list(range(g.n)), "pjesa e parë e x duhet të jetë permutacion i 0..n-1"
    assert 0 <= t <= g.n - 1, "t duhet të jetë në {0..n-1}"
    return g.n - t, suffix_widths(outdegrees(g, perm))[t]


# ============================================================================ fronti dhe hypervolume
# Në hapësirën e minimizimit përdorim (t, gjerësia); pika e referencës = (n, 501).

def front_from_widths(w: list[int]) -> list[tuple[int, int]]:
    """Pikat jo-dominuese (t, gjerësia) që jep një permutacion: për çdo gjerësi, t më i vogël."""
    pts, last = [], None
    for t, wt in enumerate(w):
        if wt != last and wt < WIDTH_CAP:
            pts.append((t, wt))
            last = wt
    return pts


def staircase_hv(w: list[int]) -> int:
    """Hypervolume i frontit të plotë të një permutacioni = Σ_t (501 - w[t]).
    Përdoret si funksion objektiv nga metaheuristikat (maksimizohet)."""
    return sum(WIDTH_CAP - x for x in w)


def hypervolume(points: list[tuple[int, int]], n: int) -> int:
    """Hypervolume 2D (minimizim i t dhe gjerësisë) me pikë reference (n, 501)."""
    pts = pareto_filter(points)
    hv = 0
    for k, (t, wt) in enumerate(pts):
        t_next = pts[k + 1][0] if k + 1 < len(pts) else n
        hv += (t_next - t) * (WIDTH_CAP - wt)
    return hv


def pareto_filter(points):
    """Pikat jo-dominuese, të renditura sipas t rritës (gjerësia zbret)."""
    best = {}
    for t, wt in points:
        if wt < WIDTH_CAP and (wt not in best or t < best[wt]):
            best[wt] = t
    pts = sorted((t, wt) for wt, t in best.items())
    out, min_w = [], None
    for t, wt in pts:
        if min_w is None or wt < min_w:
            out.append((t, wt))
            min_w = wt
    return out


def select_best_subset(points, n: int, k: int = MAX_POINTS):
    """Zgjedh ≤ k pika që maksimizojnë hypervolume-in (programim dinamik, optimal në 2D)."""
    pts = pareto_filter(points)
    m = len(pts)
    if m <= k:
        return pts
    # best[c][i] = HV maksimal duke filluar me pikën i dhe duke përdorur c pika nga i..m-1
    NEG = -1
    best = [[NEG] * m for _ in range(k + 1)]
    choice = [[-1] * m for _ in range(k + 1)]
    for i in range(m):
        best[1][i] = (n - pts[i][0]) * (WIDTH_CAP - pts[i][1])
    for c in range(2, k + 1):
        for i in range(m - c, -1, -1):
            ti, hi = pts[i][0], WIDTH_CAP - pts[i][1]
            b, bj = NEG, -1
            for j in range(i + 1, m - c + 2):
                if best[c - 1][j] < 0:
                    continue
                val = (pts[j][0] - ti) * hi + best[c - 1][j]
                if val > b:
                    b, bj = val, j
            best[c][i], choice[c][i] = b, bj
    i = max(range(m), key=lambda i: best[k][i])
    out, c = [], k
    while i >= 0 and c >= 1:
        out.append(pts[i])
        i, c = choice[c][i], c - 1
    return out
