"""Layer-0 tests for the monitor's pure helpers. Deterministic, stdlib-only.

The check logic that reads real repos isn't unit-tested (it's I/O over the live
tree — the monitor run itself is the integration check); these pin the parsing
+ classification helpers, especially the status-prose false-positive guard that
must NOT flag a 'see ROADMAP' pointer or an incidental 'O0 gate' reference."""

import datetime
import json
import os
import shutil
import subprocess
import tempfile
import unittest

import monitor


def _write(d, name, content):
    p = os.path.join(d, name)
    os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(p) else None
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return d


class TestReadmeStaleness(unittest.TestCase):
    def test_last_verified_parsed(self):
        d = tempfile.mkdtemp()
        _write(d, "README.md", "# x\n\n*Last verified current: 2026-07-01.*\n")
        self.assertEqual(monitor.readme_last_verified(d), "2026-07-01")

    def test_absent_line(self):
        d = tempfile.mkdtemp()
        _write(d, "README.md", "# x\nno date here\n")
        self.assertIsNone(monitor.readme_last_verified(d))

    def test_days_since(self):
        self.assertEqual(
            monitor.days_since("2026-07-01", datetime.date(2026, 7, 31)), 30)


class TestStatusProse(unittest.TestCase):
    def prose(self, status):
        d = tempfile.mkdtemp()
        _write(d, "project.manifest.json", json.dumps({"status": status}))
        return monitor.manifest_status_prose(d)

    def test_flags_progress_glyph_and_words(self):
        self.assertIsNotNone(self.prose("O3 DONE, plugin builds ✅"))
        self.assertIsNotNone(self.prose("D2 CLOSED; analyst next"))

    def test_flags_overlong(self):
        self.assertIsNotNone(self.prose("RATIFIED " + "x" * 260))

    def test_pointer_is_clean(self):
        # the correct post-Decision-28 form must NOT be flagged
        self.assertIsNone(self.prose(
            "RATIFIED 2026-07-13 at the O0 gate (DECISIONS #10). "
            "Phase/progress status lives EXCLUSIVELY in ROADMAP.md."))
        self.assertIsNone(self.prose("RATIFIED 2026-07-10 (E0 gate)"))


class TestLeakGateDetection(unittest.TestCase):
    def test_present_absent_missing(self):
        d = tempfile.mkdtemp()
        _write(d, "verify", "fast() { leak_gate || ok=1; }")
        self.assertIs(monitor.verify_has_leak_gate(d), True)
        d2 = tempfile.mkdtemp()
        _write(d2, "verify", "fast() { pytest; }")
        self.assertIs(monitor.verify_has_leak_gate(d2), False)
        self.assertIsNone(monitor.verify_has_leak_gate(tempfile.mkdtemp()))


