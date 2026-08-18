#!/usr/bin/env python3
"""migrate_to_vendored — move a repo's `verify` from copied gates to `.kit/`.

One-time, per repo, deterministic. Removes the KIT-OWNED definitions
(`record`, `leak_gate`) that were copied in at scaffold time, sources
`.kit/kit-gates.sh` instead, and wires `kit_integrity` into `fast`. Project
gates, project test commands, and everything else are left untouched — that
code is the repo's, and this script has no opinion about it.

The payoff is not tidiness. Nine repos' copies were missing the Windows
identity pattern while declaring a kit_version that promised it; after this,
the bytes cannot differ from canonical without `./verify` going red.

Refuses rather than guesses: a repo whose `verify` does not contain the exact
copied blocks is REPORTED for a human, never pattern-matched loosely. Prints a
diff summary; never commits (writes stay home).

  migrate_to_vendored.py <repo> [--apply]
"""
import argparse, os, re, subprocess, sys

_HERE = os.path.dirname(os.path.abspath(__file__))

SOURCE_BLOCK = """# Kit-owned gates: record, leak_gate, kit_integrity. A repo missing this file
# is not a lesser repo, it is an UNGATED one, so failing loudly beats degrading
# quietly — a silently skipped privacy gate is exactly the shape of bug the
# gate exists to prevent.
if [ -r .kit/kit-gates.sh ]; then
  . .kit/kit-gates.sh
else
  echo "verify: .kit/kit-gates.sh missing — run kit_sync.py (gates cannot be skipped)" >&2
  exit 1
fi
"""

_RECORD = re.compile(r"record\(\) \{ # record <target> <exit_code>\n.*?\n\}\n", re.S)
# The copied gate always arrives with its kit-core comment banner; take both,
# anchored on the banner so a project comment above it survives.
_GATE = re.compile(r"# --- leak gate \(kit-core.*?\nleak_gate\(\) \{.*?\n\}\n", re.S)


def plan(repo):
    v = os.path.join(repo, "verify")
    if not os.path.isfile(v):
        return None, "no ./verify"
    with open(v, encoding="utf-8") as fh:
        s = fh.read()
    if ".kit/kit-gates.sh" in s:
        return None, "already vendored"
    if not _RECORD.search(s):
        return None, "no copied record() block — hand-written verify, needs a human"
    if not _GATE.search(s):
        return None, "no copied leak_gate block — hand-written gate, needs a human"
    out = _GATE.sub("", _RECORD.sub("", s), count=1)
    out = out.replace("mkdir -p \"$HARNESS_DIR\"\n",
                      "mkdir -p \"$HARNESS_DIR\"\n\n" + SOURCE_BLOCK, 1)
    # kit_integrity runs with the other kit gate, first, in fast().
    m = re.search(r"^(\s*)leak_gate(\s*)\|\| ok=1(.*)$", out, re.M)
    if not m:
        return None, "fast() does not call leak_gate in the expected shape"
    out = out[:m.start()] + f"{m.group(1)}kit_integrity || ok=1   # kit-owned files match .kit/MANIFEST\n" + out[m.start():]
    # Removing two blocks leaves their surrounding blank lines stacked; collapse
    # runs of 3+ so the migrated file reads like a written one, not a patched one.
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    new, err = plan(a.repo)
    if err:
        print(f"migrate: SKIP {a.repo} — {err}")
        return 1
    v = os.path.join(a.repo, "verify")
    with open(v, encoding="utf-8") as fh:
        old = fh.read()
    print(f"migrate: {os.path.basename(os.path.abspath(a.repo))} "
          f"{len(old.splitlines())} -> {len(new.splitlines())} lines "
          f"({len(old.splitlines()) - len(new.splitlines())} removed, all kit-owned)")
    if not a.apply:
        print("  (dry run — pass --apply)")
        return 0
    with open(v, "w", encoding="utf-8") as fh:
        fh.write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
