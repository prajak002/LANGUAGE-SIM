"""S7b of docs/supplementary_plan_s7.md v1.0. Usage: s7b_history_by_subset.py RAW_AUDIT_DIR HISTORY_DIR BASELINE_DIR OUT_DIR

Label history (S1 states, same reader) by S2 subset. Writes s7b_history_by_subset.csv and s7b_differences.csv.
Fetches nothing. A stable label is not a correct label.
"""
import csv, gzip, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import ety_sections, ety_text, routes  # noqa: E402

RAW, HIST, B, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)
MAX_RANK = 60


def wilson(k, n):
    if not n:
        return None, None
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, c - h), min(1.0, c + h)


def newcombe(k1, n1, k2, n2):
    p1, p2, (l1, u1), (l2, u2) = k1 / n1, k2 / n2, wilson(k1, n1), wilson(k2, n2)
    d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


subset = {(r["lang"], r["title"], r["wiktionary_route"]): r["subset"] for r in csv.DictReader(gzip.open(B / "oof_predictions.csv.gz", "rt", encoding="utf-8"))}
snap = {}
with gzip.open(HIST / "snapshots.jsonl.gz", "rt", encoding="utf-8") as f:
    for d in map(json.loads, f):
        snap[(d["title"], d["snapshot"])] = d
dates = sorted({k[1] for k in snap}, reverse=True)
c, not_item, missing = defaultdict(Counter), 0, 0
for s in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")):
    if int(s["rank"]) > MAX_RANK or s["category"] not in ("INH", "LRN"):
        continue
    sub = subset.get((s["lang"], s["title"], s["category"]))
    if sub is None:  # not a baseline item (Urdu, no single route, or no ancestor form)
        not_item += 1
        continue
    for date in dates:
        d = snap.get((s["title"], date))
        if d is None:
            missing += 1
            continue
        sec = d["sections"].get(s["lang"])
        if not sec:
            state = "absent"
        else:
            r = set().union(*(routes(ety_text(x), s["ancestor_code"]) for x in ety_sections(sec)))
            state = "no route" if not r else ("same" if s["category"] in r else "changed")
        for fam in (s["ancestor"], "ALL"):
            c[(fam, date[:10], sub)][state] += 1
print("sampled rows that are not baseline items:", not_item, "| item/snapshot pairs with no stored snapshot:", missing)
r4 = lambda x: "" if x is None else round(x, 4)
with open(OUT / "s7b_history_by_subset.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "snapshot", "subset", "absent", "no_route", "same", "changed", "H1_changed_share", "H1_low", "H1_high",
                "H2_route_added_later_share", "H2_low", "H2_high"])
    for (fam, date, sub), k in sorted(c.items()):
        n1, n2 = k["same"] + k["changed"], k["no route"] + k["same"] + k["changed"]
        w.writerow([fam, date, sub, k["absent"], k["no route"], k["same"], k["changed"], r4(k["changed"] / n1) if n1 else "", *map(r4, wilson(k["changed"], n1)),
                    r4(k["no route"] / n2) if n2 else "", *map(r4, wilson(k["no route"], n2))])
        print(fam.ljust(14), date, sub.ljust(11), dict(k))
with open(OUT / "s7b_differences.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "snapshot", "dissociated_changed", "dissociated_n", "congruent_changed", "congruent_n", "difference_H1", "ci95_low", "ci95_high", "interpreted"])
    for fam, date in sorted({k[:2] for k in c}):
        a, b = c[(fam, date, "dissociated")], c[(fam, date, "congruent")]
        na, nb = a["same"] + a["changed"], b["same"] + b["changed"]
        if not na or not nb:
            w.writerow([fam, date, a["changed"], na, b["changed"], nb, "", "", "", "no"])
            continue
        d, lo, hi = newcombe(a["changed"], na, b["changed"], nb)
        w.writerow([fam, date, a["changed"], na, b["changed"], nb, round(d, 4), round(lo, 4), round(hi, 4), "yes" if min(na, nb) >= 30 else "no (fewer than 30)"])
        print(fam.ljust(14), date, f"H1 dissociated {a['changed']}/{na} vs congruent {b['changed']}/{nb}: difference {d:.3f} [{lo:.3f}, {hi:.3f}]")
