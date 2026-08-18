---
description: Reload the session frame — re-read state and re-render it. Reads only; touches no ledger, no registry, no reflection log.
---

Re-orient in this repo: $ARGUMENTS

**The cheapest of the three session commands, and the one you will use most.**
Its whole job is to put the frame back in your head after a break, a context
compaction, or a fresh window — which the brief expects to be the common case.
It is `/wakeup` with the writes removed, which is also how it validates the
shared routine.

## Do

```
python3 ~/Documents/Claude/autonomous/kit/session/state.py .
```

That is deterministic and pure-read: SESSION.md, the ROADMAP phase, the newest
DECISIONS, REFLECTIONS.md, the recorded verify result, branch/dirty/unpushed,
recent traces. Then render for the human, in this order and no longer than it
takes:

1. **Where the project is** — phase, and the last close's first move.
2. **What changed since** — commits, uncommitted work, unpushed branches.
3. **Whether it is green** — and if the recorded verify was for a different
   commit, say that it says nothing about HEAD rather than repeating its
   colour. Offer to run `./verify fast`; do not run it unasked.
4. **The obvious next move**, stated as an assumption to be corrected.

## Do NOT

- Write anything. No registry row, no REFLECTIONS entry, no SESSION.md, no
  commits. If the human says something worth keeping, say it belongs in
  `/breakdown` or offer to write it — and then only that one thing.
- Survey. `/reorient` re-renders; it does not interview. If the state is
  genuinely ambiguous, name the ambiguity in one line and let the human
  resolve it.
- Re-derive history. If SESSION.md exists, it is the prior session's own
  account and outranks your reconstruction from the diff.

## When there is no SESSION.md

Say so plainly: this repo has never closed a session, so there is no prior
account and everything below is reconstructed from git and traces. Do not
present a reconstruction as if it were a handoff.
