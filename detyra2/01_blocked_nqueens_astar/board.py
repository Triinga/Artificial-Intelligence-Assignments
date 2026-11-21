"""
Blocked N-Queens: reprezentimi i tabelës, leximi/shkrimi i instancave dhe gjeneratori.

Formati zyrtar (ASP Competition 2009, KU Leuven):
    num(1). num(2). ... num(N).      -> madhësia e tabelës
    block(i,j).                      -> qeliza në rreshtin i, kolonën j është e bllokuar
Indekset në skedar janë 1..N; brenda programit përdorim 0..N-1.

Dalja zyrtare është predikati queen(i,j) për çdo mbretëreshë.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field

_NUM_RE = re.compile(r"num\(\s*(\d+)\s*\)")
_BLOCK_RE = re.compile(r"block\(\s*(\d+)\s*,\s*(\d+)\s*\)")


@dataclass
class Board:
    """Tabela N x N me qeliza të bllokuara."""

    n: int
    blocked: set[tuple[int, int]] = field(default_factory=set)  # (rresht, kolonë), 0-indexed
    name: str = "board"

    def __post_init__(self) -> None:
        full = (1 << self.n) - 1
        # free_rows[r] = bitmask i kolonave të lira në rreshtin r (biti c = kolona c).
        self.free_rows: list[int] = [full] * self.n
        for r, c in self.blocked:
            self.free_rows[r] &= ~(1 << c)

    @property
    def density(self) -> float:
        return len(self.blocked) / (self.n * self.n) if self.n else 0.0

    def is_free(self, r: int, c: int) -> bool:
        return (r, c) not in self.blocked


# ----------------------------------------------------------------------------- I/O

def parse_instance(text: str, name: str = "board") -> Board:
    """Lexon një instancë në formatin ASP (num/block). Komentet '%' injorohen."""
    text = "\n".join(line.split("%", 1)[0] for line in text.splitlines())
    nums = {int(m) for m in _NUM_RE.findall(text)}
    if not nums:
        raise ValueError("Instanca nuk përmban asnjë fakt num(i).")
    n = max(nums)
    blocked = set()
    for i, j in _BLOCK_RE.findall(text):
        r, c = int(i) - 1, int(j) - 1
        if not (0 <= r < n and 0 <= c < n):
            raise ValueError(f"block({i},{j}) është jashtë tabelës {n}x{n}.")
        blocked.add((r, c))
    return Board(n, blocked, name)


def load_instance(path: str) -> Board:
    import os

    with open(path, encoding="utf-8") as fh:
        return parse_instance(fh.read(), os.path.splitext(os.path.basename(path))[0])


def to_asp(board: Board) -> str:
    """Shkruan tabelën në formatin zyrtar ASP."""
    lines = [" ".join(f"num({i})." for i in range(1, board.n + 1))]
    lines += [f"block({r + 1},{c + 1})." for r, c in sorted(board.blocked)]
    return "\n".join(lines) + "\n"


def random_board(n: int, density: float, seed: int) -> Board:
    """Gjeneron tabelë të rastësishme: secila qelizë bllokohet me probabilitet `density`.
    Seed-i fiks e bën eksperimentin të riprodhueshëm."""
    rng = random.Random(seed)
    blocked = {(r, c) for r in range(n) for c in range(n) if rng.random() < density}
    return Board(n, blocked, f"rand_n{n}_d{int(round(density * 100))}_s{seed}")


# ----------------------------------------------------------------------------- zgjidhja

def verify(board: Board, cols: tuple[int, ...]) -> list[str]:
    """Kontrollon një zgjidhje (cols[r] = kolona e mbretëreshës në rreshtin r).
    Kthen listën e gabimeve (bosh nëse zgjidhja është e saktë)."""
    errors = []
    if len(cols) != board.n:
        errors.append(f"janë vendosur {len(cols)} mbretëresha, duhen {board.n}")
    for r, c in enumerate(cols):
        if not board.is_free(r, c):
            errors.append(f"mbretëresha ({r + 1},{c + 1}) është në qelizë të bllokuar")
    for r1 in range(len(cols)):
        for r2 in range(r1 + 1, len(cols)):
            c1, c2 = cols[r1], cols[r2]
            if c1 == c2 or abs(c1 - c2) == r2 - r1:
                errors.append(f"({r1 + 1},{c1 + 1}) sulmon ({r2 + 1},{c2 + 1})")
    return errors


def solution_to_asp(cols: tuple[int, ...]) -> str:
    """Dalja në formatin zyrtar: queen(i,j). me indekse 1..N."""
    return " ".join(f"queen({r + 1},{c + 1})." for r, c in enumerate(cols))


def render(board: Board, cols: tuple[int, ...] | None = None) -> str:
    """Vizatim tekstual: Q = mbretëreshë, # = e bllokuar, . = e lirë."""
    queens = set(enumerate(cols)) if cols else set()
    rows = []
    for r in range(board.n):
        row = []
        for c in range(board.n):
            row.append("Q" if (r, c) in queens else "#" if (r, c) in board.blocked else ".")
        rows.append(" ".join(row))
    return "\n".join(rows)
