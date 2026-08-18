"""Layer-0 tests for currency.py — the deterministic half of /retrofit.

The property that matters most is the LAST test: a repo at the kit version
with every requirement present yields an empty delta. That is the K1 gate
("re-running the retrofit is a no-op"), and it is what makes the migration
safe to run repeatedly on 46 repos.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest

import currency

_KIT = os.path.dirname(os.path.abspath(__file__))


def _touch(root, rel, body="x", exe=False):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p) or root, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(body)
    if exe:
        os.chmod(p, 0o755)
    return p


def _full_baseline(root):
    """Everything REQUIREMENTS['2.0.0'] asks for."""
    for f in ("CLAUDE.md", "ROADMAP.md", "DECISIONS.md", "INDEX.md", "LIBRARY.md"):
        _touch(root, f)
    # Declare whatever the kit's CURRENT version is, never a hardcoded one:
    # pinning "2.0.0" here made every one of these tests fail the moment 2.1.0
    # shipped, which is the test asserting the kit never moves rather than
    # asserting the property under test.
    _touch(root, "project.manifest.json",
           json.dumps({"kit_version": currency.kit_version(_KIT)}))
    os.makedirs(os.path.join(root, "traces"), exist_ok=True)
    # A REAL gate, not a stub: 2.2.0 asserts the gate FIRES on planted
    # identity paths, so a `leak_gate() { :; }` placeholder now correctly
    # reads as behind. The fixture's verify is autonomous's own leak_gate,
    # lifted verbatim, so the fixture is current for the same reason a real
    # repo is.
    real = os.path.join(_KIT, "..", "harness", "verify")
    with open(real, encoding="utf-8") as fh:
        _touch(root, "verify", fh.read(), exe=True)
    subprocess.run(["git", "init", "-q", root], check=True)   # leak_gate uses git grep
    _touch(root, ".github/workflows/ci.yml", "name: ci")
    _touch(root, ".gitattributes", "* text=auto eol=lf")


class TestVersionOrdering(unittest.TestCase):
    def test_pre_sorts_below_everything(self):
        self.assertLess(currency.parse_version("pre-2.0.0"), currency.parse_version("0.0.1"))
        self.assertLess(currency.parse_version(None), currency.parse_version("2.0.0"))

    def test_semver_compares_numerically_not_lexically(self):
        self.assertGreater(currency.parse_version("2.10.0"), currency.parse_version("2.9.0"))


class TestChangelogParse(unittest.TestCase):
    def test_reads_the_real_changelog(self):
        entries = currency.changelog_entries(_KIT)
        self.assertTrue(entries)
        self.assertEqual(entries[0][0], "2.0.0")

    def test_every_changelog_version_has_a_requirements_row(self):
        """The prose in CHANGELOG.md is the explanation; REQUIREMENTS is the
        gate. A version present in one and absent from the other means the
        retrofit will silently skip that migration."""
        for ver, *_ in currency.changelog_entries(_KIT):
            self.assertIn(ver, currency.REQUIREMENTS,
                          f"CHANGELOG {ver} has no REQUIREMENTS row")


class TestReport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_empty_repo_is_behind_by_everything(self):
        r = currency.report(self.tmp, _KIT)
        self.assertEqual(r["declared"], "pre-2.0.0")
        self.assertFalse(r["current"])
        # every non-tool-only CHANGELOG entry, not a fixed count — the point
        # is "behind by everything", which grows as the kit does
        expected = [v for v in currency.REQUIREMENTS if v not in currency.TOOL_ONLY]
        self.assertEqual(len(r["behind"]), len(expected))
        # the baseline entry is the one with real requirements
        base = next(b for b in r["behind"] if b["version"] == "2.0.0")
        self.assertEqual(len(base["missing"]), len(currency.REQUIREMENTS["2.0.0"]))

    def test_undeclared_but_complete_repo_is_still_behind(self):
        """Antiphon's shape: full harness, no kit_version. It is BEHIND —
        currency is declared, never inferred — but with an empty missing list,
        so the retrofit's only action is to write the declaration."""
        _full_baseline(self.tmp)
        _touch(self.tmp, "project.manifest.json", json.dumps({"survey": {}}))
        r = currency.report(self.tmp, _KIT)
        self.assertFalse(r["current"])
        self.assertEqual(r["behind"][0]["missing"], [])

    def test_declared_current_but_missing_items_is_reported_as_drift(self):
        """autonomous on 2026-08-17: declared 2.0.0 with no CLAUDE.md. A
        declaration the checks contradict must be LOUDER than no declaration."""
        _full_baseline(self.tmp)
        os.remove(os.path.join(self.tmp, "CLAUDE.md"))
        r = currency.report(self.tmp, _KIT)
        self.assertTrue(r["current"])
        self.assertIn("CLAUDE.md", r["declared_but_missing"])

    def test_verify_must_be_executable_not_just_present(self):
        """The Write tool does not set the exec bit (retrofit gotcha,
        2026-07-12). A verify that exists but cannot run is not a verify."""
        _full_baseline(self.tmp)
        os.chmod(os.path.join(self.tmp, "verify"), 0o644)
        r = currency.report(self.tmp, _KIT)
        self.assertIn("./verify", r["declared_but_missing"])

    def test_tool_only_bump_does_not_put_the_fleet_behind(self):
        """2.0.1 changed /retrofit, not what a repo must contain. A repo at
        2.0.0 must read CURRENT, or the checker manufactures 46 rows of
        'behind by nothing you can act on' — noise that gets the tool ignored."""
        _full_baseline(self.tmp)   # declares the current kit version
        r = currency.report(self.tmp, _KIT)
        self.assertTrue(r["current"])
        self.assertEqual(r["behind"], [])

    def test_current_and_complete_is_a_noop(self):
        """THE K1 GATE. Re-running the retrofit on a current repo must find
        nothing to do."""
        _full_baseline(self.tmp)
        r = currency.report(self.tmp, _KIT)
        self.assertTrue(r["current"])
        self.assertEqual(r["behind"], [])
        self.assertEqual(r["declared_but_missing"], [])


