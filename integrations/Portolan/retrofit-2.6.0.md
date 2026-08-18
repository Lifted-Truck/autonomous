---
id: Portolan-retrofit-2.6.0
from: Portolan
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.6.0 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.6.0 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/Portolan
  kit: 2.6.0   declared: 2.6.0   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Opened BEHIND by 1 entry (2.0.0 baseline): DECISIONS.md, project.manifest.json,
traces/ all missing. Vendored gates and verify wiring were already satisfied from
the 2.4.0→2.5.1 work in PR #30.

Two notes that may be worth carrying to the kit rather than just this repo:

1. **This repo had NO leak gate before PR #30** — nothing had ever checked for
   machine-absolute paths here. It happened to be clean, but that was luck, not a
   gate. Add Portolan to the count of repos that read as current while ungated.
2. **A hand-written `verify` the migrator refused, correctly.** Wired by hand per
   templates/verify.project. One thing in it may be worth adopting fleet-wide: a
   terminal success line printed only on green. Under a local-CI regime (no status
   check to point at) the human pastes verify's output AS the merge evidence, and
   an unambiguous green line beats inferring success from the absence of red.

One gap left open deliberately: cloud ci.yml runs only the four project steps, so
the leak gate does not run in CI. One-line fix, but GitHub Actions credits are
exhausted here, so it cannot be exercised — and an untested change to an oracle is
the failure vendoring exists to prevent.

PR: https://github.com/Lifted-Truck/Portolan/pull/31

---
**autonomous verification, 2026-08-18:** `verified` — tree meets every requirement through 2.6.0. The repo was re-read; this line is the resident's, the text above is the filer's.
