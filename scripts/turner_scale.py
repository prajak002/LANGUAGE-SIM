"""S4 of docs/supplementary_plan_s4.md v1.0. Usage: turner_scale.py JAMBU_FORMS_CSV JAMBU_EDGES_CSV BASELINE_ITEMS ANNOTATION_DIR PRACTICE_RAW OUT_DIR

Reads a temporary copy of Jambu's cldf/forms.csv (not stored in this repository). Writes only counts, entry
numbers and yes/no flags. Run the validation block first; read results only if it passes.
"""
import csv, gzip, json, math, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import assertions_with_forms, ety_sections, ety_text

FORMS, EDGES, ITEMS, ANN, PRACT, OUT = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4]), Path(sys.argv[5]), Path(sys.argv[6])
OUT.mkdir(parents=True, exist_ok=True)
csv.field_size_limit(10 ** 9)
JAMBU = {"Hindi": "H", "Bengali": "B", "Marathi": "M", "Gujarati": "G", "Punjabi": "P", "Odia": "Or", "Assamese": "A"}
CONS = dict(zip("कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ",
                ["k", "kh", "g", "gh", "ṅ", "c", "ch", "j", "jh", "ñ", "ṭ", "ṭh", "ḍ", "ḍh", "ṇ", "t", "th", "d", "dh", "n",
                 "p", "ph", "b", "bh", "m", "y", "r", "l", "v", "ś", "ṣ", "s", "h", "ḷ"]))
VOW = dict(zip("अआइईउऊऋॠएऐओऔ", ["a", "ā", "i", "ī", "u", "ū", "r̥", "r̥̄", "e", "ai", "o", "au"]))
SIGN = dict(zip("ािीुूृॄेैोौ", ["ā", "i", "ī", "u", "ū", "r̥", "r̥̄", "e", "ai", "o", "au"]))
INDIC = [(0x0980, 0x09FF), (0x0A00, 0x0A7F), (0x0A80, 0x0AFF), (0x0B00, 0x0B7F)]


def to_deva(s):
    return "".join(chr(ord(c) - lo + 0x0900) if any(lo <= ord(c) <= hi for lo, hi in INDIC[i:i + 1]) else c
                   for c in s for i in [next((k for k, (lo, hi) in enumerate(INDIC) if lo <= ord(c) <= hi), 0)]
                   for lo in [INDIC[i][0]])


def translit(s):
    """Devanagari to Latin with the inherent vowel; characters outside the table are dropped."""
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


def skeleton(latin):
    s = norm(latin)
    s = re.sub(r"(?<=[kgcjtdpb])h", "", s)
    s = re.sub(r"[aeiou]", "", s)
    return re.sub(r"(.)\1+", r"\1", s)


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
head, listed, tagcount = defaultdict(set), defaultdict(lambda: defaultdict(set)), Counter()
for r in csv.DictReader(open(FORMS, encoding="utf-8")):
    if not r["Source"].startswith("CDIAL"):
        continue
    if r["Language_ID"] == "Indo-Aryan":
        for hw in re.split(r"[,;]", r["Original"] or r["Form"]):
            if norm(hw):
                head[norm(hw)].add(r["ID"])
    elif r["Language_ID"] in JAMBU.values():
        for entry in article_of.get(r["ID"], ()):
            listed[entry][r["Language_ID"]].add(skeleton(r["Original"] or r["Form"]))
        tagcount.update(t for t in r["Tags"].split() if re.search(r"lw|loan|bor", t))
print("Turner head-word keys:", len(head), "| articles with a listed form in the seven languages:", len(listed))
print("tags that look like loan marks:", dict(tagcount) or "none found")


def check(word_deva, etymon_deva, lang):
    arts = head.get(norm(translit(etymon_deva)), set())
    t2 = any(JAMBU[lang] in listed[a] for a in arts if a in listed)
    sk = skeleton(translit(word_deva))
    t3 = any(sk in listed[a][JAMBU[lang]] for a in arts if a in listed and JAMBU[lang] in listed[a])
    return arts, t2, t3


