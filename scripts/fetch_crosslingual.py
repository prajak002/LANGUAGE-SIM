"""Fetch for docs/crosslingual_audit_plan.md v1.0. Usage: fetch_crosslingual.py OUT_DIR STAGE

STAGE is sizes | members | pages. Each stage reads the previous stage's output and can be re-run:
finished work is skipped. Stores only what the plan lists (section 3).
"""
import csv, gzip, hashlib, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT, STAGE = Path(sys.argv[1]), sys.argv[2]
OUT.mkdir(parents=True, exist_ok=True)
UA = "naacle-crosslingual-audit/1.0 (academic research; serial low-rate reads) python-urllib"
API = "https://en.wiktionary.org/w/api.php"
SEED, N, MIN_PAGES = "crosslingual-audit-v1-2026-10-11", 400, 100
PAIRS = {  # ancestor name: (ancestor code, modern languages)
    "Sanskrit": ("sa", ["Hindi", "Bengali", "Marathi", "Gujarati", "Punjabi", "Odia", "Assamese", "Nepali",
                        "Sinhalese", "Urdu", "Konkani", "Maithili"]),
    "Latin": ("la", ["Spanish", "Portuguese", "French", "Italian", "Romanian", "Catalan", "Galician", "Occitan"]),
    "Ancient Greek": ("grc", ["Greek"]), "Old Armenian": ("xcl", ["Armenian"]), "Middle Persian": ("pal", ["Persian"]),
    "Old Irish": ("sga", ["Irish"]), "Old Norse": ("non", ["Icelandic"]), "Old Georgian": ("oge", ["Georgian"]),
    "Ottoman Turkish": ("ota", ["Turkish"]), "Old East Slavic": ("orv", ["Russian"]), "Old Javanese": ("kaw", ["Javanese"]),
    "Old Japanese": ("ojp", ["Japanese"]), "Biblical Hebrew": ("hbo", ["Hebrew"]), "Old English": ("ang", ["English"]),
}
CATS = {"LRN": "{L} learned borrowings from {A}", "SEMI": "{L} semi-learned borrowings from {A}",
        "INH": "{L} terms inherited from {A}"}
_last = [0.0]


def api(params):
    params = {**params, "format": "json", "formatversion": "2", "maxlag": "5"}
    data = urllib.parse.urlencode(params).encode()
    for attempt in range(6):
        wait = 1.5 - (time.monotonic() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(API, data=data, headers={"User-Agent": UA}), timeout=60) as r:
                body = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                ra = e.headers.get("Retry-After")
                time.sleep(int(ra) if ra and ra.isdigit() else 30 * (attempt + 1))
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            time.sleep(20 * (attempt + 1))
            continue
        if body.get("error", {}).get("code") == "maxlag":
            time.sleep(5 * (attempt + 1))
            continue
        if "error" in body:
            raise RuntimeError(body["error"])
        return body
    raise RuntimeError("gave up after retries")


def lang_section(text, name):
    m = re.search(rf"^=={re.escape(name)}==\s*$", text, re.M)
    if not m:
        return None
    nxt = re.search(r"^==[^=].*?==\s*$", text[m.end():], re.M)
    return text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]


def sizes():
    rows = [(A, code, L, c, CATS[c].format(L=L, A=A)) for A, (code, Ls) in PAIRS.items() for L in Ls for c in CATS]
    info = {}
    for i in range(0, len(rows), 50):
        b = api({"action": "query", "prop": "categoryinfo", "titles": "|".join("Category:" + r[4] for r in rows[i:i + 50])})
        for p in b["query"]["pages"]:
            info[p["title"][len("Category:"):]] = (not p.get("missing", False), p.get("categoryinfo", {}).get("pages", 0))
    size = {(A, L, c): info.get(name, (False, 0)) for A, code, L, c, name in rows}
    with open(OUT / "sizes.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ancestor", "ancestor_code", "lang", "category", "category_name", "exists", "pages", "pair_included"])
        for A, code, L, c, name in rows:
            inc = all(size[(A, L, k)][0] and size[(A, L, k)][1] >= MIN_PAGES for k in ("LRN", "INH"))
            w.writerow([A, code, L, c, name, *size[(A, L, c)], inc])
    print("checked at", datetime.now(timezone.utc).isoformat(timespec="seconds"))


