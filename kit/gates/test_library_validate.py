"""Tests for library_validate. Every case here is either a rule from the
contract or a bug this validator shipped on its FIRST run against real corpora.

It reported autonomous's own correct `origin` as broken and HYPERSAW's correct
`added` as malformed. A checker that cries wolf on its first run is worse than
none — it teaches the reader to skip it — so those two are pinned by name.
"""
import os
import tempfile
import unittest

import library_validate as lv

GOOD = ("[L0001] A title | canonical | added: 2026-08-14 | tags: x | "
        "lesson: L | evidence: E | falsifier: F")


class TestConformingEntries(unittest.TestCase):
    def test_minimal_valid_entry(self):
        self.assertEqual(lv.validate_entry(GOOD), [])

    def test_labelled_tier_is_equally_valid(self):
        e = GOOD.replace("| canonical |", "| tier: canonical |")
        self.assertEqual(lv.validate_entry(e), [])

    def test_absorbs_list_with_annotation(self):
        """HYPERSAW's real 2026-08-18 emission. This is the case the whole
        amendment existed for; if it ever fails, the amendment is inert again."""
        e = GOOD + (" | absorbs: L0011, L0021, L0034 — shell-path, superset and "
                    "layer blindness respectively; consolidated 2026-08-11")
        self.assertEqual(lv.validate_entry(e), [])

    def test_prose_pipes_survive(self):
        e = ("[L0002] T | canonical | added: 2026-08-14 | tags: x | "
             "lesson: a threshold on |x[n]-x[n-1]| is the slope | "
             "evidence: E | falsifier: F")
        self.assertEqual(lv.validate_entry(e), [])


class TestFirstRunFalsePositives(unittest.TestCase):
    """The two bugs, pinned so a 'simplification' cannot reintroduce them."""

    def test_origin_uses_the_child_hash_shape(self):
        """`origin` is `<child>#Lxxxx`, NOT `L\\d{4}` — the one field the
        contract gives a different pattern. Applying the local shape reported
        autonomous's own valid L0001 as broken."""
        e = GOOD + " | origin: life-os-app#L0002"
        self.assertEqual(lv.validate_entry(e), [])

    def test_unknown_label_goes_to_extra_not_into_the_open_field(self):
        """An unknown `label:` segment is collected under `extra` (contract
        §Segment rules). Folding it in glued `consolidated:` onto `added:` and
        reported a valid date as malformed."""
        e = ("[L0003] T | canonical | added: 2026-08-10 | consolidated: 2026-08-11 "
             "| tags: x | lesson: L | evidence: E | falsifier: F")
        self.assertEqual(lv.validate_entry(e), [])

    def test_one_finding_per_field_not_per_comma(self):
        """A prose value split on its own commas produced three findings for
        one defect."""
        e = GOOD + " | supersedes: nothing; escalated, then again, and again"
        self.assertEqual(len(lv.validate_entry(e)), 1)


class TestRealNonConformance(unittest.TestCase):
    def test_missing_required_field(self):
        e = "[L0004] T | canonical | added: 2026-08-14 | tags: x | lesson: L | evidence: E"
        self.assertTrue(any("falsifier" in f for f in lv.validate_entry(e)))

    def test_placeholder_on_a_required_field_is_missing_information(self):
        e = GOOD.replace("falsifier: F", "falsifier: —")
        self.assertTrue(any("placeholder" in f for f in lv.validate_entry(e)))

    def test_supersedes_is_single_valued(self):
        e = GOOD + " | supersedes: L0011, L0021"
        self.assertTrue(any("single-valued" in f for f in lv.validate_entry(e)))

    def test_bad_tier_and_date(self):
        self.assertTrue(any("tier" in f for f in
                            lv.validate_entry(GOOD.replace("| canonical |", "| retracted |"))))
        self.assertTrue(any("added" in f for f in
                            lv.validate_entry(GOOD.replace("2026-08-14", "Aug 14"))))


class TestOwnCorpus(unittest.TestCase):
    """PAIRED control (HYPERSAW round 4). The clean read alone cannot fail:
    if `validate_file` became a no-op it would still return [], and the whole
    suite passed 12/12 against a neutered one — every other test exercises
    `validate_entry` and never touches the file-level path. A validator that
    stops crying wolf is indistinguishable from one that stopped looking, so
    the zero must be paired with a corruption of the SAME file that must
    read non-zero."""

    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        self.lib = os.path.join(here, "..", "..", "LIBRARY.md")

    def test_autonomous_library_conforms_to_its_own_contract(self):
        """The standards repo must not ship a LIBRARY that fails the contract
        it authored — the same self-check as kit currency."""
        self.assertEqual(lv.validate_file(self.lib), [])

    def test_the_zero_is_earned_not_vacuous(self):
        """Corrupt a copy of the real file and require the file-level path to
        notice. This is the control that makes the test above mean something."""
        with open(self.lib, encoding="utf-8") as fh:
            text = fh.read()
        broken = text.replace("| canonical |", "| retracted |", 1)
        self.assertNotEqual(broken, text, "fixture no longer matches the corpus")
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(broken)
            path = fh.name
        try:
            self.assertTrue(lv.validate_file(path),
                            "file-level path did not notice a planted defect")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()


class CorpusShapes(unittest.TestCase):
    """Two shapes real projects write that the contract admitted in spirit and
    the validator rejected in fact (distillery report-003 §1). Each test names
    the project that forced it, per distillery's own regression discipline."""

    def test_capitalised_labels_parse_case_insensitively(self):
        # resume-workshop writes `Lesson:` / `Evidence:` / `Falsifier:`
        line = ("[L0001] a title | tier: candidate | added: 2026-08-01 | "
                "tags: x | Lesson: learned | Evidence: seen | Falsifier: f")
        fields, bad = lv.parse_entry(line)
        self.assertEqual(fields.get("lesson"), "learned")
        self.assertEqual(fields.get("evidence"), "seen")
        self.assertEqual(lv.validate_entry(line), [])

    def test_backtick_wrapped_segments_parse(self):
        # Tonality writes block fields as code spans joined by pipes
        line = ("[L0002] t | `tier: candidate` | `added: 2026-08-01` | "
                "`tags: x` | `lesson: l` | `evidence: e` | `falsifier: f`")
        fields, bad = lv.parse_entry(line)
        self.assertEqual(fields.get("tier"), "candidate")
        self.assertEqual(lv.validate_entry(line), [])

