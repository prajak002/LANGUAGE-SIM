"""Join frozen source labels with Wiktionary candidates (v1.1 §5''). Usage: compare_round.py ROUND_DIR RAW_DIR"""
import csv, json, re, sys
from collections import Counter
from pathlib import Path

D, RAW = Path(sys.argv[1]), Path(sys.argv[2])
ex = list(csv.DictReader(open(D / "extraction.csv", encoding="utf-8")))
cand = {r["item_id"]: r for r in csv.DictReader(open(D / "wiktionary_candidates.csv", encoding="utf-8"))}
sealed = {r["item_id"]: r for r in csv.DictReader(open(D / "_sealed_mapping.csv", encoding="utf-8"))}
DECIDED = {"INH", "LRN", "SEMI", "MIX", "EXT", "NIA"}


def cites_cdial(item_id):
    page = json.load(open(RAW / "pages" / sealed[item_id]["raw_file"], encoding="utf-8"))["query"]["pages"][0]
    return "yes" if re.search(r"R:CDIAL", page["revisions"][0]["slots"]["main"]["content"]) else "no"


rows = []
for e in ex:
    c = cand[e["item_id"]]
    if e["label"] == "NSF":
        rel = "no source found"
    elif e["label"] not in DECIDED:
        rel = "undecided by sources"
    elif c["wiktionary_candidate"] in ("UNSPEC", "NOETY", "SKT-BOR", "IA-BOR"):
        rel = "candidate unspecified"
    else:
        rel = "agree" if e["label"] == c["wiktionary_candidate"] else "disagree"
    rows.append({"item_id": e["item_id"], "lang": e["lang"], "lemma": e["lemma"], "sense": e["sense"],
                 "source_label": e["label"], "evidence_strength": e["evidence_strength"],
                 "wiktionary_candidate": c["wiktionary_candidate"], "templates": c["templates"],
                 "stratum_v1.0": c["stratum_v1.0"], "relation": rel, "page_cites_CDIAL": cites_cdial(e["item_id"])})
with open(D / "comparison_post_freeze.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def tab(title, key):
    print(f"\n{title}")
    for k, v in sorted(Counter(key(r) for r in rows).items()):
        print(f"  {k}: {v}")


print(f"{len(rows)} sense rows, {len({r['item_id'][:10] for r in rows})} lemmas")
tab("label", lambda r: r["source_label"])
tab("label x lang", lambda r: (r["lang"], r["source_label"]))
tab("strength", lambda r: r["evidence_strength"])
tab("relation", lambda r: r["relation"])
tab("candidate x label", lambda r: (r["wiktionary_candidate"], r["source_label"]))
tab("candidate x lang x label", lambda r: (r["wiktionary_candidate"], r["lang"], r["source_label"]))
tab("stratum x candidate", lambda r: (r["stratum_v1.0"], r["wiktionary_candidate"]))
tab("relation x cites CDIAL", lambda r: (r["relation"], r["page_cites_CDIAL"]))
print("\ndisagree:", [(r["lemma"], r["sense"][:18], r["source_label"], r["wiktionary_candidate"]) for r in rows if r["relation"] == "disagree"])
print("multi-sense lemmas:", sorted({r["lemma"] for r in rows if sum(x["lemma"] == r["lemma"] for x in rows) > 1}))
