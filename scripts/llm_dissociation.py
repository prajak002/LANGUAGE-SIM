"""S5 of docs/supplementary_plan_s5.md v1.0. Usage: llm_dissociation.py BASELINE_DIR OUT_DIR MODEL [run|score|export]

run:   queries a local Ollama model (temperature 0, fixed seed); resumable; stores every raw answer.
score: agreement with Wiktionary's label by family, condition and subset. Model output is never a label.
"""
import csv, gzip, hashlib, json, math, re, sys, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

D, OUT, MODEL, MODE = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
OUT.mkdir(parents=True, exist_ok=True)
ANC = {**dict.fromkeys(["Assamese", "Bengali", "Gujarati", "Hindi", "Marathi", "Odia", "Punjabi"], "Sanskrit"),
       **dict.fromkeys(["Catalan", "French", "Galician", "Italian", "Portuguese", "Romanian", "Spanish"], "Latin"),
       "Greek": "Ancient Greek", "Armenian": "Old Armenian"}
OPT = {"INH": "inherited from {A} by continuous transmission through the intermediate stages",
       "LRN": "a learned borrowing taken later directly from {A}"}


def key(r):
    return hashlib.sha256(f"s5-v1|{r['lang']}|{r['title']}|{r['wiktionary_route']}".encode()).hexdigest()


def wilson(k, n):
    if not n:
        return "", ""
    z, p = 1.959964, k / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


oof = list(csv.DictReader(gzip.open(D / "oof_predictions.csv.gz", "rt", encoding="utf-8")))
ety = {(r["lang"], r["title"], r["wiktionary_route"]): r["etymon_norm"] for r in csv.DictReader(gzip.open(D / "items.csv.gz", "rt", encoding="utf-8"))}
items = []
for L in sorted({r["lang"] for r in oof}):
    dis = [r for r in oof if r["lang"] == L and r["subset"] == "dissociated"]
    con = sorted((r for r in oof if r["lang"] == L and r["subset"] == "congruent"), key=key)[:len(dis)]
    items += dis + con


def prompt(r, with_etymon):
    A = ANC[r["lang"]]
    a_is = "INH" if int(key(r), 16) % 2 == 0 else "LRN"
    b_is = "LRN" if a_is == "INH" else "INH"
    lines = [f"Language: {r['lang']}", f"Word: {r['title']}"]
    if with_etymon:
        lines.append(f"{A} source form: {ety[(r['lang'], r['title'], r['wiktionary_route'])]}")
    lines += [f"Question: Is this {r['lang']} word (A) {OPT[a_is].format(A=A)}, or (B) {OPT[b_is].format(A=A)}?",
              "Answer with the single letter A or B."]
    return "\n".join(lines), a_is


store = OUT / "answers.jsonl"
if MODE == "export":
    with open(OUT / "prompts.jsonl", "w", encoding="utf-8") as f:
        for r in items:
            for cond in ("word", "word+etymon"):
                text, a_is = prompt(r, cond == "word+etymon")
                f.write(json.dumps({"lang": r["lang"], "title": r["title"], "route": r["wiktionary_route"], "subset": r["subset"],
                                    "condition": cond, "A_is": a_is, "prompt": text}, ensure_ascii=False) + "\n")
    print("exported", 2 * len(items), "prompts")
    sys.exit(0)
if MODE == "run":
    done = {(d["lang"], d["title"], d["route"], d["condition"]) for d in map(json.loads, open(store, encoding="utf-8"))} if store.exists() else set()
    with open(store, "a", encoding="utf-8") as f:
        n = 0
        for r in items:
            for cond in ("word", "word+etymon"):
                if (r["lang"], r["title"], r["wiktionary_route"], cond) in done:
                    continue
                text, a_is = prompt(r, cond == "word+etymon")
                req = urllib.request.Request("http://localhost:11434/api/generate", headers={"Content-Type": "application/json"},
                                             data=json.dumps({"model": MODEL, "prompt": text, "stream": False,
                                                              "options": {"temperature": 0, "seed": 20261011, "num_predict": 8}}).encode())
                with urllib.request.urlopen(req, timeout=300) as resp:
                    raw = json.load(resp)["response"]
                f.write(json.dumps({"lang": r["lang"], "title": r["title"], "route": r["wiktionary_route"], "subset": r["subset"],
                                    "condition": cond, "A_is": a_is, "raw": raw}, ensure_ascii=False) + "\n")
                n += 1
                if n % 100 == 0:
                    f.flush()
                    print(n, flush=True)
    print("done; items:", len(items))
else:
    b3 = {(r["lang"], r["title"], r["wiktionary_route"]): ("LRN" if r["B3_learned"] == "1" else "INH") for r in oof}
    c = defaultdict(Counter)
    for d in map(json.loads, open(store, encoding="utf-8")):
        m = re.search(r"[AB]", d["raw"].upper())
        ans = None if not m else (d["A_is"] if m.group(0) == "A" else ("LRN" if d["A_is"] == "INH" else "INH"))
        for fam in (ANC[d["lang"]], "ALL (pooled, related languages)"):
            k = c[(fam, d["condition"], d["subset"])]
            k["n"] += 1
            k["unparsed"] += ans is None
            k["agree"] += ans == d["route"]
            k["says_learned"] += ans == "LRN"
            k["same_as_B3"] += ans == b3[(d["lang"], d["title"], d["route"])]
    with open(OUT / "s5_scores.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["family", "condition", "subset", "n", "agrees_with_wiktionary", "share", "ci95_low", "ci95_high", "says_learned", "unparsed", "same_as_B3"])
        for (fam, cond, sub), k in sorted(c.items()):
            w.writerow([fam, cond, sub, k["n"], k["agree"], round(k["agree"] / k["n"], 4), *wilson(k["agree"], k["n"]), k["says_learned"], k["unparsed"], k["same_as_B3"]])
            print(fam[:14].ljust(14), cond.ljust(12), sub.ljust(11), f"{k['agree']}/{k['n']} = {100 * k['agree'] / k['n']:.0f}%  says learned {k['says_learned']}  unparsed {k['unparsed']}  same as B3 {k['same_as_B3']}")
