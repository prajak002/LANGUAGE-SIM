"""S10 of docs/supplementary_plan_s10.md v1.0. Usage: s10_three_conditions.py JAMBU_FORMS_CSV JAMBU_EDGES_CSV BASELINE_DIR OUT_DIR

Reads a temporary copy of Jambu's forms (not stored in this repository). Writes counts and, per item, three
distances and a category; no Turner form is written. Validates no label.
"""
import csv, gzip, math, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedGroupKFold

FORMS, EDGES, B, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
ALL_MIA = len(sys.argv) > 5 and sys.argv[5] == "all-mia"
TAG = "_all_mia" if ALL_MIA else ""
OUT.mkdir(parents=True, exist_ok=True)
csv.field_size_limit(10 ** 9)
SEED = 20261011
SKT = ["Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi"]
LINK = {"Pa", "Pk"} | ({"Ap", "As", "Dhp", "jmag", "jmh", "KharI", "MIA", "NiDoc", "OMIA"} if ALL_MIA else set())
CONS = dict(zip("कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ",
                ["k", "kh", "g", "gh", "ṅ", "c", "ch", "j", "jh", "ñ", "ṭ", "ṭh", "ḍ", "ḍh", "ṇ", "t", "th", "d", "dh", "n",
                 "p", "ph", "b", "bh", "m", "y", "r", "l", "v", "ś", "ṣ", "s", "h", "ḷ"]))
VOW = dict(zip("अआइईउऊऋॠएऐओऔ", ["a", "ā", "i", "ī", "u", "ū", "r̥", "r̥̄", "e", "ai", "o", "au"]))
SIGN = dict(zip("ािीुूृॄेैोौ", ["ā", "i", "ī", "u", "ū", "r̥", "r̥̄", "e", "ai", "o", "au"]))


def translit(s):
    out, i = [], 0
    s = unicodedata.normalize("NFC", s).replace("़", "")
    while i < len(s):
        c = s[i]
        if c in CONS:
            out.append(CONS[c])
            nxt = s[i + 1] if i + 1 < len(s) else ""
            if nxt == "्":
                i += 1
            elif nxt in SIGN:
                out.append(SIGN[nxt])
                i += 1
            else:
                out.append("a")
        elif c in VOW:
            out.append(VOW[c])
        elif c in "ंँ":
            out.append("ṁ")
        elif c == "ः":
            out.append("ḥ")
        i += 1
    return "".join(out)


def norm(latin):
    s = latin.lower().replace("ṁ", "n").replace("ṃ", "n").replace("m̐", "n")
    s = "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn")
    s = re.sub(r"[^a-z]", "", s.replace("ʰ", "h"))
    return re.sub(r"[nm](?=[kgcjtdpb])", "n", s)


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
    if not n:
        return "", ""
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


article_of = defaultdict(set)
for e in csv.DictReader(open(EDGES, encoding="utf-8")):
    if e["Kind"] == "reflex" and e["Child_ID"].startswith("f_"):
        article_of[e["Child_ID"]].add(e["Parent_ID"])
head, mia = defaultdict(set), defaultdict(set)
for r in csv.DictReader(open(FORMS, encoding="utf-8")):
    if not r["Source"].startswith("CDIAL"):
        continue
    if r["Language_ID"] == "Indo-Aryan":
        for hw in re.split(r"[,;]", r["Original"] or r["Form"]):
            if norm(hw):
                head[norm(hw)].add(r["ID"])
    elif r["Language_ID"] in LINK:
        for f in re.split(r"[,;]", r["Original"] or r["Form"]):
            if norm(f):
                for entry in article_of.get(r["ID"], ()):
                    mia[entry].add(norm(f))
print("link languages:", sorted(LINK), "| head-word keys:", len(head), "| articles with a link form:", len(mia))