class TestStatusShapeResilience(unittest.TestCase):
    """monitor crashed the ENTIRE fleet dashboard because one repo shipped a
    structured (dict) manifest status. A crashed monitor reports nothing, which
    is indistinguishable from a healthy fleet — the exact silent failure this
    tool exists to catch."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _manifest(self, status):
        with open(os.path.join(self.tmp, "project.manifest.json"), "w") as f:
            json.dump({"status": status}, f)

    def test_dict_status_does_not_raise(self):
        self._manifest({"ratified": None, "note": "Phase state lives in ROADMAP.md only."})
        self.assertIsNone(monitor.manifest_status_prose(self.tmp))

    def test_dict_status_still_detects_prose(self):
        """Structured shape must not become a way to smuggle progress prose past
        the check — flatten and scan the strings inside."""
        self._manifest({"ratified": None, "note": "Phase 3 DONE and shipped ✅"})
        self.assertIsNotNone(monitor.manifest_status_prose(self.tmp))

    def test_list_and_scalar_status_do_not_raise(self):
        for shape in ([{"a": 1}, "x"], 42, None, True):
            with self.subTest(shape=shape):
                self._manifest(shape)
                monitor.manifest_status_prose(self.tmp)  # must not raise


class TestDormancy(unittest.TestCase):
    """Dormancy (antiphon-001): a deliberately-inactive green repo must be
    distinguishable from an abandoned one — WITHOUT becoming a way to silence
    rot forever. So it expires, and the expiry is louder than what it muted."""

    def setUp(self):
        # A REAL git repo: check_repo early-returns {} for non-git dirs, so a
        # bare tmpdir silently tests nothing at all.
        self.tmp = tempfile.mkdtemp()
        subprocess.run(["git", "init", "-q", self.tmp], check=True)
        self.today = datetime.date(2026, 8, 20)
        _write(self.tmp, "CLAUDE.md", "x")
        _write(self.tmp, "README.md",
               "*Last verified current: 2026-07-13.*")   # 38d stale at self.today

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _dormant(self, **kw):
        _write(self.tmp, "project.manifest.json", json.dumps({"dormant": kw}))

    def _checks(self):
        return monitor.check_repo({"name": "t", "path": self.tmp}, self.today, 30)

    def test_fixture_is_actually_a_repo(self):
        """Guard the guard: if this fixture stops being a git repo, every other
        test in this class passes vacuously on an empty dict."""
        self.assertTrue(monitor.sweep.derive_status(self.tmp)["git"])

    def test_live_dormancy_suppresses_stale(self):
        self._dormant(since="2026-07-13", reason="conditions unmet", review_by="2026-10-13")
        c = self._checks()
        self.assertNotIn("STALE", c)
        self.assertIn("DORMANT", c)
        self.assertEqual(c["DORMANT"][0], "INFO")

    def test_expired_dormancy_is_louder_than_what_it_muted(self):
        self._dormant(since="2026-07-13", reason="conditions unmet", review_by="2026-08-01")
        c = self._checks()
        self.assertIn("DORMANT-EXPIRED", c)
        self.assertEqual(c["DORMANT-EXPIRED"][0], "WARN")
        self.assertIn("STALE", c)   # expiry restores the underlying warning too

    def test_missing_review_by_is_ignored(self):
        """The incomplete form must fail toward NOISE, not toward silence —
        otherwise omitting review_by becomes a permanent mute."""
        self._dormant(since="2026-07-13", reason="no review date")
        c = self._checks()
        self.assertNotIn("DORMANT", c)
        self.assertIn("STALE", c)


class TestDormancyDefersMaintenanceNotSecurity(unittest.TestCase):
    """The line that keeps dormancy honest: a repo nobody develops still leaks
    in public. Dormancy is permission to skip CHORES, never permission to stop
    looking for exposure."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        subprocess.run(["git", "init", "-q", self.tmp], check=True)
        subprocess.run(["git", "-C", self.tmp, "remote", "add", "origin",
                        "https://example.invalid/x.git"], check=True)
        self.today = datetime.date(2026, 8, 17)
        _write(self.tmp, "CLAUDE.md", "x")
        _write(self.tmp, "README.md", "*Last verified current: 2026-01-01.*")
        _write(self.tmp, "project.manifest.json", json.dumps({
            "dormant": {"since": "2026-07-12", "reason": "delivered",
                        "review_by": "2027-02-17"}}))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _checks(self, today=None):
        return monitor.check_repo({"name": "t", "path": self.tmp},
                                  today or self.today, 30)

    def test_maintenance_warnings_are_deferred(self):
        c = self._checks()
        for chore in ("NO-CI", "STALE", "KIT-PRE", "GAPS"):
            self.assertNotIn(chore, c, f"{chore} should be deferred while dormant")
        self.assertIn("DORMANT", c)

    def test_a_leak_still_fires_while_dormant(self):
        """A dormant PUBLIC repo that leaks is not less exposed for being
        quiet. If this ever passes, dormancy has become a hiding place."""
        _write(self.tmp, "notes.md", "path /Users/someone/secret/thing\n")
        subprocess.run(["git", "-C", self.tmp, "add", "-A"], check=True)
        c = self._checks()
        self.assertTrue("LEAK" in c or "PATH" in c,
                        "a leak must fire regardless of dormancy")

    def test_expiry_restores_the_deferred_chores(self):
        c = self._checks(datetime.date(2027, 6, 1))
        self.assertIn("DORMANT-EXPIRED", c)
        self.assertIn("NO-CI", c)
        self.assertIn("STALE", c)


if __name__ == "__main__":
    unittest.main()
