"""S6 of docs/supplementary_plan_s6.md v1.0. Usage: wold_romanian.py WOLD_FORMS WOLD_BORROWINGS AUDIT_RAW BASELINE_DIR STORE_DIR OUT_DIR"""
import csv, gzip, json, math, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

FORMS, BORR, RAW, BASE, STORE, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5]), Path(sys.argv[6])
STORE.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
csv.field_size_limit(10 ** 9)


def wilson(k, n):
    if not n:
        return "", ""
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


def norm(s):
    s = unicodedata.normalize("NFC", s.strip().lower())
    return s.replace("ş", "ș").replace("ţ", "ț")


def variants(value):
    v = re.sub(r"\([^)]*\)|\[[^\]]*\]", "", value)
    return {norm(re.sub(r"^a\s+", "", p.strip())) for p in re.split(r"[,;/]", v) if p.strip()}


donors = defaultdict(set)
for b in csv.DictReader(open(BORR, encoding="utf-8")):
    donors[b["Target_Form_ID"]].add(b["Source_languoid"])
entries, status_seen = [], Counter()
for r in csv.DictReader(open(FORMS, encoding="utf-8")):
    if r["Language_ID"] != "Romanian":
        continue
    status_seen[r["Borrowed"]] += 1
    m = re.match(r"\s*([1-5])", r["Borrowed"] or "")
    st = {"1": "borrowed", "2": "borrowed", "3": "uncertain", "4": "not borrowed", "5": "not borrowed"}.get(m.group(1) if m else "", "missing")
    entries.append({"id": r["ID"], "value": r["Value"], "status": st, "borrowed_raw": r["Borrowed"], "donors": sorted(donors.get(r["ID"], ()))})
print(len(entries), "Romanian entries; status values:", dict(status_seen))
with open(STORE / "romanian_entries.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["wold_form_id", "value", "borrowed_status", "donor_languoids"])
    w.writerows([e["id"], e["value"], e["borrowed_raw"], "; ".join(e["donors"])] for e in entries)
(STORE / "README.md").write_text(
    "# Romanian rows of the World Loanword Database\n\nSource: Kim Schulte. 2009. Romanian vocabulary. In: Haspelmath, Martin & Tadmor, Uri (eds.) "
    "World Loanword Database. Leipzig: Max Planck Institute for Evolutionary Anthropology. CLDF edition: https://github.com/lexibank/wold "
    "(CC BY 4.0, https://creativecommons.org/licenses/by/4.0/). Only the form, the borrowed status and the donor languoids are kept here.\n", encoding="utf-8")

by_word = defaultdict(list)
for e in entries:
    for v in variants(e["value"]):
        by_word[v].append(e)


def expert(word):
    es = by_word.get(norm(word))
    if not es:
        return None
    if all(e["status"] == "not borrowed" for e in es):
        return "NB"
    if all(e["status"] == "borrowed" for e in es):
        lat = [any("latin" in d.lower() for d in e["donors"]) for e in es]
        if all(lat):
            return "BL"
        if not any(lat):
            return "BO"
    return "MIX"


# ---- V1
cats = {}
for c, name in (("LRN", "Romanian_learned_borrowings_from_Latin"), ("SEMI", "Romanian_semi-learned_borrowings_from_Latin"), ("INH", "Romanian_terms_inherited_from_Latin")):
    with gzip.open(RAW / "members" / (name + ".jsonl.gz"), "rt", encoding="utf-8") as f:
        cats[c] = {m["title"] for line in f for m in json.loads(line)["query"]["categorymembers"]}
multi = {t for t in set().union(*cats.values()) if sum(t in s for s in cats.values()) > 1}
tab, found = Counter(), Counter()
for c, titles in cats.items():
    for t in titles - multi:
        x = expert(t)
        if x:
            tab[(c, x)] += 1
            found[c] += 1
rows = [["wiktionary_category", "titles", "found_in_wold", "NB", "BL", "BO", "MIX"]]
for c in ("INH", "LRN", "SEMI"):
    rows.append([c, len(cats[c] - multi), found[c], *(tab[(c, x)] for x in ("NB", "BL", "BO", "MIX"))])
rows.append(["in two categories", len(multi), sum(bool(expert(t)) for t in multi), *(sum(expert(t) == x for t in multi) for x in ("NB", "BL", "BO", "MIX"))])
with open(OUT / "v1_crosstab.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(rows)
for r in rows:
    print(r)
key = [("inherited category: expert says not borrowed", tab[("INH", "NB")], found["INH"]),
       ("learned category: expert says borrowed, Latin named", tab[("LRN", "BL")], found["LRN"]),
       ("learned category: expert says borrowed, Latin not named", tab[("LRN", "BO")], found["LRN"]),
       ("learned category: expert says not borrowed", tab[("LRN", "NB")], found["LRN"]),
       ("inherited category: expert says borrowed (BL or BO)", tab[("INH", "BL")] + tab[("INH", "BO")], found["INH"])]
with open(OUT / "v1_shares.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["measure", "k", "n", "share", "ci95_low", "ci95_high"])
    for name, k, n in key:
        w.writerow([name, k, n, round(k / n, 4) if n else "", *wilson(k, n)])
        print(f"{name}: {k}/{n}", wilson(k, n))
donor_lrn = Counter(d for t in cats["LRN"] - multi if expert(t) == "BO" for e in by_word[norm(t)] for d in e["donors"])
print("donors named for learned-category words where Latin is not named:", donor_lrn.most_common(6))

# ---- V2
v2, detail = Counter(), []
for r in csv.DictReader(gzip.open(BASE / "oof_predictions.csv.gz", "rt", encoding="utf-8")):
    if r["lang"] != "Romanian":
        continue
    x = expert(r["title"])
    if x not in ("NB", "BL"):
        v2[("not usable", x or "not in WOLD")] += 1
        continue
    gold = "LRN" if x == "BL" else "INH"
    pred = "LRN" if r["B3_learned"] == "1" else "INH"
    v2[(r["subset"], "n")] += 1
    v2[(r["subset"], "B3 = expert")] += pred == gold
    v2[(r["subset"], "Wiktionary = expert")] += r["wiktionary_route"] == gold
    detail.append([r["title"], r["wiktionary_route"], x, pred, r["subset"], r["norm_edit_distance"]])
with open(OUT / "v2_baseline_vs_expert.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["title", "wiktionary_route", "expert_class", "B3_prediction", "subset", "norm_edit_distance"])
    w.writerows(detail)
for k, v in sorted(v2.items()):
    print(k, v)
