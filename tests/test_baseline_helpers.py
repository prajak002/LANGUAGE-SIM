"""Hand-checked cases for the normalisation and edit distance of scripts/baseline.py. Run with .venv/bin/python."""
import math, unicodedata
from pathlib import Path

src = (Path(__file__).resolve().parent.parent / "scripts/baseline.py").read_text(encoding="utf-8")
ns = {"unicodedata": unicodedata, "math": math}
exec(src[src.index("INDIC_TO_DEVA"):src.index("# ---- items")], ns)  # the helper definitions only
n, ned = ns["normalise"], ns["ned"]
assert n("vīvus") == "vivus" and n("*Oculus-") == "oculus"
assert n("কলা") == n("कला")            # Bengali -> Devanagari
assert n("ਕਰਮ") == n("करम") and n("કમળ") == n("कमळ")  # Gurmukhi, Gujarati
assert n("ଘର") == n("घर")              # Odia
assert n("λόγος") == "λογος"
assert ned("kitten", "sitting") == 3 / 7 and ned("abc", "abc") == 0 and ned("", "a") == 1.0
print("baseline helpers: all checks pass")
