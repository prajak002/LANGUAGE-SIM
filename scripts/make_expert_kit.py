"""Blind sheets for human annotation and for manual dictionary lookups. Usage: make_expert_kit.py RAW_DIR OUT_DIR

Draws from the audit sample only (no fetch). Order and choice are fixed by a keyed hash. The Wiktionary
route goes to a sealed key file; the sheets show the word and a gloss and nothing else from Wiktionary.
"""
import csv, gzip, hashlib, json, os, re, sys, urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import assertions_with_forms, ety_sections, ety_text, from_ancestor  # noqa: E402

RAW, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
SEED = "expert-kit-v1-2026-10-11"
PER_ROUTE = {"Hindi": 30, "Bengali": 30, "Romanian": 30, "French": 30}
LOOKUP = {"Romanian": "https://dexonline.ro/definitie/{}", "French": "https://www.cnrtl.fr/etymologie/{}"}
FORM_OF = re.compile(r"\{\{([^{}|]*(?: of|form))\|[a-z-]+\|([^{}|]+)[^{}]*\}\}")


def clean(defn):
    s = re.sub(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>|<!--.*?-->", "", defn)
    s = FORM_OF.sub(lambda m: f"{m.group(1)} {m.group(2)}", s)
    s = re.sub(r"\{\{(?:l|m|link|mention)\|[a-z-]+\|([^{}|]+)[^{}]*\}\}", r"\1", s)
    s = re.sub(r"\{\{(?:gloss|gl|non-gloss|ng|n-g)\|([^{}|]+)[^{}]*\}\}", r"\1", s)
    while re.search(r"\{\{[^{}]*\}\}", s):
        s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", s)
    return re.sub(r"\s+", " ", re.sub(r"'{2,}", "", s)).strip(" ;,:")[:80]


def gloss(chunk):
    out = [g for line in chunk.splitlines() if re.match(r"^#(?![:*#])", line) for g in [clean(line[1:])] if g][:2]
    return "; ".join(out) or "(no definition line)"


sections = {}
with gzip.open(RAW / "sections.jsonl.gz", "rt", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        sections[d["title"]] = d
pool, seen = {}, set()
for s in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")):
    L, code, t = s["lang"], s["ancestor_code"], s["title"]
    if L not in PER_ROUTE or (L, t) in seen:
        continue
    seen.add((L, t))
    for i, chunk in enumerate(ety_sections(sections[t]["sections"][L]), 1):
        kinds = {r for r, src, _ in assertions_with_forms(ety_text(chunk)) if from_ancestor(src, code) and r in ("INH", "LRN", "SEMI")}
        if len(kinds) == 1:
            iid = hashlib.sha256(f"{SEED}|{L}|{t}|{i}".encode()).hexdigest()[:10]
            pool.setdefault((L, kinds.pop()), []).append((iid, t, i, gloss(chunk), sections[t]["revid"]))
for L, n in PER_ROUTE.items():
    chosen = [(iid, t, i, g, rev, r) for r in ("INH", "LRN", "SEMI") for iid, t, i, g, rev in sorted(pool.get((L, r), []))[:n]]
    chosen.sort()  # hash order mixes the routes
    manual = L in LOOKUP
    cols = ["item_id", "lang", "word", "gloss"] + (["lookup_url", "etymology_marker_as_printed", "label", "notes"] if manual
                                                    else ["label", "confidence", "sources_consulted", "notes"])
    for who in ("A", "B"):
        with open(OUT / f"{L.lower()}_annotator_{who}.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for iid, t, i, g, rev, r in chosen:
                w.writerow([iid, L, t, g] + ([LOOKUP[L].format(urllib.parse.quote(t)), "", "", ""] if manual else ["", "", "", ""]))
    key = OUT / f"_sealed_key_{L.lower()}.csv"
    if key.exists():
        os.chmod(key, 0o644)
    with open(key, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "word", "ety_index", "revid", "wiktionary_route"])
        w.writerows([iid, t, i, rev, r] for iid, t, i, g, rev, r in chosen)
    os.chmod(key, 0o444)
    print(L, len(chosen), "items")  # counts only: routes stay in the sealed key
