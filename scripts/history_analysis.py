"""S1 of docs/supplementary_plan.md v1.0. Usage: history_analysis.py RAW_AUDIT_DIR HISTORY_DIR OUT_DIR

Classifies each sampled page at each past snapshot as absent / no route / same / changed, with the same
template reader as the audit. Writes history_measures.csv and history_changes.csv. Fetches nothing.
"""
import csv, gzip, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import ety_sections, ety_text, routes  # noqa: E402

RAW, HIST, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
MAX_RANK = 60


def wilson(k, n):
    if not n:
        return "", ""
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


snap = {}
with gzip.open(HIST / "snapshots.jsonl.gz", "rt", encoding="utf-8") as f:
    for d in map(json.loads, f):
        snap[(d["title"], d["snapshot"])] = d
dates = sorted({k[1] for k in snap}, reverse=True)
cnt, changes, missing = defaultdict(Counter), Counter(), 0
for s in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")):
    if int(s["rank"]) > MAX_RANK:
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
            r = set().union(*(routes(ety_text(c), s["ancestor_code"]) for c in ety_sections(sec)))
            state = "no route" if not r else ("same" if s["category"] in r else "changed")
            if state == "changed":
                changes[(s["ancestor"], s["lang"], date[:10], "+".join(sorted(r)), s["category"])] += 1
        for key in ((s["ancestor"], s["lang"], s["category"], date[:10]), (s["ancestor"], "ALL (pooled, related languages)", s["category"], date[:10])):
            cnt[key][state] += 1
with open(OUT / "history_measures.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ancestor", "lang", "category_now", "snapshot", "absent", "no_route", "same", "changed",
                "H1_changed_share", "H1_low", "H1_high", "H2_route_added_later_share", "H2_low", "H2_high"])
    for (A, L, c, date), k in sorted(cnt.items()):
        n1, n2 = k["same"] + k["changed"], k["no route"] + k["same"] + k["changed"]
        w.writerow([A, L, c, date, k["absent"], k["no route"], k["same"], k["changed"],
                    round(k["changed"] / n1, 4) if n1 else "", *wilson(k["changed"], n1),
                    round(k["no route"] / n2, 4) if n2 else "", *wilson(k["no route"], n2)])
with open(OUT / "history_changes.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ancestor", "lang", "snapshot", "route_then", "category_now", "pages"])
    w.writerows([*k, v] for k, v in sorted(changes.items()))
print("sample-row/snapshot pairs with no stored snapshot:", missing)
for (A, L, c, date), k in sorted(cnt.items()):
    if L.startswith("ALL"):
        print(A, c, date, dict(k))
