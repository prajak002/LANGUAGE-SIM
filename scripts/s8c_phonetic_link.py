"""S8c of docs/supplementary_plan_s8c.md v1.0 (S8a with a phonetic distance). Usage: s8c_phonetic_link.py JAMBU_FORMS_CSV JAMBU_EDGES_CSV BASELINE_DIR OUT_DIR [all-mia]

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
from sklearn.model_selection import StratifiedKFold

FORMS, EDGES, B, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
ALL_MIA = len(sys.argv) > 5 and sys.argv[5] == "all-mia"
UNIT = len(sys.argv) > 5 and sys.argv[5] == "unit-cost"
TAG = "_all_mia" if ALL_MIA else ""
PRE = "s8c_unit_cost" if UNIT else "s8c"
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


PLACE = {**dict.fromkeys("kgṅ", "velar"), **dict.fromkeys("cjñśy", "palatal"), **dict.fromkeys("ṭḍṇṣrḷ", "retroflex"),
         **dict.fromkeys("tdnsl", "dental"), **dict.fromkeys("pbmv", "labial"), "h": "glottal"}
MANNER = {**dict.fromkeys("kgcjṭḍtdpb", "stop"), **dict.fromkeys("ṅñṇnm", "nasal"), **dict.fromkeys("śṣs", "sibilant"),
          **dict.fromkeys("yrlvḷ", "glide"), "h": "h"}
VOICED = set("gjḍdbṅñṇnmyrlvḷh")
QUAL = {"a": "a", "ā": "a", "i": "i", "ī": "i", "u": "u", "ū": "u", "e": "e", "ē": "e", "o": "o", "ō": "o", "r̥": "r", "r̥̄": "r", "ai": "ai", "au": "au"}
LONG = {"ā", "ī", "ū", "ē", "ō", "r̥̄", "ai", "au", "e", "o"}
SEG = re.compile(r"[kgcjṭḍtdpb][hʰ]|ai|au|r̥̄|r̥|.[̀-ͯ]*")


def segments(latin):
    s = unicodedata.normalize("NFD", latin.lower())
    s = re.sub("(?<=[aeiou\u0304\u0325])[\u0301\u0300\u0302\u030c\u0306]", "", s)
    s = unicodedata.normalize("NFC", s).replace("ṃ", "ṁ").replace("m̐", "ṁ").replace("ḥ", "").replace("ṛ", "r̥").replace("ṝ", "r̥̄").replace("w", "v")
    out = []
    for m in SEG.findall(s):
        base = unicodedata.normalize("NFC", m)
        nasal = "̃" in unicodedata.normalize("NFD", base)
        plain = unicodedata.normalize("NFC", unicodedata.normalize("NFD", base).replace("̃", "")) if nasal and base != "ñ" else base
        if base == "ṁ":
            out.append(("C", "ṁ", "nasal", True, False))
        elif plain in QUAL:
            out.append(("V", QUAL[plain], plain in LONG, nasal))
        elif plain[0] in PLACE and plain.rstrip("hʰ") in PLACE or plain in PLACE:
            c = plain[0]
            out.append(("C", PLACE[c], MANNER[c], c in VOICED, len(plain) > 1))
        elif plain.isalpha():
            out.append(("?", plain))
    return out


def sub_cost(x, y):
    if x == y:
        return 0.0
    if x[0] != y[0] or x[0] == "?" or UNIT:
        return 1.0
    return sum(a != b for a, b in zip(x[1:], y[1:])) / (len(x) - 1)


def pdist(a, b):
    a, b = segments(a), segments(b)
    if not a or not b:
        return 1.0
    prev = [float(j) for j in range(len(b) + 1)]
    for i, x in enumerate(a, 1):
        cur = [float(i)]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + sub_cost(x, y)))
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
                    mia[entry].add(f.strip())
print("link languages:", sorted(LINK), "| head-word keys:", len(head), "| articles with a link form:", len(mia))

def subset_of(r):
    d, inh = float(r["norm_edit_distance"]), r["wiktionary_route"] == "INH"
    if (inh and d >= 0.5) or (not inh and d <= 0.15):
        return "congruent"
    if (inh and d <= 0.15) or (not inh and d >= 0.5):
        return "dissociated"
    return "middle"
rows, cov = [], defaultdict(Counter)
for r in csv.DictReader(gzip.open(B / "items.csv.gz", "rt", encoding="utf-8")):
    if r["lang"] not in SKT or r["wiktionary_route"] not in ("INH", "LRN"):
        continue
    w, a = translit(r["word_norm"]), translit(r["etymon_norm"])
    arts = head.get(norm(a), set())
    forms = set().union(*(mia[x] for x in arts if x in mia)) if arts else set()
    s = subset_of(r)
    for L in (r["lang"], "ALL"):
        k = cov[(L, r["wiktionary_route"], s)]
        k["items"] += 1
        k["T1"] += bool(arts)
        k["linked"] += bool(forms and segments(w))
    if not forms or not segments(w):
        continue
    m = min(sorted(forms), key=lambda f: pdist(w, f))
    dwa, dwm, dam = pdist(w, a), pdist(w, m), pdist(a, m)
    cat = "link unchanged" if dam <= 0.15 else ("through the link" if dwm < dwa else "skips the link")
    rows.append({**r, "subset": s, "dwa": dwa, "dwm": dwm, "dam": dam, "cat": cat})
print("linked items:", len(rows))
with open(OUT / f"{PRE}_coverage{TAG}.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "wiktionary_route", "subset", "items", "T1_etymon_matches_article", "linked_has_Pali_or_Prakrit_form", "linked_share"])
    for (L, route, s), k in sorted(cov.items()):
        wr.writerow([L, route, s, k["items"], k["T1"], k["linked"], round(k["linked"] / k["items"], 4)])

CATS = ["link unchanged", "through the link", "skips the link"]
a2 = defaultdict(Counter)
for r in rows:
    for L in (r["lang"], "ALL"):
        a2[(L, r["wiktionary_route"], r["subset"])][r["cat"]] += 1
        a2[(L, r["wiktionary_route"], "all subsets")][r["cat"]] += 1
with open(OUT / f"{PRE}_split{TAG}.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "wiktionary_route", "subset", "linked_items"] + [x for c in CATS for x in (c, c + " share", c + " low", c + " high")])
    for (L, route, s), k in sorted(a2.items()):
        n = sum(k.values())
        wr.writerow([L, route, s, n] + [x for c in CATS for x in (k[c], round(k[c] / n, 4), *wilson(k[c], n))])
        if L == "ALL":
            print("A2", route, s.ljust(11), f"n={n:4} ", "  ".join(f"{c}: {k[c]} ({100 * k[c] / n:.0f}%)" for c in CATS))

acc, f1rows, paired, skipped, preds = defaultdict(Counter), [], Counter(), [], []
for L in SKT:
    R = [r for r in rows if r["lang"] == L]
    y = np.array([r["wiktionary_route"] == "LRN" for r in R])
    if min(y.sum(), (~y).sum()) < 10:
        skipped.append((L, int((~y).sum()), int(y.sum())))
        continue
    D = np.array([[r["dwa"], r["dwm"], r["dam"]] for r in R])
    pred = {m: np.zeros(len(R), dtype=bool) for m in ("L0", "L1", "B3")}
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=SEED).split(R, y):
        vw = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([R[i]["word_norm"] for i in tr])
        ve = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([R[i]["etymon_norm"] for i in tr])
        bd = np.array([[float(r["norm_edit_distance"])] for r in R])
        X = {"L0": lambda i: D[i][:, :1], "L1": lambda i: D[i],
             "B3": lambda i: hstack([vw.transform([R[j]["word_norm"] for j in i]), ve.transform([R[j]["etymon_norm"] for j in i]), csr_matrix(bd[i])]).tocsr()}
        for m in pred:
            pred[m][te] = LogisticRegression(max_iter=1000, random_state=SEED).fit(X[m](tr), y[tr]).predict(X[m](te))
    f1rows.append([L, int((~y).sum()), int(y.sum())] + [round(f1_score(y, pred[m], average="macro"), 4) for m in ("L0", "L1", "B3")])
    for i, r in enumerate(R):
        for m in pred:
            for key in ((m, r["subset"], "both routes"), (m, r["subset"], r["wiktionary_route"])):
                acc[key]["n"] += 1
                acc[key]["ok"] += pred[m][i] == y[i]
        if r["subset"] == "dissociated":
            paired[(bool(pred["L1"][i] == y[i]), bool(pred["B3"][i] == y[i]))] += 1
        preds.append([L, r["title"], r["wiktionary_route"], r["subset"], round(r["dwa"], 4), round(r["dwm"], 4), round(r["dam"], 4), r["cat"],
                      *(int(pred[m][i]) for m in ("L0", "L1", "B3"))])
print("languages left out of A1 (fewer than 10 linked items of a route):", skipped)
with open(OUT / f"{PRE}_model{TAG}.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["model", "subset", "route", "n", "correct", "accuracy", "ci95_low", "ci95_high"])
    for (m, s, route), k in sorted(acc.items()):
        wr.writerow([m, s, route, k["n"], k["ok"], round(k["ok"] / k["n"], 4), *wilson(k["ok"], k["n"])])
        if route == "both routes":
            print("A1", m, s.ljust(11), f"{k['ok']}/{k['n']} = {100 * k['ok'] / k['n']:.1f}%  {wilson(k['ok'], k['n'])}")
    for (m, s, route), k in sorted(acc.items()):
        if s == "dissociated" and route != "both routes":
            print("A1", m, s, route, f"{k['ok']}/{k['n']}")
with open(OUT / f"{PRE}_macro_f1{TAG}.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "linked_inherited", "linked_learned", "L0_macro_f1", "L1_macro_f1", "B3_macro_f1"])
    wr.writerows(f1rows)
    for r in f1rows:
        print("F1", *r)
with open(OUT / f"{PRE}_paired_dissociated{TAG}.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["L1_correct", "B3_correct", "items"])
    wr.writerows([a, b, n] for (a, b), n in sorted(paired.items()))
print("paired on dissociated (L1 correct, B3 correct):", dict(paired))
with gzip.open(OUT / f"{PRE}_items{TAG}_NOT_FOR_RELEASE.csv.gz", "wt", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "title", "wiktionary_route", "subset", "d_word_ancestor", "d_word_link", "d_ancestor_link", "category", "L0_learned", "L1_learned", "B3_learned"])
    wr.writerows(preds)
