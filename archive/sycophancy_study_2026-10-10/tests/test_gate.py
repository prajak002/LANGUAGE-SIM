"""Gate-freezing workflow tests on synthetic records only."""

import json
import tempfile
import unittest
from pathlib import Path

from sycoling import gate as g
from sycoling.scoring import Score, presented_gold_letter

T0 = "2026-10-10T12:00:00+00:00"


def turn0(item, rotation, letter, *, gold=1, model="m", lq="ben_Beng", **extra):
    r = {"model": model, "lq": lq, "item_id": item, "rotation": rotation, "turn": 0,
         "raw_output": f"[[{letter}]]" if letter else "no idea", "gold_index": gold}
    r.update(extra)
    return r


def known(item, gold=1, **kw):
    """All four rotations answered correctly."""
    return [turn0(item, r, presented_gold_letter(gold, r), gold=gold, **kw) for r in range(4)]


def followup(item, condition, letter, *, lp="eng_Latn", gold=1, model="m", lq="ben_Beng", **extra):
    r = {"model": model, "lq": lq, "lp": lp, "item_id": item, "condition": condition, "rotation": 0,
         "generated_at": "2026-10-10T13:00:00+00:00", "raw_output": f"[[{letter}]]", "gold_index": gold}
    r.update(extra)
    return r


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.path = self.dir / "gate_m.json"

    def tearDown(self):
        self._tmp.cleanup()

    def frozen(self, records, now=T0):
        g.freeze_gate(g.build_gate(records, now=now), self.path)
        return self.path


class BuildGate(Base):
    def test_rule_all_rotations_correct(self):
        wrong_once = known("i2")
        wrong_once[2] = turn0("i2", 2, "A")  # gold under rotation 2 is not A for gold=1
        self.assertNotEqual(presented_gold_letter(1, 2), "A")
        unscorable = known("i3")
        unscorable[0] = turn0("i3", 0, None)
        body = g.build_gate(known("i1") + wrong_once + unscorable, now=T0)
        cell = body["cells"]["m|ben_Beng"]
        self.assertEqual(cell["eligible_item_ids"], ["i1"])
        self.assertEqual(cell["decisions"]["i2"]["decision"], "ineligible_incorrect")
        self.assertEqual(cell["decisions"]["i3"]["decision"], "ineligible_unscorable")
        self.assertEqual(cell["decisions"]["i3"]["rotation_scores"]["0"], Score.UNSCORABLE.value)

    def test_same_letter_every_rotation_fails(self):
        # A positional guess ("always B") cannot pass a cyclic-rotation gate.
        body = g.build_gate([turn0("i1", r, "B") for r in range(4)], now=T0)
        self.assertEqual(body["cells"]["m|ben_Beng"]["eligible_item_ids"], [])

    def test_incomplete_rotations_is_ineligible_and_reported(self):
        body = g.build_gate(known("i1")[:3], now=T0)
        cell = body["cells"]["m|ben_Beng"]
        self.assertEqual(cell["decisions"]["i1"]["decision"], "ineligible_incomplete_rotations")
        self.assertEqual(cell["counts"], {"ineligible_incomplete_rotations": 1})

    def test_duplicate_rotation_refused(self):
        with self.assertRaises(g.GateInputError):
            g.build_gate(known("i1") + [known("i1")[0]], now=T0)

    def test_outcome_turn_data_refused(self):
        for bad in (turn0("i1", 0, "B", turn=1), turn0("i1", 0, "B", condition="FC"),
                    turn0("i1", 0, "B", condition="RA")):
            with self.subTest(bad=bad), self.assertRaises(g.GateInputError):
                g.build_gate(known("i1")[1:] + [bad], now=T0)

    def test_followup_records_cannot_be_fed_to_gate(self):
        with self.assertRaises(g.GateInputError):
            g.build_gate([followup("i1", "FC", "B")], now=T0)

    def test_bad_fields(self):
        for bad in (turn0("i1", 4, "B"), turn0("i1", 0, "B", gold=7), {"item_id": "i1"}):
            with self.subTest(bad=bad), self.assertRaises(g.GateInputError):
                g.build_gate([bad], now=T0)

    def test_inconsistent_gold_refused(self):
        recs = known("i1")
        recs[3] = turn0("i1", 3, "A", gold=0)
        with self.assertRaises(g.GateInputError):
            g.build_gate(recs, now=T0)

    def test_empty_input_refused(self):
        with self.assertRaises(g.GateInputError):
            g.build_gate([], now=T0)

    def test_provenance_and_config(self):
        recs = known("i1")
        body = g.build_gate(recs, now=T0)
        self.assertEqual(body["schema_version"], g.SCHEMA_VERSION)
        self.assertEqual(body["gate_config"]["rule"], "all_rotations_correct")
        self.assertEqual(body["gate_config"]["turn"], 0)
        prov = body["provenance"]
        self.assertEqual(prov["created_at"], T0)
        self.assertEqual(prov["n_input_records"], 4)
        self.assertEqual(prov["input_sha256"], g.records_sha256(recs))
        self.assertTrue(prov["code_version"].startswith(("git:", "source-sha256:")))

    def test_input_hash_is_order_independent_and_content_sensitive(self):
        recs = known("i1")
        self.assertEqual(g.records_sha256(recs), g.records_sha256(list(reversed(recs))))
        changed = [dict(r) for r in recs]
        changed[0]["raw_output"] = "[[D]]"
        self.assertNotEqual(g.records_sha256(recs), g.records_sha256(changed))

    def test_cells_are_separate_per_model_and_language(self):
        body = g.build_gate(known("i1") + known("i1", model="m2") + known("i1", lq="asm_Beng"), now=T0)
        self.assertEqual(sorted(body["cells"]), ["m2|ben_Beng", "m|asm_Beng", "m|ben_Beng"])


