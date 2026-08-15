#!/usr/bin/env python3
"""s4_scan — is the fleet's intelligence organ alive, and is its output being
consumed?

VSM System 4 is outside-and-then: the function that watches the environment
and feeds adaptation back into policy. Here that is the monthly landscape audit
plus the research/ corpus. Decision 47 found it demonstrably broken twice over:
the 2026-08 audit ran on schedule, opened a PR, and sat unsurfaced for four
days; and its predecessor was MERGED without a single recommendation ever
being applied. An intelligence function that silently stops — or whose output
is delivered and never read — is indistinguishable from a quiet environment.
This makes both failures loud.

Three checks, all deterministic, no model calls (VSM amendment A):

  S4-STALE      newest dated research artifact older than --s4-days
  S4-UNMERGED   a `landscape-audit/*` branch exists on the remote with no
                merged PR — the organ ran and the channel dropped it
  OPEN-PR       any open PR on THIS repo. An open PR here is an obligation
                on the human that nothing else surfaces; the hook that reads
                PR state per-prompt reports the current branch only.

Network calls (`git ls-remote`, `gh pr list`) are wrapped: absence of `gh` or
of network yields "unknown", never a crash and never a silent pass — the
monitor's own history (Decision 35) is why.
"""

import datetime
import os
import re
import subprocess

_DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def _run(args, cwd):
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                              timeout=15, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError,
            subprocess.TimeoutExpired):
        return None


def newest_research_date(repo):
    """Newest YYYY-MM-DD prefix across research/ and research/proposals/, or None."""
    dates = []
    for sub in ("research", os.path.join("research", "proposals")):
        d = os.path.join(repo, sub)
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            m = _DATED.match(name)
            if m:
                dates.append(m.group(1))
    return max(dates) if dates else None


def audit_branches(repo):
    """Remote `landscape-audit/*` branch names (from a fresh ls-remote), or None
    if the remote could not be queried. Reads the REMOTE, not local refs — a
    stale local fetch would report a branch as absent that GitHub still has."""
    out = _run(["git", "ls-remote", "--heads", "origin", "landscape-audit/*"], repo)
    if out is None:
        return None
    return sorted(l.split("refs/heads/")[-1] for l in out.splitlines() if "refs/heads/" in l)


def open_prs(repo):
    """[(number, title, headRefName)] for open PRs on this repo, or None if gh
    is unavailable. Not merged is not the same as merged: `state` is what GitHub
    says, never what a human said in chat."""
    out = _run(["gh", "pr", "list", "--state", "open",
                "--json", "number,title,headRefName"], repo)
    if out is None:
        return None
    import json
    try:
        return [(p["number"], p["title"], p["headRefName"]) for p in json.loads(out)]
    except (ValueError, KeyError):
        return None


def merged_audit_heads(repo):
    """headRefNames of MERGED PRs whose head was an audit branch, or None."""
    out = _run(["gh", "pr", "list", "--state", "merged", "--limit", "50",
                "--json", "headRefName"], repo)
    if out is None:
        return None
    import json
    try:
        return {p["headRefName"] for p in json.loads(out)
                if p["headRefName"].startswith("landscape-audit/")}
    except (ValueError, KeyError):
        return None


def scan(repo, today=None, s4_days=35):
    """-> {check: (severity, detail)} for the S4 organ. Empty dict = healthy."""
    today = today or datetime.date.today()
    out = {}

    newest = newest_research_date(repo)
    if newest is None:
        out["S4-STALE"] = ("WARN", "no dated research artifact at all")
    else:
        age = (today - datetime.date.fromisoformat(newest)).days
        if age > s4_days:
            out["S4-STALE"] = ("WARN", f"newest research artifact {age}d old ({newest})")

    branches = audit_branches(repo)
    merged = merged_audit_heads(repo)
    if branches is None or merged is None:
        out["S4-UNKNOWN"] = ("INFO", "could not query remote/gh — S4 delivery unverified")
    else:
        stranded = [b for b in branches if b not in merged]
        if stranded:
            out["S4-UNMERGED"] = ("WARN", "audit ran, output not merged: " + ", ".join(stranded))

    prs = open_prs(repo)
    if prs is None:
        out.setdefault("S4-UNKNOWN", ("INFO", "gh unavailable — open PRs unverified"))
    elif prs:
        out["OPEN-PR"] = ("WARN", "; ".join(f"#{n} {t}" for n, t, _ in prs))
    return out
