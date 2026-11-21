"""
Krijon instancat e folderit instances/ (të riprodhueshme, seed fiks):

    python make_instances.py

sat_party         – 100 mysafirë (50 burra), 150 konflikte, 40 çifte bashkë (plan i fshehtë -> SAT)
unsat_big_family  – sat_party + familja M90..M100 (11 veta) duhet të ulet bashkë, por tavolina ka 10 vende
unsat_enemies     – sat_party + M1..M11 janë armiq dy nga dy: 11 veta në 10 tavolina (pigeonhole)
"""

import copy
import os

from instance import generate, save_instance

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    base = generate(2026)
    out = lambda name: os.path.join(HERE, "instances", name)
    order = lambda p: (base.guests.index(p[0]), base.guests.index(p[1]))
    save_instance(base, out("sat_party"), "SAT: generate(seed=2026), 150 konflikte, 40 çifte bashkë")

    fam = copy.deepcopy(base)
    members = base.guests[89:100]                                  # M90..M100
    fam.together += [(members[0], m) for m in members[1:]]
    fam.conflicts = [p for p in fam.conflicts if not (p[0] in members and p[1] in members)]
    save_instance(fam, out("unsat_big_family"), "UNSAT: familja M90..M100 (11 veta) duhet bashkë")

    enemies = copy.deepcopy(base)
    group = base.guests[:11]                                       # M1..M11
    enemies.together = [p for p in enemies.together if not (p[0] in group and p[1] in group)]
    enemies.conflicts = sorted(set(enemies.conflicts) | {(group[i], group[j]) for i in range(11)
                                                         for j in range(i + 1, 11)}, key=order)
    save_instance(enemies, out("unsat_enemies"), "UNSAT: M1..M11 armiq dy nga dy (11 veta, 10 tavolina)")
    print("Instancat u krijuan në instances/")


if __name__ == "__main__":
    main()
