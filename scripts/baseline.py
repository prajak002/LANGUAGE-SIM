"""Form-based baseline per docs/baseline_plan.md v1.0. Usage: baseline.py RAW_DIR OUT_DIR  (run with .venv/bin/python)

Reads the audit sample; fetches nothing. Writes items.csv.gz, a1_cv.csv, a2_semi.csv, a3_transfer.csv.
The labels are Wiktionary's own and are not validated.
"""
import csv, gzip, json, math, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import assertions_with_forms, ety_sections, ety_text, from_ancestor

RAW, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20261011
INDIC_TO_DEVA = [(0x0980, 0x09FF), (0x0A00, 0x0A7F), (0x0A80, 0x0AFF), (0x0B00, 0x0B7F)]


def normalise(s):
    out = []
    for ch in unicodedata.normalize("NFD", s):
        cp = ord(ch)
        for lo, hi in INDIC_TO_DEVA:
            if lo <= cp <= hi:
                cp = cp - lo + 0x0900
        ch = chr(cp)
        if 0x0900 <= cp <= 0x097F:
            out.append(ch)
        elif unicodedata.category(ch) != "Mn" and ch not in "-* ":
            out.append(ch.lower())
    return "".join(out)


def ned(a, b):
    if not a or not b:
        return 1.0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] / max(len(a), len(b))


def wilson(k, n):
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(c - h, 4), round(c + h, 4)


sections = {}
with gzip.open(RAW / "sections.jsonl.gz", "rt", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        sections[d["title"]] = d["sections"]
items, seen, dropped = [], set(), Counter()
for s in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")):
    L, A, code, title = s["lang"], s["ancestor"], s["ancestor_code"], s["title"]
    if (L, title) in seen:
        continue
    seen.add((L, title))
    if L == "Urdu":
        dropped["Urdu (script)"] += 1
        continue
    for chunk in ety_sections(sections[title][L]):
        tri = [(r, form) for r, src, form in assertions_with_forms(ety_text(chunk)) if from_ancestor(src, code) and r in ("INH", "LRN", "SEMI")]
        kinds = {r for r, _ in tri}
        if len(kinds) != 1:
            dropped["no single route from the ancestor"] += 1
            continue
        w, e = normalise(title), normalise(next((f for _, f in tri if normalise(f)), ""))
        if not w or not e:
            dropped["empty word or etymon"] += 1
            continue
        items.append((L, A, title, w, e, kinds.pop()))
before = len(items)
items = list(dict.fromkeys(items))
dropped["duplicate item"] = before - len(items)
with gzip.open(OUT / "items.csv.gz", "wt", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lang", "ancestor", "title", "word_norm", "etymon_norm", "wiktionary_route", "norm_edit_distance"])
    w.writerows([*it, round(ned(it[3], it[4]), 4)] for it in items)
print(len(items), "items;", dict(dropped))
by = defaultdict(list)
for it in items:
    by[it[0]].append(it)
anc = {it[0]: it[1] for it in items}


def feats(model, train, test):
    d = lambda rows: csr_matrix(np.array([[ned(r[3], r[4])] for r in rows]))
    if model == "B1":
        return d(train), d(test)
    vw = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([r[3] for r in train])
    Xtr, Xte = vw.transform([r[3] for r in train]), vw.transform([r[3] for r in test])
    if model == "B2":
        return Xtr, Xte
    ve = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([r[4] for r in train])
    return (hstack([Xtr, ve.transform([r[4] for r in train]), d(train)]).tocsr(),
            hstack([Xte, ve.transform([r[4] for r in test]), d(test)]).tocsr())


def fit_predict(model, train, test):
    ytr = np.array([r[5] == "LRN" for r in train])
    if model == "B0":
        return np.full(len(test), ytr.mean() >= 0.5)
    Xtr, Xte = feats(model, train, test)
    return LogisticRegression(max_iter=1000, random_state=SEED).fit(Xtr, ytr).predict(Xte)


def score(y, p):
    return accuracy_score(y, p), f1_score(y, p, average="macro", zero_division=0)


a1 = []
for L in sorted(by, key=lambda x: (anc[x], x)):
    rows = [r for r in by[L] if r[5] in ("INH", "LRN")]
    y = np.array([r[5] == "LRN" for r in rows])
    if min(y.sum(), (~y).sum()) < 50:
        a1.append([anc[L], L, int((~y).sum()), int(y.sum()), "skipped: fewer than 50 items in a class", "", "", "", ""])
        continue
    folds = list(StratifiedKFold(5, shuffle=True, random_state=SEED).split(rows, y))
    for m in ("B0", "B1", "B2", "B3"):
        sc = np.array([score(y[te], fit_predict(m, [rows[i] for i in tr], [rows[i] for i in te])) for tr, te in folds])
        a1.append([anc[L], L, int((~y).sum()), int(y.sum()), m, *np.round(sc.mean(0), 4), *np.round(sc.std(0), 4)][:9])
with open(OUT / "a1_cv.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ancestor", "lang", "n_inherited", "n_learned", "model", "accuracy_mean", "macro_f1_mean", "accuracy_sd", "macro_f1_sd"])
    w.writerows(a1)

a2 = []
for L in sorted(by, key=lambda x: (anc[x], x)):
    two, semi = [r for r in by[L] if r[5] in ("INH", "LRN")], [r for r in by[L] if r[5] == "SEMI"]
    mean = lambda k: round(float(np.mean([ned(r[3], r[4]) for r in by[L] if r[5] == k])), 4) if any(r[5] == k for r in by[L]) else ""
    if len(semi) < 20:
        a2.append([anc[L], L, len(semi), "skipped: fewer than 20 semi-learned items", "", "", "", mean("INH"), mean("SEMI"), mean("LRN")])
        continue
    for m in ("B1", "B3"):
        k = int(fit_predict(m, two, semi).sum())
        a2.append([anc[L], L, len(semi), m, k, *wilson(k, len(semi)), mean("INH"), mean("SEMI"), mean("LRN")])
with open(OUT / "a2_semi.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ancestor", "lang", "n_semi", "model", "predicted_learned", "ci95_low", "ci95_high", "mean_ned_inherited", "mean_ned_semi", "mean_ned_learned"])
    w.writerows(a2)

a3 = []
for A in ("Sanskrit", "Latin"):
    Ls = sorted(L for L in by if anc[L] == A)
    for held in Ls:
        train = [r for L in Ls if L != held for r in by[L] if r[5] in ("INH", "LRN")]
        test = [r for r in by[held] if r[5] in ("INH", "LRN")]
        y = np.array([r[5] == "LRN" for r in test])
        a3.append([A, held, len(train), len(test), *np.round(score(y, fit_predict("B1", train, test)), 4)])
with open(OUT / "a3_transfer.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ancestor", "held_out_lang", "n_train", "n_test", "accuracy", "macro_f1"])
    w.writerows(a3)
print("A1 rows", len(a1), "A2 rows", len(a2), "A3 rows", len(a3))
