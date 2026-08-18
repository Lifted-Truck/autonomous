"""The contract must not be able to define a field nobody can write.

hypersaw-001 round 2: the `absorbs` amendment updated the prose, the JSON
Schema and the quarantine rule, but not the label-opening regex — so a
conforming parser routed `| absorbs: …` to `extra`, and the quarantine rule
guarding it could never fire. A check that cannot fire reads exactly like a
check that passes (autonomous LIBRARY L0002; HYPERSAW L0032/L0024).

Caught by the first party to WRITE the field, not by its author or its first
reader. This test is the mechanical replacement for that luck.
"""
import json
import os
import re
import unittest

_CONTRACT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "contracts", "library-entry.md")

# Fields the parser DERIVES rather than reads from a labelled segment.
_DERIVED = {"id", "title", "entry_form", "extra"}


def _load():
    with open(_CONTRACT, encoding="utf-8") as fh:
        return fh.read()


class TestSchemaAndLabelRuleAgree(unittest.TestCase):
    def setUp(self):
        self.text = _load()
        block = re.search(r"```json\n(\{.*?\n\})\n```", self.text, re.S)
        self.assertIsNotNone(block, "contract must carry a JSON Schema block")
        self.props = set(json.loads(block.group(1))["properties"])
        m = re.search(r"\^\\s\*\((.*?)\)\\s\*:", self.text)
        self.assertIsNotNone(m, "contract must state the label-opening rule")
        self.labels = set(m.group(1).split("|"))

    def _writable(self):
        return self.props - _DERIVED - {p for p in self.props if p.endswith("_note")}

    def test_every_writable_field_can_be_opened(self):
        """THE GATE. A schema field with no label rule is unwritable, and the
        checks guarding it are unreachable."""
        unopenable = sorted(self._writable() - self.labels)
        self.assertEqual(unopenable, [],
                         f"schema defines {unopenable} but no segment can open them")

    def test_every_label_has_a_schema_field(self):
        """The reverse: a label the schema does not know produces a value with
        nowhere to land."""
        orphan = sorted(self.labels - self.props)
        self.assertEqual(orphan, [], f"label rule admits {orphan}, absent from schema")

    def test_absorbs_specifically(self):
        """Pinned by name because it is the one that got through, and a future
        'simplification' of the regex would silently reintroduce it."""
        self.assertIn("absorbs", self.labels)
        self.assertIn("absorbs", self.props)


if __name__ == "__main__":
    unittest.main()
