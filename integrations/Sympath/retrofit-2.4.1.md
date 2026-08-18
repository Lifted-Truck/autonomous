---
id: Sympath-retrofit-2.4.1
from: Sympath
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. `currency.py` output at close:

```
kit currency — ~/Documents/Claude/synthetic-worlds/Sympath
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Committed: `ac4ab32` on `main`. Pushed: **no** — pushes are the human's.
(There is also an earlier unpushed human commit, `b7ce200` .gitattributes;
the branch is 2 ahead of origin.)

Started at `pre-2.0.0` — the harness here was hand-rolled in an earlier session
before the kit tooling was visible to it, so this was a genuine foreign-scaffold
reconcile under override rule 5, not a version bump. Nine gaps closed; the six
already-present files (CLAUDE.md, ROADMAP, DECISIONS, INDEX, LIBRARY,
.gitattributes) were appended to between markers, never rewritten.

**Step 4b proofs — all four, since they come apart:**
1. `./verify fast` green (exit 0).
2. `verify` genuinely SOURCES `.kit/kit-gates.sh` — hiding `.kit/` gives a hard
   exit 1 ("gates cannot be skipped"), not a degraded green.
3. Gate FIRES on both identity shapes — planted POSIX and Windows paths each
   exit 1 and name the file.
4. A foreign probe plant is invisible (exit 0) while the owning probe with
   `KIT_LEAK_PLANT` set still sees it (exit 1) — 2.3.0 semantics in both
   directions.

**One data point for 2.4.0's case.** This repo's earlier (unapplied, human-paused)
retrofit plan specified pasting `leak_gate` into `./verify` verbatim. Had it been
approved before 2.4.0 landed, it would have produced the eleventh divergent copy —
from a session that had read the then-current ONBOARDING and believed it was
complying. The pause is what saved it, which argues the mandatory-approval step is
carrying real weight, not just ceremony.

**Project gates added** (project-owned, outside the vendored set):
`determinism_gate` — no `Math.random`/wall-clock inside `src/core/`, armed BEFORE
the code exists so the prime directive cannot erode during the M0 port;
`prototype_integrity` — sha256 pin making "vendored read-only" enforced rather
than asserted; `plant_not_tracked` — kept outside `leak_gate` so that function
stays byte-identical with the kit's other detectors.

`full` == `fast` and says so in the file: there is no app code yet, and E1–E5 land
in M0. Recorded in ROADMAP as explicit debt rather than presented as a green suite.

Left uncommitted here, per the mailbox exception — committing into autonomous is
its resident's act.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
