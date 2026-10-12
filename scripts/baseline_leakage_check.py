"""Robustness check added after the planned baseline run (not in docs/baseline_plan.md v1.0).

Usage: baseline_leakage_check.py ITEMS_CSV_GZ OUT_CSV   (run with .venv/bin/python)
Question: do the cross-validation scores depend on the same etymon, or the same word, falling in both
the training and the test fold? Repeats A1 for B1 and B3 with folds grouped by etymon, so that all items
sharing an ancestor form stay together, and reports how many items share an etymon or a word.
"""
import csv, gzip, sys
from collections import Counter

import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold

SEED = 20261011
items = [r for r in csv.DictReader(gzip.open(sys.argv[1], "rt", encoding="utf-8")) if r["wiktionary_route"] in ("INH", "LRN")]
out = []
for L in sorted({r["lang"] for r in items}):
    rows = [r for r in items if r["lang"] == L]
    y = np.array([r["wiktionary_route"] == "LRN" for r in rows])
    ety, word = Counter(r["etymon_norm"] for r in rows), Counter(r["word_norm"] for r in rows)
    share_e = sum(ety[r["etymon_norm"]] > 1 for r in rows) / len(rows)
    share_w = sum(word[r["word_norm"]] > 1 for r in rows) / len(rows)
    d = np.array([[float(r["norm_edit_distance"])] for r in rows])
    res = {}
    for name, splitter, groups in (("plain", StratifiedKFold(5, shuffle=True, random_state=SEED), None),
                                   ("grouped", StratifiedGroupKFold(5, shuffle=True, random_state=SEED), [r["etymon_norm"] for r in rows])):
        for m in ("B1", "B3"):
            f1 = []
            for tr, te in splitter.split(rows, y, groups):
                if m == "B1":
                    Xtr, Xte = d[tr], d[te]
                else:
                    vw = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([rows[i]["word_norm"] for i in tr])
                    ve = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([rows[i]["etymon_norm"] for i in tr])
                    X = lambda idx: hstack([vw.transform([rows[i]["word_norm"] for i in idx]), ve.transform([rows[i]["etymon_norm"] for i in idx]), csr_matrix(d[idx])]).tocsr()
                    Xtr, Xte = X(tr), X(te)
                p = LogisticRegression(max_iter=1000, random_state=SEED).fit(Xtr, y[tr]).predict(Xte)
                f1.append(f1_score(y[te], p, average="macro", zero_division=0))
            res[(name, m)] = round(float(np.mean(f1)), 4)
    out.append([L, len(rows), round(share_e, 4), round(share_w, 4), res[("plain", "B1")], res[("grouped", "B1")], res[("plain", "B3")], res[("grouped", "B3")]])
with open(sys.argv[2], "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lang", "n_items", "share_items_sharing_an_etymon", "share_items_sharing_a_word", "B1_plain", "B1_grouped_by_etymon", "B3_plain", "B3_grouped_by_etymon"])
    w.writerows(out)
