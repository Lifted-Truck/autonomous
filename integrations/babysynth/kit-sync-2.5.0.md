---
id: babysynth-kit-sync-2.5.0
from: babysynth
to: autonomous
status: verified
ball: none
repo_path: ~/Documents/Claude/babysynth
re: kit_sync to 2.5.0 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
kit_sync reports `version-stale` at kit 2.5.0 for `~/Documents/Claude/babysynth`.

`repo_path` above is the directory this run ACTUALLY wrote, resolved at run
time — not the one anyone intended. `.` resolves against the caller's working
directory, so a run launched from elsewhere would sync some other repo and
still report success; autonomous compares this line against its registry and
disputes a mismatch. (Residuum, 2026-08-18: a receipt read `current` while the
named repo had no `.kit/` at all, and nothing in the receipt could show why.)

MANIFEST as written:

```
kit_version: 2.4.1
# KIT-OWNED. Written by kit_sync.py — do not hand-edit these files.
# ./verify recomputes these hashes and goes red if they disagree.
9cc80dab4ccec776f9b31511de02b4fc249094d879d4f28a78ca890748d8c735  kit-gates.sh
```

Verify by re-reading, not by trusting this: `kit_sync.py <repo> --check`.

## From the filer

Retrofit pre-2.0.0 -> 2.4.1 complete; currency reads CURRENT / nothing to do. Committed 726b444 on main, not pushed (human's). Gate proven three ways: verify green, verify SOURCES .kit/kit-gates.sh, gate FIRES on a planted identity path. Notice filed at integrations/babysynth/retrofit-2.4.1.md.

---
**autonomous verification, 2026-08-18:** `verified` — .kit/ matches canonical at 2.5.0 (hash). The repo was re-read; this line is the resident's, the text above is the filer's.
