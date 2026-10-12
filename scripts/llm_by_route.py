"""Additions fixed in docs/supplementary_plan_s5b.md v1.0. Usage: llm_by_route.py OUT_DIR

Reads OUT_DIR/answers.jsonl. Writes the share of "learned" answers by Wiktionary route (by_route.csv) and the
balanced score per family, condition and subset (balanced.csv; cells with at least 20 items of each route).
Model output is never a label.
"""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(sys.argv[1])
ANC = {**dict.fromkeys(["Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi"], "Sanskrit"),
       **dict.fromkeys(["Catalan", "French", "Galician", "Italian", "Portuguese", "Romanian", "Spanish"], "Latin"),
       "Greek": "Ancient Greek", "Armenian": "Old Armenian"}
c = defaultdict(Counter)
for d in map(json.loads, open(OUT / "answers.jsonl", encoding="utf-8")):
    m = re.search(r"[AB]", d["raw"].upper())
    ans = None if not m else (d["A_is"] if m.group(0) == "A" else ("LRN" if d["A_is"] == "INH" else "INH"))
    for fam in (ANC[d["lang"]], "ALL"):
        k = c[(fam, d["condition"], d["subset"], d["route"])]
        k["n"] += 1
        k["lrn"] += ans == "LRN"
        k["ok"] += ans == d["route"]
with open(OUT / "by_route.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "condition", "subset", "wiktionary_route", "n", "model_says_learned", "share_says_learned"])
    for key, k in sorted(c.items()):
        w.writerow([*key, k["n"], k["lrn"], round(k["lrn"] / k["n"], 4)])
with open(OUT / "balanced.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "condition", "subset", "n_inherited", "correct_inherited", "n_learned", "correct_learned", "balanced_score"])
    for fam, cond, sub in sorted({k[:3] for k in c}):
        i, l = c[(fam, cond, sub, "INH")], c[(fam, cond, sub, "LRN")]
        bal = round((i["ok"] / i["n"] + l["ok"] / l["n"]) / 2, 4) if min(i["n"], l["n"]) >= 20 else ""
        w.writerow([fam, cond, sub, i["n"], i["ok"], l["n"], l["ok"], bal])
        print(fam.ljust(14), cond.ljust(12), sub.ljust(11), f"INH {i['ok']}/{i['n']}  LRN {l['ok']}/{l['n']}  balanced {bal}")
