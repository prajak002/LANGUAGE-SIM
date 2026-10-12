"""Past revisions for docs/supplementary_plan.md v1.0, S1. Usage: fetch_history.py RAW_AUDIT_DIR OUT_DIR

One request per (page, snapshot). Resumable: finished (title, snapshot) pairs are skipped.
"""
import csv, gzip, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
UA = "naacle-crosslingual-audit/1.0 (academic research; serial low-rate reads) python-urllib"
API = "https://en.wiktionary.org/w/api.php"
SNAPSHOTS, MAX_RANK = ["2024-10-11T00:00:00Z", "2021-10-11T00:00:00Z"], 60
PAUSE = 4.0
_last, _429 = [0.0], [0]


def api(params):
    data = urllib.parse.urlencode({**params, "format": "json", "formatversion": "2", "maxlag": "5"}).encode()
    for attempt in range(6):
        wait = PAUSE - (time.monotonic() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(API, data=data, headers={"User-Agent": UA}), timeout=60) as r:
                body = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                _429[0] += 1
                if _429[0] >= 8:
                    raise RuntimeError("stopping: the server keeps answering 429/503; do not retry without a longer pause")
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


need = {}
for s in csv.DictReader(open(RAW / "sample.csv", encoding="utf-8")):
    if int(s["rank"]) <= MAX_RANK:
        need.setdefault(s["title"], set()).add(s["lang"])
store, done = OUT / "snapshots.jsonl.gz", set()
if store.exists():
    with gzip.open(store, "rt", encoding="utf-8") as f:
        done = {(d["title"], d["snapshot"]) for d in map(json.loads, f)}
todo = [(t, snap) for t in sorted(need) for snap in SNAPSHOTS if (t, snap) not in done]
print(len(need), "titles;", len(todo), "requests to make", flush=True)
with gzip.open(store, "at", encoding="utf-8") as f:
    for i, (t, snap) in enumerate(todo, 1):
        b = api({"action": "query", "prop": "revisions", "titles": t, "rvprop": "ids|timestamp|content", "rvslots": "main",
                 "rvlimit": "1", "rvstart": snap, "rvdir": "older"})
        p = b["query"]["pages"][0]
        rev = (p.get("revisions") or [{}])[0]
        text = rev.get("slots", {}).get("main", {}).get("content")
        f.write(json.dumps({"title": t, "snapshot": snap, "revid": rev.get("revid"), "timestamp": rev.get("timestamp"),
                            "page_existed": text is not None,
                            "sections": {L: (lang_section(text, L) if text is not None else None) for L in sorted(need[t])}}, ensure_ascii=False) + "\n")
        if i % 50 == 0:
            f.flush()
            print(i, "/", len(todo), flush=True)
print("done", datetime.now(timezone.utc).isoformat(timespec="seconds"))
