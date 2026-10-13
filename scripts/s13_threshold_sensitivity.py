"""S13 of docs/supplementary_plan_s13.md v1.0. Usage: s13_threshold_sensitivity.py BASELINE_DIR

Recounts the stored out-of-fold predictions on the dissociated and congruent subsets for a grid of near and
far thresholds. Trains nothing. Writes s13_threshold_sensitivity.csv and prints the largest fold SD of B3 macro-F1.
"""
import csv, gzip, math, sys
from pathlib import Path

D = Path(sys.argv[1])
NEAR, FAR = (0.05, 0.10, 0.15, 0.20, 0.25), (0.40, 0.50, 0.60)
FAMILY = {l: "Sanskrit" for l in ("Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi")}
FAMILY.update({l: "Latin" for l in ("Catalan", "French", "Galician", "Italian", "Portuguese", "Romanian", "Spanish")})


def wilson(k, n):
    if not n:
        return "", ""
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


rows = [r for r in csv.DictReader(gzip.open(D / "oof_predictions.csv.gz", "rt", encoding="utf-8")) if r["lang"] in FAMILY]
out = []
for fam in ("Sanskrit", "Latin"):
    R = [r for r in rows if FAMILY[r["lang"]] == fam]
    for near in NEAR:
        for far in FAR:
            c = {"dis": [0, 0, 0], "con": [0, 0, 0]}
            for r in R:
                d, lrn = float(r["norm_edit_distance"]), r["wiktionary_route"] == "LRN"
                if (not lrn and d <= near) or (lrn and d >= far):
                    k = "dis"
                elif (not lrn and d >= far) or (lrn and d <= near):
                    k = "con"
                else:
                    continue
                c[k][0] += 1
                c[k][1] += int(r["B3_learned"]) == int(lrn)
                c[k][2] += int(r["B2_learned"]) == int(lrn)
            n, b3, b2 = c["dis"]
            lo, hi = wilson(b3, n)
            out.append([fam, near, far, n, b3, round(b3 / n, 4) if n else "", lo, hi, b2, round(b2 / n, 4) if n else "",
                        c["con"][0], c["con"][1], round(c["con"][1] / c["con"][0], 4)])
with open(D / "s13_threshold_sensitivity.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "near", "far", "n_dissociated", "B3_correct", "B3_accuracy", "ci95_low", "ci95_high", "B2_correct",
                "B2_accuracy", "n_congruent", "B3_congruent_correct", "B3_congruent_accuracy"])
    w.writerows(out)
for o in out:
    print(*o)
sd = [(float(r["macro_f1_sd"]), r["lang"]) for r in csv.DictReader(open(D / "a1_cv.csv")) if r["model"] == "B3"]
print("largest fold SD of B3 macro-F1:", max(sd), "; in the two families:", max(s for s in sd if s[1] in FAMILY))
