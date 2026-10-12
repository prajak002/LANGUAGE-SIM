"""S11 of docs/supplementary_plan_s11.md v1.0. Usage: s11_transformer.py JAMBU_FORMS_CSV JAMBU_EDGES_CSV BASELINE_DIR OUT_DIR [smoke]

Needs PyTorch; uses a GPU if one is present. Reads a temporary copy of Jambu's forms (not stored in this repository).
Writes counts and per-item probabilities; no Turner form is written. Validates no label. "smoke" runs one fold,
one seed and two epochs to check that the code runs, and writes nothing.
"""
import csv, gzip, math, re, sys, unicodedata
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from torch import nn
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedGroupKFold

FORMS, EDGES, B, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
SMOKE = len(sys.argv) > 5 and sys.argv[5] == "smoke"
csv.field_size_limit(10 ** 9)
SEED, SEEDS, EPOCHS, MAXLEN = 20261011, 5, 30, 96
SKT = ["Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi"]
LINK = {"Pa", "Pk"}
DEV = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
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


def fine(latin):
    """Transliteration with diacritics kept, as a list of base letters and combining marks."""
    s = unicodedata.normalize("NFD", latin.lower().replace("ʰ", "h"))
    return [ch for ch in s if ch.isalpha() or unicodedata.category(ch) == "Mn"]


article_of = defaultdict(set)
for e in csv.DictReader(open(EDGES, encoding="utf-8")):
    if e["Kind"] == "reflex" and e["Child_ID"].startswith("f_"):
        article_of[e["Child_ID"]].add(e["Parent_ID"])
head, mia = defaultdict(set), defaultdict(dict)
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
                    mia[entry].setdefault(norm(f), f)

sub = {(r["lang"], r["title"], r["wiktionary_route"]): r["subset"] for r in csv.DictReader(gzip.open(B / "oof_predictions.csv.gz", "rt", encoding="utf-8"))}
R = []
for r in csv.DictReader(gzip.open(B / "items.csv.gz", "rt", encoding="utf-8")):
    if r["lang"] not in SKT or r["wiktionary_route"] not in ("INH", "LRN"):
        continue
    tw, ta = translit(r["word_norm"]), translit(r["etymon_norm"])
    w, a = norm(tw), norm(ta)
    forms = {}
    for x in sorted(head.get(a, ())):
        for k, v in sorted(mia.get(x, {}).items()):
            forms.setdefault(k, v)
    if not forms or not w:
        continue
    m = min(sorted(forms), key=lambda f: ned(w, f))
    R.append({**r, "subset": sub[(r["lang"], r["title"], r["wiktionary_route"])], "link": m, "dwm": ned(w, m), "dam": ned(a, m),
              "fw": fine(tw), "fa": fine(ta), "fm": fine(forms[m])})
print("linked items:", len(R), "| device:", DEV, flush=True)
y = np.array([r["wiktionary_route"] == "LRN" for r in R])
strata = [f'{r["lang"]}|{r["wiktionary_route"]}' for r in R]
folds = list(StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(R, strata, [r["etymon_norm"] for r in R]))
for tr, te in folds:
    assert not {R[i]["etymon_norm"] for i in tr} & {R[i]["etymon_norm"] for i in te}
if SMOKE:
    folds, SEEDS, EPOCHS = folds[:1], 1, 2

TFIDF = lambda: TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3))
bd = np.array([[float(r["norm_edit_distance"])] for r in R])
ld = np.array([[r["dwm"], r["dam"]] for r in R])
prob = {m: np.full(len(R), np.nan) for m in ("A0", "A1", "A2", "T0", "T1", "T2")}
for tr, te in folds:
    vw, ve, vl = (TFIDF().fit([R[i][k] for i in tr]) for k in ("word_norm", "etymon_norm", "link"))
    W = lambda i: vw.transform([R[j]["word_norm"] for j in i])
    E = lambda i: ve.transform([R[j]["etymon_norm"] for j in i])
    K = lambda i: vl.transform([R[j]["link"] for j in i])
    X = {"A0": W, "A1": lambda i: hstack([W(i), E(i), csr_matrix(bd[i])]).tocsr(),
         "A2": lambda i: hstack([W(i), E(i), csr_matrix(bd[i]), K(i), csr_matrix(ld[i])]).tocsr()}
    for m in X:
        prob[m][te] = LogisticRegression(max_iter=1000, random_state=SEED).fit(X[m](tr), y[tr]).predict_proba(X[m](te))[:, 1]

PAD, CLS, SEP, UNK = 0, 1, 2, 3
PARTS = {"T0": ("fw",), "T1": ("fw", "fa"), "T2": ("fw", "fa", "fm")}


class Net(nn.Module):
    def __init__(self, vocab):
        super().__init__()
        self.tok, self.seg, self.pos = nn.Embedding(vocab, 128, padding_idx=PAD), nn.Embedding(3, 128), nn.Embedding(MAXLEN, 128)
        self.enc = nn.TransformerEncoder(nn.TransformerEncoderLayer(128, 4, 256, 0.1, batch_first=True), 3, enable_nested_tensor=False)
        self.out = nn.Linear(128, 1)

    def forward(self, ids, seg):
        x = self.tok(ids) + self.seg(seg) + self.pos(torch.arange(ids.shape[1], device=ids.device))
        return self.out(self.enc(x, src_key_padding_mask=ids == PAD)[:, 0]).squeeze(-1)


