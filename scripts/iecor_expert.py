"""S9 of docs/supplementary_plan_s9.md v1.0. Usage: iecor_expert.py IECOR_DIR AUDIT_RAW BASELINE_DIR STORE_DIR OUT_DIR

Expert loan judgements (IE-CoR, CC BY 4.0) against Wiktionary's route labels in thirteen languages.
One team's judgement on basic vocabulary; not a two-annotator validation.
"""
import csv, gzip, math, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

IE, RAW, BASE, STORE, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
STORE.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
csv.field_size_limit(10 ** 9)
LANG = {"272": "Assamese", "10": "Bengali", "35": "Hindi", "50": "Marathi", "266": "Punjabi", "17": "Catalan", "25": "French", "39": "Italian",
        "56": "Portuguese", "59": "Romanian", "68": "Spanish", "32": "Greek", "8": "Armenian"}
FAMILY = {**dict.fromkeys(["Assamese", "Bengali", "Hindi", "Marathi", "Punjabi"], "Sanskrit"),
          **dict.fromkeys(["Catalan", "French", "Italian", "Portuguese", "Romanian", "Spanish"], "Latin"), "Greek": "Ancient Greek", "Armenian": "Old Armenian"}
DONOR = {"Sanskrit": ("sanskrit", "vedic", "indo-aryan"), "Latin": ("latin",), "Ancient Greek": ("greek",), "Old Armenian": ("armenian",)}
INDIC_TO_DEVA = [(0x0980, 0x09FF), (0x0A00, 0x0A7F), (0x0A80, 0x0AFF), (0x0B00, 0x0B7F)]


def normalise(s):
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


def wilson(k, n):
    if not n:
        return "", ""
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


def variants(value):
    v = re.sub(r"\([^)]*\)|\[[^\]]*\]", "", value or "")
    return {normalise(p) for p in re.split(r"[,;/]", v) if normalise(p)}


loan_sets = defaultdict(set)
for r in csv.DictReader(open(IE / "loans.csv", encoding="utf-8")):
    loan_sets[r["Cognateset_ID"]].add(r["Source_languoid"] or "")
sets_of = defaultdict(set)
for r in csv.DictReader(open(IE / "cognates.csv", encoding="utf-8")):
    sets_of[r["Form_ID"]].add(r["Cognateset_ID"])
loan_values, by_word, stored = Counter(), defaultdict(list), []
for r in csv.DictReader(open(IE / "forms.csv", encoding="utf-8")):
    L = LANG.get(r["Language_ID"])
    if not L:
        continue
    loan_values[r["Loan"]] += 1
    donors = set().union(*(loan_sets[c] for c in sets_of.get(r["ID"], ()) if c in loan_sets)) if sets_of.get(r["ID"]) else set()
    is_loan = r["Loan"].strip().lower() in ("true", "1", "yes") or any(c in loan_sets for c in sets_of.get(r["ID"], ()))
    keys = variants(r["native_script"]) or (variants(r["Form"]) | variants(r["Value"]))
    e = {"id": r["ID"], "loan": is_loan, "donors": sorted(d for d in donors if d)}
    stored.append([L, r["ID"], r["native_script"] or r["Form"], r["Loan"], int(is_loan), "; ".join(e["donors"])])
    for k in keys:
        by_word[(L, k)].append(e)
print("lexemes of the thirteen languages:", len(stored), "| values of the Loan field:", dict(loan_values))
with open(STORE / "iecor_rows_used.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["language", "iecor_form_id", "form", "loan_field", "loan_by_plan_rule", "donor_languoids"])
    w.writerows(stored)
(STORE / "README.md").write_text(
    "# Rows of IE-CoR used in S9\n\nSource: Heggarty, Paul & Anderson, Cormac & Scarborough, Matthew. 2024. Indo-European Cognate Relationships database "
    "(IE-CoR version 1.1). Leipzig: Max Planck Institute for Evolutionary Anthropology. CLDF edition: https://github.com/lexibank/iecor "
    "(CC BY 4.0, https://creativecommons.org/licenses/by/4.0/). Only the language, the form, the loan status and the donor languoids are kept here.\n", encoding="utf-8")


def expert(L, title):
    es = by_word.get((L, normalise(title)))
    if not es:
        return None
    keys = DONOR[FAMILY[L]]
    named = [any(any(k in d.lower() for k in keys) for d in e["donors"]) for e in es]
    if not any(e["loan"] for e in es):
        return "NL"
    if all(e["loan"] for e in es):
        return "LA" if all(named) else ("LO" if not any(named) else "MIX")
    return "MIX"


cats = defaultdict(set)
for s in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")):
    if s["lang"] in FAMILY:
        cats[(s["lang"], s["title"])].add(s["category"])
e1, n_sampled = defaultdict(Counter), Counter()
for (L, title), cs in cats.items():
    c = "+".join(sorted(cs))
    cl = expert(L, title)
    for fam in (FAMILY[L], "ALL", FAMILY[L] + " | " + L):
        n_sampled[(fam, c)] += 1
        if cl:
            e1[(fam, c)][cl] += 1
with open(OUT / "e1_sample_vs_expert.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family_or_language", "wiktionary_category", "sampled_titles", "found", "NL", "LA", "LO", "MIX", "share_NL", "NL_low", "NL_high", "share_LA", "LA_low", "LA_high"])
    for (fam, c), k in sorted(e1.items()):
        n = sum(k.values())
        w.writerow([fam, c, n_sampled[(fam, c)], n, k["NL"], k["LA"], k["LO"], k["MIX"], round(k["NL"] / n, 4), *wilson(k["NL"], n), round(k["LA"] / n, 4), *wilson(k["LA"], n)])
        if " | " not in fam:
            print("E1", fam.ljust(14), c.ljust(8), f"found {n:4} of {n_sampled[(fam, c)]:5}  NL {k['NL']}  LA {k['LA']}  LO {k['LO']}  MIX {k['MIX']}")

e2, detail = defaultdict(Counter), []
for r in csv.DictReader(gzip.open(BASE / "oof_predictions.csv.gz", "rt", encoding="utf-8")):
    L = r["lang"]
    if L not in FAMILY or r["wiktionary_route"] not in ("INH", "LRN"):
        continue
    cl = expert(L, r["title"])
    if cl not in ("NL", "LA"):
        continue
    truth = "INH" if cl == "NL" else "LRN"
    b3 = "LRN" if r["B3_learned"] == "1" else "INH"
    for fam in (FAMILY[L], "ALL"):
        k = e2[(fam, r["subset"])]
        k["n"] += 1
        k["wikt"] += r["wiktionary_route"] == truth
        k["b3"] += b3 == truth
    detail.append([L, r["title"], r["wiktionary_route"], r["subset"], cl, b3])
with open(OUT / "e2_baseline_vs_expert.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "subset", "items_with_expert_class", "wiktionary_agrees", "wikt_low", "wikt_high", "B3_agrees", "b3_low", "b3_high"])
    for (fam, sub), k in sorted(e2.items()):
        w.writerow([fam, sub, k["n"], k["wikt"], *wilson(k["wikt"], k["n"]), k["b3"], *wilson(k["b3"], k["n"])])
        print("E2", fam.ljust(14), sub.ljust(11), f"n={k['n']:4}  Wiktionary agrees with expert {k['wikt']}  B3 agrees {k['b3']}")
with open(OUT / "e2_items.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lang", "title", "wiktionary_route", "subset", "expert_class", "B3"])
    w.writerows(detail)
