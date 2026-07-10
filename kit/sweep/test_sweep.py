"""Layer-0 tests for the sweep primitive. Deterministic, stdlib-only."""

import json
import os
import shutil
import tempfile
import unittest

import sweep


def touch(path, content=b"x"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(content)


class SweepFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sweep-test-")
        root = os.path.join(self.tmp, "Claude")
        # plain projects
        for name in ("alpha", "beta"):
            os.makedirs(os.path.join(root, name))
        # excluded dir + hidden dir + stray file
        os.makedirs(os.path.join(root, "Projects"))
        os.makedirs(os.path.join(root, ".hidden"))
        touch(os.path.join(root, "stray.md"))
        # group with two children + a group-level file (must be ignored)
        os.makedirs(os.path.join(root, "worlds", "g1"))
        os.makedirs(os.path.join(root, "worlds", "g2"))
        touch(os.path.join(root, "worlds", "AUDIT-STATE.json"))
        # explicit external project
        os.makedirs(os.path.join(self.tmp, "Extra"))
        self.registry = {
            "rules": [
                {
                    "root": root,
                    "include": "immediate-children",
                    "exclude": ["Projects"],
                    "groups": ["worlds"],
                },
                {"project": os.path.join(self.tmp, "Extra")},
            ]
        }
        self.root = root

    def tearDown(self):
        shutil.rmtree(self.tmp)


class TestResolve(SweepFixture):
    def test_enumeration(self):
        names = [p["name"] for p in sweep.resolve(self.registry)]
        self.assertEqual(
            names, ["alpha", "beta", "worlds/g1", "worlds/g2", "Extra"]
        )

    def test_excludes_and_hidden(self):
        names = [p["name"] for p in sweep.resolve(self.registry)]
        self.assertNotIn("Projects", names)
        self.assertNotIn(".hidden", names)
        self.assertNotIn("stray.md", names)
        self.assertNotIn("worlds", names)  # group itself is not a project

    def test_group_attribution(self):
        by_name = {p["name"]: p for p in sweep.resolve(self.registry)}
        self.assertEqual(by_name["worlds/g1"]["group"], "worlds")
        self.assertIsNone(by_name["alpha"]["group"])

    def test_missing_root_is_skipped_not_fatal(self):
        reg = {"rules": [{"root": os.path.join(self.tmp, "nope")}]}
        self.assertEqual(sweep.resolve(reg), [])

    def test_deterministic_ordering(self):
        a = sweep.resolve(self.registry)
        b = sweep.resolve(self.registry)
        self.assertEqual(a, b)


class TestStatus(SweepFixture):
    def test_derived_status(self):
        alpha = os.path.join(self.root, "alpha")
        touch(os.path.join(alpha, "CLAUDE.md"))
        touch(os.path.join(alpha, "LIBRARY.md"))
        os.makedirs(os.path.join(alpha, "traces"))
        status = sweep.derive_status(alpha)
        self.assertTrue(status["claude_md"])
        self.assertTrue(status["library"])
        self.assertTrue(status["traces"])
        self.assertFalse(status["verify"])
        self.assertFalse(status["status_surface"])


class TestLedger(SweepFixture):
    def test_change_detection_cycle(self):
        alpha = os.path.join(self.root, "alpha")
        touch(os.path.join(alpha, "LIBRARY.md"), b"[L0001] a | candidate\n")

        # first pass: everything with content is "changed" vs empty ledger
        recs = sweep.sweep(self.registry, targets=["LIBRARY.md"], ledger={})
        by_name = {r["name"]: r for r in recs}
        self.assertTrue(by_name["alpha"]["changed"])
        self.assertIsNone(by_name["beta"]["hash"])  # no target files at all

        # second pass against the updated ledger: nothing changed
        ledger = {r["name"]: r["hash"] for r in recs}
        recs2 = sweep.sweep(self.registry, targets=["LIBRARY.md"], ledger=ledger)
        self.assertFalse(any(r["changed"] for r in recs2))

        # modify -> only alpha flips
        touch(os.path.join(alpha, "LIBRARY.md"), b"[L0002] b | candidate\n")
        recs3 = sweep.sweep(self.registry, targets=["LIBRARY.md"], ledger=ledger)
        changed = [r["name"] for r in recs3 if r["changed"]]
        self.assertEqual(changed, ["alpha"])

    def test_hash_is_content_not_mtime(self):
        alpha = os.path.join(self.root, "alpha")
        touch(os.path.join(alpha, "LIBRARY.md"), b"same")
        h1 = sweep.content_hash(alpha, ["LIBRARY.md"])
        touch(os.path.join(alpha, "LIBRARY.md"), b"same")  # rewrite, same bytes
        h2 = sweep.content_hash(alpha, ["LIBRARY.md"])
        self.assertEqual(h1, h2)


class TestCli(SweepFixture):
    def test_cli_changed_update_ledger_roundtrip(self):
        reg_path = os.path.join(self.tmp, "registry.json")
        ledger_path = os.path.join(self.tmp, "ledger.json")
        with open(reg_path, "w") as f:
            json.dump(self.registry, f)
        touch(os.path.join(self.root, "alpha", "LIBRARY.md"), b"entry\n")

        import contextlib, io

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            sweep.main(["--registry", reg_path, "changed",
                        "--ledger", ledger_path, "--update-ledger"])
        first = json.loads(out.getvalue())
        self.assertTrue(any(r["changed"] for r in first))

        out2 = io.StringIO()
        with contextlib.redirect_stdout(out2):
            sweep.main(["--registry", reg_path, "changed", "--ledger", ledger_path])
        second = json.loads(out2.getvalue())
        self.assertFalse(any(r["changed"] for r in second))


if __name__ == "__main__":
    unittest.main()
