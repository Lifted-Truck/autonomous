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




def _git_track(repo):
    """A fixture must be a real repo: `current` now requires .kit/ to be TRACKED,
    because untracked vendored gates reach no clone and no CI (terrane,
    2026-08-18). A fixture that never inits git was silently testing the
    one machine it ran on."""
    subprocess.run(["git", "init", "-q", repo], check=True, capture_output=True)
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True, capture_output=True)

class KitSync(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def test_absent_then_untracked_then_current(self):
        self.assertEqual(kit_sync.check(self.repo)[0], "absent")
        kit_sync.install(self.repo)
        subprocess.run(["git", "init", "-q", self.repo], check=True, capture_output=True)
        self.assertEqual(kit_sync.check(self.repo)[0], "untracked",
                         "installed but unstaged must NOT read current")
        _git_track(self.repo)
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

    def test_notify_does_not_write(self):
        """A report must not change what it reports. --notify used to imply a
        sync, leaving a repo that checked in AFTER committing with an
        uncommitted kit-owned change (vertex, 2026-08-18)."""
        import subprocess as sp
        aut = tempfile.mkdtemp()
        try:
            kit_sync.install(self.repo)
            man = os.path.join(self.repo, ".kit", "MANIFEST")
            with open(man, "w") as fh:                    # make it version-stale
                fh.write("kit_version: 0.0.1\n")
            before = open(man).read()
            r = sp.run([sys.executable, os.path.join(HERE, "kit_sync.py"), self.repo,
                        "--notify"], capture_output=True, text=True,
                       env=dict(os.environ, KIT_MAILBOX_ROOT=aut))
            self.assertTrue(os.path.isdir(os.path.join(aut, "integrations")),
                            "receipt did not land in the redirected mailbox")
            self.assertEqual(before, open(man).read(), "--notify rewrote the manifest")
        finally:
            shutil.rmtree(aut, ignore_errors=True)

    def test_install_is_idempotent(self):
        kit_sync.install(self.repo)
        before = open(os.path.join(self.repo, ".kit", "MANIFEST")).read()
        kit_sync.install(self.repo)
        self.assertEqual(before, open(os.path.join(self.repo, ".kit", "MANIFEST")).read())


class Receipt(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.aut = tempfile.mkdtemp()
        kit_sync.install(self.repo)
        _git_track(self.repo)

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)
        shutil.rmtree(self.aut, ignore_errors=True)

    def test_records_the_path_it_actually_wrote(self):
        out = kit_sync.receipt(self.repo, autonomous_root=self.aut)
        text = open(out).read()
        self.assertIn("repo_path:", text)
        self.assertIn(os.path.realpath(self.repo).split(os.sep)[-1], text)

    def test_filers_note_survives_into_the_receipt(self):
        out = kit_sync.receipt(self.repo, autonomous_root=self.aut,
                               note="ran from the wrong cwd the first time")
        self.assertIn("ran from the wrong cwd the first time", open(out).read())

    def test_a_stale_receipt_carries_its_own_remedy(self):
        """--notify is read-only, so a receipt filed from a stale tree stays
        stale. The receipt must therefore say how to fix it, in itself — a doc
        line elsewhere is a doc line the filer may never have read."""
        # A GENUINELY stale state: the vendored bytes differ from what MANIFEST
        # records. (This used to fake it by aging the version line, but 2.6.0
        # made that line provenance rather than a status — a version string is
        # not a defect, and pretending it was is what generated fleet-wide
        # churn on every bump.)
        with open(os.path.join(self.repo, ".kit", "kit-gates.sh"), "a") as fh:
            fh.write("\n# local edit\n")
        text = open(kit_sync.receipt(self.repo, autonomous_root=self.aut)).read()
        self.assertIn("READ-ONLY", text)
        self.assertIn("--notify", text)
        self.assertIn("sync", text.lower())

    def test_a_current_receipt_has_no_remedy_section(self):
        """The paired control: the remedy must NOT appear when it does not
        apply, or its presence stops meaning anything."""
        text = open(kit_sync.receipt(self.repo, autonomous_root=self.aut)).read()
        self.assertNotIn("Why this receipt does not read", text)

    def test_receipt_carries_no_absolute_home_path(self):
        """Receipts land in a PUBLIC repo whose leak gate rejects them (2.2.3)."""
        out = kit_sync.receipt(self.repo, autonomous_root=self.aut)
        self.assertNotIn(os.path.expanduser("~") + os.sep, open(out).read())


# A pre-2.4.0 `verify`: the copied shape the migrator knows how to rewrite.
# Built here rather than copied from harness/verify, because that template is
# now THIN by design — using it as the fixture silently turned three of these
# tests into no-ops the moment it was thinned, and ./verify did not notice
# because test_kit_sync was named as 2.4.0's gate in the CHANGELOG and never
# actually wired in. A fixture must not depend on the artifact under reform.
LEGACY_VERIFY = """#!/usr/bin/env bash
set -uo pipefail
TARGET="${1:-fast}"
HARNESS_DIR=".harness"
mkdir -p "$HARNESS_DIR"

record() { # record <target> <exit_code>
  local git_hash; git_hash=$(git rev-parse --short HEAD 2>/dev/null || echo "no-git")
  printf '{"target":"%s","exit":%d}\\n' "$1" "$2" > "$HARNESS_DIR/last-verify.json"
  return "$2"
}

# --- leak gate (kit-core — DO NOT delete; keep self-contained) --------------
leak_gate() {
  local hits
  hits=$(git grep --untracked -nIE 'PATTERN' -- . 2>/dev/null || true)
  [ -z "$hits" ] && return 0
  return 1
}

fast() {
  local ok=0
  leak_gate     || ok=1
  return "$ok"
}

case "$TARGET" in
  fast) fast; record fast $? ;;
esac
"""


class Migration(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        with open(os.path.join(self.repo, "verify"), "w") as fh:
            fh.write(LEGACY_VERIFY)

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
