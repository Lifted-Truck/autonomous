#!/usr/bin/env python3
"""batch_gitattributes — K4 batch 1: the CRLF guard into every behind repo.

WHY A BATCH AND NOT 43 /retrofit RUNS: there is no judgement in this file. It
is the same lines everywhere (kit/templates/gitattributes), asks no survey
question, and is what stands between the human and a clean Windows clone
(Decision 34: git-for-Windows' autocrlf=true rewrites checkouts to CRLF, so
identical content has different bytes per machine and every byte-comparison
gate fails for reasons unrelated to the change).

WRITES-STAY-HOME, HONOURED NOT WAIVED: this COMMITS only where a resident would
not be disturbed — clean tree, on the default branch. A repo mid-flight on a
feature branch, or with uncommitted work, gets the FILE written and left for
its resident to commit: their branch, their commit. Archived repos are skipped.
NOTHING is pushed; every push is the human's.

  python3 kit/batch_gitattributes.py          # plan only
  python3 kit/batch_gitattributes.py --apply
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ARCHIVED = {"agent-knowledge-loop"}


def git(p, *a):
    return subprocess.run(["git", "-C", p, *a], capture_output=True, text=True)


def main():
    apply = "--apply" in sys.argv
    with open(os.path.join(HERE, "templates", "gitattributes"), encoding="utf-8") as fh:
        tmpl = fh.read()
    rows = json.loads(subprocess.run(
        [sys.executable, os.path.join(HERE, "sweep", "sweep.py"),
         "--registry", os.path.join(ROOT, "registry.json"), "list"],
        capture_output=True, text=True, check=True).stdout)
    counts = {"committed": 0, "written": 0, "skipped": 0, "current": 0}
    for r in rows:
        if not r["status"].get("git"):
            continue
        p, name = r["path"], r["name"]
        ga = os.path.join(p, ".gitattributes")
        if os.path.isfile(ga):
            with open(ga, encoding="utf-8", errors="ignore") as fh:
                if "eol=lf" in fh.read():
                    counts["current"] += 1
                    continue
        if name in ARCHIVED:
            print(f"  SKIP    {name:34} archived")
            counts["skipped"] += 1
            continue
        head = git(p, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD").stdout.strip()
        default = head.rsplit("/", 1)[-1] if head else "main"
        branch = git(p, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        dirty = bool(git(p, "status", "--porcelain").stdout.strip())
        safe = branch == default and not dirty
        why = "" if safe else ("dirty tree" if dirty else f"on {branch}")
        if not apply:
            print(f"  {'COMMIT' if safe else 'WRITE ':7} {name:34} {why}")
            continue
        mode = "a" if os.path.isfile(ga) else "w"
        with open(ga, mode, encoding="utf-8") as fh:
            fh.write(("\n" if mode == "a" else "") + tmpl)
        if safe:
            git(p, "add", ".gitattributes")
            c = git(p, "commit", "-q", "-m",
                    "Add .gitattributes: LF in the repo on every platform\n\n"
                    "Kit K4 batch 1 (autonomous kit/CHANGELOG 2.0.0 baseline). Git for\n"
                    "Windows defaults to autocrlf=true, which rewrites checkouts to CRLF;\n"
                    "identical content then has different bytes per machine and every\n"
                    "byte-comparison gate fails for reasons unrelated to the change.\n"
                    "`text=auto eol=lf` normalizes what git STORES; working trees keep\n"
                    "native endings. Not pushed by the batch — the push is the human's.\n\n"
                    "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>")
            ok = c.returncode == 0
            print(f"  {'commit' if ok else 'FAILED':7} {name:34}" + ("" if ok else c.stderr[:60]))
            counts["committed" if ok else "written"] += 1
        else:
            print(f"  written {name:34} left for resident ({why})")
            counts["written"] += 1
    print(f"\n  {counts}")


if __name__ == "__main__":
    main()
