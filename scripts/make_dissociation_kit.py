"""Blind sheets of dissociated items and matched controls for human annotators.
Usage: make_dissociation_kit.py BASELINE_DIR OUT_DIR LANGUAGE [LANGUAGE ...]

Per language: every dissociated item and as many congruent items (same selection as the S5 plan), mixed in
hash order. The sheets show the word only. Route and subset go to a sealed key.
"""
import csv, gzip, hashlib, os, sys
from pathlib import Path

D, OUT, LANGS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
OUT.mkdir(parents=True, exist_ok=True)
key = lambda r: hashlib.sha256(f"s5-v1|{r['lang']}|{r['title']}|{r['wiktionary_route']}".encode()).hexdigest()
oof = list(csv.DictReader(gzip.open(D / "oof_predictions.csv.gz", "rt", encoding="utf-8")))
for L in LANGS:
    dis = [r for r in oof if r["lang"] == L and r["subset"] == "dissociated"]
    con = sorted((r for r in oof if r["lang"] == L and r["subset"] == "congruent"), key=key)[:len(dis)]
    rows = sorted(dis + con, key=lambda r: hashlib.sha256(("mix|" + key(r)).encode()).hexdigest())
    ident = lambda r: "d" + key(r)[:9]
    for who in ("A", "B"):
        with open(OUT / f"{L.lower()}_dissociation_annotator_{who}.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["item_id", "lang", "word", "label", "confidence", "sources_consulted", "notes"])
            w.writerows([ident(r), L, r["title"], "", "", "", ""] for r in rows)
    path = OUT / f"_sealed_key_{L.lower()}_dissociation.csv"
    if path.exists():
        os.chmod(path, 0o644)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "word", "wiktionary_route", "subset", "norm_edit_distance"])
        w.writerows([ident(r), r["title"], r["wiktionary_route"], r["subset"], r["norm_edit_distance"]] for r in rows)
    os.chmod(path, 0o444)
    print(L, len(rows), "rows")  # counts only
