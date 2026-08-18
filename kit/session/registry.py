#!/usr/bin/env python3
"""registry — which sessions are currently OPEN, across machines.

Per briefs/2026-08-17-session-boundary.md §4. Deliberately tiny:

  - ONE FILE PER SESSION, not one file of rows. Concurrent opens on two
    machines never touch the same path, so a merge is trivial and a conflict
    is impossible by construction.
  - Keyed by `session_id`, NOT by repo: two concurrent sessions in one repo
    (a fleet job and the human) are legible rather than a collision.
  - CONTAINS NO CONTENT — repo, session_id, machine, opened_at, and nothing
    else. It is the one sanctioned cross-repo write precisely because it
    carries nothing worth reading. dispatch and distillery read closed-session
    artifacts (SESSION.md, traces) and never this, so they cannot race a
    running build.
  - NEVER BLOCKS A SESSION (brief §5). No registry configured, unreachable,
    unwritable — every call degrades to a warning and a local marker. A
    bookkeeping store that can stop work is worse than no store.

Location is configured, not guessed: `KIT_SESSION_REGISTRY` env var, else
`~/.claude/session-registry` if it exists. The brief proposes a private repo
both machines already pull; that choice is the human's, and this module is
the one place it is named, so swapping to a hosted store later touches one
file (brief §4).

  registry.py open <repo> --session-id ID
  registry.py close --session-id ID
  registry.py list
"""
import argparse, datetime, json, os, platform, socket, sys

_ENV = "KIT_SESSION_REGISTRY"
_FALLBACK = os.path.expanduser("~/.claude/session-registry")


def root():
    """Configured location, or None. None is a supported state, not an error."""
    p = os.environ.get(_ENV)
    if p:
        return os.path.expanduser(p)
    return _FALLBACK if os.path.isdir(_FALLBACK) else None


def _machine():
    # Hostname only — no username, no path. This file may live in a repo that
    # syncs between machines, and machine identity is the one thing doctrine
    # forbids committing.
    return platform.node().split(".")[0] or "unknown"


def open_session(repo, session_id, at=None):
    r = root()
    row = {"repo": os.path.basename(os.path.abspath(repo)),
           "session_id": session_id,
           "machine": _machine(),
           "opened_at": at or datetime.datetime.now(datetime.timezone.utc)
           .strftime("%Y-%m-%dT%H:%M:%SZ")}
    if not r:
        return {"ok": False, "reason": "no registry configured", "row": row}
    try:
        os.makedirs(r, exist_ok=True)
        with open(os.path.join(r, f"{session_id}.json"), "w", encoding="utf-8") as fh:
            json.dump(row, fh, indent=2)
        return {"ok": True, "row": row, "path": r}
    except OSError as e:
        return {"ok": False, "reason": f"registry unwritable: {e}", "row": row}


def close_session(session_id):
    r = root()
    if not r:
        return {"ok": False, "reason": "no registry configured"}
    p = os.path.join(r, f"{session_id}.json")
    if not os.path.isfile(p):
        return {"ok": True, "reason": "no row (already closed, or never opened)"}
    try:
        os.remove(p)
        return {"ok": True}
    except OSError as e:
        return {"ok": False, "reason": f"could not remove row: {e}"}


def list_open():
    r = root()
    if not r or not os.path.isdir(r):
        return []
    out = []
    for f in sorted(os.listdir(r)):
        if not f.endswith(".json"):
            continue
        try:
            with open(os.path.join(r, f), encoding="utf-8") as fh:
                out.append(json.load(fh))
        except (OSError, ValueError):
            continue
    return out


def stale_rows_for(repo, session_id=None):
    """Rows for THIS repo that are not this session — an unclean shutdown
    (brief §5). Never silently overwritten: the caller offers /reorient, then
    an abbreviated close, because a row nobody closed means a session nobody
    finished, and that is information."""
    name = os.path.basename(os.path.abspath(repo))
    return [r for r in list_open()
            if r.get("repo") == name and r.get("session_id") != session_id]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("open"); o.add_argument("repo"); o.add_argument("--session-id", required=True)
    c = sub.add_parser("close"); c.add_argument("--session-id", required=True)
    sub.add_parser("list")
    a = ap.parse_args()
    if a.cmd == "open":
        r = open_session(a.repo, a.session_id)
        print(json.dumps(r, indent=2))
        return 0                                  # never blocks, even on failure
    if a.cmd == "close":
        print(json.dumps(close_session(a.session_id), indent=2))
        return 0
    rows = list_open()
    if not rows:
        print("registry: no open sessions"
              + ("" if root() else f"  (none configured — set ${_ENV})"))
        return 0
    for r in rows:
        print(f"  {r.get('repo',''):28} {r.get('session_id','')[:12]:14} "
              f"{r.get('machine',''):12} opened {r.get('opened_at','')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
