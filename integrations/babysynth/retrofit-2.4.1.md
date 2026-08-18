---
id: babysynth-retrofit-2.4.1
from: babysynth
to: autonomous
status: verified
ball: none
filed: 2026-06-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/babysynth
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Committed: 726b444 on main. Pushed: no — pushes are the human's.

Notes for the verifier:

- Was `pre-2.0.0` (no declaration), BEHIND by 5 entries. 2.2.0 / 2.3.0 / 2.4.0
  closed together via vendoring: `kit_sync.py` wrote `.kit/` and
  `migrate_to_vendored.py` reported the freshly-written `./verify` as already
  vendored (it was authored from `kit/templates/verify.project`, so it sources
  `.kit/kit-gates.sh` rather than carrying gate code).
- Step 4b's three properties proven separately, since they come apart:
  `./verify fast` green; `verify` SOURCES `.kit/kit-gates.sh` (line 21); the
  gate FIRES on a planted identity path (named the file, exit 1) and returns
  green once removed.
- `.harness/` is gitignored; `.kit/` is committed; `.kit-currency-plant-*` is
  deliberately NOT ignored (kit 2.3.0 — ignoring it blinds the owning probe).
- Project oracle is `node test/*.test.mjs` (4 suites, dependency-free, fake
  AudioContext). No pre-existing red suite to quarantine — all green before and
  after, so no test debt was recorded in ROADMAP.
- The human also asked, in the same session, for the CLAUDE.md/INDEX.md/
  LIBRARY.md knowledge loop; it is folded into this retrofit rather than
  installed twice. LIBRARY seeded with one real lesson (L0001) from this
  session's own verification work.

---
**autonomous verification, 2026-08-18:** `verified` — tree satisfies 2.4.1 in full; the kit has since moved on (2.5.0) — not a defect. The repo was re-read; this line is the resident's, the text above is the filer's.