sub = {(r["lang"], r["title"], r["wiktionary_route"]): r["subset"] for r in csv.DictReader(gzip.open(B / "oof_predictions.csv.gz", "rt", encoding="utf-8"))}
rows, cov = [], defaultdict(Counter)
for r in csv.DictReader(gzip.open(B / "items.csv.gz", "rt", encoding="utf-8")):
    if r["lang"] not in SKT or r["wiktionary_route"] not in ("INH", "LRN"):
        continue
    w, a = norm(translit(r["word_norm"])), norm(translit(r["etymon_norm"]))
    arts = head.get(a, set())
    forms = set().union(*(mia[x] for x in arts if x in mia)) if arts else set()
    s = sub[(r["lang"], r["title"], r["wiktionary_route"])]
    for L in (r["lang"], "ALL"):
        k = cov[(L, r["wiktionary_route"], s)]
        k["items"] += 1
        k["T1"] += bool(arts)
        k["linked"] += bool(forms and w)
    if not forms or not w:
        continue
    m = min(sorted(forms), key=lambda f: ned(w, f))
    dwa, dwm, dam = ned(w, a), ned(w, m), ned(a, m)
    cat = "link unchanged" if dam <= 0.15 else ("through the link" if dwm < dwa else "skips the link")
    rows.append({**r, "subset": s, "dwa": dwa, "dwm": dwm, "dam": dam, "cat": cat, "link": m})
print("linked items:", len(rows))

TFIDF = lambda: TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3))
pred_all = []
for L in SKT:
    R = [r for r in rows if r["lang"] == L]
    y = np.array([r["wiktionary_route"] == "LRN" for r in R])
    bd = np.array([[float(r["norm_edit_distance"])] for r in R])
    ld = np.array([[r["dwm"], r["dam"]] for r in R])
    pred = {m: np.zeros(len(R), dtype=bool) for m in ("A0", "A1", "A2")}
    for tr, te in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(R, y, [r["etymon_norm"] for r in R]):
        vw, ve, vl = (TFIDF().fit([R[i][k] for i in tr]) for k in ("word_norm", "etymon_norm", "link"))
        W = lambda i: vw.transform([R[j]["word_norm"] for j in i])
        E = lambda i: ve.transform([R[j]["etymon_norm"] for j in i])
        K = lambda i: vl.transform([R[j]["link"] for j in i])
        X = {"A0": W, "A1": lambda i: hstack([W(i), E(i), csr_matrix(bd[i])]).tocsr(),
             "A2": lambda i: hstack([W(i), E(i), csr_matrix(bd[i]), K(i), csr_matrix(ld[i])]).tocsr()}
        for m in pred:
            pred[m][te] = LogisticRegression(max_iter=1000, random_state=SEED).fit(X[m](tr), y[tr]).predict(X[m](te))
    for i, r in enumerate(R):
        pred_all.append((L, r["subset"], bool(y[i]), {m: bool(pred[m][i]) for m in pred}))
with open(OUT / "s10_scores.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "condition", "items", "inherited", "learned", "macro_f1", "f1_inherited", "f1_learned"])
    for L in ["ALL"] + SKT:
        P = [p for p in pred_all if L in ("ALL", p[0])]
        yy = np.array([p[2] for p in P])
        for m in ("A0", "A1", "A2"):
            pp = np.array([p[3][m] for p in P])
            row = [L, m, len(P), int((~yy).sum()), int(yy.sum()), round(f1_score(yy, pp, average="macro"), 4),
                   round(f1_score(~yy, ~pp), 4), round(f1_score(yy, pp), 4)]
            wr.writerow(row)
            if L == "ALL":
                print("F1", *row)
with open(OUT / "s10_by_subset.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "subset", "route", "condition", "n", "correct", "accuracy", "ci95_low", "ci95_high"])
    for L in ["ALL"] + SKT:
        for sub in ("congruent", "middle", "dissociated"):
            for route in ("both", "INH", "LRN"):
                P = [p for p in pred_all if L in ("ALL", p[0]) and p[1] == sub and (route == "both" or p[2] == (route == "LRN"))]
                if not P:
                    continue
                for m in ("A0", "A1", "A2"):
                    k = sum(p[3][m] == p[2] for p in P)
                    wr.writerow([L, sub, route, m, len(P), k, round(k / len(P), 4), *wilson(k, len(P))])
                    if L == "ALL":
                        print(sub.ljust(11), route.ljust(4), m, f"{k}/{len(P)} = {100 * k / len(P):.1f}%", wilson(k, len(P)))
