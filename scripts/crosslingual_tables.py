"""Markdown tables from the audit's measures.csv. Usage: crosslingual_tables.py AUDIT_DIR"""
import csv, sys
from pathlib import Path

D = Path(sys.argv[1])
M = list(csv.DictReader(open(D / "measures.csv", encoding="utf-8")))
langs = list(dict.fromkeys((r["ancestor"], r["lang"]) for r in M))


def cell(L, cat, measure):
    r = [x for x in M if x["lang"] == L and x["category"] == cat and x["measure"] == measure]
    if not r or not int(r[0]["n"]):
        return "–"
    r = r[0]
    return f"{r['k']}/{r['n']} ({100 * float(r['share']):.1f}%; {100 * float(r['ci95_low']):.1f}–{100 * float(r['ci95_high']):.1f})"


def table(title, cols):
    print(f"\n**{title}**\n\n| Ancestor | Language | " + " | ".join(c[0] for c in cols) + " |\n|---|---|" + "---|" * len(cols))
    for A, L in langs:
        print(f"| {A} | {L} | " + " | ".join(cell(L, c[1], c[2]) for c in cols) + " |")


print("| Ancestor | Language | Learned | Semi-learned | Inherited |\n|---|---|---|---|---|")
for A, L in langs:
    note = dict(p.split("=") for p in next(x for x in M if x["lang"] == L and x["measure"].startswith("M1"))["note"].split())
    print(f"| {A} | {L} | {note['LRN']} | {note['SEMI']} | {note['INH']} |")
table("M1–M2. Semi-learned share; titles in two or more categories (whole population)",
      [("Semi / (learned + semi)", "", "M1_semi_share_of_learned_plus_semi"), ("In ≥2 categories", "", "M2_titles_in_two_or_more_categories"),
       ("In both learned and inherited", "", "M2b_titles_in_both_LRN_and_INH")])
table("M3. Category not supported by a template on the page (sample)",
      [(c, k, "M3_category_not_supported_by_template") for c, k in (("Learned", "LRN"), ("Semi-learned", "SEMI"), ("Inherited", "INH"))])
table("M3c (addition to the plan). Inherited category: same route stated from an intermediate stage only",
      [("Inherited", "INH", "M3c_of_which_same_route_stated_from_another_stage_only")])
table("M3b. Of the sampled pages, no route template from the ancestor at all",
      [(c, k, "M3b_of_which_no_route_template_from_ancestor") for c, k in (("Learned", "LRN"), ("Semi-learned", "SEMI"), ("Inherited", "INH"))])
table("M4–M5. Multiple etymologies; conflicting routes under one spelling (sample)",
      [("Multiple etymologies: learned", "LRN", "M4_multiple_etymologies"), ("inherited", "INH", "M4_multiple_etymologies"),
       ("Conflicting routes: learned", "LRN", "M5_conflicting_routes_under_one_spelling"),
       ("semi-learned", "SEMI", "M5_conflicting_routes_under_one_spelling"), ("inherited", "INH", "M5_conflicting_routes_under_one_spelling")])
table("M6. Entry cites any reference (sample)",
      [(c, k, "M6_entry_cites_any_reference") for c, k in (("Learned", "LRN"), ("Semi-learned", "SEMI"), ("Inherited", "INH"))])
table("M7. Etymology cites a reference inline (senses with the category's route)",
      [(c, k, "M7_etymology_cites_reference_inline") for c, k in (("Learned", "LRN"), ("Semi-learned", "SEMI"), ("Inherited", "INH"))])
print("\n**M8. Most-cited reference templates (sampled pages citing)**\n\n| Language | Templates |\n|---|---|")
R = list(csv.DictReader(open(D / "references.csv", encoding="utf-8")))
for A, L in langs:
    print(f"| {L} | " + "; ".join(f"`{r['template']}` {r['sampled_pages_citing']}" for r in R if r["lang"] == L) + " |")