def included():
    return [r for r in csv.DictReader(open(OUT / "sizes.csv", encoding="utf-8"))
            if r["pair_included"] == "True" and r["exists"] == "True" and int(r["pages"]) > 0]


def members():
    (OUT / "members").mkdir(exist_ok=True)
    for r in included():
        path = OUT / "members" / (r["category_name"].replace(" ", "_") + ".jsonl.gz")
        if path.exists():
            continue
        cont, n = {}, 0
        with gzip.open(str(path) + ".part", "wt", encoding="utf-8") as f:
            while True:
                b = api({"action": "query", "list": "categorymembers", "cmtitle": "Category:" + r["category_name"],
                         "cmnamespace": "0", "cmlimit": "500", **cont})
                f.write(json.dumps(b, ensure_ascii=False) + "\n")
                n += len(b["query"]["categorymembers"])
                if "continue" not in b:
                    break
                cont = {"cmcontinue": b["continue"]["cmcontinue"]}
        Path(str(path) + ".part").rename(path)
        print(r["category_name"], n, flush=True)


def member_titles(name):
    with gzip.open(OUT / "members" / (name.replace(" ", "_") + ".jsonl.gz"), "rt", encoding="utf-8") as f:
        return [m["title"] for line in f for m in json.loads(line)["query"]["categorymembers"]]


def pages():
    sample, need = [], {}  # need: title -> set of language names
    for r in included():
        ts = sorted(set(member_titles(r["category_name"])),
                    key=lambda t: hashlib.sha256(f"{SEED}|{r['lang']}|{r['ancestor']}|{r['category']}|{t}".encode()).hexdigest())[:N]
        for rank, t in enumerate(ts, 1):
            sample.append([r["lang"], r["ancestor"], r["ancestor_code"], r["category"], rank, t])
            need.setdefault(t, set()).add(r["lang"])
    with open(OUT / "sample.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["lang", "ancestor", "ancestor_code", "category", "rank", "title"])
        w.writerows(sample)
    store, done = OUT / "sections.jsonl.gz", set()
    if store.exists():
        with gzip.open(store, "rt", encoding="utf-8") as f:
            done = {json.loads(line)["title"] for line in f}
    todo = sorted(t for t in need if t not in done)
    print(len(sample), "sample rows;", len(need), "distinct titles;", len(todo), "to fetch", flush=True)
    with gzip.open(store, "at", encoding="utf-8") as f:
        for i in range(0, len(todo), 50):
            batch, got, cont = todo[i:i + 50], {}, {}
            while True:
                b = api({"action": "query", "prop": "revisions", "titles": "|".join(batch),
                         "rvprop": "ids|timestamp|content", "rvslots": "main", **cont})
                for p in b["query"]["pages"]:
                    if p.get("revisions"):
                        got[p["title"]] = p
                    else:
                        got.setdefault(p["title"], p)
                if "continue" not in b:
                    break
                cont = b["continue"]
            for t in batch:
                p = got.get(t, {})
                rev = (p.get("revisions") or [{}])[0]
                text = rev.get("slots", {}).get("main", {}).get("content", "")
                f.write(json.dumps({"title": t, "pageid": p.get("pageid"), "revid": rev.get("revid"),
                                    "timestamp": rev.get("timestamp"), "fetched": bool(text),
                                    "sections": {L: lang_section(text, L) for L in sorted(need[t])}}, ensure_ascii=False) + "\n")
            f.flush()
            if (i // 50) % 20 == 0:
                print(i + len(batch), "/", len(todo), flush=True)
    print("done", datetime.now(timezone.utc).isoformat(timespec="seconds"))


{"sizes": sizes, "members": members, "pages": pages}[STAGE]()
