---
id: auricle-retrofit-2.4.1
from: auricle
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. currency.py output at close:

kit currency — ~/Documents/Claude/synthetic-worlds/auricle
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op

Was `pre-2.0.0`, BEHIND by 5 entries (2.0.0 manifest/traces/verify/leak_gate,
2.1.0 mailbox, 2.2.0 gate-fires, 2.3.0 plant-invisible, 2.4.0 vendored).

Notes for your re-read:
- `migrate_to_vendored.py` REFUSED (no pre-existing `./verify`), so verify is
  hand-wired from `kit/templates/verify.project` per the refusal path. It
  sources `.kit/kit-gates.sh`; no gate code is copied into the repo.
- `plant_not_tracked` is a PROJECT gate outside `leak_gate`, so the kit
  function stays byte-identical across the three detectors.
- Gate proven to FIRE on both a planted POSIX and a planted Windows identity
  path (named the file each time), then green again once removed.
- `./verify full` wraps `tools/ci_local.sh`, which is this repo's merge gate
  while cloud CI is disabled (D-24): 62/62 oracles green.

Committed: 31cc727 on main. Pushed: no — pushes are the human's.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
