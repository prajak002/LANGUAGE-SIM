"""Reading routes from Wiktionary etymology sections. Shared by the audit and the baseline scripts."""
import re

ROUTE = {"inh": "INH", "inh+": "INH", "inherited": "INH", "lbor": "LRN", "learned borrowing": "LRN",
         "slbor": "SEMI", "semi-learned borrowing": "SEMI", "bor": "BOR", "bor+": "BOR", "borrowed": "BOR"}
ETYMON_KW = {"inh": "INH", "lbor": "LRN", "slbor": "SEMI", "bor": "BOR"}
OLD_LATIN = {"VL.", "LL.", "ML.", "NL.", "CL.", "EL.", "RL."}


def ety_sections(sec):
    heads = list(re.finditer(r"^===\s*Etymology(?: \d+)?\s*===\s*$", sec, re.M))
    if len(heads) <= 1:
        return [sec]
    return [sec[h.start(): (heads[i + 1].start() if i + 1 < len(heads) else len(sec))] for i, h in enumerate(heads)]


def ety_text(chunk):
    m = re.search(r"^=+\s*Etymology(?: \d+)?\s*=+\s*$", chunk, re.M)
    if not m:
        return ""
    nxt = re.search(r"^=+[^=].*?=+\s*$", chunk[m.end():], re.M)
    return chunk[m.end(): m.end() + nxt.start()] if nxt else chunk[m.end():]


def from_ancestor(src, code):
    return src == code or src.startswith(code + "-") or (code == "la" and src in OLD_LATIN)


DIRECT = re.compile(r"\{\{\s*(" + "|".join(re.escape(k) for k in sorted(ROUTE, key=len, reverse=True)) + r")\s*\|[^|{}]*\|\s*([^|{}<]+)(?:\|\s*[A-Za-z0-9_]+=[^|{}]*)*(?:\|\s*([^|{}<=]*))?")
TREE_TOP = re.compile(r"\|\s*:(inh|lbor|slbor|bor)(?:<[^|<>]*>)*\s*\|\s*([A-Za-z][A-Za-z.\-]*)[:>]([^|<>{}]*)")
TREE_NESTED = re.compile(r"<ety:(inh|lbor|slbor|bor)<([A-Za-z][A-Za-z.\-]*):([^|<>{}]*)")


def tree_bodies(ety):
    """Bodies of {{ety|...}} / {{etymon|...}} templates, with nested templates kept (brace matching)."""
    out = []
    for m in re.finditer(r"\{\{\s*(?:ety|etymon)\s*\|", ety):
        depth, i = 2, m.end()
        while i < len(ety) and depth > 0:
            depth += 2 * ety.startswith("{{", i) - 2 * ety.startswith("}}", i)
            i += 2 if ety.startswith(("{{", "}}"), i) else 1
        out.append(ety[m.end() - 1: i])
    return out


def assertions_with_forms(ety):
    """(route, source language code, source form) triples stated on the page, in order of appearance."""
    found = [(ROUTE[n], src.strip(), form.strip()) for n, src, form in DIRECT.findall(ety)]
    for body in tree_bodies(ety):
        found += [(ETYMON_KW[k], src, form.strip()) for k, src, form in TREE_TOP.findall(body) + TREE_NESTED.findall(body)]
    return found


def assertions(ety):
    """(route, source language code) pairs stated on the page, from direct templates and from etymology trees."""
    return [(r, src) for r, src, _ in assertions_with_forms(ety)]


def routes(ety, code):
    """Routes (INH, LRN, SEMI, BOR) that the page asserts from the ancestor."""
    return {r for r, src in assertions(ety) if from_ancestor(src, code)}
