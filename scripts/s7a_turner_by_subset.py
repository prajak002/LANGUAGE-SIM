"""S7a of docs/supplementary_plan_s7.md v1.0. Usage: s7a_turner_by_subset.py BASELINE_DIR TURNER_DIR OUT_DIR

Turner flags (S4) by S2 subset for the Sanskrit family. Writes s7a_turner_by_subset.csv and s7a_differences.csv.
Reads only flags; no Turner text. Validates no label.
"""
import csv, gzip, math, sys
from collections import Counter, defaultdict
from pathlib import Path

B, T, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
SKT = ["Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi"]


def wilson(k, n):
    if not n:
        return None, None
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, c - h), min(1.0, c + h)


def newcombe(k1, n1, k2, n2):
    """95% interval for p1 - p2 from the two Wilson intervals."""
    p1, p2, (l1, u1), (l2, u2) = k1 / n1, k2 / n2, wilson(k1, n1), wilson(k2, n2)
    d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


flags = {(r["lang"], r["title"], r["wiktionary_route"]): r for r in csv.DictReader(gzip.open(T / "item_flags.csv.gz", "rt", encoding="utf-8"))}
c, unjoined = defaultdict(Counter), 0
for r in csv.DictReader(gzip.open(B / "oof_predictions.csv.gz", "rt", encoding="utf-8")):
    if r["lang"] not in SKT or r["wiktionary_route"] not in ("INH", "LRN"):
        continue
    f = flags.get((r["lang"], r["title"], r["wiktionary_route"]))
    if f is None:
        unjoined += 1
        continue
    for L in (r["lang"], "ALL"):
        k = c[(L, r["subset"], r["wiktionary_route"])]
        k["n"] += 1
        k["T1"] += f["T1"] == "1"
        k["T2"] += f["T2"] == "1"
        k["T3"] += f["T3"] == "1"
print("baseline items without a Turner flag row:", unjoined)
r4 = lambda x: "" if x is None else round(x, 4)
with open(OUT / "s7a_turner_by_subset.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lang", "subset", "wiktionary_route", "items", "T1", "T1_share", "T1_low", "T1_high", "T2", "T3", "T3_of_T1", "T3_low", "T3_high"])
    for (L, sub, route), k in sorted(c.items()):
        w.writerow([L, sub, route, k["n"], k["T1"], r4(k["T1"] / k["n"]), *map(r4, wilson(k["T1"], k["n"])), k["T2"], k["T3"],
                    r4(k["T3"] / k["T1"]) if k["T1"] else "", *map(r4, wilson(k["T3"], k["T1"]))])
        if L == "ALL":
            print(sub.ljust(11), route, f"items {k['n']}  T1 {k['T1']}  T3 {k['T3']}" + (f"  T3/T1 {k['T3'] / k['T1']:.3f}" if k["T1"] else ""))
with open(OUT / "s7a_differences.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lang", "comparison", "inherited_T3", "inherited_T1", "learned_T3", "learned_T1", "difference_T3_of_T1", "ci95_low", "ci95_high", "interpreted"])
    for L in ["ALL"] + SKT:
        for name, a, b in (("near the Sanskrit form (d<=0.15): dissociated inherited minus congruent learned", ("dissociated", "INH"), ("congruent", "LRN")),
                           ("far from the Sanskrit form (d>=0.5): congruent inherited minus dissociated learned", ("congruent", "INH"), ("dissociated", "LRN"))):
            i, l = c[(L, *a)], c[(L, *b)]
            if not i["T1"] or not l["T1"]:
                w.writerow([L, name, i["T3"], i["T1"], l["T3"], l["T1"], "", "", "", "no"])
                continue
            d, lo, hi = newcombe(i["T3"], i["T1"], l["T3"], l["T1"])
            ok = "yes" if min(i["T1"], l["T1"]) >= 30 else "no (fewer than 30)"
            w.writerow([L, name, i["T3"], i["T1"], l["T3"], l["T1"], round(d, 4), round(lo, 4), round(hi, 4), ok])
            if L == "ALL":
                print(name, f"\n   {i['T3']}/{i['T1']} vs {l['T3']}/{l['T1']}: difference {d:.3f} [{lo:.3f}, {hi:.3f}]")
