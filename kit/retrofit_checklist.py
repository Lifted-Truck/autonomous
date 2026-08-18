#!/usr/bin/env python3
"""retrofit_checklist — the K4 catch-up list, DERIVED from the fleet, never
maintained by hand.

The human asked for a checklist that updates as each retrofit happens,
suggesting each repo "send a notice" that I would use to tick the list. That
is a DECLARED-state design, and this week's record (Decisions 53–57) is a
list of declared states that lied: frontmatter that said `filed` after being
answered, a kit_version that said 2.0.0 with no CLAUDE.md, an amendment that
declared a field no parser could open. A notice is one more declaration.

The EFFECTIVE state already exists and is cheaper: `currency.py` reads each
repo's manifest and tree. A retrofit is done when the repo READS as done —
declares the kit version and has every requirement present. So this list has
no tick-box, no notice channel, and no state file. It cannot be stale, because
it is not stored; and it cannot be wrong about a repo, because it re-reads the
repo. Run it any time; the answer is the fleet's actual state at that moment.

Groups repos by what the retrofit will actually involve, so the human can
choose a batch:

  DECLARE   zero baseline gaps — retrofit writes kit_version + ## Mailbox only
  LIGHT     1–3 gaps, usually CI / leak_gate / verify — an hour each
  FULL      4+ gaps — the real procedure: survey, rung, plan-then-pause
  DORMANT   declared dormant; not on the list (Decision 55)
  DONE      declares current and passes its own check

Usage:  retrofit_checklist.py [--md]
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")


def _load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def classify(repo_path):
    r = json.loads(subprocess.run(
        [sys.executable, os.path.join(HERE, "currency.py"), repo_path, "--json"],
        capture_output=True, text=True).stdout or "{}")
    manifest = _load(os.path.join(repo_path, "project.manifest.json"))
    dormant = manifest.get("dormant") if isinstance(manifest, dict) else None
    if isinstance(dormant, dict) and dormant.get("review_by"):
        return "DORMANT", [], r
    if r.get("current"):
        return "DONE", [], r
    base = [b for b in r.get("behind", []) if b["version"] == "2.0.0"]
    missing = base[0]["missing"] if base else []
    if not missing:
        return "DECLARE", missing, r
    return ("LIGHT" if len(missing) <= 3 else "FULL"), missing, r


def main():
    md = "--md" in sys.argv
    rows = json.loads(subprocess.run(
        [sys.executable, os.path.join(HERE, "sweep", "sweep.py"),
         "--registry", os.path.join(ROOT, "registry.json"), "list"],
        capture_output=True, text=True, check=True).stdout)
    groups = {"DONE": [], "DECLARE": [], "LIGHT": [], "FULL": [], "DORMANT": []}
    for r in rows:
        if not r["status"].get("git"):
            continue
        g, missing, _ = classify(r["path"])
        groups[g].append((r["name"], missing))

    order = ("DONE", "DECLARE", "LIGHT", "FULL", "DORMANT")
    total = sum(len(groups[g]) for g in order)
    done = len(groups["DONE"]) + len(groups["DORMANT"])
    if md:
        print(f"# Retrofit checklist — derived {subprocess.run(['date','-u','+%Y-%m-%dT%H:%MZ'],capture_output=True,text=True).stdout.strip()}\n")
        print(f"**{done}/{total} settled** (current or dormant). Re-run to refresh; nothing here is stored.\n")
    else:
        print(f"retrofit checklist — {done}/{total} settled (current or dormant)\n")
    for g in order:
        items = groups[g]
        if not items:
            continue
        label = {"DONE": "DONE — declares current, passes own check",
                 "DECLARE": "DECLARE — zero gaps; retrofit writes kit_version + ## Mailbox",
                 "LIGHT": "LIGHT — 1–3 gaps",
                 "FULL": "FULL — 4+ gaps; survey + rung + plan-then-pause",
                 "DORMANT": "DORMANT — declared; off the list (Decision 55)"}[g]
        print(("## " if md else "") + f"{label}  ({len(items)})")
        for name, missing in sorted(items, key=lambda t: (len(t[1]), t[0])):
            tick = "x" if g in ("DONE", "DORMANT") else " "
            gap = f" — {', '.join(missing)}" if missing else ""
            print(f"- [{tick}] {name}{gap}" if md else f"  [{tick}] {name:34}{gap}")
        print()


if __name__ == "__main__":
    main()
