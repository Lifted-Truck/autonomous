"""A batch close must refuse more than it accepts, and must never produce an
artifact that looks like a human closed it."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import batch_close  # noqa: E402


def _repo(files=("f.txt",)):
    d = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q", d], check=True, capture_output=True)
    for f in files:
        with open(os.path.join(d, f), "w") as fh:
            fh.write("x\n")
    subprocess.run(["git", "-C", d, "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", d, "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "init"], check=True, capture_output=True)
    return d


class Triage(unittest.TestCase):
    def setUp(self):
        self.repo = _repo()

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def test_a_clean_repo_has_nothing_to_close(self):
        self.assertEqual(batch_close.triage(self.repo)[0], "clean")

    def test_their_own_uncommitted_work_needs_a_session(self):
        """Only that repo's session knows what its work-in-progress is."""
        with open(os.path.join(self.repo, "src.py"), "w") as fh:
            fh.write("half a feature\n")
        self.assertEqual(batch_close.triage(self.repo)[0], "needs-session")

    def test_kit_owned_files_alone_are_mechanical(self):
        """.kit/ and project.manifest.json are THIS repo's batch writes sitting
        in someone else's tree — litter awaiting a commit, not their session."""
        os.makedirs(os.path.join(self.repo, ".kit"))
        with open(os.path.join(self.repo, ".kit", "MANIFEST"), "w") as fh:
            fh.write("kit_version: 9.9.9\n")
        self.assertEqual(batch_close.triage(self.repo)[0], "mechanical")

    def test_a_red_oracle_needs_a_human_not_a_sweep(self):
        """A red verify is a finding. Closing past it in a batch would hide the
        one thing a close is supposed to surface."""
        os.makedirs(os.path.join(self.repo, ".harness"))
        head = subprocess.run(["git", "-C", self.repo, "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        with open(os.path.join(self.repo, ".harness", "last-verify.json"), "w") as fh:
            fh.write('{"target":"fast","exit":1,"git":"%s","ts":"t"}' % head)
        self.assertEqual(batch_close.triage(self.repo)[0], "needs-session")

    def test_a_STALE_red_does_not_condemn_the_repo(self):
        """A red recorded at another commit says nothing about HEAD — the same
        distinction the state routine draws. It must not be read as a finding."""
        os.makedirs(os.path.join(self.repo, ".harness"))
        with open(os.path.join(self.repo, ".harness", "last-verify.json"), "w") as fh:
            fh.write('{"target":"fast","exit":1,"git":"deadbee","ts":"t"}')
        self.assertNotEqual(batch_close.triage(self.repo)[0], "needs-session")


class Close(unittest.TestCase):
    def setUp(self):
        self.repo = _repo()
        os.makedirs(os.path.join(self.repo, ".kit"))
        with open(os.path.join(self.repo, ".kit", "MANIFEST"), "w") as fh:
            fh.write("kit_version: 9.9.9\n")

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def test_dry_run_writes_nothing(self):
        batch_close.close_one(self.repo, "r", apply=False)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "SESSION.md")))

    def test_the_session_md_declares_itself_mechanical_and_unsurveyed(self):
        """THE constraint. SESSION.md is the only prior-session context the next
        session trusts; one that looks human-written but carries no answers
        would poison exactly the artifact it is meant to serve."""
        batch_close.close_one(self.repo, "r", apply=True)
        text = open(os.path.join(self.repo, "SESSION.md")).read()
        self.assertIn("closed: mechanical", text)
        self.assertIn("No survey was taken", text)
        self.assertIn("not a handoff", text)

    def test_it_refuses_a_repo_that_needs_a_session(self):
        with open(os.path.join(self.repo, "src.py"), "w") as fh:
            fh.write("wip\n")
        r = batch_close.close_one(self.repo, "r", apply=True)
        self.assertEqual(r["action"], "skipped")
        self.assertFalse(os.path.exists(os.path.join(self.repo, "SESSION.md")))

    def test_it_commits_only_its_own_artifacts(self):
        """It must never sweep a repo's source into a commit nobody reviewed."""
        batch_close.close_one(self.repo, "r", apply=True)
        files = subprocess.run(["git", "-C", self.repo, "show", "--name-only",
                                "--format=", "HEAD"], capture_output=True,
                               text=True).stdout.split()
        self.assertTrue(set(files) <= {"SESSION.md", ".kit/MANIFEST",
                                       "project.manifest.json"}, files)


if __name__ == "__main__":
    unittest.main()
