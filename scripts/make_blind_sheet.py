"""Blind sheet with glosses per docs/evidence_extraction_protocol_v1.1.md §4'.

Usage: make_blind_sheet.py RAW_DIR OUT_DIR ROUND_TAG [--only-pilot PILOT_MAPPING | --exclude PILOT_MAPPING]

Writes OUT_DIR/blind_sheet.csv (item_id, lang, lemma, gloss) and a read-only
OUT_DIR/_sealed_mapping.csv. Prints only row counts: stratum, file names and
etymology text never reach stdout.
"""
import csv, hashlib, json, os, re, sys
from pathlib import Path

RAW, OUT, TAG = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
MODE, PILOT = (sys.argv[4], sys.argv[5]) if len(sys.argv) > 5 else (None, None)
LANGS = {"hi": "Hindi", "bn": "Bengali"}
FORM_OF = re.compile(r"\{\{([^{}|]*(?: of|form))\|[a-z-]+\|([^{}|]+)[^{}]*\}\}")


def lang_section(text, name):
    m = re.search(rf"^=={re.escape(name)}==\s*$", text, re.M)
    if not m:
        return ""
    nxt = re.search(r"^==[^=].*?==\s*$", text[m.end():], re.M)
    return text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]


def ety_sections(sec):
    """One chunk per ===Etymology n=== heading; the whole section if there is at most one."""
    heads = list(re.finditer(r"^===\s*Etymology(?: \d+)?\s*===\s*$", sec, re.M))
    if len(heads) <= 1:
        return [sec]
    return [sec[h.start(): (heads[i + 1].start() if i + 1 < len(heads) else len(sec))] for i, h in enumerate(heads)]


def clean(defn):
    s = re.sub(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>|<!--.*?-->", "", defn)
    s = FORM_OF.sub(lambda m: f"{m.group(1)} {m.group(2)}", s)
    s = re.sub(r"\{\{(?:l|m|link|mention)\|[a-z-]+\|([^{}|]+)[^{}]*\}\}", r"\1", s)
    s = re.sub(r"\{\{(?:gloss|gl|non-gloss|ng|n-g)\|([^{}|]+)[^{}]*\}\}", r"\1", s)
    while re.search(r"\{\{[^{}]*\}\}", s):
        s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"'{2,}", "", s)
    return re.sub(r"\s+", " ", s).strip(" ;,:")[:80]


def gloss(chunk):
    out = []
    for line in chunk.splitlines():
        if re.match(r"^#(?![:*#])", line):
            g = clean(line[1:])
            if g:
                out.append(g)
        if len(out) == 2:
            break
    return "; ".join(out) or "(no definition line)"


manifest = list(csv.DictReader(open(RAW / "manifest.csv", encoding="utf-8")))
pilot = {r["raw_file"] for r in csv.DictReader(open(PILOT, encoding="utf-8"))} if PILOT else set()
blind, sealed = [], []
for r in manifest:
    if r["status"] != "ok":
        continue
    if (MODE == "--exclude" and r["raw_file"] in pilot) or (MODE == "--only-pilot" and r["raw_file"] not in pilot):
        continue
    page = json.load(open(RAW / "pages" / r["raw_file"], encoding="utf-8"))["query"]["pages"][0]
    text = page["revisions"][0]["slots"]["main"]["content"]
    base = hashlib.sha256(f"{TAG}|{r['lang']}|{r['title']}".encode()).hexdigest()[:10]
    for i, chunk in enumerate(ety_sections(lang_section(text, LANGS[r["lang"]])), 1):
        iid = f"{base}-{i}"
        blind.append({"item_id": iid, "lang": r["lang"], "lemma": r["title"], "gloss": gloss(chunk)})
        sealed.append({"item_id": iid, "stratum": r["stratum"], "raw_file": r["raw_file"], "revid": r["revid"], "ety_index": i})

OUT.mkdir(parents=True, exist_ok=True)
for name, rows in (("blind_sheet.csv", blind), ("_sealed_mapping.csv", sealed)):
    rows.sort(key=lambda x: x["item_id"])
    with open(OUT / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
os.chmod(OUT / "_sealed_mapping.csv", 0o444)
print(f"{len({b['item_id'][:10] for b in blind})} lemmas, {len(blind)} sense rows -> {OUT}")
