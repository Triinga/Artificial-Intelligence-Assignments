"""
Instancat e problemit të uljes së mysafirëve: lexim, shkrim dhe gjenerim.

Një instancë është një folder me tre skedarë CSV:
    guests.csv     id,gender          (gender = M ose F), p.sh. "M1,F"
    conflicts.csv  a,b                çifte që NUK duhet të ulen në të njëjtën tavolinë
    together.csv   a,b                çifte që DUHET të ulen në të njëjtën tavolinë
Rreshtat bosh dhe ato që fillojnë me '#' injorohen. Emrat e mysafirëve ndjekin shembullin e
detyrës: M1, M2, ..., M100.
"""

from __future__ import annotations

import csv
import os
import random
from dataclasses import dataclass, field


@dataclass
class Instance:
    guests: list[str]                         # identifikuesit, në rend
    gender: dict[str, str]                    # id -> "M" / "F"
    conflicts: list[tuple[str, str]] = field(default_factory=list)
    together: list[tuple[str, str]] = field(default_factory=list)
    tables: int = 10
    capacity: int = 10
    max_diff: int = 3                         # |burra - gra| <= max_diff në çdo tavolinë
    name: str = "instance"

    @property
    def n(self) -> int:
        return len(self.guests)

    def index(self) -> dict[str, int]:
        return {g: i for i, g in enumerate(self.guests)}

    def men(self) -> list[str]:
        return [g for g in self.guests if self.gender[g] == "M"]


# ----------------------------------------------------------------------------- I/O

def _rows(path: str):
    if not os.path.exists(path):
        return
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            row = [x.strip() for x in row]
            if not row or not row[0] or row[0].startswith("#"):
                continue
            yield row


def load_instance(folder: str, tables: int = 10, capacity: int = 10, max_diff: int = 3) -> Instance:
    guests, gender = [], {}
    for row in _rows(os.path.join(folder, "guests.csv")):
        if row[0].lower() == "id":            # header
            continue
        g, sex = row[0], row[1].upper()
        if sex not in ("M", "F"):
            raise ValueError(f"gjinia e panjohur për {g}: {sex}")
        guests.append(g)
        gender[g] = sex

    def pairs(fname):
        out = []
        for row in _rows(os.path.join(folder, fname)):
            if row[0].lower() == "a":
                continue
            a, b = row[0], row[1]
            for x in (a, b):
                if x not in gender:
                    raise ValueError(f"{fname}: mysafiri i panjohur {x}")
            out.append((a, b))
        return out

    return Instance(guests, gender, pairs("conflicts.csv"), pairs("together.csv"),
                    tables, capacity, max_diff, os.path.basename(os.path.normpath(folder)))


def save_instance(inst: Instance, folder: str, header_comment: str = "") -> None:
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "guests.csv"), "w", newline="", encoding="utf-8") as fh:
        if header_comment:
            fh.write(f"# {header_comment}\n")
        w = csv.writer(fh)
        w.writerow(["id", "gender"])
        for g in inst.guests:
            w.writerow([g, inst.gender[g]])
    for fname, pairs in (("conflicts.csv", inst.conflicts), ("together.csv", inst.together)):
        with open(os.path.join(folder, fname), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["a", "b"])
            w.writerows(pairs)


# ----------------------------------------------------------------------------- gjeneratori

def generate(seed: int, n_conflicts: int = 150, n_together: int = 40, n_men: int = 50,
             tables: int = 10, capacity: int = 10, max_diff: int = 3,
             planted: bool = True) -> Instance:
    """Gjeneron një instancë të rastësishme me seed fiks.

    planted=True: së pari ndërtohet një plan i fshehtë i vlefshëm (çdo tavolinë ka 4–6 burra kur
    kjo është e mundur), pastaj konfliktet zgjidhen vetëm mes mysafirëve në tavolina të ndryshme
    dhe çiftet "bashkë" vetëm brenda së njëjtës tavolinë. Kështu instanca garantohet të jetë SAT.
    planted=False: çiftet zgjidhen krejt rastësisht (mund të dalë SAT ose UNSAT).
    """
    rng = random.Random(seed)
    n = tables * capacity
    guests = [f"M{i}" for i in range(1, n + 1)]
    sexes = ["M"] * n_men + ["F"] * (n - n_men)
    rng.shuffle(sexes)
    gender = dict(zip(guests, sexes))

    conflicts: set[tuple[str, str]] = set()
    together: set[tuple[str, str]] = set()
    if planted:
        # Plan i fshehtë: shpërndaj burrat sa më njëtrajtshëm, pastaj mbush me gra.
        men = [g for g in guests if gender[g] == "M"]
        women = [g for g in guests if gender[g] == "F"]
        rng.shuffle(men)
        rng.shuffle(women)
        plan = [[] for _ in range(tables)]
        for k, g in enumerate(men):
            plan[k % tables].append(g)
        for g in women:
            min(plan, key=len).append(g)
        table_of = {g: t for t, members in enumerate(plan) for g in members}
        while len(conflicts) < n_conflicts:
            a, b = rng.sample(guests, 2)
            if table_of[a] != table_of[b]:
                conflicts.add(tuple(sorted((a, b), key=guests.index)))
        while len(together) < n_together:
            t = rng.randrange(tables)
            a, b = rng.sample(plan[t], 2)
            together.add(tuple(sorted((a, b), key=guests.index)))
    else:
        while len(conflicts) < n_conflicts:
            a, b = rng.sample(guests, 2)
            conflicts.add(tuple(sorted((a, b), key=guests.index)))
        while len(together) < n_together:
            a, b = rng.sample(guests, 2)
            p = tuple(sorted((a, b), key=guests.index))
            if p not in conflicts:
                together.add(p)

    key = lambda p: (guests.index(p[0]), guests.index(p[1]))
    return Instance(guests, gender, sorted(conflicts, key=key), sorted(together, key=key),
                    tables, capacity, max_diff, f"random_s{seed}")
