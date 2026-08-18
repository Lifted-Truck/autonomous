---
id: Wend-retrofit-2.4.1
from: Wend
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/synthetic-worlds/Wend
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Was `pre-2.0.0` (no declaration), BEHIND by 5 entries; every `[ ]` closed.

Notes for the re-read:
- 2.2.0/2.3.0/2.4.0 satisfied by VENDORING, not by a hand-written gate.
  `migrate_to_vendored.py` reported "already vendored" — `./verify` was built
  from the thin `harness/verify` template, so it sources `.kit/kit-gates.sh`
  and defines no gate code of its own (0 local definitions of
  leak_gate/record/kit_integrity).
- Gate proven to FIRE on a planted identity path in BOTH POSIX and Windows
  forms, then the tree verified clean again.
- `.harness/` gitignored. `.kit-currency-plant-*` deliberately NOT ignored
  (per the 2.3.0 warning that ignoring it blinds the owning probe); guarded
  instead by a `plant_not_tracked` check kept OUTSIDE `leak_gate` so the
  kit-owned function stays byte-identical.
- Project gates are Wend's real oracle: `import_gate`, `determinism_gate`
  (same seed ⇒ byte-identical MIDI — the standing invariant), and in `full`,
  `validate_gate` (closed loop against the Tonality engine; needs `mts`, so
  CI runs `fast` only). No red tests existed; nothing quarantined.
- Architecture rung 1 (single thread), ratified by the human at retrofit.

Committed: 0d21e75 on main. Pushed: no — pushes are the human's.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
