---
id: automata-retrofit-2.5.0
from: automata
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.5.0 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.5.0 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/synthetic-worlds/automata
  kit: 2.5.0   declared: 2.5.0   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Committed: 4c5a8bf on main. Pushed: no — pushes are the human's.

Notes for the verifier:

- Was `pre-2.0.0`, BEHIND by 5 entries. Append-only retrofit on a working repo
  whose suite was already green (159 tests): nothing quarantined, no existing
  check weakened, CI untouched.
- Gate code VENDORED via `kit_sync.py` (`.kit/kit-gates.sh` + sha256 MANIFEST),
  never copied. `./verify` is the project-owned template that sources it.
- `plant_not_tracked` added as a PROJECT gate outside `leak_gate` (CHANGELOG
  2.3.0), so the kit-core function stays byte-identical. `.kit-currency-plant-*`
  is deliberately NOT gitignored.
- Three proofs run separately because they come apart: `./verify fast` exit 0;
  `verify` genuinely SOURCES `.kit/kit-gates.sh` (line 21); the gate FIRES on a
  planted identity path (exit 1, names the file) and returns green when removed.
- 2.5.0 landed mid-retrofit. Its requirement (`.gitattributes` TRACKED) was
  already met by commit `f126267`, so only the declaration moved — caught
  because the closing check was re-run against the tree, not pasted from the
  earlier run.
- Architecture rung 1 (single thread), human-ratified at the plan pause.

---
**autonomous verification, 2026-08-18:** `verified` — tree satisfies 2.5.0 in full. The repo was re-read; this line is the resident's, the text above is the filer's.
