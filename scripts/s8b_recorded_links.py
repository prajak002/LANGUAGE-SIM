"""S8b of docs/supplementary_plan_s8.md v1.0. Usage: s8b_recorded_links.py RAW_AUDIT_DIR OUT_DIR

The intermediate-stage forms that Wiktionary itself records, and the fixed three-way split. Uses Wiktionary only.
Measures whether an entry is consistent with itself; supports no label.
"""
import csv, gzip, json, math, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import assertions_with_forms, ety_sections, ety_text, from_ancestor  # noqa: E402

RAW, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
INDIC_TO_DEVA = [(0x0980, 0x09FF), (0x0A00, 0x0A7F), (0x0A80, 0x0AFF), (0x0B00, 0x0B7F)]
FIXED = {"fro", "frm", "osp", "roa-opt", "roa-oca", "roa-oit", "gkm", "axm", "pi", "omr"}
INDO_ARYAN = {"Sanskrit"}


def is_link(src):
    return src in FIXED or src.startswith("pra") or (src.startswith("inc-") and src != "inc-pro")


def normalise(s):  # unchanged from scripts/baseline.py
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


def ned(a, b):  # unchanged from scripts/baseline.py
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


def subset(d, inh):
    if (inh and d >= 0.5) or (not inh and d <= 0.15):
        return "congruent"
    if (inh and d <= 0.15) or (not inh and d >= 0.5):
        return "dissociated"
    return "middle"


sections = {}
with gzip.open(RAW / "sections.jsonl.gz", "rt", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        sections[d["title"]] = d["sections"]
CATS = ["link unchanged", "through the link", "skips the link"]
seen, done, cnt, cov, skipped_script, out = set(), set(), defaultdict(Counter), defaultdict(Counter), Counter(), []
for s in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")):
    L, A, code, title = s["lang"], s["ancestor"], s["ancestor_code"], s["title"]
    if (L, title) in seen or L == "Urdu":
        continue
    seen.add((L, title))
    for chunk in ety_sections(sections[title][L]):
        allt = assertions_with_forms(ety_text(chunk))
        tri = [(r, form) for r, src, form in allt if from_ancestor(src, code) and r in ("INH", "LRN", "SEMI")]
        kinds = {r for r, _ in tri}
        if len(kinds) != 1 or kinds & {"SEMI"}:
            continue
        w, e, route = normalise(title), normalise(next((f for _, f in tri if normalise(f)), "")), next(iter(kinds))
        if not w or not e or (L, title, w, e, route) in done:
            continue
        done.add((L, title, w, e, route))
        dwa = ned(w, e)
        sub = subset(round(dwa, 4), route == "INH")
        links = []
        for _, src, form in allt:
            m = normalise(form)
            if not is_link(src) or not m:
                continue
            if A in INDO_ARYAN and not all(0x0900 <= ord(ch) <= 0x097F for ch in m):
                skipped_script[L] += 1
                continue
            links.append(m)
        for fam in (A, A + " | " + L):
            cov[(fam, route, sub)]["items"] += 1
            cov[(fam, route, sub)]["linked"] += bool(links)
        if not links:
            continue
        m = min(sorted(set(links)), key=lambda x: ned(w, x))
        dwm, dam = ned(w, m), ned(e, m)
        cat = "link unchanged" if dam <= 0.15 else ("through the link" if dwm < dwa else "skips the link")
        for fam in (A, A + " | " + L):
            cnt[(fam, route, sub)][cat] += 1
            cnt[(fam, route, "all subsets")][cat] += 1
        out.append([L, title, route, sub, round(dwa, 4), round(dwm, 4), round(dam, 4), cat])
print("Indo-Aryan intermediate forms skipped for script:", dict(skipped_script))
with open(OUT / "s8b_split.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["family_or_language", "wiktionary_route", "subset", "items", "linked_items"] + [x for c in CATS for x in (c, c + " share", c + " low", c + " high")])
    for (fam, route, sub), k in sorted(cnt.items()):
        n = sum(k.values())
        items = cov[(fam, route, sub)]["items"] if sub != "all subsets" else sum(v["items"] for (f2, r2, _), v in cov.items() if f2 == fam and r2 == route)
        wr.writerow([fam, route, sub, items, n] + [x for c in CATS for x in (k[c], round(k[c] / n, 4), *wilson(k[c], n))])
        if " | " not in fam:
            print(fam.ljust(14), route, sub.ljust(11), f"linked {n:4} of {items:4} ", "  ".join(f"{c}: {k[c]} ({100 * k[c] / n:.0f}%)" for c in CATS))
with gzip.open(OUT / "s8b_items.csv.gz", "wt", encoding="utf-8", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["lang", "title", "wiktionary_route", "subset", "d_word_ancestor", "d_word_link", "d_ancestor_link", "category"])
    wr.writerows(out)
