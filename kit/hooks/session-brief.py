#!/usr/bin/env python3
"""session-brief — SessionStart hook. Tells THIS repo's session what THIS repo
owes, and nothing else.

WHY SCOPED (2026-08-17, Decision 54): the previous version read the fleet-wide
STATUS.md and reported its counts into every session on the machine, because
the hook is installed globally. Agents in several unrelated projects all warned
the human about one uncommitted brief sitting in autonomous's mailbox — a repo
none of them had standing to touch. That is a requisite-variety failure: an
attenuator must deliver a signal its recipient can ACT on, and fleet state
delivered to a leaf project is pure noise that trains the reader to skip the
channel.

Rule, and it is the same rule the protocol states for humans and agents alike:
**a repo acts only on exchanges in its own mailbox, plus responses addressed to
it elsewhere.** Everything else is somebody else's territory.

Fleet-wide roll-up appears ONLY in the standards repo, which is the one place
it is actionable.

Fail-open: an observer, not a gate.
"""
import datetime
import json
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
AUT = os.environ.get("AUTONOMOUS_HOME", os.path.join(HOME, "Documents/Claude/autonomous"))
sys.path.insert(0, os.path.join(AUT, "governor"))
sys.path.insert(0, os.path.join(AUT, "kit", "sweep"))


def out(msg):
    if msg:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": msg}}))
    sys.exit(0)


def main():
    try:
        root = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        out(None)
    if not root:
        out(None)                      # not in a repo: nothing scoped to say
    name = os.path.basename(root)

    try:
        import ball_scan
    except Exception:
        out(None)

    today = datetime.date.today()
    bits = []

    # 1. What THIS repo owes (its own mailbox).
    try:
        mine = ball_scan.scan_repo(root, name, today)
    except Exception:
        mine = []
    overdue = [t for t in mine if t["days_overdue"]]
    held = [t for t in mine if t["ours"] and not t["days_overdue"]]
    if overdue:
        bits.append("OVERDUE: " + "; ".join(
            f"{t['id']} ({t['days_overdue']}d past {t['respond_by']})" for t in overdue))
    if held:
        bits.append("ball on us: " + ", ".join(t["id"] for t in held))

    # 2. Mailbox writes a visitor left here that a RESIDENT must commit.
    try:
        unc = ball_scan.untracked_mailbox_files(root)
    except Exception:
        unc = []
    if unc:
        bits.append(f"{len(unc)} uncommitted mailbox write(s) here: "
                    + ", ".join(os.path.basename(f) for f in unc))

    # 3. Responses to OUR briefs, sitting in other repos' trees. The delivery
    #    gap (Decision 53): without this a repo cannot tell an answered brief
    #    from an ignored one. Roster read is best-effort — never block on it.
    try:
        import sweep
        with open(os.path.join(AUT, "registry.json"), encoding="utf-8") as fh:
            reg = json.load(fh)
        paths = [p["path"] for p in sweep.resolve(reg)]
        awaiting = ball_scan.responses_awaiting(name, paths, today)
        if awaiting:
            bits.append("answered elsewhere, unread by us: " + ", ".join(
                f"{a['id']} in {a['in_repo']}" for a in awaiting))
    except Exception:
        pass

    # 4. Fleet roll-up: ONLY in the standards repo.
    if os.path.realpath(root) == os.path.realpath(AUT):
        st = os.path.join(AUT, "governor", "STATUS.md")
        if os.path.isfile(st):
            age_h = int((datetime.datetime.now().timestamp()
                         - os.path.getmtime(st)) // 3600)
            try:
                with open(st, encoding="utf-8") as fh:
                    text = fh.read()
            except OSError:
                text = ""
            fleet = []
            n_over = text.count("d overdue**")
            if n_over:
                fleet.append(f"{n_over} overdue fleet-wide")
            for tag in ("S4-UNMERGED", "S4-STALE", "OPEN-PR"):
                if f"`{tag}`" in text:
                    fleet.append(tag)
            if age_h > 48:
                fleet.append(f"sweep cache {age_h}h old")
            if fleet:
                bits.append("fleet: " + ", ".join(fleet))

    if not bits:
        out(None)
    out(f"[{name}] " + " · ".join(bits)
        + " — scoped to this repo; other repos' obligations are theirs.")


if __name__ == "__main__":
    main()
