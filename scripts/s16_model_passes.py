"""S16 of docs/supplementary_plan_s16.md v1.0. Usage: s16_model_passes.py KIT_DIR BASELINE_DIR OUT_CSV

Compares the two model passes over the dissociation sheets with Wiktionary's route, for controls and dissociated
items that are still so in the corrected baseline. Descriptive; validates no label.
"""
import csv, gzip, math, sys
from collections import Counter, defaultdict
from pathlib import Path

KIT, B, OUT = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
LANGS = ["Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi"]


def wilson(k, n):
    if not n:
        return "", ""
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


def subset(d, inh):
    if (inh and d >= 0.5) or (not inh and d <= 0.15):
        return "congruent"
    if (inh and d <= 0.15) or (not inh and d >= 0.5):
        return "dissociated"
    return "middle"


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


dist = defaultdict(set)
for r in csv.DictReader(gzip.open(B / "items.csv.gz", "rt", encoding="utf-8")):
    dist[(r["lang"], r["title"], r["wiktionary_route"])].add(float(r["norm_edit_distance"]))
rows, pairs, out = [], [], []
for L in LANGS:
    key = {r["item_id"]: r for r in csv.DictReader(open(KIT / f"_sealed_key_{L.lower()}_dissociation.csv", encoding="utf-8"))}
    lab = {p: {r["item_id"]: r["label"].strip().upper() for r in csv.DictReader(open(KIT / f"{L.lower()}_dissociation_annotator_{p}.csv", encoding="utf-8"))} for p in "AB"}
    for i, k in key.items():
        d = dist.get((L, k["word"], k["wiktionary_route"]), set())
        if len(d) != 1 or subset(next(iter(d)), k["wiktionary_route"] == "INH") != k["subset"]:
            continue
        for p in "AB":
            if i in lab[p] and lab[p][i]:
                rows.append((L, p, k["subset"], k["wiktionary_route"], lab[p][i]))
        if L != "Hindi" and lab["A"].get(i) and lab["B"].get(i):
            pairs.append((lab["A"][i], lab["B"][i]))
    print(L, "key rows", len(key), "| pass A rows in key", sum(i in key for i in lab["A"]), "| pass B rows in key", sum(i in key for i in lab["B"]))
for scope in ["ALL"] + LANGS:
    for p in "AB":
        for sub in ("congruent", "dissociated"):
            for route in ("both", "INH", "LRN"):
                R = [r for r in rows if scope in ("ALL", r[0]) and r[1] == p and r[2] == sub and route in ("both", r[3])]
                dec = [r for r in R if r[4] in ("INH", "LRN")]
                k = sum(r[4] == r[3] for r in dec)
                out.append([scope, p, sub, route, len(R), len(dec), k, round(k / len(dec), 4) if dec else "", *wilson(k, len(dec))])
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["scope", "pass", "subset", "wiktionary_route", "rows", "decided", "agree_with_wiktionary", "share", "ci95_low", "ci95_high"])
    w.writerows(out)
for o in out:
    if o[0] == "ALL":
        print(*o)
po, ka = kappa(pairs)
print("between passes (Hindi left out):", len(pairs), "rows; raw agreement", round(po, 4), "; kappa", round(ka, 4))
