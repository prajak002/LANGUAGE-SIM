"""Local release package of the benchmark (not published). Usage: build_release.py AUDIT_RAW BASELINE_DIR WOLD_AUDIT_DIR OUT_DIR

Everything in it derives from English Wiktionary (CC BY-SA 4.0) or the World Loanword Database (CC BY 4.0).
Nothing from Turner, Platts, the Dasa dictionaries, Chatterji or Jambu is included.
"""
import csv, gzip, json, sys
from collections import Counter
from pathlib import Path

RAW, BASE, WOLD, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)
rev = {}
with gzip.open(RAW / "sections.jsonl.gz", "rt", encoding="utf-8") as f:
    for d in map(json.loads, f):
        rev[d["title"]] = (d["pageid"], d["revid"], d["timestamp"])
oof = {(r["lang"], r["title"], r["wiktionary_route"]): r for r in csv.DictReader(gzip.open(BASE / "oof_predictions.csv.gz", "rt", encoding="utf-8"))}
expert = {r["title"]: r["expert_class"] for r in csv.DictReader(open(WOLD / "v2_baseline_vs_expert.csv", encoding="utf-8"))}
rows, n = [], Counter()
for r in csv.DictReader(gzip.open(BASE / "items.csv.gz", "rt", encoding="utf-8")):
    o = oof.get((r["lang"], r["title"], r["wiktionary_route"]))
    subset = o["subset"] if o else "semi-learned (not in the two-class split)"
    pid, revid, ts = rev[r["title"]]
    rows.append([r["lang"], r["ancestor"], r["title"], r["etymon_norm"], r["wiktionary_route"], r["norm_edit_distance"], subset,
                 o["B1_learned"] if o else "", o["B2_learned"] if o else "", o["B3_learned"] if o else "",
                 expert.get(r["title"], "") if r["lang"] == "Romanian" else "", pid, revid, ts,
                 f"https://en.wiktionary.org/w/index.php?oldid={revid}"])
    n[(r["lang"], subset.split(" ")[0])] += 1
with gzip.open(OUT / "route_label_benchmark.csv.gz", "wt", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["language", "ancestor", "word", "ancestor_form_normalised", "wiktionary_route", "norm_edit_distance", "subset",
                "baseline_B1_says_learned", "baseline_B2_says_learned", "baseline_B3_says_learned", "expert_class_romanian_wold",
                "wiktionary_pageid", "wiktionary_revid", "revision_timestamp", "revision_url"])
    w.writerows(rows)
with open(OUT / "counts.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["language", "congruent", "middle", "dissociated", "semi-learned"])
    for L in sorted({k[0] for k in n}):
        w.writerow([L, *(n[(L, s)] for s in ("congruent", "middle", "dissociated", "semi-learned"))])
print(len(rows), "rows;", sum(v for (L, s), v in n.items() if s == "dissociated"), "dissociated")