if __name__ == "__main__":
    unittest.main()


class TestProbeLeavesHarnessAlone(unittest.TestCase):
    """juce-rag 2026-08-18: the gate-fires probe runs the target's ./verify,
    whose record() overwrote .harness/last-verify.json with the probe's exit 1
    and deleted .harness/dirty — a red Stop hook for a PASSING check. The
    probe must restore both, byte for byte, including 'absent'."""

    def test_green_record_and_dirty_flag_survive_the_probe(self):
        with tempfile.TemporaryDirectory() as root:
            _full_baseline(root)
            hd = os.path.join(root, ".harness")
            os.makedirs(hd)
            green = b'{"target":"fast","exit":0,"git":"abc","at":"t"}'
            with open(os.path.join(hd, "last-verify.json"), "wb") as fh:
                fh.write(green)
            with open(os.path.join(hd, "dirty"), "wb") as fh:
                fh.write(b"1")
            currency._GATE_CACHE.clear()
            self.assertTrue(currency._gate_report(root)["posix"])   # gate fired (exit 1)
            with open(os.path.join(hd, "last-verify.json"), "rb") as fh:
                self.assertEqual(fh.read(), green)                 # ...and left no trace
            self.assertTrue(os.path.exists(os.path.join(hd, "dirty")))

    def test_absent_record_stays_absent(self):
        with tempfile.TemporaryDirectory() as root:
            _full_baseline(root)
            currency._GATE_CACHE.clear()
            currency._gate_report(root)
            self.assertFalse(os.path.exists(os.path.join(root, ".harness", "last-verify.json")))


class TestForeignPlantIsInvisible(unittest.TestCase):
    """mind-lathe, 2026-08-18: the probe plants INSIDE the target tree, so a
    concurrent `./verify fast` there read the plant and reported a leak in a
    file that vanished seconds later. The gate must be blind to a plant it
    does not own, and must still see the one it does."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        _full_baseline(self.root)
        self.plant = ".kit-currency-plant-99999.md"
        with open(os.path.join(self.root, self.plant), "w") as fh:
            fh.write("x " + "/" + "Users" + "/nobody/secret\n")   # assembled, never literal

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def _verify(self, own=None):
        env = dict(os.environ)
        env.pop("KIT_LEAK_PLANT", None)
        if own:
            env["KIT_LEAK_PLANT"] = own
        return subprocess.run(["./verify", "fast"], cwd=self.root, env=env,
                              capture_output=True, text=True)

    def test_unowned_plant_does_not_red_a_concurrent_verify(self):
        # The assertion is that the gate never NAMES the foreign plant. Exit
        # code is not usable here: the baseline fixture's verify is the kit
        # template, which exits 1 with NOT IMPLEMENTED by design. (Checked on
        # a real repo separately: autonomous exits 0 with a foreign plant.)
        r = self._verify()
        self.assertNotIn(self.plant, r.stderr + r.stdout)

    def test_owned_plant_still_fires(self):
        r = self._verify(own=self.plant)
        self.assertIn(self.plant, r.stderr + r.stdout)
        self.assertNotEqual(r.returncode, 0)