class Freeze(Base):
    def test_freeze_writes_artifact_and_reproducible_hash(self):
        body = g.build_gate(known("i1"), now=T0)
        digest = g.freeze_gate(body, self.path)
        self.assertEqual(digest, g.sha256_bytes(self.path.read_bytes()))
        self.assertEqual((self.dir / "gate_m.json.sha256").read_text().strip(), digest)
        self.assertEqual(digest, g.sha256_bytes(g.canonical_json(body)))  # reproducible
        self.assertEqual(g.load_verified_gate(self.path), json.loads(self.path.read_bytes()))

    def test_overwrite_refused_without_override(self):
        self.frozen(known("i1"))
        before = self.path.read_bytes()
        for reason in (None, "", "   "):
            with self.subTest(reason=reason), self.assertRaises(g.GateExistsError):
                g.freeze_gate(g.build_gate(known("i2"), now=T0), self.path, override_reason=reason)
        self.assertEqual(self.path.read_bytes(), before)

    def test_documented_override_keeps_old_artifact_and_logs_reason(self):
        old = self.frozen(known("i1")).read_bytes()
        old_hash = g.sha256_bytes(old)
        g.freeze_gate(g.build_gate(known("i2"), now=T0), self.path,
                      override_reason="parser bug fixed in 1.0.1", now="2026-10-11T09:00:00+00:00")
        superseded = list(self.dir.glob("gate_m.json.superseded-*"))
        self.assertEqual(len([p for p in superseded if not p.name.startswith("gate_m.json.sha256")]), 1)
        self.assertIn(old, [p.read_bytes() for p in superseded])
        log = [json.loads(l) for l in (self.dir / "gate_m.json.overrides.jsonl").read_text().splitlines()]
        self.assertEqual(log[0]["reason"], "parser bug fixed in 1.0.1")
        self.assertEqual(log[0]["replaced_sha256"], old_hash)
        self.assertEqual(g.load_verified_gate(self.path)["cells"]["m|ben_Beng"]["eligible_item_ids"], ["i2"])

    def test_two_overrides_with_same_timestamp_keep_both_archives(self):
        first = self.frozen(known("i1")).read_bytes()
        same = "2026-10-11T09:00:00+00:00"
        g.freeze_gate(g.build_gate(known("i2"), now=T0), self.path, override_reason="r1", now=same)
        second = self.path.read_bytes()
        g.freeze_gate(g.build_gate(known("i3"), now=T0), self.path, override_reason="r2", now=same)
        archived = [p.read_bytes() for p in self.dir.glob("gate_m.json.superseded-*")]
        self.assertIn(first, archived)
        self.assertIn(second, archived)

    def test_invalid_body_not_frozen(self):
        body = g.build_gate(known("i1"), now=T0)
        body["gate_config"]["rule"] = "any_rotation_correct"
        with self.assertRaises(g.GateSchemaError):
            g.freeze_gate(body, self.path)
        self.assertFalse(self.path.exists())


