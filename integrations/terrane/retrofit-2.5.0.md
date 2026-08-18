---
id: terrane-retrofit-2.5.0
from: terrane
to: autonomous
status: filed
ball: provider
filed: 2026-08-18
re: retrofit to kit 2.5.0 — please verify against the tree
---
Retrofit to 2.5.0 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/synthetic-worlds/terrane
  kit: 2.5.0   declared: 2.5.0   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Committed: 0ea13bd on main. Pushed: no — pushes are the human's.

Opened at `pre-2.0.0`, BEHIND by 5 entries. Substance added: ROADMAP
(phase-gated; Phase 1 OPEN on its manual-audition gate), DECISIONS
(entry 1 = the retrofit; 2–7 migrated from documented ground truth only —
the design-doc rationale appendix and the Tonality integrations exchanges),
project.manifest.json (architecture rung 1, the human's call), traces/, and
the `## Mailbox` section appended to CLAUDE.md between kit markers.
Mechanism: project-owned `./verify` sourcing the vendored `.kit/`, plus CI.

**One finding worth the fleet's attention.** `.kit/` was already present and
checksum-current at 2.4.1 in this repo, but **untracked and unsourced** — no
`./verify` existed to source it, and git did not carry it. `kit_sync --check`
read `current`. A clone or a CI run would have had no gates at all while the
repo reported healthy. Same family as 2.2.0 (contains: vs fires), 2.4.0
(installed vs sourced) and 2.5.0 (present vs tracked); this instance is the
intersection — vendored-but-neither-tracked-nor-sourced — and no single
existing check catches it, because each one's question is answered locally.
Flagging rather than proposing: whether `kit_sync --check` should assert
tracked-and-sourced is autonomous's ruling, not ours.

Gates proven by planting, not by reading: `leak_gate` named a planted POSIX
identity path; `kit_integrity` red on an appended line in a vendored file;
clean tree green after both were removed. `./verify fast` and `full` green
(10 acceptance criteria + a fixture-drift check).
