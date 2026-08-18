#!/usr/bin/env python3
"""advance — raise a repo's declared kit_version when it ALREADY meets the bar.

The problem this exists for, measured 2026-08-18: 24 repos had retrofitted
that same day and read BEHIND again, and every one of them satisfied every
requirement of every version it was behind. Zero needed work. The only stale
thing was a string in `project.manifest.json`, and the ledger was telling the
human to open 24 sessions to edit 24 strings.

A retrofit is for closing GAPS. When there is no gap, advancing the
declaration is a deterministic edit with nothing to decide — so it should not
cost a session, a plan-then-pause, or a round of dialogue.

Never invents currency: it advances to the highest version whose requirements
are ALL met, checking each version at or below it too, so it can only ever
declare something already true. If any requirement is unmet it stops below
that version and says which.

  advance.py <repo> [--apply]      one repo
  advance.py --all [--apply]       every repo in the registry
"""
import argparse, json, os, subprocess, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..")
sys.path.insert(0, _HERE)
import currency  # noqa: E402


def plan(repo):
    """(new_version, reason) or (None, reason). Pure read."""
    r = json.loads(subprocess.run(
        [sys.executable, os.path.join(_HERE, "currency.py"), repo, "--json"],
        capture_output=True, text=True).stdout or "{}")
    declared = r.get("declared", "pre-2.0.0")
    if r.get("declared_but_missing"):
        return None, f"declares {declared} but is MISSING {r['declared_but_missing']} — real gap"
    behind = r.get("behind", [])
    if not behind:
        return None, "already current"
    highest = None
    for entry in behind:                       # currency emits these in order
        unmet = [c["label"] for c in entry.get("checks", []) if not c["present"]]
        if unmet:
            return (highest,
                    f"stops at {highest or declared}: {entry['version']} needs {unmet}")
        highest = entry["version"]
    return highest, f"satisfies every requirement through {highest}"


def apply_to(repo, version):
    p = os.path.join(repo, "project.manifest.json")
    with open(p, encoding="utf-8") as fh:
        text = fh.read()
    data = json.loads(text)
    data["kit_version"] = version
    # Rewrite minimally: preserve the file's own formatting habits where we can,
    # since this file is the REPO's, not ours — we are only correcting one value.
    import re
    if re.search(r'"kit_version"\s*:\s*"[^"]*"', text):
        new = re.sub(r'("kit_version"\s*:\s*)"[^"]*"', r'\1"%s"' % version, text, count=1)
    else:
        new = json.dumps(data, indent=2) + "\n"
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--registry", default=os.path.join(_ROOT, "registry.json"))
    a = ap.parse_args()
    if a.all:
        sys.path.insert(0, os.path.join(_HERE, "sweep"))
        import sweep
        with open(a.registry, encoding="utf-8") as fh:
            targets = [(p["name"], p["path"]) for p in sweep.resolve(json.load(fh))]
    elif a.repo:
        targets = [(os.path.basename(os.path.abspath(a.repo)), a.repo)]
    else:
        ap.error("give a repo path or --all")
    moved = held = 0
    for name, path in targets:
        if not os.path.isfile(os.path.join(path, "project.manifest.json")):
            continue
        ver, why = plan(path)
        if ver:
            moved += 1
            print(f"  {'ADVANCE' if a.apply else 'would':9} {name:32} -> {ver}   ({why})")
            if a.apply:
                apply_to(path, ver)
        elif "already current" not in why:
            held += 1
            print(f"  {'hold':9} {name:32} {why}")
    print(f"advance: {moved} advanced, {held} held back by a real gap"
          + ("" if a.apply else "   (dry run — pass --apply)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
