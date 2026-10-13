"""S15 of docs/supplementary_plan_s15.md v1.0. Usage: s15_label_change_dates.py RAW_AUDIT_DIR HISTORY_DIR OUT_DIR

For sampled learned-category pages whose route differed in the 2024 snapshot, finds the first later revision that
states the learned route. One request per page. Stores month, an unlinkable pseudonym of the account and a bot flag.
"""
import csv, gzip, hashlib, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wikt_routes import ety_sections, ety_text, routes

RAW, HIST, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
UA = "naacle-crosslingual-audit/1.0 (academic research; serial low-rate reads) python-urllib"
API = "https://en.wiktionary.org/w/api.php"
SNAP, MAX_RANK, PAUSE = "2024-10-11T00:00:00Z", 60, 4.0
_last, _429 = [0.0], [0]


def api(params):
    data = urllib.parse.urlencode({**params, "format": "json", "formatversion": "2", "maxlag": "5"}).encode()
    for attempt in range(6):
        wait = PAUSE - (time.monotonic() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(API, data=data, headers={"User-Agent": UA}), timeout=90) as r:
                body = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                _429[0] += 1
                if _429[0] >= 8:
                    raise RuntimeError("stopping: the server keeps answering 429/503")
                ra = e.headers.get("Retry-After")
                time.sleep(int(ra) if ra and ra.isdigit() else 60 * (attempt + 1))
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
        _429[0] = 0
        return body
    raise RuntimeError("gave up after retries")


def lang_section(text, name):
    m = re.search(rf"^=={re.escape(name)}==\s*$", text, re.M)
    if not m:
        return None
    nxt = re.search(r"^==[^=].*?==\s*$", text[m.end():], re.M)
    return text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]


def state(sec, code):
    return set().union(*(routes(ety_text(c), code) for c in ety_sections(sec))) if sec else set()


snap = {}
with gzip.open(HIST / "snapshots.jsonl.gz", "rt", encoding="utf-8") as f:
    for d in map(json.loads, f):
        if d["snapshot"] == SNAP:
            snap[d["title"]] = d
todo = []
for s in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")):
    if int(s["rank"]) > MAX_RANK or s["category"] != "LRN":
        continue
    d = snap.get(s["title"])
    r = state(d["sections"].get(s["lang"]) if d else None, s["ancestor_code"])
    if r and "LRN" not in r:
        todo.append((s, d))
print(len(todo), "pages", Counter(s["ancestor"] for s, _ in todo), flush=True)
salt = os.urandom(16)
rows, names = [], {}
for i, (s, d) in enumerate(todo, 1):
    b = api({"action": "query", "prop": "revisions", "titles": s["title"], "rvprop": "ids|timestamp|user|content", "rvslots": "main",
             "rvlimit": "50", "rvstart": d["timestamp"], "rvdir": "newer"})
    month = user = ""
    for rev in b["query"]["pages"][0].get("revisions", []):
        text = rev.get("slots", {}).get("main", {}).get("content")
        if rev.get("revid") == d["revid"] or text is None:
            continue
        if "LRN" in state(lang_section(text, s["lang"]), s["ancestor_code"]):
            month, user = rev["timestamp"][:7], rev.get("user", "")
            break
    names[len(rows)] = user
    rows.append({"ancestor": s["ancestor"], "lang": s["lang"], "month": month})
    if i % 25 == 0:
        print(i, "/", len(todo), flush=True)
distinct = sorted({u for u in names.values() if u})
bots = set()
for k in range(0, len(distinct), 50):
    b = api({"action": "query", "list": "users", "ususers": "|".join(distinct[k:k + 50]), "usprop": "groups"})
    bots |= {u["name"] for u in b["query"]["users"] if "bot" in u.get("groups", [])}
for k, r in enumerate(rows):
    u = names[k]
    r["account"] = hashlib.sha256(salt + u.encode()).hexdigest()[:10] if u else ""
    r["bot"] = int(u in bots) if u else ""
del names, distinct, bots, salt
with open(OUT / "s15_changes.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["ancestor", "lang", "month", "account", "bot"])
    w.writeheader()
    w.writerows(rows)
summ = []
for A in sorted({r["ancestor"] for r in rows}):
    R = [r for r in rows if r["ancestor"] == A]
    loc = [r for r in R if r["month"]]
    mon, acc = Counter(r["month"] for r in loc), Counter(r["account"] for r in loc)
    top = [v for _, v in acc.most_common(3)]
    summ.append([A, len(R), len(loc), len(acc), top[0] if top else 0, sum(top), sum(r["bot"] == 1 for r in loc),
                 mon.most_common(1)[0][0] if mon else "", mon.most_common(1)[0][1] if mon else 0, sum(v for _, v in mon.most_common(3)),
                 " ".join(f"{m}:{v}" for m, v in sorted(mon.items()))])
with open(OUT / "s15_summary.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ancestor", "pages", "located", "distinct_accounts", "by_most_active_account", "by_three_most_active", "by_bots",
                "busiest_month", "in_busiest_month", "in_busiest_three_months", "by_month"])
    w.writerows(summ)
for x in summ:
    print(*x)
