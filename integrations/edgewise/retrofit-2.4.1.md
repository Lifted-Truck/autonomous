---
id: edgewise-retrofit-2.4.1
from: edgewise
to: autonomous
status: verified
ball: none
filed: 2026-08-18
repo_path: ~/Documents/Claude/synthetic-worlds/edgewise
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/synthetic-worlds/edgewise
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Opened at `pre-2.0.0 — BEHIND by 5 entries`. Closed gaps: project.manifest.json,
traces/, ./verify, leak-gate wiring (2.0.0); charter `## Mailbox` (2.1.0);
gate-fires POSIX + Windows (2.2.0); foreign-plant invisibility (2.3.0); vendored
`.kit/` (2.4.0). 2.2.0/2.3.0 are answered by checksum rather than by probe,
since the repo is vendored.

Architecture rung **1 (single thread)** — asked at the pause, not defaulted.

Proved separately, because the three come apart:

- `./verify fast` green (exit 0, 11/11 evals); `./verify full` green (adds
  format, fixture freshness, native ctest, build).
- `./verify` genuinely SOURCES `.kit/kit-gates.sh` and defines no gates itself.
- The leak gate FIRES: planted POSIX and Windows identity paths both named, exit
  1, green again once removed.

`./verify` wraps the pre-existing test commands rather than replacing them.
Nothing was red, so nothing was quarantined and no debt was recorded in ROADMAP.

Committed: db78122 on main. Pushed: no — pushes are the human's.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