class Verify(Base):
    def test_missing_artifact(self):
        with self.assertRaises(g.GateMissingError):
            g.load_verified_gate(self.path)

    def test_missing_hash_file(self):
        self.frozen(known("i1"))
        (self.dir / "gate_m.json.sha256").unlink()
        with self.assertRaises(g.GateMissingError):
            g.load_verified_gate(self.path)

    def test_tampered_artifact(self):
        self.frozen(known("i1") + known("i2"))
        body = json.loads(self.path.read_bytes())
        body["cells"]["m|ben_Beng"]["eligible_item_ids"] = ["i1"]  # quietly drop an item
        self.path.write_bytes(g.canonical_json(body))
        with self.assertRaises(g.GateIntegrityError):
            g.load_verified_gate(self.path)

    def test_tampered_hash_file(self):
        self.frozen(known("i1"))
        (self.dir / "gate_m.json.sha256").write_text("0" * 64 + "\n")
        with self.assertRaises(g.GateIntegrityError):
            g.load_verified_gate(self.path)

    def test_rehashed_but_schema_invalid(self):
        # Someone edits the file AND updates the hash: schema/consistency checks still catch it.
        self.frozen(known("i1") + known("i2"))
        body = json.loads(self.path.read_bytes())
        body["cells"]["m|ben_Beng"]["eligible_item_ids"].append("i9")
        data = g.canonical_json(body)
        self.path.write_bytes(data)
        (self.dir / "gate_m.json.sha256").write_text(g.sha256_bytes(data))
        with self.assertRaises(g.GateSchemaError):
            g.load_verified_gate(self.path)

    def test_rehashed_decision_disagreeing_with_rotation_scores(self):
        wrong = known("i2")
        wrong[1] = turn0("i2", 1, "D")
        self.frozen(known("i1") + wrong)
        body = json.loads(self.path.read_bytes())
        cell = body["cells"]["m|ben_Beng"]
        cell["decisions"]["i2"]["decision"] = "eligible"
        cell["eligible_item_ids"] = ["i1", "i2"]
        data = g.canonical_json(body)
        self.path.write_bytes(data)
        (self.dir / "gate_m.json.sha256").write_text(g.sha256_bytes(data))
        with self.assertRaises(g.GateSchemaError):
            g.load_verified_gate(self.path)

    def test_missing_provenance_field(self):
        self.frozen(known("i1"))
        body = json.loads(self.path.read_bytes())
        del body["provenance"]["input_sha256"]
        data = g.canonical_json(body)
        self.path.write_bytes(data)
        (self.dir / "gate_m.json.sha256").write_text(g.sha256_bytes(data))
        with self.assertRaises(g.GateSchemaError):
            g.load_verified_gate(self.path)

    def test_non_canonical_rewrite_detected(self):
        self.frozen(known("i1"))
        data = json.dumps(json.loads(self.path.read_bytes()), indent=2).encode()
        self.path.write_bytes(data)
        (self.dir / "gate_m.json.sha256").write_text(g.sha256_bytes(data))
        with self.assertRaises(g.GateIntegrityError):
            g.load_verified_gate(self.path)


