---
id: Curvature-retrofit-2.5.0
from: Curvature
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.5.0 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.5.0 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/synthetic-worlds/Curvature
  kit: 2.5.0   declared: 2.5.0   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Opened at `declared: pre-2.0.0 — BEHIND by 5 entries` (nine open boxes across
the 2.0.0 baseline and 2.1.0's charter clause).

Note for the verifier: the kit released 2.5.0 while this retrofit was in
flight. It was planned and executed against 2.4.1, and `kit_sync --check`
reported `version-stale` at step 4b. 2.5.0's requirement (`.gitattributes`
TRACKED, not merely present) was already satisfied — committed hours earlier in
this repo's PR #2 — so `.kit/MANIFEST` was re-synced and the retrofit closed at
2.5.0 rather than declaring the version it had started against. `kit-gates.sh`
hashed identical across the bump; only the version line moved.

Gate behaviour proven rather than declared: `verify` confirmed to SOURCE
`.kit/kit-gates.sh`; `leak_gate` fires on planted POSIX and Windows identity
paths and stays quiet on a `/Users/<user>/` placeholder near-miss.

PR: https://github.com/Lifted-Truck/curvature/pull/3

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.5.0 (notice claims 2.5.0). The repo was re-read; this line is the resident's, the text above is the filer's.
