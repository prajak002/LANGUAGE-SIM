"""Measures M1-M8 of docs/crosslingual_audit_plan.md v1.0. Usage: audit_crosslingual.py RAW_DIR OUT_DIR

Reads sizes.csv, members/, sample.csv and sections.jsonl.gz; fetches nothing.
Writes OUT_DIR/measures.csv (long format, with Wilson 95% intervals), senses.csv.gz and references.csv.
"""
import csv, gzip, json, math, re, sys
from collections import Counter, defaultdict
from pathlib import Path

RAW, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import assertions, ety_sections, ety_text, routes  # noqa: E402


def wilson(k, n):
    if n == 0:
        return ("", "")
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))


def has_ref(text):
    return bool(re.search(r"<ref[ >]|\{\{R:", text))


sizes = [r for r in csv.DictReader(open(RAW / "sizes.csv", encoding="utf-8"))]
pairs = sorted({(r["ancestor"], r["ancestor_code"], r["lang"]) for r in sizes if r["pair_included"] == "True"})
size = {(r["lang"], r["category"]): int(r["pages"]) for r in sizes if r["exists"] == "True"}
catname = {(r["lang"], r["category"]): r["category_name"] for r in sizes}
sections = {}
with gzip.open(RAW / "sections.jsonl.gz", "rt", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        sections[d["title"]] = d
sample = list(csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")))

rows, sense_rows, refs = [], [], defaultdict(Counter)


def add(A, L, cat, measure, k, n, note=""):
    lo, hi = wilson(k, n)
    rows.append({"ancestor": A, "lang": L, "category": cat, "measure": measure, "k": k, "n": n,
                 "share": round(k / n, 4) if n else "", "ci95_low": lo, "ci95_high": hi, "note": note})


for A, code, L in pairs:
    # M1, M2: whole population
    lrn, semi, inh = (size.get((L, c), 0) for c in ("LRN", "SEMI", "INH"))
    add(A, L, "", "M1_semi_share_of_learned_plus_semi", semi, lrn + semi, f"LRN={lrn} SEMI={semi} INH={inh}")
    mem = {}
    for c in ("LRN", "SEMI", "INH"):
        p = RAW / "members" / (catname[(L, c)].replace(" ", "_") + ".jsonl.gz")
        mem[c] = set()
        if p.exists():
            with gzip.open(p, "rt", encoding="utf-8") as f:
                mem[c] = {m["title"] for line in f for m in json.loads(line)["query"]["categorymembers"]}
    union = mem["LRN"] | mem["SEMI"] | mem["INH"]
    cnt = Counter(t for c in mem for t in mem[c])
    add(A, L, "", "M2_titles_in_two_or_more_categories", sum(v >= 2 for v in cnt.values()), len(union))
    add(A, L, "", "M2b_titles_in_both_LRN_and_INH", len(mem["LRN"] & mem["INH"]), len(mem["LRN"] | mem["INH"]))

    pooled = {}  # title -> page-level facts, for the per-language pooled rows
    for cat in ("LRN", "SEMI", "INH"):
        S = [s for s in sample if s["lang"] == L and s["category"] == cat]
        if not S:
            continue
        n_sec = k_unsup = k_none = k_stage = k_multi = k_conf = k_ref = n_sense = k_sense_ref = 0
        missing = 0
        for s in S:
            sec = (sections.get(s["title"], {}).get("sections") or {}).get(L)
            if not sec:
                missing += 1
                continue
            n_sec += 1
            chunks = ety_sections(sec)
            per_sense = [routes(ety_text(c), code) for c in chunks]
            kinds_any = {r for c in chunks for r, _ in assertions(ety_text(c))}
            page_routes = set().union(*per_sense)
            single = {next(iter(r)) for r in per_sense if len(r & {"INH", "LRN", "SEMI"}) == 1 for r in [r & {"INH", "LRN", "SEMI"}]}
            unsup, conf, multi, ref = cat not in page_routes, len(single) >= 2 and len(chunks) >= 2, len(chunks) >= 2, \
                has_ref(sec) or bool(re.search(r"^=+\s*(References|Further reading)\s*=+\s*$", sec, re.M))
            k_unsup += unsup
            k_none += unsup and not page_routes
            k_stage += unsup and cat in kinds_any
            k_multi += multi
            k_conf += conf
            k_ref += ref
            pooled[s["title"]] = (multi, conf, ref)
            for t in set(re.findall(r"\{\{(R:[^|{}]+)", sec)):
                refs[L][t.strip()] += 1
            for i, (c, r) in enumerate(zip(chunks, per_sense), 1):
                sense_rows.append([L, A, cat, s["title"], i, "+".join(sorted(r)) or "NONE", int(has_ref(ety_text(c)))])
                if cat in r:
                    n_sense += 1
                    k_sense_ref += has_ref(ety_text(c))
        add(A, L, cat, "M3_category_not_supported_by_template", k_unsup, n_sec, f"no_language_section={missing}")
        add(A, L, cat, "M3b_of_which_no_route_template_from_ancestor", k_none, n_sec)
        add(A, L, cat, "M3c_of_which_same_route_stated_from_another_stage_only", k_stage, n_sec,
            "addition to the plan: the page states this route from an intermediate stage; the ancestor is reached only through another entry")
        add(A, L, cat, "M4_multiple_etymologies", k_multi, n_sec)
        add(A, L, cat, "M5_conflicting_routes_under_one_spelling", k_conf, n_sec)
        add(A, L, cat, "M6_entry_cites_any_reference", k_ref, n_sec)
        add(A, L, cat, "M7_etymology_cites_reference_inline", k_sense_ref, n_sense, "senses with the category's route")
    n = len(pooled)
    for j, name in enumerate(("M4_multiple_etymologies", "M5_conflicting_routes_under_one_spelling", "M6_entry_cites_any_reference")):
        add(A, L, "ALL", name, sum(v[j] for v in pooled.values()), n, "distinct sampled titles, categories pooled (not population-weighted)")

with open(OUT / "measures.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
with gzip.open(OUT / "senses.csv.gz", "wt", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lang", "ancestor", "sampled_from", "title", "ety_index", "routes_from_ancestor", "etymology_has_inline_ref"])
    w.writerows(sense_rows)
with open(OUT / "references.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lang", "rank", "template", "sampled_pages_citing"])
    for L in sorted(refs):
        for i, (t, c) in enumerate(refs[L].most_common(5), 1):
            w.writerow([L, i, t, c])
print(len(pairs), "pairs;", len(rows), "measure rows;", len(sense_rows), "sense rows")
