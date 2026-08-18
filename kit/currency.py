#!/usr/bin/env python3
"""currency — the deterministic half of `/retrofit`: where is this repo
against the kit, and exactly which entries does it need?

Phase K1 (Decision 51). `/retrofit` used to re-derive a repo's harness state
every run and then re-scaffold. Now it MIGRATES: read the repo's declared
`kit_version`, diff it against `kit/CHANGELOG.md`, and emit the ordered list
of entries the repo is behind — each with a presence check the retrofit can
act on. AI does the parts that need judgement (inferring survey answers,
mapping a foreign kit's substance into standard slots); THIS does the parts
that must never depend on judgement (what version, what delta, what present).

Absence is never current: a repo with no `kit_version` is `pre-2.0.0` and
gets every entry. Idempotence is the gate — a repo AT the kit version gets an
empty delta, so re-running the retrofit is a no-op by construction.

Usage:
  currency.py <repo> [--kit <autonomous>] [--json]
Exit 0 always for a readable repo (report tool). Exit 2 = repo unreadable.
"""

import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_VERSION_RE = re.compile(r"^## (\d+\.\d+\.\d+) — (\d{4}-\d{2}-\d{2}) — (.+)$", re.M)


def parse_version(v):
    """'2.1.0' -> (2, 1, 0). 'pre-X' sorts below everything."""
    if not v or v.startswith("pre-"):
        return (-1, 0, 0)
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return (-1, 0, 0)


def kit_version(kit_dir):
    with open(os.path.join(kit_dir, "VERSION"), encoding="utf-8") as fh:
        return fh.read().strip()


def changelog_entries(kit_dir):
    """[(version, date, title, body)] in file order (oldest first)."""
    with open(os.path.join(kit_dir, "CHANGELOG.md"), encoding="utf-8") as fh:
        text = fh.read()
    heads = list(_VERSION_RE.finditer(text))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.append((m.group(1), m.group(2), m.group(3).strip(),
                    text[m.end():end].strip()))
    return out


# What each CHANGELOG version REQUIRES to be present in a repo for it to
# declare that version. Kept here rather than parsed out of the prose, so the
# check is a table an agent cannot misread — the prose in CHANGELOG.md is the
# explanation; this is the gate. Add a row when you add a CHANGELOG entry.
# Patch versions that change the TOOL and ask nothing new of a repo are listed
# with an EMPTY requirement list. currency.py treats an empty-requirement entry
# as satisfied by every repo, so a tool-only bump never reports the fleet
# behind by something it cannot act on. Repos still get the declaration bumped
# on their next retrofit, which is the right time.
TOOL_ONLY = {"2.0.1"}

REQUIREMENTS = {
    # 2.1.0 asks for a CLAUDE.md section; presence of the FILE is already
    # required by 2.0.0, and gating on the section's prose would reward the
    # words over the understanding (see CHANGELOG). So: no new mechanical
    # check — the retrofit still applies the entry, and a repo below 2.1.0
    # reads as behind until it does.
    "2.1.0": [],
    "2.0.1": [],
    "2.0.0": [
        # (label, relative path or callable-name, kind)
        ("CLAUDE.md", "CLAUDE.md", "file"),
        ("ROADMAP.md", "ROADMAP.md", "file"),
        ("DECISIONS.md", "DECISIONS.md", "file"),
        ("project.manifest.json", "project.manifest.json", "file"),
        ("INDEX.md", "INDEX.md", "file"),
        ("LIBRARY.md", "LIBRARY.md", "file"),
        ("traces/", "traces", "dir"),
        ("./verify", "verify", "exec"),
        ("verify wires leak_gate", "verify", "contains:leak_gate"),
        ("CI workflow", ".github/workflows", "dir-nonempty"),
        (".gitattributes (LF)", ".gitattributes", "contains:eol=lf"),
    ],
}


def _present(repo, target, kind):
    p = os.path.join(repo, target)
    if kind == "file":
        return os.path.isfile(p)
    if kind == "dir":
        return os.path.isdir(p)
    if kind == "dir-nonempty":
        return os.path.isdir(p) and any(
            f.endswith((".yml", ".yaml")) for f in os.listdir(p))
    if kind == "exec":
        return os.path.isfile(p) and os.access(p, os.X_OK)
    if kind.startswith("contains:"):
        needle = kind.split(":", 1)[1]
        try:
            with open(p, encoding="utf-8", errors="ignore") as fh:
                return needle in fh.read()
        except OSError:
            return False
    raise ValueError(kind)


def declared_version(repo):
    m = os.path.join(repo, "project.manifest.json")
    try:
        with open(m, encoding="utf-8") as fh:
            v = json.load(fh).get("kit_version")
        return v if isinstance(v, str) and v else None
    except (OSError, ValueError):
        return None


def report(repo, kit_dir):
    kv = kit_version(kit_dir)
    declared = declared_version(repo)
    entries = changelog_entries(kit_dir)
    behind = [e for e in entries
              if parse_version(e[0]) > parse_version(declared)
              and e[0] not in TOOL_ONLY]          # tool-only bumps ask nothing
    out = {
        "repo": os.path.abspath(repo),
        "kit_version": kv,
        "declared": declared or "pre-2.0.0",
        # "current" = nothing to migrate. A repo at 2.0.0 is current against a
        # kit at 2.0.1 when 2.0.1 is tool-only; the checker must not manufacture
        # 46 behind-by-nothing rows.
        "current": not any(parse_version(e[0]) > parse_version(declared)
                           and e[0] not in TOOL_ONLY for e in entries),
        "behind": [],
    }
    for ver, date, title, _ in behind:
        reqs = REQUIREMENTS.get(ver, [])
        checks = [{"label": lbl, "present": _present(repo, tgt, kind)}
                  for lbl, tgt, kind in reqs]
        out["behind"].append({
            "version": ver, "date": date, "title": title,
            "checks": checks,
            "missing": [c["label"] for c in checks if not c["present"]],
        })
    # A repo may DECLARE current while missing baseline items (hand-edited
    # manifest, or an item deleted since). Report that as drift, loudly —
    # a declaration the checks contradict is worse than no declaration.
    if out["current"]:
        # check against the newest version that HAS requirements
        newest_req = max((v for v in REQUIREMENTS if REQUIREMENTS[v]), key=parse_version)
        reqs = REQUIREMENTS.get(newest_req, [])
        missing = [lbl for lbl, tgt, kind in reqs if not _present(repo, tgt, kind)]
        out["declared_but_missing"] = missing
    return out


def render(r):
    lines = [f"kit currency — {r['repo']}",
             f"  kit: {r['kit_version']}   declared: {r['declared']}   "
             + ("CURRENT" if r["current"] else f"BEHIND by {len(r['behind'])} entr{'y' if len(r['behind'])==1 else 'ies'}")]
    if r.get("declared_but_missing"):
        lines.append(f"  !! declares {r['kit_version']} but is missing: "
                     + ", ".join(r["declared_but_missing"]))
    for b in r["behind"]:
        lines.append(f"  → {b['version']} ({b['date']}) {b['title']}")
        for c in b["checks"]:
            lines.append(f"      [{'x' if c['present'] else ' '}] {c['label']}")
    if r["current"] and not r.get("declared_but_missing"):
        lines.append("  nothing to do — re-running the retrofit is a no-op")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--kit", default=_HERE)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.repo):
        print(f"currency: {a.repo} is not a directory", file=sys.stderr)
        return 2
    r = report(a.repo, a.kit)
    print(json.dumps(r, indent=2) if a.json else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