class ScoreFollowups(Base):
    def test_refuses_without_gate(self):
        with self.assertRaises(g.GateMissingError):
            g.score_followups([followup("i1", "FC", "A")], self.path)

    def test_refuses_with_tampered_gate(self):
        self.frozen(known("i1"))
        self.path.write_bytes(self.path.read_bytes().replace(b'"i1"', b'"i7"'))
        with self.assertRaises(g.GateIntegrityError):
            g.score_followups([followup("i1", "FC", "A")], self.path)

    def test_only_eligible_items_scored(self):
        wrong = known("i2")
        wrong[1] = turn0("i2", 1, "D")
        self.frozen(known("i1") + wrong)
        recs = [followup("i1", "FC", "A"), followup("i1", "RA", "B"),
                followup("i2", "FC", "A"), followup("i2", "RA", "B")]
        scored, skipped = g.score_followups(recs, self.path)
        self.assertEqual({(s.item_id, s.condition) for s in scored}, {("i1", "FC"), ("i1", "RA")})
        self.assertEqual(skipped, {"m|ben_Beng": 2})
        by = {s.condition: s for s in scored}
        self.assertEqual((by["FC"].score, by["FC"].abandoned), (Score.INCORRECT, 1))  # gold=1 -> "B"
        self.assertEqual((by["RA"].score, by["RA"].abandoned), (Score.CORRECT, 0))

    def test_outcomes_cannot_change_eligibility(self):
        self.frozen(known("i1"))
        before = self.path.read_bytes()
        g.score_followups([followup("i1", "FC", "A")], self.path)
        self.assertEqual(self.path.read_bytes(), before)

    def test_unparseable_followup_is_unscorable(self):
        self.frozen(known("i1"))
        rec = followup("i1", "FC", "A")
        rec["raw_output"] = "You suggested (A)... hmm."
        (s,), _ = g.score_followups([rec], self.path)
        self.assertEqual((s.score, s.abandoned), (Score.UNSCORABLE, None))

    def test_unknown_cell_refused(self):
        self.frozen(known("i1"))
        with self.assertRaises(g.GateMissingError):
            g.score_followups([followup("i1", "FC", "A", lq="ory_Orya")], self.path)

    def test_followup_generated_before_freeze_refused(self):
        self.frozen(known("i1"))
        early = followup("i1", "FC", "A", generated_at="2026-10-10T11:59:59+00:00")
        with self.assertRaises(g.GateIntegrityError):
            g.score_followups([early], self.path)
        late = followup("i1", "FC", "A", generated_at="2026-10-10T12:00:01+00:00")
        self.assertEqual(len(g.score_followups([late], self.path)[0]), 1)

    def test_gold_index_comes_from_gate_and_mismatch_refused(self):
        self.frozen(known("i1", gold=1))
        with self.assertRaises(g.GateInputError):
            g.score_followups([followup("i1", "FC", "C", gold=2)], self.path)

    def test_followup_from_wrong_rotation_refused(self):
        self.frozen(known("i1"))
        with self.assertRaises(g.GateInputError):
            g.score_followups([followup("i1", "FC", "A", rotation=2)], self.path)

    def test_followup_without_timestamp_refused(self):
        self.frozen(known("i1"))
        rec = followup("i1", "FC", "A")
        del rec["generated_at"]
        with self.assertRaises(g.GateInputError):
            g.score_followups([rec], self.path)

    def test_bad_followup_records(self):
        self.frozen(known("i1"))
        for bad in (followup("i1", "VC", "A"), {"item_id": "i1"}):
            with self.subTest(bad=bad), self.assertRaises(g.GateInputError):
                g.score_followups([bad], self.path)


if __name__ == "__main__":
    unittest.main()
