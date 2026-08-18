---
id: Plexus-retrofit-2.4.1
from: Plexus
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/synthetic-worlds/Plexus
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Was `pre-2.0.0`, BEHIND by 5 entries (no manifest, no traces/, no ./verify,
therefore no privacy gate at all). Gates vendored via kit_sync.py; none copied
or hand-written. ./verify wraps the pre-existing `npm run gate`.

Proved separately, since they come apart: `./verify fast` and `full` green;
verify hard-exits when `.kit/kit-gates.sh` is hidden (so it genuinely SOURCES
the vendored gates rather than merely coexisting with a checksum-perfect copy);
leak_gate fires on both POSIX and Windows identity plants and goes quiet on a
clean tree; kit_integrity fires on a local edit to a vendored file.

Note for the kit, not a blocker: this repo's CI runs its npm gate but not
`./verify fast`, so leak_gate is local-only here. Left out of scope
deliberately — currency read CURRENT and the retrofit does not "improve"
past its delta — and reported to the human as a recommended follow-up.

Committed: 87cf696 on main. Pushed: no — pushes are the human's.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