LANG = {"hi": "Hindi", "bn": "Bengali"}
val = []
for rnd in ("pilot_1", "round_2"):
    sealed = {r["item_id"]: r for r in csv.DictReader(open(ANN / rnd / "_sealed_mapping.csv", encoding="utf-8"))}
    seen = Counter()
    for s in csv.DictReader(open(ANN / rnd / "source_checks.csv", encoding="utf-8")):
        if not s["source"].startswith("Turner") or s["found"] != "yes":
            continue
        m = re.search(r"entry (\d+[a-z]?)", s["entry_ref"])
        if not m:
            continue
        idx = int(s["item_id"].split("-")[1]) if "-" in s["item_id"] else None
        page = json.load(open(PRACT / "pages" / sealed[s["item_id"]]["raw_file"], encoding="utf-8"))["query"]["pages"][0]
        text = page["revisions"][0]["slots"]["main"]["content"]
        L = LANG[s["lang"]]
        sec = re.split(r"^==[^=].*?==\s*$", text.split(f"=={L}==", 1)[1], maxsplit=1, flags=re.M)[0]
        chunks = ety_sections(sec)
        ety = [f for c in (chunks if idx is None else chunks[idx - 1: idx]) for k, src, f in assertions_with_forms(ety_text(c)) if src.startswith("sa")]
        hand_listed = s["route_asserted"].startswith("inherited") and "variant" not in s["route_asserted"]
        entry = m.group(1)
        sk = skeleton(translit(to_deva(s["lemma"])))
        t3_hand_entry = JAMBU[L] in listed.get(entry, {}) and sk in listed[entry][JAMBU[L]]
        t1 = any(entry in head.get(norm(translit(e)), set()) for e in ety) if ety else None
        val.append([rnd, s["lemma"], entry, hand_listed, t3_hand_entry, t1])
cmp3 = [(h, t) for _, _, _, h, t, _ in val]
agree3 = sum(h == t for h, t in cmp3)
t1rows = [v for v in val if v[5] is not None]
print(f"\nVALIDATION  T3 against hand record, at the hand-recorded article: {agree3}/{len(cmp3)} agree "
      f"(hand listed & matcher yes {sum(h and t for h, t in cmp3)}, hand listed & matcher no {sum(h and not t for h, t in cmp3)}, "
      f"hand not listed & matcher yes {sum(t and not h for h, t in cmp3)}, both no {sum(not h and not t for h, t in cmp3)})")
print(f"VALIDATION  T1: Wiktionary's Sanskrit etymon reaches the hand-recorded article in {sum(v[5] for v in t1rows)}/{len(t1rows)} rows with a Sanskrit etymon on the page")
with open(OUT / "validation.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["round", "lemma", "hand_entry", "hand_form_listed", "matcher_T3_at_hand_entry", "matcher_T1_reaches_hand_entry"])
    w.writerows(val)
passed = agree3 / len(cmp3) >= 0.8
print("T3 validation", "PASSED" if passed else "FAILED (below 80%): T3 is not to be interpreted")

rows, flags = [], []
items = [r for r in csv.DictReader(gzip.open(ITEMS, "rt", encoding="utf-8")) if r["lang"] in JAMBU]
cnt = defaultdict(Counter)
for r in items:
    arts, t2, t3 = check(r["word_norm"], r["etymon_norm"], r["lang"])
    c = cnt[(r["lang"], r["wiktionary_route"])]
    c["n"] += 1
    c["t1"] += bool(arts)
    c["t2"] += t2
    c["t3"] += t3
    c["multi"] += len(arts) > 1
    flags.append([r["lang"], r["title"], r["wiktionary_route"], ";".join(sorted(arts)), int(bool(arts)), int(t2), int(t3)])
for (L, route), c in sorted(cnt.items()):
    rows.append([L, route, c["n"], c["t1"], *wilson(c["t1"], c["n"]), c["t2"], *wilson(c["t2"], c["t1"]), c["t3"], *wilson(c["t3"], c["t1"]), c["multi"]])
for route in ("INH", "SEMI", "LRN"):
    c = sum((v for (L, r), v in cnt.items() if r == route), Counter())
    rows.append(["ALL SEVEN (pooled, related languages)", route, c["n"], c["t1"], *wilson(c["t1"], c["n"]), c["t2"], *wilson(c["t2"], c["t1"]), c["t3"], *wilson(c["t3"], c["t1"]), c["multi"]])
with open(OUT / "measures.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lang", "wiktionary_route", "items", "T1_etymon_matches_article", "T1_low", "T1_high", "T2_article_lists_language", "T2_low", "T2_high",
                "T3_listed_form_matches_word", "T3_low", "T3_high", "items_matching_several_articles"])
    w.writerows(rows)
with gzip.open(OUT / "item_flags.csv.gz", "wt", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lang", "title", "wiktionary_route", "turner_entry_numbers", "T1", "T2", "T3"])
    w.writerows(flags)
for r in rows:
    print(r[0][:12].ljust(12), r[1].ljust(4), f"n={r[2]:4}  T1 {r[3]:4}  T2|T1 {r[6]:4}  T3|T1 {r[9]:4}")
