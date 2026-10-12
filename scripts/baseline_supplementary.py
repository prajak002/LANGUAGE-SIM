"""S2 and S3 of docs/supplementary_plan.md v1.0. Usage: baseline_supplementary.py RAW_AUDIT_DIR BASELINE_DIR  (.venv/bin/python)

Reruns the A1 cross-validation with the same folds and seed as scripts/baseline.py, keeps one out-of-fold
prediction per item, and reports accuracy on the congruent / middle / dissociated subsets (S2) and on
items with and without an inline citation (S3). Writes oof_predictions.csv.gz, s2_dissociation.csv, s3_citation.csv.
"""
import csv, gzip, json, math, re, sys
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import assertions_with_forms, ety_sections, ety_text, from_ancestor  # noqa: E402

RAW, D = Path(sys.argv[1]), Path(sys.argv[2])
SEED = 20261011


def wilson(k, n):
    if not n:
        return "", ""
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


items = [r for r in csv.DictReader(gzip.open(D / "items.csv.gz", "rt", encoding="utf-8")) if r["wiktionary_route"] in ("INH", "LRN")]
code = {r["lang"]: r["ancestor_code"] for r in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8"))}
sections = {}
with gzip.open(RAW / "sections.jsonl.gz", "rt", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        sections[d["title"]] = d["sections"]


def cited(r):
    """True if a sense of this page that states exactly this route from the ancestor has an inline citation."""
    for chunk in ety_sections(sections[r["title"]][r["lang"]]):
        e = ety_text(chunk)
        kinds = {k for k, src, _ in assertions_with_forms(e) if from_ancestor(src, code[r["lang"]]) and k in ("INH", "LRN", "SEMI")}
        if kinds == {r["wiktionary_route"]} and re.search(r"<ref[ >]|\{\{R:", e):
            return True
    return False


def subset(r):
    d, inh = float(r["norm_edit_distance"]), r["wiktionary_route"] == "INH"
    if (inh and d >= 0.5) or (not inh and d <= 0.15):
        return "congruent"
    if (inh and d <= 0.15) or (not inh and d >= 0.5):
        return "dissociated"
    return "middle"


oof, s2, s3 = [], [], []
for L in sorted({r["lang"] for r in items}):
    rows = [r for r in items if r["lang"] == L]
    y = np.array([r["wiktionary_route"] == "LRN" for r in rows])
    dist = np.array([[float(r["norm_edit_distance"])] for r in rows])
    pred = {m: np.zeros(len(rows), dtype=bool) for m in ("B1", "B2", "B3")}
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=SEED).split(rows, y):
        vw = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([rows[i]["word_norm"] for i in tr])
        ve = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([rows[i]["etymon_norm"] for i in tr])
        W = lambda idx: vw.transform([rows[i]["word_norm"] for i in idx])
        X = {"B1": lambda idx: csr_matrix(dist[idx]), "B2": W,
             "B3": lambda idx: hstack([W(idx), ve.transform([rows[i]["etymon_norm"] for i in idx]), csr_matrix(dist[idx])]).tocsr()}
        for m in pred:
            pred[m][te] = LogisticRegression(max_iter=1000, random_state=SEED).fit(X[m](tr), y[tr]).predict(X[m](te))
    sub = np.array([subset(r) for r in rows])
    cit = np.array([cited(r) for r in rows])
    for i, r in enumerate(rows):
        oof.append([L, r["title"], r["wiktionary_route"], r["norm_edit_distance"], sub[i], int(cit[i]), *(int(pred[m][i]) for m in ("B1", "B2", "B3"))])
    for m in pred:
        ok = pred[m] == y
        for name in ("congruent", "middle", "dissociated"):
            k, n = int(ok[sub == name].sum()), int((sub == name).sum())
            s2.append([L, m, name, k, n, round(k / n, 4) if n else "", *wilson(k, n)])
    if min(cit.sum(), (~cit).sum()) >= 30:
        ok = pred["B3"] == y
        kc, nc, ku, nu = int(ok[cit].sum()), int(cit.sum()), int(ok[~cit].sum()), int((~cit).sum())
        s3.append([L, nc, round(kc / nc, 4), *wilson(kc, nc), nu, round(ku / nu, 4), *wilson(ku, nu), round(kc / nc - ku / nu, 4),
                   round(float(y[cit].mean()), 4), round(float(y[~cit].mean()), 4)])
    else:
        s3.append([L, int(cit.sum()), "", "", "", int((~cit).sum()), "", "", "", "skipped: fewer than 30 items in a group", "", ""])
    print(L, "B3 macro-F1 from out-of-fold predictions", round(f1_score(y, pred["B3"], average="macro"), 4), flush=True)

for name, head, data in (("oof_predictions.csv.gz", ["lang", "title", "wiktionary_route", "norm_edit_distance", "subset", "inline_citation", "B1_learned", "B2_learned", "B3_learned"], oof),
                         ("s2_dissociation.csv", ["lang", "model", "subset", "correct", "n", "accuracy", "ci95_low", "ci95_high"], s2),
                         ("s3_citation.csv", ["lang", "n_cited", "acc_cited", "cited_ci_low", "cited_ci_high", "n_uncited", "acc_uncited", "uncited_ci_low", "uncited_ci_high",
                                              "difference", "share_learned_among_cited", "share_learned_among_uncited"], s3)):
    opener = gzip.open if name.endswith(".gz") else open
    with opener(D / name, "wt", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerows(data)
