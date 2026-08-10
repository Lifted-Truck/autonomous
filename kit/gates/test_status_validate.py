"""Contract tests for `status.1`.

Fixtures are dispatch's, filed verbatim in
`integrations/dispatch/contract-tests-status1.md` (dispatch-001) and landed
here per INTEGRATIONS §3 — consumer-authored, resident-landed. A consumer
declares "I depend on X" and this suite is what makes that declaration
executable: a boundary change that breaks dispatch fails autonomous's build,
which is the whole point of the arrangement.

The third fixture is the interesting one. It pins error GRANULARITY, not just
rejection — four named findings. A validator that rejects the right document for
the wrong reason passes a pass/fail test and is useless to a consumer trying to
repair its own output, so "it returned non-empty" is not good enough.
"""

import json
import os
import unittest

import status_validate

_FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "status1")


def _load(name):
    with open(os.path.join(_FIX, name), encoding="utf-8") as f:
        return json.load(f)


class TestStatus1Fixtures(unittest.TestCase):
    def test_valid_parses_with_zero_errors(self):
        self.assertEqual(status_validate.validate(_load("valid.json")), [])

    def test_quiet_day_is_a_record_not_an_absence(self):
        """`quiet: true` with empty lists is a VALID collected record. If this
        ever fails, consumers lose the only signal separating 'nothing changed'
        from 'never collected' (contract §Semantics)."""
        self.assertEqual(status_validate.validate(_load("quiet.json")), [])

    def test_missing_field_is_rejected_with_the_four_named_findings(self):
        findings = status_validate.validate(_load("missing-field.json"))
        joined = " | ".join(findings)
        self.assertTrue(findings, "must be rejected")
        for expected in (
            "missing required `quiet`",                 # root
            "last_verify: missing required `ts`",
            "recent.commits[0]: missing required `subject`",
            "recent.lessons[0]",                        # not matching L\\d{4}
        ):
            self.assertIn(expected, joined, f"missing finding: {expected}")


class TestStatus1Edges(unittest.TestCase):
    """Cases the fixtures do not cover. Added by the resident, not the consumer —
    dispatch pinned what IT depends on; these guard the validator itself."""

    def test_wrong_schema_id_is_rejected(self):
        doc = _load("valid.json")
        doc["schema"] = "status.2"
        self.assertTrue(any("schema" in f for f in status_validate.validate(doc)))

    def test_quiet_must_be_boolean_not_truthy(self):
        """`"quiet": "true"` is the classic JSON mistake and would read as a
        quiet day to any consumer doing a truthiness check."""
        doc = _load("valid.json")
        doc["quiet"] = "false"
        self.assertTrue(any("quiet" in f for f in status_validate.validate(doc)))

    def test_gate_state_enum_is_closed(self):
        doc = _load("valid.json")
        doc["roadmap_phase"]["gate_state"] = "shipped"
        self.assertTrue(any("gate_state" in f for f in status_validate.validate(doc)))

    def test_optional_blocks_may_be_absent(self):
        """Only schema/project/ts/quiet are required. A minimal record must pass,
        or every project is forced to fabricate phase and verify data it lacks."""
        self.assertEqual(status_validate.validate({
            "schema": "status.1", "project": "x",
            "ts": "2026-08-09T00:00:00Z", "quiet": True,
        }), [])

    def test_non_object_root_does_not_crash(self):
        self.assertTrue(status_validate.validate([1, 2, 3]))


if __name__ == "__main__":
    unittest.main()
