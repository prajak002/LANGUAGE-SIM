"""Hand-checked fixture for scripts/audit_crosslingual.py and scripts/crosslingual_tables.py.

Run: python3 tests/test_audit_fixture.py
Twelve invented pages whose measures were worked out by hand (see EXPECTED). No network.
"""
import csv, gzip, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = {  # title -> {language: section wikitext or None}
    "A": {"Hindi": "\n===Etymology===\n{{lbor|hi|sa|अ}}.\n===Noun===\n# x\n===References===\n* {{R:hi:McGregor}}\n"},
    "B": {"Hindi": "\n===Etymology 1===\n{{inh|hi|psu|x}}, from {{inh|hi|sa|अ}}.<ref>{{R:CDIAL|1}}</ref>\n====Noun====\n# x\n"
                   "===Etymology 2===\n{{lbor|hi|sa|आ}}.\n====Noun====\n# y\n"},
    "C": {"Hindi": "\n===Etymology===\n{{bor|hi|fa|x}}.\n===Noun===\n# x\n====Derived terms====\n{{dercat|hi|sa}}\n"},
    "D": {"Hindi": None},
    "E": {"Hindi": "\n===Etymology===\n{{inh|hi|sa|अ}}.\n===Noun===\n# x\n"},
    "F": {"Hindi": "\n===Etymology===\n{{etymon|hi|:inh|sa>अ>id|id=x}}\n===Noun===\n# x\n"},
    "G": {"Spanish": "\n===Etymology===\n{{lbor|es|LL.|foo}}.\n===Noun===\n# x\n"},
    "H": {"Spanish": "\n===Etymology===\n{{lbor|es|la-med|foo}}.\n===Noun===\n# x\n"},
    "I": {"Spanish": "\n===Etymology===\n{{bor|es|la|foo}}.\n===Noun===\n# x\n"},
    # etymology trees: nested chain with a reference template inside; another stage only; keyword with a modifier
    "J": {"Spanish": "\n===Etymology===\n{{ety|es|:inh|osp:foo<ety:inh<la:fōō<t:x>>><ref:{{R:es:DCECH|foo}}>|text=2|tree=1}}\n===Noun===\n# x\n"},
    "K": {"Spanish": "\n===Etymology===\n{{etymon|es|id=x|:inh|osp:foo<id:x>|tree=1}}\n===Noun===\n# x\n"},
    "M": {"Spanish": "\n===Etymology===\n{{ety|es|:bor<conj:and>|fr:foo|:lbor<conj:and>|la:foo|text=+}}\n===Noun===\n# x\n"},
}
MEMBERS = {("Hindi", "LRN"): "ABCDE", ("Hindi", "INH"): "BF", ("Spanish", "LRN"): "GHIM", ("Spanish", "INH"): "JK"}
ANC = {"Hindi": ("Sanskrit", "sa"), "Spanish": ("Latin", "la")}
NAME = {"LRN": "{L} learned borrowings from {A}", "SEMI": "{L} semi-learned borrowings from {A}", "INH": "{L} terms inherited from {A}"}
EXPECTED = {  # (lang, category, measure) -> (k, n)
    ("Hindi", "", "M1_semi_share_of_learned_plus_semi"): (0, 5),
    ("Hindi", "", "M2_titles_in_two_or_more_categories"): (1, 6),
    ("Hindi", "LRN", "M3_category_not_supported_by_template"): (2, 4),      # C and E; D has no section
    ("Hindi", "LRN", "M3b_of_which_no_route_template_from_ancestor"): (1, 4),  # C only
    ("Hindi", "LRN", "M4_multiple_etymologies"): (1, 4),
    ("Hindi", "LRN", "M5_conflicting_routes_under_one_spelling"): (1, 4),
    ("Hindi", "LRN", "M6_entry_cites_any_reference"): (2, 4),               # A and B
    ("Hindi", "LRN", "M7_etymology_cites_reference_inline"): (0, 2),        # A, and B's second etymology
    ("Hindi", "INH", "M3_category_not_supported_by_template"): (0, 2),
    ("Hindi", "INH", "M5_conflicting_routes_under_one_spelling"): (1, 2),
    ("Hindi", "INH", "M7_etymology_cites_reference_inline"): (1, 2),        # B's first etymology
    ("Hindi", "ALL", "M6_entry_cites_any_reference"): (2, 5),
    ("Spanish", "LRN", "M3_category_not_supported_by_template"): (1, 4),    # I: plain borrowing; M is supported
    ("Spanish", "LRN", "M3b_of_which_no_route_template_from_ancestor"): (0, 4),
    ("Spanish", "INH", "M3_category_not_supported_by_template"): (1, 2),    # K names Old Spanish only; J is supported
    ("Spanish", "INH", "M3c_of_which_same_route_stated_from_another_stage_only"): (1, 2),
    ("Spanish", "INH", "M7_etymology_cites_reference_inline"): (1, 1),      # J
}

with tempfile.TemporaryDirectory() as tmp:
    raw, out = Path(tmp) / "raw", Path(tmp) / "out"
    (raw / "members").mkdir(parents=True)
    with open(raw / "sizes.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ancestor", "ancestor_code", "lang", "category", "category_name", "exists", "pages", "pair_included"])
        for L, (A, code) in ANC.items():
            for c in NAME:
                titles = MEMBERS.get((L, c))
                w.writerow([A, code, L, c, NAME[c].format(L=L, A=A), titles is not None, len(titles or ""), True])
                if titles is not None:
                    with gzip.open(raw / "members" / (NAME[c].format(L=L, A=A).replace(" ", "_") + ".jsonl.gz"), "wt", encoding="utf-8") as g:
                        g.write(json.dumps({"query": {"categorymembers": [{"title": t} for t in titles]}}) + "\n")
    with open(raw / "sample.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["lang", "ancestor", "ancestor_code", "category", "rank", "title"])
        for (L, c), titles in MEMBERS.items():
            for i, t in enumerate(titles, 1):
                w.writerow([L, *ANC[L], c, i, t])
    with gzip.open(raw / "sections.jsonl.gz", "wt", encoding="utf-8") as f:
        for t, secs in PAGES.items():
            f.write(json.dumps({"title": t, "pageid": 1, "revid": 1, "timestamp": "", "fetched": True, "sections": secs}) + "\n")
    subprocess.run([sys.executable, str(ROOT / "scripts/audit_crosslingual.py"), str(raw), str(out)], check=True, stdout=subprocess.DEVNULL)
    got = {(r["lang"], r["category"], r["measure"]): (int(r["k"]), int(r["n"])) for r in csv.DictReader(open(out / "measures.csv", encoding="utf-8"))}
    bad = [(k, v, got.get(k)) for k, v in EXPECTED.items() if got.get(k) != v]
    tables = subprocess.run([sys.executable, str(ROOT / "scripts/crosslingual_tables.py"), str(out)], check=True, capture_output=True, text=True).stdout
    assert "| Sanskrit | Hindi | 2/4 (50.0%" in tables, "table cell for Hindi M3 learned is missing"
for k, want, have in bad:
    print("FAIL", k, "expected", want, "got", have)
print("fixture:", len(EXPECTED) - len(bad), "of", len(EXPECTED), "checks pass")
sys.exit(1 if bad else 0)