def encode(idx, cond, vocab):
    ids, seg = [], []
    for i in idx:
        t, s = [CLS, vocab.get("<" + R[i]["lang"] + ">", UNK)], [0, 0]
        for k, part in enumerate(PARTS[cond]):
            if k:
                t.append(SEP)
                s.append(k)
            t += [vocab.get(ch, UNK) for ch in R[i][part]]
            s += [k] * len(R[i][part])
        ids.append(t[:MAXLEN])
        seg.append(s[:MAXLEN])
    n = max(map(len, ids))
    pad = lambda rows: torch.tensor([row + [0] * (n - len(row)) for row in rows], device=DEV)
    return pad(ids), pad(seg)


seed_f1 = defaultdict(list)
for cond in PARTS:
    per_seed = np.full((SEEDS, len(R)), np.nan)
    for f, (tr, te) in enumerate(folds):
        chars = sorted({ch for i in tr for part in PARTS[cond] for ch in R[i][part]})
        vocab = {t: n + 4 for n, t in enumerate(["<" + L + ">" for L in SKT] + chars)}
        Xte, yt = encode(te, cond, vocab), torch.tensor(y[tr], dtype=torch.float32, device=DEV)
        for s in range(SEEDS):
            torch.manual_seed(SEED + s)
            order = np.random.default_rng(SEED + s)
            net = Net(len(vocab) + 4).to(DEV)
            opt = torch.optim.AdamW(net.parameters(), lr=1e-3, weight_decay=0.01)
            for _ in range(EPOCHS):
                net.train()
                perm = order.permutation(len(tr))
                for b in range(0, len(perm), 64):
                    pick = perm[b:b + 64]
                    loss = nn.functional.binary_cross_entropy_with_logits(net(*encode(tr[pick], cond, vocab)), yt[torch.as_tensor(pick, device=DEV)])
                    opt.zero_grad()
                    loss.backward()
                    nn.utils.clip_grad_norm_(net.parameters(), 1.0)
                    opt.step()
            net.eval()
            with torch.no_grad():
                per_seed[s, te] = torch.sigmoid(net(*Xte)).cpu().numpy()
            print(cond, "fold", f, "seed", s, "done", flush=True)
    prob[cond] = per_seed.mean(0)
    done = ~np.isnan(prob[cond])
    seed_f1[cond] = [f1_score(y[done], per_seed[s][done] >= 0.5, average="macro") for s in range(SEEDS)]
if SMOKE:
    print("smoke run finished; nothing written")
    sys.exit(0)

OUT.mkdir(parents=True, exist_ok=True)
MODELS = ("A0", "A1", "A2", "T0", "T1", "T2")
pred = {m: prob[m] >= 0.5 for m in MODELS}
lang, subset = np.array([r["lang"] for r in R]), np.array([r["subset"] for r in R])
with gzip.open(OUT / "s11_items_NOT_FOR_RELEASE.csv.gz", "wt", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "title", "wiktionary_route", "subset", *(m + "_p_learned" for m in MODELS)])
    wr.writerows([r["lang"], r["title"], r["wiktionary_route"], r["subset"], *(round(float(prob[m][i]), 4) for m in MODELS)] for i, r in enumerate(R))
with open(OUT / "s11_scores.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "condition", "items", "inherited", "learned", "macro_f1", "f1_inherited", "f1_learned", "seed_macro_f1_min", "seed_macro_f1_max"])
    for L in ["ALL"] + SKT:
        k = np.ones(len(R), bool) if L == "ALL" else lang == L
        for m in MODELS:
            rng = [round(min(seed_f1[m]), 4), round(max(seed_f1[m]), 4)] if L == "ALL" and m in seed_f1 else ["", ""]
            row = [L, m, int(k.sum()), int((~y[k]).sum()), int(y[k].sum()), round(f1_score(y[k], pred[m][k], average="macro"), 4),
                   round(f1_score(~y[k], ~pred[m][k]), 4), round(f1_score(y[k], pred[m][k]), 4), *rng]
            wr.writerow(row)
            if L == "ALL":
                print("F1", *row)
with open(OUT / "s11_by_subset.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "subset", "route", "condition", "n", "correct", "accuracy", "ci95_low", "ci95_high"])
    for L in ["ALL"] + SKT:
        for sb in ("congruent", "middle", "dissociated"):
            for route in ("both", "INH", "LRN"):
                k = (subset == sb) & (np.ones(len(R), bool) if L == "ALL" else lang == L) & (np.ones(len(R), bool) if route == "both" else y == (route == "LRN"))
                if not k.sum():
                    continue
                for m in MODELS:
                    c, n = int((pred[m][k] == y[k]).sum()), int(k.sum())
                    wr.writerow([L, sb, route, m, n, c, round(c / n, 4), *wilson(c, n)])
                    if L == "ALL":
                        print(sb.ljust(11), route.ljust(4), m, f"{c}/{n} = {100 * c / n:.1f}%", wilson(c, n))
with open(OUT / "s11_abstention.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["condition", "coverage", "kept", "accuracy_kept", "dissociated_total", "dissociated_kept", "dissociated_kept_correct"])
    dis = subset == "dissociated"
    for m in ("T1", "T2"):
        rank = np.argsort(-np.abs(prob[m] - 0.5), kind="stable")
        for cov in (1.0, 0.9, 0.8, 0.7, 0.5):
            keep = np.zeros(len(R), bool)
            keep[rank[:round(cov * len(R))]] = True
            ok = pred[m] == y
            row = [m, cov, int(keep.sum()), round(float(ok[keep].mean()), 4), int(dis.sum()), int((keep & dis).sum()), int((keep & dis & ok).sum())]
            wr.writerow(row)
            print("abstain", *row)
