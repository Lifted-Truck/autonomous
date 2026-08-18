"""kit_sync must distinguish the three ways a vendored repo can be wrong, and
the migration must REFUSE a verify it does not recognise rather than pattern-
match loosely. A sync tool that only ever says 'current' is a copy model with
extra steps."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit_sync            # noqa: E402
import migrate_to_vendored as mig   # noqa: E402


class KitSync(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def test_absent_then_current(self):
        self.assertEqual(kit_sync.check(self.repo)[0], "absent")
        kit_sync.install(self.repo)
        self.assertEqual(kit_sync.check(self.repo)[0], "current")

    def test_local_edit_reads_edited_not_current(self):
        kit_sync.install(self.repo)
        with open(os.path.join(self.repo, ".kit", "kit-gates.sh"), "a") as fh:
            fh.write("\n# local edit\n")
        status, d = kit_sync.check(self.repo)
        self.assertEqual(status, "edited")
        self.assertIn("kit-gates.sh", d["files"])

    def test_old_version_reads_stale_not_current(self):
        """An HONEST copy of an OLD version: MANIFEST agrees with the file, the
        file disagrees with the kit. That is the case a naive integrity check
        misses, because everything is internally consistent."""
        kit_sync.install(self.repo)
        p = os.path.join(self.repo, ".kit", "kit-gates.sh")
        with open(p, "a") as fh:
            fh.write("\n# pretend this is v1\n")
        # rewrite MANIFEST so it matches the altered file — internally consistent
        sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
        man = os.path.join(self.repo, ".kit", "MANIFEST")
        with open(man, "w") as fh:
            fh.write(f"kit_version: 0.0.1\n{sha}  kit-gates.sh\n")
        self.assertEqual(kit_sync.check(self.repo)[0], "stale")

    def test_install_is_idempotent(self):
        kit_sync.install(self.repo)
        before = open(os.path.join(self.repo, ".kit", "MANIFEST")).read()
        kit_sync.install(self.repo)
        self.assertEqual(before, open(os.path.join(self.repo, ".kit", "MANIFEST")).read())


class Migration(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        shutil.copy(os.path.join(HERE, "..", "harness", "verify"),
                    os.path.join(self.repo, "verify"))

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def test_migrates_a_kit_shaped_verify(self):
        new, err = mig.plan(self.repo)
        self.assertIsNone(err)
        self.assertIn(".kit/kit-gates.sh", new)
        self.assertIn("kit_integrity || ok=1", new)
        self.assertNotIn("leak_gate() {", new)       # kit-owned definition gone
        self.assertRegex(new, r"leak_gate\s+\|\| ok=1")   # ...but still CALLED

    def test_refuses_a_hand_written_verify(self):
        with open(os.path.join(self.repo, "verify"), "w") as fh:
            fh.write("#!/bin/bash\necho hi\n")
        new, err = mig.plan(self.repo)
        self.assertIsNone(new)
        self.assertIn("needs a human", err)

    def test_second_run_is_a_noop(self):
        new, _ = mig.plan(self.repo)
        with open(os.path.join(self.repo, "verify"), "w") as fh:
            fh.write(new)
        again, err = mig.plan(self.repo)
        self.assertIsNone(again)
        self.assertEqual(err, "already vendored")

    def test_migrated_verify_is_valid_bash(self):
        new, _ = mig.plan(self.repo)
        p = os.path.join(self.repo, "verify")
        with open(p, "w") as fh:
            fh.write(new)
        self.assertEqual(subprocess.run(["bash", "-n", p]).returncode, 0)


if __name__ == "__main__":
    unittest.main()
