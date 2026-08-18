---
id: Place-retrofit-2.4.1
from: Place
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/synthetic-worlds/Place
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Before, for the delta: `declared: pre-2.0.0 — BEHIND by 5 entries`, with
9 unmet requirements across 2.0.0 (manifest, traces/, ./verify, verify wires
leak_gate, CI workflow), 2.2.0 (gate-fires posix + windows), 2.3.0
(plant-invisible) and 2.4.0 (vendored).

Committed: 0a62065 on main. Pushed: no — pushes are the human's.

## Notes for the verifier

- `migrate_to_vendored.py` reported `already vendored`: the verify was written
  thin from the start against `kit/templates/verify.project`, so there was
  nothing to thin. Vendored hash `9cc80dab…` matches canonical.
- The gate was proven behaviourally rather than by presence, since a vendored
  repo answers 2.2.0/2.3.0 by checksum and I did not want to take the checksum's
  word for the behaviour: POSIX plant fired and named the file, Windows plant
  fired and named the file, `.kit-currency-plant-*` left the gate green.
- **One thing worth folding back into the kit.** That verification left an
  ORPHANED plant in the tree when the script running it timed out. It was
  untracked and unignored — one `git add -A` from committing identity paths
  that `leak_gate` ignores by design. `plant_not_tracked` caught it, so the
  2.3.0 guidance held exactly as written; but the failure mode it describes as
  hypothetical happened here for real, from a *timeout* rather than a crash.
  If `currency.py`'s own probe can be interrupted the same way, a plant-sweep
  on entry (remove `.kit-currency-plant-*` older than the current run before
  planting) would close it at the source rather than at every repo.
- Nothing was quarantined: the suite was already green, so `fast()` gates all
  of it and no ROADMAP debt was recorded. `./verify full` is also green.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
