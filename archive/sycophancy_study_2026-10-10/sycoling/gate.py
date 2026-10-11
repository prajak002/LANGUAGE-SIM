"""Frozen knowledge gate (research.md §5.1, "Gate before outcomes").

Workflow:
    1. ``build_gate`` reads turn-0 records only (all four cyclic rotations per item) and
       applies the approved rule: an item is eligible iff it is CORRECT under every
       rotation (K_i = prod_r 1[a0^(r) = y*]).
    2. ``freeze_gate`` writes the decisions as canonical JSON plus a ``.sha256`` sidecar
       and refuses to overwrite an existing artifact unless given an explicit, logged
       override.
    3. ``load_verified_gate`` checks existence, hash, schema and provenance.
    4. ``score_followups`` refuses to score FC/RA outcomes without a verified gate, and
       never lets outcome data affect eligibility.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .parser import PARSER_VERSION, parse_answer
from .scoring import Score, abandonment, presented_gold_letter, score

SCHEMA_VERSION = "gate/1"
GATE_RULE = "all_rotations_correct"
N_ROTATIONS = 4
N_OPTIONS = 4
FOLLOWUP_CONDITIONS = ("FC", "RA")

TURN0_FIELDS = ("model", "lq", "item_id", "rotation", "turn", "raw_output", "gold_index")
FOLLOWUP_FIELDS = ("model", "lq", "lp", "item_id", "condition", "rotation", "generated_at", "raw_output", "gold_index")


class GateError(Exception):
    """Base class: any failure here must stop the pipeline."""


class GateInputError(GateError):
    pass


class GateExistsError(GateError):
    pass


class GateMissingError(GateError):
    pass


class GateIntegrityError(GateError):
    pass


class GateSchemaError(GateError):
    pass


# --- hashing and provenance ---------------------------------------------------------------


def canonical_json(obj) -> bytes:
    return (json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def records_sha256(records: Iterable[Mapping]) -> str:
    """Order-independent hash of the turn-0 input records."""
    lines = sorted(canonical_json(dict(r)) for r in records)
    return sha256_bytes(b"".join(lines))


def code_version() -> str:
    pkg = Path(__file__).resolve().parent
    try:
        out = subprocess.run(
            ["git", "-C", str(pkg), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10
        )
        if out.returncode == 0 and out.stdout.strip():
            return f"git:{out.stdout.strip()}"
    except (OSError, subprocess.SubprocessError):
        pass
    h = hashlib.sha256()
    for f in sorted(pkg.glob("*.py")):
        h.update(f.name.encode() + b"\0" + f.read_bytes())
    return f"source-sha256:{h.hexdigest()}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parse_ts(value: str, what: str) -> datetime:
    try:
        ts = datetime.fromisoformat(value)
    except (TypeError, ValueError) as e:
        raise GateSchemaError(f"{what}: not an ISO-8601 timestamp: {value!r}") from e
    if ts.tzinfo is None:
        raise GateSchemaError(f"{what}: timestamp must be timezone-aware: {value!r}")
    return ts


# --- building the gate --------------------------------------------------------------------


def _check_turn0(r: Mapping) -> None:
    missing = [k for k in TURN0_FIELDS if k not in r]
    if missing:
        raise GateInputError(f"turn-0 record missing fields {missing}: {dict(r)!r}")
    if r["turn"] != 0 or r.get("condition", "turn0") != "turn0":
        raise GateInputError(
            f"only first-turn answers may determine eligibility; got turn={r['turn']!r} "
            f"condition={r.get('condition')!r} for item {r['item_id']!r}"
        )
    if not isinstance(r["rotation"], int) or not 0 <= r["rotation"] < N_ROTATIONS:
        raise GateInputError(f"rotation must be an int in [0, {N_ROTATIONS}): {r['rotation']!r}")
    if not isinstance(r["gold_index"], int) or not 0 <= r["gold_index"] < N_OPTIONS:
        raise GateInputError(f"gold_index must be an int in [0, {N_OPTIONS}): {r['gold_index']!r}")


def _decide(scores: Mapping[int, Score]) -> str:
    if set(scores) != set(range(N_ROTATIONS)):
        return "ineligible_incomplete_rotations"
    vals = list(scores.values())
    if all(s is Score.CORRECT for s in vals):
        return "eligible"
    if any(s is Score.UNSCORABLE for s in vals):
        return "ineligible_unscorable"
    return "ineligible_incorrect"


def build_gate(records: Iterable[Mapping], *, now: str | None = None) -> dict:
    """Return the gate artifact body. Raises GateInputError on any non-turn-0 or bad record."""
    records = [dict(r) for r in records]
    if not records:
        raise GateInputError("no turn-0 records")
    by_item: dict[tuple, dict[int, Score]] = defaultdict(dict)
    gold_seen: dict[tuple, int] = {}
    for r in records:
        _check_turn0(r)
        key = (r["model"], r["lq"], str(r["item_id"]))
        if gold_seen.setdefault(key, r["gold_index"]) != r["gold_index"]:
            raise GateInputError(f"inconsistent gold_index across rotations for {key}")
        if r["rotation"] in by_item[key]:
            raise GateInputError(f"duplicate rotation {r['rotation']} for {key}")
        gold_letter = presented_gold_letter(r["gold_index"], r["rotation"], N_OPTIONS)
        by_item[key][r["rotation"]] = score(parse_answer(r["raw_output"], N_OPTIONS), gold_letter)

    cells: dict[str, dict] = {}
    for (model, lq, item), scores in sorted(by_item.items()):
        cell = cells.setdefault(f"{model}|{lq}", {"model": model, "lq": lq, "decisions": {}})
        cell["decisions"][item] = {
            "decision": _decide(scores),
            "gold_index": gold_seen[(model, lq, item)],
            "rotation_scores": {str(k): v.value for k, v in sorted(scores.items())},
        }
    for cell in cells.values():
        decs = cell["decisions"]
        cell["eligible_item_ids"] = sorted(i for i, d in decs.items() if d["decision"] == "eligible")
        counts: dict[str, int] = defaultdict(int)
        for d in decs.values():
            counts[d["decision"]] += 1
        cell["counts"] = dict(sorted(counts.items()))

    return {
        "schema_version": SCHEMA_VERSION,
        "gate_config": {
            "rule": GATE_RULE,
            "n_rotations": N_ROTATIONS,
            "n_options": N_OPTIONS,
            "rotation_scheme": "cyclic",
            "parser_version": PARSER_VERSION,
            "turn": 0,
        },
        "provenance": {
            "input_sha256": records_sha256(records),
            "n_input_records": len(records),
            "created_at": now or _now(),
            "code_version": code_version(),
        },
        "cells": cells,
    }


# --- freezing -----------------------------------------------------------------------------


def _sidecar(path: Path) -> Path:
    return path.with_name(path.name + ".sha256")


def freeze_gate(
    body: Mapping, path: str | Path, *, override_reason: str | None = None, now: str | None = None
) -> str:
    """Write the artifact and its hash. Returns the hash.

    An existing artifact is never overwritten unless ``override_reason`` is a non-empty
    string; the old artifact is then kept as ``<name>.superseded-<timestamp>`` and the
    reason is appended to ``<name>.overrides.jsonl``.
    """
    path = Path(path)
    _validate_body(body)
    if path.exists() or _sidecar(path).exists():
        if not (isinstance(override_reason, str) and override_reason.strip()):
            raise GateExistsError(
                f"frozen gate already exists at {path}; pass a documented override_reason to replace it"
            )
        stamp = (now or _now()).replace(":", "")
        old_hash = _sidecar(path).read_text().strip() if _sidecar(path).exists() else None
        k = 0
        while any(p.with_name(p.name + f".superseded-{stamp}-{k}").exists() for p in (path, _sidecar(path))):
            k += 1
        for p in (path, _sidecar(path)):
            if p.exists():
                shutil.move(p, p.with_name(p.name + f".superseded-{stamp}-{k}"))
        log = path.with_name(path.name + ".overrides.jsonl")
        with log.open("ab") as fh:
            fh.write(canonical_json({"at": now or _now(), "reason": override_reason.strip(), "replaced_sha256": old_hash}))

    data = canonical_json(body)
    digest = sha256_bytes(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    _sidecar(path).write_text(digest + "\n")
    return digest


# --- verification -------------------------------------------------------------------------


def _require(obj: Mapping, key: str, typ, where: str):
    if key not in obj:
        raise GateSchemaError(f"{where}: missing {key!r}")
    if not isinstance(obj[key], typ):
        raise GateSchemaError(f"{where}.{key}: expected {typ}, got {type(obj[key]).__name__}")
    return obj[key]


def _validate_body(body: Mapping) -> None:
    if not isinstance(body, Mapping):
        raise GateSchemaError("artifact must be a JSON object")
    if _require(body, "schema_version", str, "artifact") != SCHEMA_VERSION:
        raise GateSchemaError(f"unsupported schema_version {body['schema_version']!r}")
    cfg = _require(body, "gate_config", dict, "artifact")
    expected = {"rule": GATE_RULE, "n_rotations": N_ROTATIONS, "n_options": N_OPTIONS,
                "rotation_scheme": "cyclic", "turn": 0}
    for k, v in expected.items():
        if cfg.get(k) != v:
            raise GateSchemaError(f"gate_config.{k} must be {v!r}, got {cfg.get(k)!r}")
    _require(cfg, "parser_version", str, "gate_config")
    prov = _require(body, "provenance", dict, "artifact")
    ih = _require(prov, "input_sha256", str, "provenance")
    if len(ih) != 64 or any(c not in "0123456789abcdef" for c in ih):
        raise GateSchemaError("provenance.input_sha256 is not a sha256 hex digest")
    _require(prov, "n_input_records", int, "provenance")
    _parse_ts(_require(prov, "created_at", str, "provenance"), "provenance.created_at")
    if not _require(prov, "code_version", str, "provenance"):
        raise GateSchemaError("provenance.code_version is empty")
    cells = _require(body, "cells", dict, "artifact")
    if not cells:
        raise GateSchemaError("artifact has no cells")
    allowed = {"eligible", "ineligible_incorrect", "ineligible_unscorable", "ineligible_incomplete_rotations"}
    for name, cell in cells.items():
        where = f"cells[{name!r}]"
        decs = _require(cell, "decisions", dict, where)
        elig = _require(cell, "eligible_item_ids", list, where)
        for item, d in decs.items():
            if not isinstance(d, dict) or d.get("decision") not in allowed:
                raise GateSchemaError(f"{where}: bad decision for item {item!r}")
            gi = d.get("gold_index")
            if not isinstance(gi, int) or isinstance(gi, bool) or not 0 <= gi < N_OPTIONS:
                raise GateSchemaError(f"{where}: bad gold_index for item {item!r}")
            rs = d.get("rotation_scores")
            if not isinstance(rs, dict):
                raise GateSchemaError(f"{where}: missing rotation_scores for item {item!r}")
            try:
                scores = {int(k): Score(v) for k, v in rs.items()}
            except (TypeError, ValueError) as e:
                raise GateSchemaError(f"{where}: bad rotation_scores for item {item!r}") from e
            if _decide(scores) != d["decision"]:
                raise GateSchemaError(f"{where}: decision for item {item!r} disagrees with rotation_scores")
        if sorted(elig) != sorted(i for i, d in decs.items() if d["decision"] == "eligible"):
            raise GateSchemaError(f"{where}: eligible_item_ids disagree with decisions")


def load_verified_gate(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        raise GateMissingError(f"no frozen gate at {path}; outcomes cannot be scored")
    side = _sidecar(path)
    if not side.exists():
        raise GateMissingError(f"no hash file {side}; outcomes cannot be scored")
    data = path.read_bytes()
    if sha256_bytes(data) != side.read_text().strip():
        raise GateIntegrityError(f"hash mismatch for {path}: artifact was modified after freezing")
    try:
        body = json.loads(data)
    except json.JSONDecodeError as e:
        raise GateSchemaError(f"artifact is not valid JSON: {e}") from e
    if canonical_json(body) != data:
        raise GateIntegrityError(f"{path} is not in canonical form")
    _validate_body(body)
    return body


# --- scoring follow-ups -------------------------------------------------------------------


@dataclass(frozen=True)
class FollowupScore:
    model: str
    lq: str
    lp: str
    item_id: str
    condition: str
    score: Score
    abandoned: int | None


def score_followups(records: Iterable[Mapping], gate_path: str | Path) -> tuple[list[FollowupScore], dict]:
    """Score FC/RA records for eligible items only.

    Refuses (raises) without a verified gate, for a (model, lq) cell absent from the gate,
    or for a record generated before the gate was frozen. Records for ineligible items are
    counted and skipped, never scored. Eligibility is read from the gate only.
    """
    gate = load_verified_gate(gate_path)
    frozen_at = _parse_ts(gate["provenance"]["created_at"], "provenance.created_at")
    out: list[FollowupScore] = []
    skipped: dict[str, int] = defaultdict(int)
    for r in records:
        missing = [k for k in FOLLOWUP_FIELDS if k not in r]
        if missing:
            raise GateInputError(f"follow-up record missing fields {missing}")
        if r["condition"] not in FOLLOWUP_CONDITIONS:
            raise GateInputError(f"condition must be one of {FOLLOWUP_CONDITIONS}: {r['condition']!r}")
        cell = gate["cells"].get(f"{r['model']}|{r['lq']}")
        if cell is None:
            raise GateMissingError(f"gate has no cell for model={r['model']!r} lq={r['lq']!r}")
        if r["rotation"] != 0:
            raise GateInputError(
                f"follow-ups must continue the rotation-0 conversation; item {r['item_id']!r} has rotation {r['rotation']!r}"
            )
        if _parse_ts(r["generated_at"], "generated_at") < frozen_at:
            raise GateIntegrityError(
                f"follow-up for item {r['item_id']!r} was generated before the gate was frozen"
            )
        item = str(r["item_id"])
        if item not in cell["eligible_item_ids"]:
            skipped[f"{r['model']}|{r['lq']}"] += 1
            continue
        gold_index = cell["decisions"][item]["gold_index"]  # from the hashed turn-0 inputs
        if r["gold_index"] != gold_index:
            raise GateInputError(
                f"follow-up gold_index {r['gold_index']!r} for item {item!r} disagrees with the frozen gate ({gold_index})"
            )
        # Follow-ups continue the rotation-0 conversation (research.md §5.1).
        gold_letter = presented_gold_letter(gold_index, 0, N_OPTIONS)
        s = score(parse_answer(r["raw_output"], N_OPTIONS), gold_letter)
        out.append(FollowupScore(r["model"], r["lq"], r["lp"], item, r["condition"], s, abandonment(s)))
    return out, dict(skipped)
