"""Practice-set selection + fetch per docs/practice_set_selection.md v1.0."""
import csv, hashlib, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=False)
(OUT / "pages").mkdir(); (OUT / "category_members").mkdir()
UA = "naacle-stratum-practice-check/0.1 (academic research; low-volume serial reads) python-urllib"
API = "https://en.wiktionary.org/w/api.php"
SEED = "practice-round-1-2026-10-10"
LANGS = {"hi": "Hindi", "bn": "Bengali"}
SKT = {"LRN": "{L} learned borrowings from Sanskrit", "SEMI": "{L} semi-learned borrowings from Sanskrit",
       "INH": "{L} terms inherited from Sanskrit"}
EXT = {"EXT-FA": "{L} terms borrowed from Classical Persian", "EXT-AR": "{L} terms borrowed from Arabic",
       "EXT-EN": "{L} terms borrowed from English"}
N = {"OVL": 3, "SEMI": 6, "LRN": 6, "INH": 6, "EXT-FA": 1, "EXT-AR": 1, "EXT-EN": 1}
ORDER = ["OVL", "SEMI", "LRN", "INH", "EXT-FA", "EXT-AR", "EXT-EN"]
_last = [0.0]

def api(params):
    params = {**params, "format": "json", "formatversion": "2", "maxlag": "5"}
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        wait = 3.0 - (time.monotonic() - _last[0])
        if wait > 0: time.sleep(wait)
        _last[0] = time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                status, body = r.status, json.load(r)
        except urllib.error.HTTPError as e:
            status, body = e.code, None
            if e.code in (429, 503):
                ra = e.headers.get("Retry-After")
                time.sleep(int(ra) if ra and ra.isdigit() else 30 * (attempt + 1)); continue
        if body and body.get("error", {}).get("code") == "maxlag":
            time.sleep(5 * (attempt + 1)); continue
        return status, url, body
    return status, url, body

def members(cat):
    titles, cont, pages = [], {}, 0
    while True:
        st, url, b = api({"action": "query", "list": "categorymembers", "cmtitle": "Category:" + cat,
                          "cmnamespace": "0", "cmlimit": "500", **cont})
        if st != 200 or not b or "error" in b: raise RuntimeError(f"member list failed: {cat} {st}")
        (OUT / "category_members" / f"{cat.replace(' ', '_')}.{pages}.json").write_text(json.dumps(b, ensure_ascii=False))
        titles += [m["title"] for m in b["query"]["categorymembers"]]; pages += 1
        if "continue" not in b: return titles
        cont = {"cmcontinue": b["continue"]["cmcontinue"]}

def eligible(t): return not re.search(r"[ \-A-Za-z0-9]", t)
def key(lang, s, t): return hashlib.sha256(f"{SEED}|{lang}|{s}|{t}".encode()).hexdigest()

manifest, log = [], []
for lang, L in LANGS.items():
    cats = {s: set(filter(eligible, members(c.format(L=L)))) for s, c in {**SKT, **EXT}.items()}
    from collections import Counter
    cnt = Counter(t for s in SKT for t in cats[s])
    pools = {"OVL": {t for t, c in cnt.items() if c >= 2}, **cats}
    chosen = set()
    for s in ORDER:
        ranked = sorted(pools[s], key=lambda t: key(lang, s, t))
        got, rank = 0, 0
        for t in ranked:
            if got == N[s]: break
            rank += 1
            if t in chosen:
                log.append([lang, s, rank, key(lang, s, t), t, "skipped_already_selected"]); continue
            st, url, b = api({"action": "query", "prop": "revisions", "titles": t,
                              "rvprop": "ids|timestamp|content", "rvslots": "main"})
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            page = (b or {}).get("query", {}).get("pages", [{}])[0]
            rev = (page.get("revisions") or [{}])[0]
            text = rev.get("slots", {}).get("main", {}).get("content", "")
            has_lang = bool(re.search(rf"^=={re.escape(L)}==\s*$", text, re.M))
            status = "ok" if st == 200 and text and has_lang else ("no_language_section" if text else f"retrieval_failed_{st}")
            fname = f"{lang}_{s}_{rank:03d}.json"
            if b is not None:
                (OUT / "pages" / fname).write_text(json.dumps(b, ensure_ascii=False))
            sec = text.split(f"=={L}==", 1)[1] if has_lang else ""
            sec = re.split(r"^==[^=].*==\s*$", sec, maxsplit=1, flags=re.M)[0]
            has_ety = bool(re.search(r"^===+\s*Etymology", sec, re.M))
            manifest.append({"lang": lang, "stratum": s, "rank": rank, "title": t, "pageid": page.get("pageid"),
                             "revid": rev.get("revid"), "rev_timestamp": rev.get("timestamp"),
                             "url": f"https://en.wiktionary.org/w/index.php?title={urllib.parse.quote(t)}&oldid={rev.get('revid')}",
                             "retrieved_at": now, "http_status": st, "status": status,
                             "has_etymology_section": has_ety, "raw_file": fname})
            log.append([lang, s, rank, key(lang, s, t), t, "selected" if status == "ok" else "replaced:" + status])
            if status == "ok": chosen.add(t); got += 1
        if got < N[s]: log.append([lang, s, "", "", "", f"shortfall:{N[s]-got}"])
    print(lang, {s: len(p) for s, p in pools.items()})

with open(OUT / "manifest.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(manifest[0])); w.writeheader(); w.writerows(manifest)
with open(OUT / "selection_log.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["lang", "stratum", "rank", "key", "title", "outcome"]); w.writerows(log)
print("pages fetched:", len(manifest), "ok:", sum(m["status"] == "ok" for m in manifest))
