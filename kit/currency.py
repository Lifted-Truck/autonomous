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
    # 2.2.0: the leak gate must FIRE, not merely exist. Behavioural, per
    # spectral-morph-001. A repo at 2.1.0 with a POSIX-only gate is correctly
    # BEHIND this — that is the migration, not a silent tightening.
    "2.2.0": [
        ("leak_gate fires on POSIX identity", "verify", "gate-fires:posix"),
        ("leak_gate fires on Windows identity", "verify", "gate-fires:windows"),
    ],
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


_GATE_CACHE = {}


def _gate_fires_cached(repo, plant_lines, key):
    """Behavioural checks run the repo's whole ./verify — seconds each, and the
    fleet checklist asks twice per repo across 46 repos. Cache on the repo's
    verify file content + git HEAD: if neither changed, the gate's behaviour
    did not either. A cache miss re-runs; a hit is free. Kept in-process only
    (one checklist run), so it can never go stale across runs.
    """
    import hashlib
    try:
        with open(os.path.join(repo, "verify"), "rb") as fh:
            vsum = hashlib.sha1(fh.read()).hexdigest()
    except OSError:
        vsum = "none"
    ck = (os.path.abspath(repo), vsum, key)
    if ck not in _GATE_CACHE:
        _GATE_CACHE[ck] = _gate_fires(repo, plant_lines)
    return _GATE_CACHE[ck]


def _gate_report(repo):
    """ONE ./verify run per repo, planting BOTH identity families in one file
    on separate lines, and reading which LINE the gate named. Halves the cost
    of the fleet checklist versus one run per family, and the result is more
    informative: {"posix": bool, "windows": bool}. Cached on verify content.
    """
    import hashlib, subprocess
    if os.environ.get("KIT_CURRENCY_NESTED"):
        return {"posix": False, "windows": False}
    v = os.path.join(repo, "verify")
    if not (os.path.isfile(v) and os.access(v, os.X_OK)):
        return {"posix": False, "windows": False}
    try:
        with open(v, "rb") as fh:
            vsum = hashlib.sha1(fh.read()).hexdigest()
    except OSError:
        vsum = "none"
    ck = (os.path.abspath(repo), vsum, "report")
    if ck in _GATE_CACHE:
        return _GATE_CACHE[ck]
    name = f".kit-currency-plant-{os.getpid()}.md"
    path = os.path.join(repo, name)
    result = {"posix": False, "windows": False}
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f"posix {_POSIX_PLANT}\nwindows {_WIN_PLANT}\n")
        env = dict(os.environ, KIT_CURRENCY_NESTED="1")
        r = subprocess.run(["./verify", "fast"], cwd=repo, capture_output=True,
                           text=True, timeout=120, env=env)
        out = r.stderr + r.stdout
        result = {"posix": f"{name}:1:" in out, "windows": f"{name}:2:" in out}
    except (OSError, subprocess.TimeoutExpired):
        pass
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
    _GATE_CACHE[ck] = result
    return result


def _gate_fires(repo, plant_lines):
    """Does the repo's OWN ./verify leak_gate go red on planted known-bad lines?

    spectral-morph-001 ask 2: `contains:leak_gate` was a presence check on the
    gate's NAME. A repo with a POSIX-only pattern (harness/verify shipped that
    for a month) read as compliant while blind to the Windows form. Kit README
    says every gate asserts the EFFECTIVE state; the currency checker was the
    exception. This plants each identity family in a scratch file inside the
    repo, runs `./verify fast`, and requires the gate to name the file. The
    plant is created and removed inside one call; the repo is left untouched.
    """
    import subprocess
    # RECURSION GUARD. autonomous's own ./verify runs `currency.py .`, and this
    # check runs `./verify fast` — so without a guard, checking autonomous is a
    # fork bomb: verify → currency → verify → currency … (it happened; ~100
    # nested plants before it was killed). An env var marks "we are already
    # inside a currency behavioural check"; a nested invocation must return the
    # honest answer for the outer one, and the honest answer for "does the gate
    # fire" cannot be established from inside the gate. So a nested call reports
    # NOT-fired, which makes the outer check fail loud rather than loop silent —
    # and verify's own self-check reads currency's --json, which the outer call
    # still produces correctly because it is not nested.
    if os.environ.get("KIT_CURRENCY_NESTED"):
        return False
    v = os.path.join(repo, "verify")
    if not (os.path.isfile(v) and os.access(v, os.X_OK)):
        return False
    name = f".kit-currency-plant-{os.getpid()}.md"
    path = os.path.join(repo, name)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(plant_lines) + "\n")
        env = dict(os.environ, KIT_CURRENCY_NESTED="1")
        r = subprocess.run(["./verify", "fast"], cwd=repo, capture_output=True,
                           text=True, timeout=120, env=env)
        return name in (r.stderr + r.stdout)
    except (OSError, subprocess.TimeoutExpired):
        return False
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


# Planted lines are ASSEMBLED, never written as literals: this file is greppable
# by every leak gate in the fleet, and a literal identity path here would make
# the currency checker itself the leak (Decision 55's test fixture lesson).
_POSIX_PLANT = "/" + "Users" + "/someone/secret"
_WIN_PLANT = "C:" + "\\" + "Users" + "\\someone\\secret"


def _present(repo, target, kind):
    if kind == "gate-fires:posix":
        return _gate_report(repo)["posix"]
    if kind == "gate-fires:windows":
        return _gate_report(repo)["windows"]
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
        # Drift is checked against EVERY version's requirements up to the
        # declared one, not only the newest — a repo declaring 2.2.0 that has
        # lost its CLAUDE.md (a 2.0.0 requirement) is in drift. Checking only
        # the newest version made exactly that invisible the moment 2.2.0
        # shipped with requirements of its own (test caught it).
        missing = []
        for ver in sorted(REQUIREMENTS, key=parse_version):
            if parse_version(ver) > parse_version(declared):
                continue
            for lbl, tgt, kind in REQUIREMENTS[ver]:
                if not _present(repo, tgt, kind):
                    missing.append(lbl)
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
