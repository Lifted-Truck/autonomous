"""Layer-0 tests for the monitor's pure helpers. Deterministic, stdlib-only.

The check logic that reads real repos isn't unit-tested (it's I/O over the live
tree — the monitor run itself is the integration check); these pin the parsing
+ classification helpers, especially the status-prose false-positive guard that
must NOT flag a 'see ROADMAP' pointer or an incidental 'O0 gate' reference."""

import datetime
import json
import os
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


if __name__ == "__main__":
    unittest.main()
