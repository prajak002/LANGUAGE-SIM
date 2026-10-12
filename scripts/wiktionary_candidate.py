"""Wiktionary candidate per docs/evidence_extraction_protocol_v1.1.md §5''. Run only after the label freeze.

Usage: wiktionary_candidate.py RAW_DIR SEALED_MAPPING OUT_CSV
"""
import csv, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

RAW, SEALED, OUT = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
LANGS = {"hi": "Hindi", "bn": "Bengali"}
IA = {"sa", "inc-pra", "pi", "pra", "pmh", "psu", "pka", "inc-apa", "inc-ash", "inc-pro", "inc-oin", "inc-mgd",
      "inc-ohi", "inc-obn", "inc-mbn", "inc-sap", "inc-psc", "inc-mas", "inc-gup", "elu-prk", "inc-kam", "iir-pro", "ine-pro"}
ROUTE = {"inh": "INH", "inh+": "INH", "inherited": "INH", "lbor": "LRN", "learned borrowing": "LRN",
         "slbor": "SEMI", "semi-learned borrowing": "SEMI", "bor": "BOR", "bor+": "BOR", "borrowed": "BOR",
         "der": "DER", "der+": "DER", "derived": "DER", "psm": "DER", "calque": "DER", "cal": "DER"}
ETYMON_KW = {"inh": "INH", "lbor": "LRN", "slbor": "SEMI", "bor": "BOR", "der": "DER", "from": "DER", "afeq": "AFF", "af": "AFF"}


def lang_section(text, name):
    m = re.search(rf"^=={re.escape(name)}==\s*$", text, re.M)
    if not m:
        return ""
    nxt = re.search(r"^==[^=].*?==\s*$", text[m.end():], re.M)
    return text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]


def ety_sections(sec):
    heads = list(re.finditer(r"^===\s*Etymology(?: \d+)?\s*===\s*$", sec, re.M))
    if len(heads) <= 1:
        return [sec]
    return [sec[h.start(): (heads[i + 1].start() if i + 1 < len(heads) else len(sec))] for i, h in enumerate(heads)]


def ety_text(chunk):
    """Text under the Etymology heading, up to the next heading."""
    m = re.search(r"^=+\s*Etymology(?: \d+)?\s*=+\s*$", chunk, re.M)
    if not m:
        return ""
    nxt = re.search(r"^=+[^=].*?=+\s*$", chunk[m.end():], re.M)
    return chunk[m.end(): m.end() + nxt.start()] if nxt else chunk[m.end():]


def routes(ety, lang):
    found = []
    for t in re.findall(r"\{\{([^{}]*)\}\}", ety):
        parts = [p.strip() for p in t.split("|")]
        name = parts[0]
        pos = [p for p in parts[1:] if "=" not in p]
        if name in ROUTE and len(pos) >= 2 and pos[0] == lang:
            found.append((ROUTE[name], pos[1]))
        elif name in ("etymon", "ety"):
            kw = None
            for p in pos[1:]:
                if p.startswith(":"):
                    kw = ETYMON_KW.get(p[1:], "DER")
                elif kw and ">" in p or (kw and re.match(r"^[a-z-]+[:>]", p)):
                    found.append((kw, re.split(r"[:>]", p)[0]))
                    kw = None
    return found


def is_ia(src):
    """Sanskrit, a Middle Indo-Aryan stage, or another Indo-Aryan language code."""
    return src in IA or src.startswith(("pra", "inc-")) or src in ("hi", "bn", "ur", "mr", "gu", "pa", "or", "as", "ne", "mai", "bho", "awa", "bra")


def candidate(found):
    cats = set()
    for r, src in found:
        if r in ("INH", "LRN", "SEMI"):
            cats.add(r if is_ia(src) else "UNSPEC")
        elif r == "BOR":
            cats.add("SKT-BOR" if src == "sa" else ("IA-BOR" if is_ia(src) else "EXT"))
    if not found:
        return "NOETY"
    if len(cats) == 1:
        return cats.pop()
    return "UNSPEC"


rows = []
for s in csv.DictReader(open(SEALED, encoding="utf-8")):
    page = json.load(open(RAW / "pages" / s["raw_file"], encoding="utf-8"))["query"]["pages"][0]
    lang = s["raw_file"][:2]
    chunks = ety_sections(lang_section(page["revisions"][0]["slots"]["main"]["content"], LANGS[lang]))
    i = int(s.get("ety_index") or 1)
    ety = ety_text(chunks[i - 1]) if i <= len(chunks) else ""
    found = routes(ety, lang)
    rows.append({"item_id": s["item_id"], "stratum_v1.0": s["stratum"], "wiktionary_candidate": candidate(found),
                 "templates": "; ".join(f"{r}<{src}" for r, src in found) or "—",
                 "etymology_wikitext": re.sub(r"\s+", " ", ety).strip()[:400]})
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"{len(rows)} rows -> {OUT}")
