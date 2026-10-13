"""S14 of docs/supplementary_plan_s14.md v1.0. Usage: s14_beyond_form.py RAW_AUDIT_DIR BASELINE_DIR TURNER_FLAGS_CSV_GZ  (.venv/bin/python)

Same items and folds as S2. Adds meaning features (definition lines), stored Turner flags and group weights to the
baseline models and reports accuracy by subset. Writes s14_scores.csv, s14_by_subset.csv, s14_oof.csv.gz. Validates no label.
"""
import csv, gzip, json, math, re, sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import assertions_with_forms, ety_sections, ety_text, from_ancestor
from baseline_norm import normalise

RAW, D, FLAGS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
SEED = 20261011
SKT = ["Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi"]
LAT = ["Catalan", "French", "Galician", "Italian", "Portuguese", "Romanian", "Spanish"]
FAMILY = {**{l: "Sanskrit" for l in SKT}, **{l: "Latin" for l in LAT}}


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


def meaning(chunk):
    out = ["pos_" + re.sub(r"\W+", "_", h.strip().lower()) for h in re.findall(r"^=+\s*([^=\n]+?)\s*=+\s*$", chunk, re.M)
           if not re.match(r"(Etymology|Pronunciation|References|Further reading|Alternative forms|See also|Anagrams|Declension|Conjugation|Inflection|Derived terms|Related terms|Descendants|Synonyms|Antonyms|Usage notes|Coordinate terms|Quotations|Notes|Gallery|Collocations|Hypernyms|Hyponyms|Translations)", h.strip())]
    for line in chunk.split("\n"):
        if not line.startswith("# "):
            continue
        t = line[2:]
        for _ in range(4):
            t = re.sub(r"\{\{[^{}]*\}\}", " ", t)
        t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)
        t = re.sub(r"<[^>]*>|'{2,}", " ", t)
        out.append(t.lower())
    return " ".join(out)


sections = {}
with gzip.open(RAW / "sections.jsonl.gz", "rt", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        sections[d["title"]] = d["sections"]
gloss = {}
for s in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")):
    L, code, title = s["lang"], s["ancestor_code"], s["title"]
    if L not in FAMILY:
        continue
    for chunk in ety_sections(sections[title][L]):
        tri = [(r, form) for r, src, form in assertions_with_forms(ety_text(chunk)) if from_ancestor(src, code) and r in ("INH", "LRN", "SEMI")]
        kinds = {r for r, _ in tri}
        if len(kinds) != 1:
            continue
        e = normalise(next((f for _, f in tri if normalise(f)), ""))
        gloss.setdefault((L, title, e, next(iter(kinds))), meaning(chunk))
flags = {(r["lang"], r["title"], r["wiktionary_route"]): [int(r["T1"]), int(r["T2"]), int(r["T3"])]
         for r in csv.DictReader(gzip.open(FLAGS, "rt", encoding="utf-8"))}
items = [r for r in csv.DictReader(gzip.open(D / "items.csv.gz", "rt", encoding="utf-8"))
         if r["wiktionary_route"] in ("INH", "LRN") and r["lang"] in FAMILY]
missing = sum((r["lang"], r["title"], r["etymon_norm"], r["wiktionary_route"]) not in gloss for r in items)
empty = sum(not gloss.get((r["lang"], r["title"], r["etymon_norm"], r["wiktionary_route"]), "").replace("pos_", "").strip() for r in items)
print(len(items), "items; no chunk found for", missing, "; empty meaning text for", empty, flush=True)

COND = ["B2", "B3", "M", "B2+M", "B3+M", "B3+W", "B3+M+W", "B3+T", "B3+M+T+W"]
oof = []
for L in SKT + LAT:
    rows = [r for r in items if r["lang"] == L]
    y = np.array([r["wiktionary_route"] == "LRN" for r in rows])
    dist = np.array([[float(r["norm_edit_distance"])] for r in rows])
    band = np.where(dist[:, 0] <= 0.15, 0, np.where(dist[:, 0] >= 0.5, 2, 1))
    grp = y.astype(int) * 3 + band
    g = [gloss.get((r["lang"], r["title"], r["etymon_norm"], r["wiktionary_route"]), "") for r in rows]
    T = np.array([flags.get((r["lang"], r["title"], r["wiktionary_route"]), [0, 0, 0]) for r in rows], dtype=float)
    T = np.hstack([T, (T[:, 2:3] * (dist <= 0.15))])
    conds = [c for c in COND if "T" not in c.split("+") or L in SKT]
    pred = {c: np.zeros(len(rows), dtype=bool) for c in conds}
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=SEED).split(rows, y):
        vw = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([rows[i]["word_norm"] for i in tr])
        ve = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)).fit([rows[i]["etymon_norm"] for i in tr])
        vm = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), token_pattern=r"(?u)\b\w+\b").fit([g[i] for i in tr])
        part = {"B2": lambda idx: [vw.transform([rows[i]["word_norm"] for i in idx])],
                "B3": lambda idx: [vw.transform([rows[i]["word_norm"] for i in idx]), ve.transform([rows[i]["etymon_norm"] for i in idx]), csr_matrix(dist[idx])],
                "M": lambda idx: [vm.transform([g[i] for i in idx])],
                "T": lambda idx: [csr_matrix(T[idx])]}
        cnt = Counter(grp[tr])
        w = np.array([1.0 / cnt[k] for k in grp[tr]])
        w = w / w.mean()
        for c in conds:
            names = [p for p in c.split("+") if p != "W"]
            X = lambda idx: hstack([m for p in names for m in part[p](idx)]).tocsr()
            m = LogisticRegression(max_iter=1000, random_state=SEED).fit(X(tr), y[tr], sample_weight=w if "W" in c.split("+") else None)
            pred[c][te] = m.predict(X(te))
    for i, r in enumerate(rows):
        oof.append({"lang": L, "family": FAMILY[L], "title": r["title"], "wiktionary_route": r["wiktionary_route"],
                    "subset": subset(dist[i, 0], not y[i]), **{c: (int(pred[c][i]) if c in pred else "") for c in COND}})
    print(L, {c: round(f1_score(y, pred[c], average="macro"), 3) for c in conds}, flush=True)

