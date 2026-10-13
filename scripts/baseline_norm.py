"""The baseline's normalisation of word and etymon, copied unchanged from scripts/baseline.py so that other scripts can import it."""
import unicodedata

INDIC_TO_DEVA = [(0x0980, 0x09FF), (0x0A00, 0x0A7F), (0x0A80, 0x0AFF), (0x0B00, 0x0B7F)]


def normalise(s):
    out = []
    for ch in unicodedata.normalize("NFD", s):
        cp = ord(ch)
        for lo, hi in INDIC_TO_DEVA:
            if lo <= cp <= hi:
                cp = cp - lo + 0x0900
        ch = chr(cp)
        if 0x0900 <= cp <= 0x097F:
            out.append(ch)
        elif unicodedata.category(ch) != "Mn" and ch not in "-* ":
            out.append(ch.lower())
    return "".join(out)
