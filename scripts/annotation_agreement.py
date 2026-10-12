"""Agreement between two annotators, and of each with Wiktionary. Usage: annotation_agreement.py SHEET_A SHEET_B [SEALED_KEY]

Sheets are CSV files with columns item_id and label. Rows with an empty label in either sheet are
counted and left out. Prints raw agreement, Cohen's kappa and the confusion table. With a key
(item_id, wiktionary_route) it also compares each annotator with Wiktionary. `--self-test` checks the
kappa computation on a worked example.
"""
import csv, sys
from collections import Counter


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


def read(path, col="label"):
    return {r["item_id"]: r[col].strip().upper() for r in csv.DictReader(open(path, encoding="utf-8"))}


def report(name, x, y):
    ids = [i for i in x if i in y]
    pairs = [(x[i], y[i]) for i in ids if x[i] and y[i]]
    print(f"\n{name}: {len(pairs)} items compared, {len(ids) - len(pairs)} left out (empty label)")
    if not pairs:
        return
    po, k = kappa(pairs)
    print(f"  raw agreement {po:.3f}   Cohen's kappa {k:.3f}")
    for (a, b), c in sorted(Counter(pairs).items()):
        print(f"  {a:>5} / {b:<5} {c}")


if sys.argv[1] == "--self-test":
    # 2x2 worked example: 20 yes/yes, 5 yes/no, 10 no/yes, 15 no/no -> po = 0.70, pe = 0.50, kappa = 0.40
    po, k = kappa([("Y", "Y")] * 20 + [("Y", "N")] * 5 + [("N", "Y")] * 10 + [("N", "N")] * 15)
    assert abs(po - 0.70) < 1e-9 and abs(k - 0.40) < 1e-9, (po, k)
    print("kappa self-test passes")
    sys.exit(0)
A, B = read(sys.argv[1]), read(sys.argv[2])
report("Annotator A / annotator B", A, B)
if len(sys.argv) > 3:
    K = read(sys.argv[3], "wiktionary_route")
    report("Annotator A / Wiktionary", A, K)
    report("Annotator B / Wiktionary", B, K)