with gzip.open(D / "s14_oof.csv.gz", "wt", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(oof[0]))
    w.writeheader()
    w.writerows(oof)
scores, by = [], []
for scope in ["Sanskrit", "Latin"] + SKT + LAT:
    R = [r for r in oof if scope in (r["family"], r["lang"])]
    for c in COND:
        if R[0][c] == "":
            continue
        y = np.array([r["wiktionary_route"] == "LRN" for r in R])
        p = np.array([bool(r[c]) for r in R])
        if scope in ("Sanskrit", "Latin"):
            f1 = float(np.mean([f1_score(y[[i for i, r in enumerate(R) if r["lang"] == l]], p[[i for i, r in enumerate(R) if r["lang"] == l]], average="macro")
                                for l in sorted({r["lang"] for r in R})]))
        else:
            f1 = f1_score(y, p, average="macro")
        scores.append([scope, c, len(R), round(f1, 4)])
        for sub in ("congruent", "middle", "dissociated"):
            for route in ("both", "INH", "LRN"):
                idx = [i for i, r in enumerate(R) if r["subset"] == sub and route in ("both", r["wiktionary_route"])]
                k = int((p[idx] == y[idx]).sum())
                by.append([scope, c, sub, route, k, len(idx), round(k / len(idx), 4) if idx else "", *wilson(k, len(idx))])
for name, head, data in (("s14_scores.csv", ["scope", "condition", "items", "macro_f1"], scores),
                         ("s14_by_subset.csv", ["scope", "condition", "subset", "route", "correct", "n", "accuracy", "ci95_low", "ci95_high"], by)):
    with open(D / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerows(data)
for b in by:
    if b[0] in ("Sanskrit", "Latin") and (b[2] == "dissociated" or b[3] == "both"):
        print(*b)
for s in scores:
    if s[0] in ("Sanskrit", "Latin"):
        print("macro-F1 (mean over languages)", *s)
