"""Layer-0 tests for s4_scan. Deterministic, stdlib-only, NO network.

The network-touching helpers (`audit_branches`, `merged_audit_heads`,
`open_prs`) are monkeypatched, because a test that hits GitHub fails in CI for
reasons unrelated to the change — and a check whose tests are flaky gets
skipped, and a skipped check reports nothing (Decision 35 again).
"""

import datetime
import os
import shutil
import tempfile
import unittest
from unittest import mock

import s4_scan

TODAY = datetime.date(2026, 8, 14)


class TestNewestResearchDate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, "research", "proposals"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _touch(self, rel):
        p = os.path.join(self.tmp, rel)
        open(p, "w").close()

    def test_picks_newest_across_research_and_proposals(self):
        self._touch("research/2026-07-10-survey.md")
        self._touch("research/proposals/2026-08-10.proposal.md")
        self._touch("research/BIBLIOGRAPHY.md")            # undated, ignored
        self.assertEqual(s4_scan.newest_research_date(self.tmp), "2026-08-10")

    def test_none_when_nothing_dated(self):
        self._touch("research/README.md")
        self.assertIsNone(s4_scan.newest_research_date(self.tmp))


class TestScan(unittest.TestCase):
    """scan() with the network mocked to controlled answers."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, "research"))
        open(os.path.join(self.tmp, "research", "2026-08-10-x.md"), "w").close()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _scan(self, branches, merged, prs, today=TODAY, s4_days=35):
        with mock.patch.object(s4_scan, "audit_branches", return_value=branches), \
             mock.patch.object(s4_scan, "merged_audit_heads", return_value=merged), \
             mock.patch.object(s4_scan, "open_prs", return_value=prs):
            return s4_scan.scan(self.tmp, today, s4_days)

    def test_healthy_is_empty(self):
        self.assertEqual(self._scan(["landscape-audit/2026-08"],
                                    {"landscape-audit/2026-08"}, []), {})

    def test_stranded_audit_branch_is_unmerged(self):
        """The 2026-08 audit: ran on schedule, opened a PR, output never reached
        main. The organ worked; the channel dropped it."""
        r = self._scan(["landscape-audit/2026-07", "landscape-audit/2026-08"],
                       {"landscape-audit/2026-07"}, [])
        self.assertIn("S4-UNMERGED", r)
        self.assertIn("2026-08", r["S4-UNMERGED"][1])
        self.assertNotIn("2026-07", r["S4-UNMERGED"][1])

    def test_open_pr_is_an_obligation(self):
        r = self._scan([], set(), [(2, "Landscape audit 2026-08", "landscape-audit/2026-08")])
        self.assertIn("OPEN-PR", r)
        self.assertIn("#2", r["OPEN-PR"][1])

    def test_stale_research(self):
        r = self._scan([], set(), [], today=datetime.date(2026, 10, 1))
        self.assertIn("S4-STALE", r)

    def test_network_unavailable_is_unknown_not_silent(self):
        """gh absent / offline must NOT read as healthy. A dead sensor that
        reports 'fine' is the failure mode this whole file exists to prevent."""
        r = self._scan(None, None, None)
        self.assertIn("S4-UNKNOWN", r)
        self.assertNotIn("S4-UNMERGED", r)

    def test_stale_threshold_is_configurable(self):
        r = self._scan([], set(), [], s4_days=1)
        self.assertIn("S4-STALE", r)


if __name__ == "__main__":
    unittest.main()
