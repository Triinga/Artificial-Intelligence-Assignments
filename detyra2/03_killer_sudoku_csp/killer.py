"""
Killer Sudoku: leximi i puzzle-ve, verifikimi dhe vizatimi.

Rregullat (https://sudoku.com/killer): Sudoku standard 9×9 (shifrat 1..9 të ndryshme në çdo rresht,
kolonë dhe kuti 3×3) plus "kafaze" (cages): shifrat brenda një kafazi janë të ndryshme dhe shuma e
tyre është e barabartë me numrin e dhënë.

Formati tekst (.txt) – 9 rreshta me 9 shkronja, çdo shkronjë = identifikuesi i kafazit;
opsionalisht 9 rreshta me shifrat e dhëna (sudoku.com jep disa shifra në nivelet më të lehta,
'.' = qelizë bosh); pastaj shumat "ID SHUMA":

    # komentet fillojnë me '#'
    aabbcddee
    ...            (9 rreshta kafazesh)
    ..3....5.
    ...            (9 rreshta me shifra të dhëna – opsionale)
    a 3   b 15   c 22 ...

Formati JSON (.json):

    {"name": "...", "cages": [{"sum": 3, "cells": ["A1", "A2"]}, ...], "givens": {"A3": 3}}

ku qelizat shënohen me rreshtin A..I dhe kolonën 1..9 (A1 = këndi lart-majtas).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

ROWS = "ABCDEFGHI"


@dataclass
class Cage:
    total: int
    cells: list[int]            # indekset 0..80 (r*9 + c)


@dataclass
class Puzzle:
    name: str
    cages: list[Cage]
    givens: list[int] = None    # 81 vlera, 0 = bosh
    difficulty: str = ""

    def __post_init__(self):
        if self.givens is None:
            self.givens = [0] * 81


def cell_name(i: int) -> str:
    return f"{ROWS[i // 9]}{i % 9 + 1}"


def parse_cell(s: str) -> int:
    s = s.strip().upper()
    if len(s) != 2 or s[0] not in ROWS or not s[1].isdigit() or s[1] == "0":
        raise ValueError(f"qelizë e pavlefshme: {s!r} (p.sh. A1 .. I9)")
    return ROWS.index(s[0]) * 9 + int(s[1]) - 1


def validate(p: Puzzle) -> None:
    """Kafazet duhet të mbulojnë çdo qelizë saktësisht një herë dhe shumat duhet të jenë të mundshme."""
    seen = {}
    for k, cage in enumerate(p.cages):
        for c in cage.cells:
            if c in seen:
                raise ValueError(f"qeliza {cell_name(c)} është në dy kafaze")
            seen[c] = k
        n = len(cage.cells)
        lo, hi = n * (n + 1) // 2, sum(range(10 - n, 10))
        if not 1 <= n <= 9 or not lo <= cage.total <= hi:
            raise ValueError(f"kafazi {k} me {n} qeliza nuk mund të ketë shumë {cage.total}")
    missing = [cell_name(i) for i in range(81) if i not in seen]
    if missing:
        raise ValueError(f"qelizat pa kafaz: {', '.join(missing)}")
    if sum(c.total for c in p.cages) != 405:
        raise ValueError(f"shuma e kafazeve është {sum(c.total for c in p.cages)}, duhet 405 (= 9 × 45)")


def load_puzzle(path: str) -> Puzzle:
    name = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if path.lower().endswith(".json"):
        data = json.loads(text)
        cages = [Cage(int(c["sum"]), [parse_cell(x) for x in c["cells"]]) for c in data["cages"]]
        givens = [0] * 81
        for cell, v in data.get("givens", {}).items():
            givens[parse_cell(cell)] = int(v)
        p = Puzzle(data.get("name", name), cages, givens, data.get("difficulty", ""))
    else:
        lines = [ln.split("#", 1)[0].strip() for ln in text.splitlines()]
        lines = [ln for ln in lines if ln]
        grid = [ln.replace(" ", "") for ln in lines[:9]]
        if len(grid) != 9 or any(len(g) != 9 for g in grid):
            raise ValueError("duhen 9 rreshta me nga 9 simbole për kafazet")
        rest = lines[9:]
        givens = [0] * 81
        g_lines = [ln.replace(" ", "") for ln in rest[:9]]
        if len(g_lines) == 9 and all(len(g) == 9 and set(g) <= set(".123456789") for g in g_lines):
            givens = [0 if ch == "." else int(ch) for g in g_lines for ch in g]
            rest = rest[9:]
        tokens = " ".join(rest).split()
        if len(tokens) % 2:
            raise ValueError("shumat duhet të jepen si çifte 'ID SHUMA'")
        sums = {tokens[i]: int(tokens[i + 1]) for i in range(0, len(tokens), 2)}
        cells: dict[str, list[int]] = {}
        for r in range(9):
            for c in range(9):
                cells.setdefault(grid[r][c], []).append(r * 9 + c)
        unknown = set(cells) - set(sums)
        if unknown:
            raise ValueError(f"mungon shuma për kafazet: {sorted(unknown)}")
        p = Puzzle(name, [Cage(sums[k], v) for k, v in cells.items()], givens)
    validate(p)
    return p


# ----------------------------------------------------------------------------- zgjidhja

UNITS = ([[r * 9 + c for c in range(9)] for r in range(9)] +                      # rreshtat
         [[r * 9 + c for r in range(9)] for c in range(9)] +                      # kolonat
         [[(br + i) * 9 + bc + j for i in range(3) for j in range(3)]            # kutitë 3×3
          for br in (0, 3, 6) for bc in (0, 3, 6)])


def verify(p: Puzzle, grid: list[int]) -> list[str]:
    """Kontrollon të gjitha rregullat. Kthen listën e shkeljeve (bosh = zgjidhje e saktë)."""
    errors = []
    if len(grid) != 81 or any(not 1 <= v <= 9 for v in grid):
        return ["rrjeta duhet të ketë 81 shifra 1..9"]
    for i, g in enumerate(p.givens):
        if g and grid[i] != g:
            errors.append(f"{cell_name(i)} duhet të jetë {g} (shifër e dhënë)")
    for unit in UNITS:
        if len({grid[i] for i in unit}) != 9:
            errors.append(f"përsëritje në njësinë {cell_name(unit[0])}..{cell_name(unit[-1])}")
    for cage in p.cages:
        vals = [grid[i] for i in cage.cells]
        if len(set(vals)) != len(vals):
            errors.append(f"përsëritje në kafazin {cell_name(cage.cells[0])}")
        if sum(vals) != cage.total:
            errors.append(f"kafazi {cell_name(cage.cells[0])}: shuma {sum(vals)} ≠ {cage.total}")
    return errors


def render(p: Puzzle, grid: list[int] | None = None) -> str:
    """Vizaton rrjetën 9×9. Pa zgjidhje: shuma e kafazit në qelizën e parë të tij, (d) = shifër e dhënë."""
    label = {}
    for cage in p.cages:
        label[min(cage.cells)] = str(cage.total)
    out = []
    for r in range(9):
        if r % 3 == 0:
            out.append("+-------+-------+-------+" if grid else "+----------+----------+----------+")
        row = "|"
        for c in range(9):
            i = r * 9 + c
            if grid:
                row += f" {grid[i]}"
            elif p.givens[i]:
                row += f"{'(' + str(p.givens[i]) + ')':>3}"
            else:
                row += f"{label.get(i, '.'):>3}"
            if c % 3 == 2:
                row += " |" if grid else " |"
        out.append(row)
    out.append("+-------+-------+-------+" if grid else "+----------+----------+----------+")
    return "\n".join(out)
