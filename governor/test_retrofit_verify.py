"""retrofit_verify must DISPUTE a false notice, not only VERIFY a true one — a
verifier that cannot say no reads exactly like one that always says yes
(L0002/L0005). Fixture: two temp repos registered under a temp registry, one
genuinely current, one declaring a version it does not meet; notices for
both, plus one from a repo the registry has never heard of."""
import json, os, re, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import retrofit_verify as rv  # noqa: E402

KIT_VERSION = open(os.path.join(ROOT, "kit", "VERSION")).read().strip()


def _git_repo(path):
    os.makedirs(path)
    subprocess.run(["git", "init", "-q", path], check=True)


def _put(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class RetrofitVerify(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        # A genuinely current repo, built the way test_currency builds one
        # (real leak_gate lifted from harness/verify, so 2.2.0's gate-fires
        # check passes) — NOT autonomous itself, whose ./verify would re-run
        # this test file from inside the check.
        self.truth = os.path.join(self.tmp, "truth")
        _git_repo(self.truth)
        for f in ("CLAUDE.md", "ROADMAP.md", "DECISIONS.md", "INDEX.md", "LIBRARY.md"):
            _put(os.path.join(self.truth, f), "x\n")
        os.makedirs(os.path.join(self.truth, "traces"))
        os.makedirs(os.path.join(self.truth, ".github", "workflows"))
        _put(os.path.join(self.truth, ".github", "workflows", "ci.yml"), "name: ci\n")
        _put(os.path.join(self.truth, ".gitattributes"), "* text=auto eol=lf\n")
        shutil.copy(os.path.join(ROOT, "harness", "verify"), os.path.join(self.truth, "verify"))
        os.chmod(os.path.join(self.truth, "verify"), 0o755)
        with open(os.path.join(self.truth, "project.manifest.json"), "w") as fh:
            json.dump({"kit_version": KIT_VERSION}, fh)
        self.liar = os.path.join(self.tmp, "liar")
        _git_repo(self.liar)
        with open(os.path.join(self.liar, "project.manifest.json"), "w") as fh:
            json.dump({"kit_version": KIT_VERSION}, fh)   # declares, has nothing
        self.registry = {"rules": [            # sweep.resolve shape: rules, not projects
            {"project": self.truth},
            {"project": self.liar},
        ]}
        self.mail = os.path.join(self.tmp, "mail", "_rvtest")
        os.makedirs(self.mail)
        self._notice("truth", "truth.md")
        self._notice("liar", "lie.md")
        self._notice("ghost", "ghost.md")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _notice(self, sender, fname):
        with open(os.path.join(self.mail, "retrofit-" + fname), "w") as fh:
            fh.write(f"---\nid: {sender}-retrofit-{KIT_VERSION}\nfrom: {sender}\n"
                     f"to: autonomous\nstatus: filed\nball: provider\nfiled: 2026-08-18\n"
                     f"re: retrofit to kit {KIT_VERSION}\n---\nclaimed done.\n")

    def _run(self, dry):
        res = rv.verify_all(self.registry, dry=dry, mail_root=os.path.join(self.tmp, "mail"))
        return {r["sender"]: r for r in res}

    def test_true_verified_lie_disputed_unknown_unresolvable(self):
        r = self._run(dry=True)
        self.assertEqual(r["truth"]["verdict"], "verified")
        self.assertEqual(r["liar"]["verdict"], "disputed")
        self.assertIn("declared but missing", r["liar"]["note"])
        self.assertEqual(r["ghost"]["verdict"], "unresolvable")

    def test_stamp_flips_frontmatter_keeps_body_and_is_idempotent(self):
        self._run(dry=False)
        with open(os.path.join(self.mail, "retrofit-lie.md")) as fh:
            lie = fh.read()
        self.assertRegex(lie, r"(?m)^status: disputed$")
        self.assertRegex(lie, r"(?m)^ball: none$")
        self.assertIn("claimed done.", lie)               # filer's words intact
        self.assertIn("autonomous verification", lie)
        self.assertEqual(self._run(dry=False), {})        # already judged → skipped

    def test_dry_run_writes_nothing(self):
        f = os.path.join(self.mail, "retrofit-lie.md")
        with open(f) as fh:
            before = fh.read()
        self._run(dry=True)
        with open(f) as fh:
            self.assertEqual(before, fh.read())


if __name__ == "__main__":
    unittest.main()
