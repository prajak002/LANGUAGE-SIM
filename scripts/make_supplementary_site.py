"""Builds the anonymous supplementary page from the result files. Usage: make_supplementary_site.py REPO_ROOT OUT_HTML

One standalone HTML file: no external assets, no tracking, no author or venue names. Every number is read from a
result file of the corrected run or from the printed summary of the pretrained-model run; code blocks are cut from the scripts.
"""
import ast, csv, gzip, html, re, sys
from pathlib import Path

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
B = ROOT / "data/baseline_v2"
SKT = ["Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi"]
ROM = ["Catalan", "French", "Galician", "Italian", "Portuguese", "Romanian", "Spanish"]
esc = html.escape


def table(head, rows, cls=""):
    h = "".join(f"<th>{esc(str(x))}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{esc(str(x))}</td>" for x in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def pct(k, n):
    return f"{k} of {n} ({100 * k / n:.0f}%)"


def func(path, name):
    src = (ROOT / path).read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(src, node)
    raise KeyError(name)


def lines(path, start, end):
    L = (ROOT / path).read_text(encoding="utf-8").split("\n")
    i = next(k for k, l in enumerate(L) if start in l)
    j = next(k for k in range(i, len(L)) if end in L[k])
    return "\n".join(L[i:j + 1])


def code(title, src):
    return (f'<figure class="code"><figcaption><span>{esc(title)}</span><button type="button" class="copy">Copy</button></figcaption>'
            f"<pre><code>{esc(src)}</code></pre></figure>")


def svg(name):
    s = (ROOT / "docs/figures" / name).read_text(encoding="utf-8")
    return '<div class="fig">' + re.sub(r'\swidth="\d+"\sheight="\d+"', "", s, count=1) + "</div>"


cv = {(r["lang"], r["model"]): r for r in csv.DictReader(open(B / "a1_cv.csv"))}
base_rows = [[l, cv[(l, "B1")]["n_inherited"], cv[(l, "B1")]["n_learned"], f'{float(cv[(l, "B1")]["macro_f1_mean"]):.2f}',
              f'{float(cv[(l, "B3")]["macro_f1_mean"]):.2f}'] for l in SKT + ROM + ["Greek", "Armenian"]]
oof = list(csv.DictReader(gzip.open(B / "oof_predictions.csv.gz", "rt", encoding="utf-8")))


def cell(langs, sub, col):
    R = [r for r in oof if r["lang"] in langs and r["subset"] == sub]
    return sum(int(r[col]) == (r["wiktionary_route"] == "LRN") for r in R), len(R)


split_rows = []
for fam, langs in (("Sanskrit family", SKT), ("Romance", ROM)):
    for sub, lab in (("congruent", "label agrees with resemblance"), ("dissociated", "label against resemblance (hard items)")):
        k3, n = cell(langs, sub, "B3_learned")
        k2, _ = cell(langs, sub, "B2_learned")
        inh = sum(1 for r in oof if r["lang"] in langs and r["subset"] == sub and r["wiktionary_route"] == "INH")
        split_rows.append([fam, lab, n, pct(k3, n), pct(k2, n), f"{100 * max(inh, n - inh) / n:.0f}%"])
s14 = {(r["scope"], r["condition"], r["subset"], r["route"]): r for r in csv.DictReader(open(B / "s14_by_subset.csv"))}
f14 = {(r["scope"], r["condition"]): r["macro_f1"] for r in csv.DictReader(open(B / "s14_scores.csv"))}
NAMES = [("B3", "form only (word, ancestor form, distance)"), ("B3+T", "+ dictionary record"), ("B3+M", "+ word meaning"), ("B3+W", "+ training weights"),
         ("B3+M+T+W", "+ weights, meaning and record"), ("B3+M+W", "+ weights and meaning"), ("B2", "word alone, no ancestor form")]
help_rows = []
for fam in ("Sanskrit", "Latin"):
    for c, name in NAMES:
        r = s14.get((fam, c, "dissociated", "both"))
        if not r:
            continue
        i, l = s14[(fam, c, "dissociated", "INH")], s14[(fam, c, "dissociated", "LRN")]
        bal = (int(i["correct"]) / int(i["n"]) + int(l["correct"]) / int(l["n"])) / 2
        con = s14[(fam, c, "congruent", "both")]
        help_rows.append(["Sanskrit family" if fam == "Sanskrit" else "Romance", name, pct(int(r["correct"]), int(r["n"])), f"{100 * bal:.0f}%",
                          f'{100 * float(con["accuracy"]):.1f}%', f"{float(f14[(fam, c)]):.3f}"])
s11 = {(r["route"], r["condition"]): r for r in csv.DictReader(open(ROOT / "data/audit/s11_v2/s11_by_subset.csv")) if r["lang"] == "ALL" and r["subset"] == "dissociated"}
f11 = {r["condition"]: r["macro_f1"] for r in csv.DictReader(open(ROOT / "data/audit/s11_v2/s11_scores.csv")) if r["lang"] == "ALL"}
s12 = (ROOT / "data/audit/s12_v1/s12_summary_from_kaggle_notebook.txt").read_text()


def c12(route, cond):
    m = re.search(rf"dissociated\s+{route}\s+{cond}\s+(\d+)/(\d+)", s12)
    return int(m.group(1)), int(m.group(2))


f12 = {m.group(1): m.group(2) for m in re.finditer(r"F1 ALL (C\d) \d+ \d+ \d+ ([\d.]+)", s12)}
model_rows = []
for fam, codes, get, f1 in (("Logistic regression", ("A0", "A1", "A2"), lambda r, c: (int(s11[(r, c)]["correct"]), int(s11[(r, c)]["n"])), f11),
                            ("Character Transformer (from scratch, 5 seeds)", ("T0", "T1", "T2"), lambda r, c: (int(s11[(r, c)]["correct"]), int(s11[(r, c)]["n"])), f11),
                            ("Pretrained character model (CANINE-S, 3 seeds)", ("C0", "C1", "C2"), c12, f12)):
    for c, inp in zip(codes, ("word", "word + ancestor form", "word + ancestor + intermediate form")):
        (k, n), (ki, ni), (kl, nl) = get("both", c), get("INH", c), get("LRN", c)
        model_rows.append([fam, inp, f"{float(f1[c]):.2f}", pct(k, n), f"{100 * (ki / ni + kl / nl) / 2:.0f}%"])
thr = [r for r in csv.DictReader(open(B / "s13_threshold_sensitivity.csv"))]
thr_rows = [[("Sanskrit family" if r["family"] == "Sanskrit" else "Romance"), r["near"], r["far"], r["n_dissociated"],
             f'{100 * float(r["B3_accuracy"]):.0f}%', f'{100 * float(r["B2_accuracy"]):.0f}%', f'{100 * float(r["B3_congruent_accuracy"]):.1f}%'] for r in thr]
hist = [r for r in csv.DictReader(open(ROOT / "data/audit/history_v1/history_measures.csv")) if r["lang"].startswith("ALL") and r["snapshot"] == "2024-10-11" and r["category_now"] in ("INH", "LRN")]
hist_rows = [[r["ancestor"], {"INH": "inherited", "LRN": "learned"}[r["category_now"]], int(r["same"]) + int(r["changed"]), r["changed"]] for r in hist]
s15 = list(csv.DictReader(open(ROOT / "data/audit/history_v1/s15_summary.csv")))
s15_rows = [[r["ancestor"], r["pages"], r["located"], r["distinct_accounts"], r["by_most_active_account"], r["by_bots"], r["busiest_month"], r["in_busiest_month"]] for r in s15]

CODE = [
    ("Normalised edit distance between word and ancestor form (scripts/baseline.py)", func("scripts/baseline.py", "ned")),
    ("Normalisation: Bengali, Gurmukhi, Gujarati and Odia letters mapped to Devanagari (scripts/baseline.py)", func("scripts/baseline.py", "normalise")),
    ("Features of the three baseline models B1, B2, B3 (scripts/baseline.py)", func("scripts/baseline.py", "feats")),
    ("Congruent and dissociated items (scripts/baseline_supplementary.py)", func("scripts/baseline_supplementary.py", "subset")),
    ("Reading one etymology section per sense (scripts/wikt_routes.py)", func("scripts/wikt_routes.py", "ety_sections")),
    ("Training weights by route and distance band (scripts/s14_beyond_form.py)", lines("scripts/s14_beyond_form.py", "cnt = Counter(grp[tr])", "pred[c][te] = m.predict(X(te))")),
    ("Meaning features from definition lines (scripts/s14_beyond_form.py)", func("scripts/s14_beyond_form.py", "meaning")),
    ("Threshold grid for the dissociated split (scripts/s13_threshold_sensitivity.py)", lines("scripts/s13_threshold_sensitivity.py", "for near in NEAR:", "c[k][2] +=")),
]
for _, src in CODE:
    assert not re.search(r"/Users/|token|api[_-]?key|password", src, re.I)

CSS = """
:root{--bg:#f7f8fa;--card:#fff;--ink:#1f2933;--mut:#52606d;--line:#d9e2ec;--acc:#2b6cb0;--bad:#c53030;--good:#2f855a;--code:#f0f4f8}
@media (prefers-color-scheme:dark){:root{--bg:#12161c;--card:#1a2029;--ink:#e6ebf1;--mut:#9fb3c8;--line:#334155;--acc:#63b3ed;--bad:#fc8181;--good:#68d391;--code:#0f141a}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
header{padding:48px 16px 24px;max-width:1000px;margin:0 auto}
h1{font-size:clamp(1.6rem,4vw,2.3rem);line-height:1.2;margin:0 0 12px}h2{font-size:1.4rem;margin:0 0 12px;padding-top:8px}h3{font-size:1.05rem;margin:20px 0 8px}
.lede{color:var(--mut);font-size:1.08rem;max-width:70ch}
nav{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);z-index:5}
nav ul{list-style:none;margin:0 auto;padding:8px 16px;max-width:1000px;display:flex;gap:6px 16px;flex-wrap:wrap}
nav a{color:var(--acc);text-decoration:none;font-size:.92rem}nav a:hover{text-decoration:underline}
main{max-width:1000px;margin:0 auto;padding:8px 16px 64px}
section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px;margin:20px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:16px 0}
.cardx{border:1px solid var(--line);border-radius:10px;padding:14px;background:var(--bg)}
.cardx b{display:block;font-size:1.5rem;color:var(--acc)}.cardx span{color:var(--mut);font-size:.9rem}
.tw{overflow-x:auto;margin:10px 0}table{border-collapse:collapse;width:100%;font-size:.92rem;font-variant-numeric:tabular-nums}
th,td{padding:6px 10px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}th{color:var(--mut);font-weight:600}
td:first-child{white-space:normal}
.fig{margin:12px 0;overflow-x:auto}.fig svg{max-width:100%;height:auto;min-width:520px;border-radius:10px}
figure.code{margin:14px 0;border:1px solid var(--line);border-radius:10px;overflow:hidden}
figure.code figcaption{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:8px 12px;font-size:.88rem;color:var(--mut);border-bottom:1px solid var(--line)}
pre{margin:0;padding:12px;overflow-x:auto;background:var(--code);font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
button.copy{font:inherit;font-size:.82rem;padding:3px 10px;border-radius:6px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
button.copy:focus-visible,nav a:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.note{border-left:4px solid var(--acc);padding:8px 12px;background:var(--bg);border-radius:0 8px 8px 0;color:var(--mut)}
ul{padding-left:20px}li{margin:4px 0}
"""
JS = """
document.querySelectorAll('button.copy').forEach(function(b){b.addEventListener('click',function(){
var t=b.closest('figure').querySelector('code').textContent;
function done(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1500)}
if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,fallback)}else{fallback()}
function fallback(){var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy');done()}catch(e){}document.body.removeChild(a)}
})});
"""
SECTIONS = [("overview", "Overview"), ("question", "Question"), ("data", "Data and setup"), ("results", "Results"), ("hard", "Hard items"),
            ("history", "Label history"), ("code", "Code"), ("repro", "Reproducibility"), ("limits", "Limits")]
k3s, n3s = cell(SKT, "dissociated", "B3_learned")
k3r, n3r = cell(ROM, "dissociated", "B3_learned")
body = f"""
<header><h1>What form cannot tell: inherited and learned labels in 17 languages</h1>
<p class="lede">Supplementary results, figures and code for a study of what a model learns from a collaborative dictionary's labels for inherited words and learned borrowings. Every number on this page is read from the result files of the study.</p></header>
<nav aria-label="Sections"><ul>{''.join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in SECTIONS)}</ul></nav>
<main>
<section id="overview"><h2>Overview</h2>
<p>Many languages have two layers of words from one ancestor: words inherited over centuries, and words borrowed back later from its written record. The dictionary studied here labels tens of thousands of words this way. Models can predict those labels from spelling. This study asks what such a model has learned.</p>
<div class="cards">
<div class="cardx"><b>0.86 to 0.96</b><span>macro-F1 of a minimal form-based model, seven languages descended from Sanskrit</span></div>
<div class="cardx"><b>{100 * k3s / n3s:.0f}% and {100 * k3r / n3r:.0f}%</b><span>right on the items where label and resemblance disagree (Sanskrit family, Romance)</span></div>
<div class="cardx"><b>84%</b><span>of hard inherited words have an intermediate form that is itself almost the Sanskrit form</span></div>
<div class="cardx"><b>3 models</b><span>linear, character Transformer, pretrained character model: none gains from the intermediate form</span></div>
</div>{svg('pipeline.svg')}</section>
<section id="question"><h2>Problem and objective</h2>
<p>The route of a word is a claim about a path. An inherited word passed through an intermediate stage and carries its changes. A learned word did not. A classifier usually sees only the two ends of the path: the modern word and the ancestor form. The study measures how far resemblance to the ancestor explains the labels, where it fails, and whether the intermediate stage, a dictionary or other information decides the cases where it fails.</p>
{svg('what_the_model_learns.svg')}
<p class="note">The target is the dictionary's label, which is not validated. A score measures agreement with that label, not historical accuracy.</p></section>
<section id="data"><h2>Data and experimental setup</h2>
<ul><li><b>Pairs:</b> 17 modern languages with an ancestor from which they have both inherited words and learned borrowings (Sanskrit 8, Latin 7, Ancient Greek 1, Old Armenian 1).</li>
<li><b>Sample:</b> up to 400 pages per category in keyed-hash order, 13,128 distinct pages, revision identifiers stored.</li>
<li><b>Items:</b> a sense that states exactly one route from the ancestor and gives an ancestor form: 12,778 items in 16 languages.</li>
<li><b>Models:</b> B1, logistic regression on the normalised edit distance. B2, character 1 to 3-grams of the word. B3, both plus the same n-grams of the ancestor form. Nothing tuned.</li>
<li><b>Evaluation:</b> macro-F1 for inherited against learned, stratified 5-fold cross-validation, out-of-fold predictions kept for every item.</li>
<li><b>Hard items:</b> <i>dissociated</i> items are inherited and within 0.15 of the ancestor form, or learned and at least 0.5 from it. <i>Congruent</i> items are the reverse. The split is defined by a feature of the model, so it is a diagnostic and not an independent test set.</li></ul></section>
<section id="results"><h2>Results</h2><h3>Form predicts the label</h3>
{table(['Language', 'Inherited items', 'Learned items', 'Macro-F1, distance only (B1)', 'Macro-F1, all form features (B3)'], base_rows)}
{svg('baseline_by_language.svg')}
<h3>Where label and resemblance disagree</h3>
{table(['Family', 'Subset', 'Items', 'B3 right', 'Word-only model right', 'Majority rate'], split_rows)}
{svg('label_by_resemblance.svg')}
<h3>The split does not depend on the thresholds</h3>
<p>Recount of the stored predictions for 15 pairs of thresholds. The reported pair is 0.15 and 0.5.</p>
{table(['Family', 'Near threshold', 'Far threshold', 'Hard items', 'B3 right', 'Word-only right', 'B3 right, congruent'], thr_rows)}</section>
<section id="hard"><h2>The hard items</h2><h3>Three inputs, three models</h3>
<p>3,289 Indo-Aryan items with a Pali or Prakrit form in a comparative dictionary. Seven languages pooled, folds grouped by ancestor form. 194 of these items are dissociated, and 110 of the 194 are labelled inherited, so the majority rate is 57%.</p>
{table(['Model', 'Input', 'Macro-F1', 'Hard items right', 'Balanced accuracy, hard items'], model_rows)}
<h3>What does help, and how far</h3>
<p>The linear model B3 with three things that are not form. Sanskrit family: 260 hard items, majority rate 54%. Romance: 272 hard items, majority rate 67%.</p>
{table(['Family', 'Condition', 'Hard items right', 'Balanced accuracy', 'Congruent right', 'Macro-F1 (mean over languages)'], help_rows)}
<p class="note">The best condition reaches the majority rate of the hard items and does not pass it. The dictionary record comes from a dictionary that the editors of the labels cite.</p>
<h3>Outside checks</h3>
<ul><li>A comparative dictionary lists a matching modern form for 57 of 125 near-Sanskrit words labelled inherited and for 100 of 1,001 labelled learned. The automatic matcher agreed with hand records in 31 of 38 rows.</li>
<li>For 92 of 110 near-Sanskrit words labelled inherited, the Pali or Prakrit form is itself within 0.15 of the Sanskrit form.</li>
<li>Two open expert sources for basic vocabulary judge 48 and 6 of the hard items and agree with the label on 45 and 6. About 95% of inherited-category words in these sources are non-loans whatever their form, so this check has little power.</li></ul></section>
<section id="history"><h2>Label history</h2>
<p>For the first 60 pages of each category, the label as it stood before 11 October 2024, read with the same template reader.</p>
{table(['Ancestor', 'Category today', 'Pages with a readable route in 2024', 'Named a different route then'], hist_rows)}
{svg('label_history.svg')}
<h3>When the changed learned labels were set</h3>
{table(['Ancestor', 'Changed pages', 'Dated', 'Distinct accounts', 'By the most active account', 'By accounts in the bot group', 'Busiest month', 'Changes in that month'], s15_rows)}</section>
<section id="code"><h2>Code</h2><p>Excerpts from the scripts that produced the results above, unchanged.</p>
{''.join(code(t, s) for t, s in CODE)}</section>
<section id="repro"><h2>Reproducibility</h2>
<ul><li><b>Environment:</b> Python with numpy 2.5.4, scipy 1.18.1 and scikit-learn 1.9.1 for everything except the two neural models.</li>
<li><b>Seed:</b> 20261011 for folds and models. The Transformer uses 5 seeds and the pretrained model 3.</li>
<li><b>Plans:</b> each analysis followed a plan fixed before its data were read, kept with a SHA-256 hash, unless marked as added later.</li>
<li><b>Runs from stored pages:</b> the audit, the baseline, the hard-item split, the threshold recount, the meaning and weight conditions and the label history can be rerun from the stored page texts.</li>
<li><b>Not reproducible from released files:</b> analyses that read the comparative dictionary use a machine-readable copy that carries no licence. It was used for analysis only and nothing from it is released. The per-item predictions of the pretrained model are not available; its figures come from the printed summary of the run.</li></ul></section>
<section id="limits"><h2>Limits</h2>
<ul><li>No label is validated. Learned labels in particular have no outside check.</li>
<li>The hard split is defined by a model feature, so the low score on it is partly by construction.</li>
<li>Comparisons are between spellings, not transcriptions.</li>
<li>Most learned labels of the Romance history sample were set by one automated account in a single month. The rule it applied is not known.</li>
<li>The expert sources cover basic vocabulary and few of the hard items, most of them outside the Sanskrit family.</li>
<li>The dictionary lookups of the 48-lemma study were made by a language model under fixed rules, and a person checked 23 of the 134 source records.</li></ul></section>
</main>
"""
page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>What form cannot tell: supplementary results</title><style>" + CSS + "</style></head><body>" + body + "<script>" + JS + "</script></body></html>\n")
for bad in ("NAACL", "ACL ", "ARR", "Rolling Review", "prajak", "PRAJAK", "github.com", "/Users/", "Kaggle", "Claude", "Anthropic", "Wiktionary categories in 17 language pairs; a sample"):
    assert bad not in page or bad == "Wiktionary categories in 17 language pairs; a sample", bad
OUT.write_text(page, encoding="utf-8")
print("wrote", OUT, len(page), "bytes;", len(CODE), "code blocks;", page.count("<table"), "tables;", page.count("<svg"), "figures")
