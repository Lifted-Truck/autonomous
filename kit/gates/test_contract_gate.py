"""Layer-0 tests for contract_gate. Deterministic, stdlib-only.

FOUNDATIONS verified these four cases before offering the gate; they are
re-implemented here because a gate landed on someone else's word is a gate
nobody has actually run. The fourth is the one that matters most for kit-core:
the check must be INERT in the majority of projects that are not composite, and
must say `skip` rather than passing silently — a gate that passes in silence is
indistinguishable from one that never ran.
"""

import json
import os
import shutil
import tempfile
import unittest

from contract_gate import contract_gate


class TestContractGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _manifest(self, obj):
        with open(os.path.join(self.tmp, "project.manifest.json"), "w") as f:
            json.dump(obj, f)

    def _contract(self, name, body):
        p = os.path.join(self.tmp, name)
        os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(p) else None
        with open(p, "w") as f:
            f.write(body)

    def test_versioned_contract_passes_and_reports_version(self):
        self._manifest({"composite": {"contract": "docs/c.md"}})
        self._contract("docs/c.md", "# C\ncontract-version: 0.1.0\n")
        ok, msg = contract_gate(self.tmp)
        self.assertTrue(ok)
        self.assertIn("0.1.0", msg)

    def test_unversioned_contract_is_red_and_names_the_file(self):
        self._manifest({"composite": {"contract": "docs/c.md"}})
        self._contract("docs/c.md", "# C\nno version here\n")
        ok, msg = contract_gate(self.tmp)
        self.assertFalse(ok)
        self.assertIn("docs/c.md", msg)

    def test_missing_contract_file_is_red_and_names_the_path(self):
        self._manifest({"composite": {"contract": "docs/gone.md"}})
        ok, msg = contract_gate(self.tmp)
        self.assertFalse(ok)
        self.assertIn("docs/gone.md", msg)

    def test_non_composite_project_skips_audibly(self):
        self._manifest({"survey": {}})
        ok, msg = contract_gate(self.tmp)
        self.assertTrue(ok)
        self.assertIn("skip", msg)

    def test_no_manifest_skips_audibly(self):
        ok, msg = contract_gate(self.tmp)
        self.assertTrue(ok)
        self.assertIn("skip", msg)

    def test_malformed_manifest_skips_rather_than_crashing(self):
        """A gate that raises on bad JSON takes the whole verify down with it —
        the same failure that killed the fleet monitor (Decision 35)."""
        with open(os.path.join(self.tmp, "project.manifest.json"), "w") as f:
            f.write("{not json")
        ok, msg = contract_gate(self.tmp)
        self.assertTrue(ok)
        self.assertIn("skip", msg)

    def test_version_must_be_at_line_start(self):
        """Prose mentioning the phrase must not satisfy the gate — otherwise a
        contract that merely DISCUSSES versioning passes."""
        self._manifest({"composite": {"contract": "c.md"}})
        self._contract("c.md", "see the contract-version: field described above\n")
        ok, _ = contract_gate(self.tmp)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
