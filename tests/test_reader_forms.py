"""Hand cases for the ancestor form read from an etymology template (scripts/wikt_routes.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from wikt_routes import assertions_with_forms as forms

assert forms("{{lbor|hi|sa|इन्दु}}") == [("LRN", "sa", "इन्दु")]
assert forms("{{lbor|hi|sa|tr=índu|इन्दु}}") == [("LRN", "sa", "इन्दु")]
assert forms("{{lbor|hi|sa|tr=a|sc=Deva|भक्ष}}") == [("LRN", "sa", "भक्ष")]
assert forms("{{lbor|hi|sa|इन्दु|tr=índu}}") == [("LRN", "sa", "इन्दु")]
assert forms("{{inh|hi|sa}}") == [("INH", "sa", "")]
assert forms("{{inh|hi|sa||t=x}}") == [("INH", "sa", "")]
print("reader forms: all checks pass")
