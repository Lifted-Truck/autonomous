---
description: Close a working session — organizational protocol, three-prompt survey, REFLECTIONS + DECISIONS + SESSION.md, PR, deregister. Writes its own artifacts and opens a PR; never merges.
---

Close the session in this repo: $ARGUMENTS

## Step 1 — read the state, then run the oracle

```
python3 ~/Documents/Claude/autonomous/kit/session/state.py .
./verify fast
```

Unlike `/reorient`, this one RUNS the oracle: a close is exactly when a stale
result is worth replacing with a real one. **A red verify is reported, never
hidden, and does not block the close** — an unfinished session that says so is
worth more than a tidy one that lies.

## Step 2 — organizational protocol (deterministic; do, don't ask)

- Uncommitted work: stage what belongs to this session; name what does not.
- Untracked `.kit/`: `git add .kit` — an untracked vendored gate reaches no
  clone and no CI.
- Orphaned traces, and TODOs left in code that belong in ROADMAP.
- **README audit** (clarity standard — a README that lies about its repo is a
  bug of the same severity as a failing test): does it still describe what the
  repo IS and where it stands? Spot-check its checkable claims against the
  tree — counts, versions, "built/not built" statuses, and the map of paths —
  the way autonomous's own README rot went unnoticed for 61 commits until its
  claims were diffed against reality. Update the dated *last verified* line
  only if you actually verified; never freshen the date on an unread file.
- Stray probe plants (`.kit-currency-plant-*`): delete them.

Tie up what you can deterministically; **list what you cannot** rather than
leaving it silent.

## Step 3 — survey the human. THREE prompts, no more.

1. What did today decide that is not yet in DECISIONS.md?
2. What is the loose thread you are most likely to forget?
3. What is the first move next session?

Everything else is derivable from the diff, the traces, and verify — so derive
it instead of asking. The three-prompt cap is the whole design: a close that
interrogates gets skipped, and a skipped close writes no SESSION.md.

## Step 3b — library roundup (the knowledge loop's harvest moment)

Walk the session for lessons that clear the write gate: something learned the
hard way that a FUTURE session would otherwise re-derive wrong. For each
candidate, draft a `library-entry.3` line — **lesson, evidence, falsifier, all
three or it does not go in**. Prefer writing nothing over writing unverified;
correcting an existing entry outranks adding a near-duplicate (check INDEX.md
first). Propose the set; the human confirms — the anti-poisoning gate is the
point, not a formality. Confirmed entries append to LIBRARY.md with a one-line
INDEX.md pointer.

Not every session yields one. Say "no library candidates" explicitly rather
than skipping the step silently — an absent roundup should be a recorded
answer, not an oversight. (`/closeout` deliberately has no version of this:
harvesting judgment is exactly what a mechanical close cannot do.)

## Step 4 — write the artifacts

- **REFLECTIONS.md** — append answer 2 and anything else worth holding, as
  `- [YYYY-MM-DD] <text>`. The dated form is what lets `/wakeup` flag entries
  that have gone stale.
- **DECISIONS.md** — append answer 1, if it is a decision. Append-only; the
  next number is **max + 1**, never last + 1, and never renumber.
- **SESSION.md** — the hot-state artifact, and the only prior-session context
  the next session trusts. State summary, next first move, open threads,
  verify status, pointer to this session's traces. Write it LAST, so it
  describes the tree as it ends.

**Concurrency:** if another session in this repo may also be closing, APPEND to
the open-thread list rather than replacing it. SESSION.md is written by
whichever close runs last, so a replacing write silently discards the other
session's threads.

## Step 5 — close with a PR, never a commit left on main

```
git switch -c chore/session-<date>
git push -u origin HEAD && gh pr create --fill
```

Evidence in the PR body. **Do not merge** — merges are the human's. No remote?
Commit on `main` and say so. Full contract: `kit/prompts/_closing.md`.

## Step 6 — deregister, and report what is still open

```
python3 ~/Documents/Claude/autonomous/kit/session/registry.py close --session-id <id>
python3 ~/Documents/Claude/autonomous/kit/session/registry.py list
```

If other rows remain, close with one line: **"Still open: X, Y."** That line is
the point of the registry — at the end of a night it is how the human sees
which projects still need closing.

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
