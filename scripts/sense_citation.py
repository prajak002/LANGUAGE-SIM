"""Does the Wiktionary entry for the target language cite Turner (CDIAL), and the same article?

Three levels are recorded, because a page holds entries for several languages:
  page_cites_CDIAL      anywhere on the page (includes Sanskrit, Assamese ... sections);
  lang_cites_CDIAL      inside the Hindi or Bengali section;
  same_article          a Turner entry number cited in that section equals one the extractor recorded
                        for this sense.
Other reference templates of the language section are listed too (Platts, Dasa ...).

Usage: sense_citation.py RAW_DIR ANNOTATION_DIR
Reads the stored pages and the post-freeze comparison files of both rounds; fetches nothing.
Writes ANNOTATION_DIR/sense_citation.csv and prints relation x citation counts.
"""
import csv, json, re, sys
from collections import Counter
from pathlib import Path

RAW, ANN = Path(sys.argv[1]), Path(sys.argv[2])
LANGS = {"hi": "Hindi", "bn": "Bengali"}


def lang_section(text, name):
    m = re.search(rf"^=={re.escape(name)}==\s*$", text, re.M)
    if not m:
        return ""
    nxt = re.search(r"^==[^=].*?==\s*$", text[m.end():], re.M)
    return text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]


def cdial_refs(chunk):
    """Entry numbers or head-words passed to {{R:CDIAL|...}}; ['(no argument)'] if cited bare."""
    hits = re.findall(r"\{\{R:CDIAL((?:\|[^{}]*)?)\}\}", chunk)
    return [h.strip("|") or "(no argument)" for h in hits]


rows = []
for rnd in ("pilot_1", "round_2"):
    comp = list(csv.DictReader(open(ANN / rnd / "comparison_post_freeze.csv", encoding="utf-8")))
    sealed = {r["item_id"]: r for r in csv.DictReader(open(ANN / rnd / "_sealed_mapping.csv", encoding="utf-8"))}
    turner = {}
    for s in csv.DictReader(open(ANN / rnd / "source_checks.csv", encoding="utf-8")):
        if s["source"].startswith("Turner"):
            turner.setdefault((s["item_id"], s["lemma"]), []).append(s["entry_ref"])
    for c in comp:
        page = json.load(open(RAW / "pages" / sealed[c["item_id"]]["raw_file"], encoding="utf-8"))["query"]["pages"][0]
        text = page["revisions"][0]["slots"]["main"]["content"]
        sec = lang_section(text, LANGS[c["lang"]])
        refs = cdial_refs(sec)
        mine = "; ".join(turner.get((c["item_id"], c["lemma"]), []))
        cited_nums = set(re.findall(r"\b\d{2,5}\b", " ".join(re.sub(r"(?:pg|page)=\d+", "", r) for r in refs)))
        same = bool(cited_nums & set(re.findall(r"\b\d{2,5}\b", mine)))
        others = sorted(set(re.findall(r"\{\{(R:[^|{}]+)", sec)) - {"R:CDIAL"})
        rows.append({"round": rnd, "item_id": c["item_id"], "lang": c["lang"], "lemma": c["lemma"],
                     "source_label": c["source_label"], "relation": c["relation"],
                     "page_cites_CDIAL": "yes" if "R:CDIAL" in text else "no",
                     "lang_cites_CDIAL": "yes" if refs else "no", "same_article": "yes" if same else "no",
                     "wiktionary_CDIAL_args": "; ".join(refs), "extractor_Turner_refs": mine,
                     "other_refs_in_lang_section": "; ".join(others)})

with open(ANN / "sense_citation.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "sense rows")
for name in ("page_cites_CDIAL", "lang_cites_CDIAL", "same_article"):
    print(name)
    for k, v in sorted(Counter((r["round"], r["relation"], r[name]) for r in rows).items()):
        print("  ", k, v)
print("other reference templates in the language section, by source label:")
for k, v in sorted(Counter((r["source_label"], t) for r in rows for t in r["other_refs_in_lang_section"].split("; ") if t).items()):
    print("  ", k, v)
