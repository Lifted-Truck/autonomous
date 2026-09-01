---
description: Open a working session — read state, prune the reflection log, register the session. Writes: registry row, confirmed graduations, reflection prunes.
---

Open a session in this repo: $ARGUMENTS

## Step 1 — read the state (shared routine)

```
python3 ~/Documents/Claude/autonomous/kit/session/state.py .
python3 ~/Documents/Claude/autonomous/kit/session/registry.py list
```

## Step 2 — check for an unclean shutdown BEFORE opening

If the registry holds a row for THIS repo that is not this session, the last
session never closed. **Never silently overwrite it** — a row nobody closed
means a session nobody finished, and that is information, not noise. Offer, in
this order: re-render the state (`/reorient`), then an abbreviated `/breakdown`
that writes SESSION.md and closes the stale row, and only then open.

## Step 3 — render the state summary

Where the project is, what changed last session, verify status (a recorded
result from a different commit says nothing about HEAD), what is ready to work
on. Same shape as `/reorient`.

## Step 4 — prune REFLECTIONS.md

Each entry: **graduate** (to DECISIONS.md, ROADMAP.md, LIBRARY.md — if it
clears the evidence+falsifier gate — or an issue), **stay**
with a note, or **drop**. Propose all three sets; the human confirms. Entries
unaddressed for 14+ days are flagged by the state routine — those are
graduate-or-drop, not stay, because a reflection log that only grows is a
place thoughts go to die.

## Step 5 — survey ONLY if genuinely ambiguous

Multiple ready threads, a stale or contradicted plan, a red verify, or an
unresolved reflection blocking the obvious move. Otherwise **state the assumed
starting point and proceed**. A survey that fires every time gets skipped every
time, and then it is not a gate, it is a habit.

## Step 6 — register the session

```
python3 ~/Documents/Claude/autonomous/kit/session/registry.py open . --session-id <id>
```

Use a stable id for this session. If the registry is unconfigured or
unreachable, **proceed with a warning** — a session never blocks on
bookkeeping.

## Permitted writes

Registry row; REFLECTIONS.md prune edits; graduation targets the human
confirmed. Nothing else. In particular `/wakeup` does not commit project work.

## Last — republish the Session Board (only if it changed)

The registry only changes at session boundaries, so republishing here is what
keeps the board current — event-driven, no polling. If
`~/.claude/session-registry/BOARD_URL` exists:

```
python3 ~/Documents/Claude/autonomous/kit/session/render_registry.py --check-changed > /tmp/session-board.html
```

It prints `CHANGED` or `UNCHANGED` on stderr and writes the page only when the
board's SUBSTANCE moved (its own clock is excluded from the comparison).
**`UNCHANGED` → publish nothing** — three identical republishes in four minutes
is noise that trains the reader to ignore the notification. On `CHANGED`,
publish `/tmp/session-board.html` with the Artifact tool, passing the URL from
`BOARD_URL` as `url` (updates the existing board; keep the 🕐 favicon). No
`BOARD_URL` → skip silently; a session never blocks on bookkeeping.
