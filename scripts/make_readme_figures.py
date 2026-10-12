"""Animated SVG charts for README.md, drawn from the result files. Usage: make_readme_figures.py REPO_ROOT

No dependencies. Writes docs/figures/*.svg. The numbers are from the corrected run (v2 folders).
"""
import csv, gzip, sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "docs/figures"
OUT.mkdir(parents=True, exist_ok=True)
SKT = ["Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi"]
ROM = ["Catalan", "French", "Galician", "Italian", "Portuguese", "Romanian", "Spanish"]
INK, MUTED, GOOD, BAD, ALT, PAPER = "#1f2933", "#627d98", "#2f855a", "#c53030", "#dd6b20", "#ffffff"
FONT = 'font-family="Helvetica, Arial, sans-serif"'


def svg(name, w, h, body):
    head = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>'
    (OUT / name).write_text(head + f'<rect width="{w}" height="{h}" rx="10" fill="{PAPER}"/>' + "".join(body) + "</svg>\n", encoding="utf-8")


def text(x, y, s, size=13, fill=INK, anchor="start", weight="normal"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'


def hbar(x, y, w, h, fill, delay=0.0):
    return (f'<rect x="{x}" y="{y}" width="0" height="{h}" rx="3" fill="{fill}">'
            f'<animate attributeName="width" from="0" to="{w:.1f}" begin="{delay:.2f}s" dur="0.9s" fill="freeze"/></rect>')


def vbar(x, base, w, h, fill, delay=0.0):
    return (f'<rect x="{x}" y="{base}" width="{w}" height="0" rx="3" fill="{fill}">'
            f'<animate attributeName="height" from="0" to="{h:.1f}" begin="{delay:.2f}s" dur="0.9s" fill="freeze"/>'
            f'<animate attributeName="y" from="{base}" to="{base - h:.1f}" begin="{delay:.2f}s" dur="0.9s" fill="freeze"/></rect>')


cell = Counter()
for r in csv.DictReader(gzip.open(ROOT / "data/baseline_v2/oof_predictions.csv.gz", "rt", encoding="utf-8")):
    fam = "Sanskrit family" if r["lang"] in SKT else "Romance" if r["lang"] in ROM else None
    if fam and r["subset"] != "middle":
        k = (fam, r["wiktionary_route"], float(r["norm_edit_distance"]) <= 0.15)
        cell[k, "n"] += 1
        cell[k, "ok"] += (r["B3_learned"] == "1") == (r["wiktionary_route"] == "LRN")
b = [text(20, 30, "Where the model is right: label by resemblance", 16, weight="bold"),
     text(20, 50, "Share of items the form-based model (B3) gets right. Red cells: label and resemblance disagree.", 12, MUTED)]
for f, fam in enumerate(("Sanskrit family", "Romance")):
    x0 = 150 + f * 300
    b.append(text(x0 + 130, 82, fam, 14, anchor="middle", weight="bold"))
    for c, lab in enumerate(("far from ancestor", "near ancestor")):
        b.append(text(x0 + 65 + c * 130, 100, lab, 11, MUTED, "middle"))
    for rr, route in enumerate(("INH", "LRN")):
        if not f:
            b.append(text(135, 145 + rr * 80, "labelled " + ("inherited" if route == "INH" else "learned"), 12, anchor="end"))
        for c, near in enumerate((False, True)):
            k = (fam, route, near)
            acc = cell[k, "ok"] / cell[k, "n"]
            hard = (route == "INH") == near
            x, y = x0 + c * 130, 108 + rr * 80
            b.append(f'<rect x="{x}" y="{y}" width="124" height="72" rx="6" fill="{"#fff5f5" if hard else "#f0fff4"}" stroke="{BAD if hard else GOOD}"/>')
            b.append(hbar(x + 8, y + 50, 108 * acc, 10, BAD if hard else GOOD, 0.2 * (rr * 2 + c)))
            b.append(text(x + 62, y + 30, f"{100 * acc:.1f}%", 20, BAD if hard else GOOD, "middle", "bold"))
            b.append(text(x + 62, y + 45, f'{cell[k, "ok"]:,} of {cell[k, "n"]:,}', 10, MUTED, "middle"))
svg("label_by_resemblance.svg", 760, 285, b)

acc = {}
for r in csv.DictReader(open(ROOT / "data/audit/s11_v2/s11_by_subset.csv", encoding="utf-8")):
    if r["lang"] == "ALL" and r["subset"] == "dissociated" and r["route"] == "both":
        acc[r["condition"]] = (int(r["correct"]), int(r["n"]))
b = [text(20, 30, "Does more history in the input help on the hard items?", 16, weight="bold"),
     text(20, 50, "Items right out of 191 where label and resemblance disagree. Dashed line: chance.", 12, MUTED)]
base, H = 250, 170
b.append(f'<line x1="70" y1="{base}" x2="730" y2="{base}" stroke="{INK}"/>')
b.append(f'<line x1="70" y1="{base - H / 2}" x2="730" y2="{base - H / 2}" stroke="{MUTED}" stroke-dasharray="6 5"/>')
b.append(text(62, base - H / 2 + 4, "50%", 11, MUTED, "end"))
for g, (lab, a, t) in enumerate((("word only", "A0", "T0"), ("word + ancestor form", "A1", "T1"), ("word + ancestor + intermediate form", "A2", "T2"))):
    x = 110 + g * 215
    for q, (m, fill) in enumerate(((a, INK), (t, ALT))):
        k, n = acc[m]
        h = H * k / n
        b.append(vbar(x + q * 78, base, 70, h, fill, 0.25 * g + 0.1 * q))
        b.append(text(x + q * 78 + 35, base - h - 8, f"{k} ({100 * k / n:.0f}%)", 12, fill, "middle", "bold"))
    b.append(text(x + 74, base + 20, lab, 12, anchor="middle"))
b.append(f'<rect x="500" y="64" width="14" height="14" rx="3" fill="{INK}"/>' + text(520, 76, "logistic model", 12))
b.append(f'<rect x="620" y="64" width="14" height="14" rx="3" fill="{ALT}"/>' + text(640, 76, "Transformer", 12))
svg("three_inputs.svg", 760, 290, b)

f1 = {r["lang"]: float(r["macro_f1_mean"]) for r in csv.DictReader(open(ROOT / "data/baseline_v2/a1_cv.csv", encoding="utf-8")) if r["model"] == "B3"}
order = sorted(SKT, key=lambda L: -f1[L]) + sorted(ROM, key=lambda L: -f1[L]) + ["Greek", "Armenian"]
b = [text(20, 30, "How well form predicts Wiktionary's label, by language", 16, weight="bold"),
     text(20, 50, "Macro-F1 of the form-based model (B3), five-fold cross-validation. 0.5 is roughly chance.", 12, MUTED)]
for i, L in enumerate(order):
    y = 70 + i * 22
    fill = INK if L in SKT else ALT if L in ROM else MUTED
    b.append(text(140, y + 13, L, 12, anchor="end"))
    b.append(hbar(150, y, 520 * f1[L], 16, fill, 0.05 * i))
    b.append(text(158 + 520 * f1[L], y + 13, f"{f1[L]:.2f}", 12, fill, weight="bold"))
b.append(f'<line x1="{150 + 260}" y1="66" x2="{150 + 260}" y2="{70 + len(order) * 22}" stroke="{MUTED}" stroke-dasharray="6 5"/>')
svg("baseline_by_language.svg", 760, 70 + len(order) * 22 + 16, b)

hist = Counter()
for r in csv.DictReader(open(ROOT / "data/audit/history_v1/history_measures.csv", encoding="utf-8")):
    if r["lang"].startswith("ALL") and r["snapshot"].startswith("2024"):
        key = "Inherited labels, all four families" if r["category_now"] == "INH" else f'{r["ancestor"]}|{r["category_now"]}'
        hist[key, "changed"] += int(r["changed"])
        hist[key, "n"] += int(r["changed"]) + int(r["same"])
rows = [("Inherited labels, all four families", "Inherited labels, all four families", GOOD), ("Learned labels, Sanskrit family", "Sanskrit|LRN", INK),
        ("Learned labels, Romance", "Latin|LRN", BAD)]
b = [text(20, 30, "How many labels named a different route two years earlier?", 16, weight="bold"),
     text(20, 50, "Pages sampled in October 2026, read as they stood in October 2024.", 12, MUTED)]
for i, (lab, key, fill) in enumerate(rows):
    y = 72 + i * 44
    k, n = hist[key, "changed"], hist[key, "n"]
    b.append(text(20, y + 14, lab, 13))
    b.append(f'<rect x="290" y="{y}" width="380" height="20" rx="3" fill="#edf2f7"/>')
    b.append(hbar(290, y, max(380 * k / n, 2), 20, fill, 0.3 * i))
    b.append(text(680, y + 15, f"{k} of {n}", 12, fill, weight="bold"))
svg("label_history.svg", 760, 210, b)
print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
