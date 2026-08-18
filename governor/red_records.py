#!/usr/bin/env python3
"""red_records — which repos are carrying a RED `.harness/last-verify.json`.

A red record blocks that repo's Stop hook, so it is the first thing its next
session sees. Two very different causes look identical from inside the repo:

  a genuine failing oracle          → the resident must fix it
  a foreign probe's exit code       → nothing is wrong; re-run and it clears

Cause (b) was real and fleet-wide: `currency.py`'s gate-fires probe runs the
target's own `./verify fast`, a correctly firing gate exits 1, and before kit
2.2.2 the probe restored the plant but not the record (LIBRARY L0006, found by
juce-rag; blast radius identified by mind-lathe). One checklist run over the
fleet left nine repos red at 2026-08-18T04:15Z.

REPORT ONLY — never writes. `.harness/` is local state, but it is the other
repo's local state, and writes stay home. The diagnostic that separates the
two causes belongs to the resident: compare the record's `git` field against
their own run logs; a red at a hash where their own verify was green was not
theirs (mind-lathe's rule).

Usage:  red_records.py [--registry ../registry.json]
"""
import argparse, json, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..")
sys.path.insert(0, os.path.join(_ROOT, "kit", "sweep"))
import sweep  # noqa: E402


def scan(registry):
    out = []
    for p in sweep.resolve(registry):
        f = os.path.join(p["path"], ".harness", "last-verify.json")
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        if d.get("exit") not in (0, None):
            out.append({"repo": p["name"], "exit": d.get("exit"),
                        "git": d.get("git"), "ts": d.get("ts")})
    return sorted(out, key=lambda r: r["repo"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default=os.path.join(_ROOT, "registry.json"))
    a = ap.parse_args()
    with open(a.registry, encoding="utf-8") as fh:
        rows = scan(json.load(fh))
    if not rows:
        print("red_records: none — every repo's last recorded verify was green")
        return 0
    print(f"red_records: {len(rows)} repo(s) blocking on a red record")
    for r in rows:
        print(f"  {r['repo']:34} exit={r['exit']} at {r['git']} {r['ts']}")
    print("  A cluster sharing one timestamp is a probe artifact, not nine "
          "broken repos; re-running ./verify clears it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
